import logging
import datetime

import celery
from django.utils.timezone import now, utc
from django.conf import settings
import stripe
import stripe.error
from psycopg2._range import DateTimeTZRange

stripe.api_key = settings.STRIPE_API_KEY

from . import models as M
from ..account import models as AM


logger = logging.getLogger(__name__)

PLANS = {"plan_GjfwNo9iFxvpQx": "basic", "plan_GjfwOnCKYlhPHc": "premium"}


@celery.shared_task
def sync_subscriptions():
    current_date = now()
    for account in AM.Account.objects.all():
        logger.info("Processing account #%s...", account.id)
        if not account.customer_id:
            logger.info("Customer ID not found for account #%s", account.id)
        try:
            stripe_customer = stripe.Customer.retrieve(account.customer_id)
        except stripe.error.InvalidRequestError as e:
            logger.warning(
                "Unable to get customer for account #%s: %s", account.id, str(e)
            )
            continue
        if "subscriptions" not in stripe_customer or stripe_customer["subscriptions"]["total_count"] == 0:
            logger.warning("Stripe does not have any subscription info for account")
            logger.info("Database subscriptions:")
            for s in account.subscriptions_set.all():
                logger.warning("%s", str(s))
            continue
        if stripe_customer["subscriptions"]["total_count"] > 1:
            logger.warning("Customer %s has more than one subscription")
            continue
        stripe_subscription = stripe_customer["subscriptions"]["data"][0]
        stripe_plan = stripe_subscription["plan"]["id"]
        stripe_start = datetime.datetime.fromtimestamp(
            stripe_subscription["current_period_start"], utc
        )
        stripe_end = datetime.datetime.fromtimestamp(
            stripe_subscription["current_period_end"], utc
        )
        if stripe_plan not in PLANS:
            logger.warning(
                "Stripe plan (%s) is not among what we have, skipping", stripe_plan
            )
            continue
        try:
            subscription = M.Subscriptions.objects.get(
                account=account, period__contains=current_date
            )
        except M.Subscriptions.DoesNotExist:
            logger.info(
                "Creating subscription %s that was missing", stripe_subscription["id"],
            )
            M.Subscriptions.objects.create(
                account=account,
                plan=PLANS[stripe_plan],
                period=(stripe_start, stripe_end),
            )
            continue
        except M.Subscriptions.MultipleObjectsReturned:
            logger.warning(
                "Multiple subscriptions returned for account #%s", account.id
            )
            continue
        subscription_different = (
            not subscription.period
            or stripe_subscription["id"] != subscription.subscription_id
            or stripe_start != subscription.period.lower
            or stripe_end != subscription.period.upper
        )
        if subscription_different:
            logger.info(
                "The subscription is corrected: %s %s %s -> %s %s",
                subscription.period,
                subscription.plan,
                subscription.subscription_id,
                (stripe_start, stripe_end),
                stripe_subscription["id"],
            )
            subscription.period = DateTimeTZRange(stripe_start, stripe_end)
            subscription.plan = PLANS[stripe_plan]
            subscription.save()
        else:
            logger.info("Subscriptions seems to be good")
