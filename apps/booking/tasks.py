import csv
import pathlib
import shutil
import tempfile
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.db.models.functions import Now
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.conf import settings

from wanderift.utils.scraper import get_scraper_class
from wanderift.utils.scraper.skyscanner import Skyscanner
from . import models as M
from .models import Deal
from ..account.models import DealWatch, DealWatchGroup
from ..auth.models import User


def place2str(p):
    if not p:
        return ""
    return f"{p['type']}:{p['code']}"


@shared_task
def send_search_history():
    objects = M.SearchHistory.objects.filter(timestamp__gt=now() - timedelta(days=1))
    temp_dir = pathlib.Path(tempfile.mkdtemp())
    reportname = temp_dir / "search_history.csv"
    with open(reportname, "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "User",
                "Timestamp",
                "From",
                "To",
                "Departure",
                "Return",
                "Adults",
                "Children",
                "Infants",
                "Fare",
                "DestinationType",
            ]
        )
        for o in objects:
            writer.writerow(
                [
                    o.user.email if o.user else "",
                    o.timestamp.isoformat(),
                    place2str(o.place_from),
                    place2str(o.place_to),
                    o.departure_date.isoformat(),
                    o.return_date.isoformat() if o.return_date else "",
                    o.adults,
                    o.children,
                    o.infants,
                    o.seat_type,
                    o.destination_type,
                ]
            )
    email = EmailMessage(
        "Search History report",
        "Search History report",
        settings.DEFAULT_FROM_EMAIL,
        settings.REPORT_RECEIVERS,
        [],
    )
    email.attach_file(reportname)
    email.send()
    shutil.rmtree(temp_dir)


@shared_task
def send_mass_deal_alerts():
    subscribers = User.objects.filter(account__subscriptions__period__contains=Now())
    for user in subscribers:
        send_deal_alerts.delay(user.pk)


@shared_task
def send_deal_alerts(user_id):
    user = User.objects.get(id=user_id)
    groups = DealWatchGroup.objects.filter(watches__user=user)
    deals = Deal.objects.filter(
        Q(group__in=groups)
        | Q(city_from="{}:{}".format(user.market["type"], user.market["code"]))
    ).order_by("?")[:5]
    random_deals = Deal.objects.all().order_by("?")[:5]
    htm_content = render_to_string(
        "emails/deal-alert-email.html",
        {
            "deals": deals,
            "user": user,
            "random_deals": random_deals,
            "SITE_URL": settings.SITE_URL,
        },
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email
    subject = "The Best Deals Brought to You by Flyline"
    send_mail(subject, "", from_email, [to_email], html_message=htm_content)


@shared_task
def request_scraper(kind, fly_from, fly_to, start_date, return_date):
    scraper = get_scraper_class(kind)
    s = scraper(origin=fly_from, destination=fly_to, start_date=start_date, return_date=return_date)
    return s.run()
