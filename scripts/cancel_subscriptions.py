import csv
import json
from collections import defaultdict

import stripe
import stripe.error
import dotenv
import os
import datetime

dotenv.load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")


basic_monthly = "plan_GVoIbmKEbAWipY"
premium_monthly = "plan_GVoH2rqqEUCTcf"
plan = basic_monthly


PLAN_TO_NAME = {basic_monthly: "basic", premium_monthly: "premium"}
NEW_PLANS = {"basic": "plan_GjfwNo9iFxvpQx", "premium": "plan_GjfwOnCKYlhPHc"}


def get_plan_subscriptions(plan):
    last_subscription = None
    result = []
    while True:
        if last_subscription:
            chunk = stripe.Subscription.list(
                plan=plan, starting_after=last_subscription
            )
        else:
            chunk = stripe.Subscription.list(plan=plan)
        if not chunk["data"]:
            break
        result.extend(chunk["data"])
        last_subscription = chunk["data"][-1]["id"]
    return result


def get_customers():
    last_customer = None
    result = []
    while True:
        if not last_customer:
            chunk = stripe.Customer.list(limit=100)
        else:
            chunk = stripe.Customer.list(starting_after=last_customer, limit=100)
        if not chunk["data"]:
            break
        result.extend(chunk["data"])
        last_customer = chunk["data"][-1]["id"]
        print(last_customer, len(result))
    return result


def pts(ts):
    return datetime.datetime.fromtimestamp(ts)


def fetch_customers():
    data = get_customers()
    with open("customers.json", "w") as f:
        json.dump(data, f)


def get_invoices():
    last_invoice = None
    result = []
    while True:
        if not last_invoice:
            chunk = stripe.Invoice.list(limit=100)
        else:
            chunk = stripe.Invoice.list(starting_after=last_invoice, limit=100)
        if not chunk["data"]:
            break
        result.extend(chunk["data"])
        last_invoice = chunk["data"][-1]["id"]
        print(last_invoice, len(result))
    return result


def fetch_invoices():
    data = get_invoices()
    with open("invoices.json", "w") as f:
        json.dump(data, f)


def fetch():
    data = get_plan_subscriptions(premium_monthly)
    with open("premium.json", "w") as f:
        json.dump(data, f)


def cancel_subscription():
    with open("plan_sub.json") as f:
        subs_basic = json.load(f)
    with open("premium.json") as f:
        subs_premium = json.load(f)

    with open("customers.json") as f:
        customers = {c["id"]: c for c in json.load(f)}

    with open("invoices.json") as f:
        invoices = json.load(f)
    im = defaultdict(list)
    for invoice in invoices:
        im[invoice["subscription"]].append(invoice)

    for plan_name, subs in (("basic", subs_basic), ("premium", subs_premium)):
        for sub in subs:
            curr_period_start = pts(sub["current_period_start"])
            curr_period_end = pts(sub["current_period_end"])
            created = pts(sub["created"])
            status = sub["status"]
            discount = sub["discount"]
            trial_end = (
                curr_period_end
                if status == "trialing"
                else curr_period_end.replace(year=curr_period_end.year + 1)
            )
            customer = customers[sub["customer"]]
            print(f'Deleting subscription for customer {customer["email"]}')
            try:
                stripe.Subscription.delete(sub["id"])
            except stripe.error.InvalidRequestError as e:
                print("Error: ", str(e))
            print(f'Creating yearly subscription for customer {customer["email"]}...')
            params = {
                "customer": customer["id"],
                "trial_end": int(trial_end.timestamp()),
                "items": [{"plan": NEW_PLANS[plan_name]}],
            }
            stripe.Subscription.create(**params)



def analyze():
    with open("plan_sub.json") as f:
        subs_basic = json.load(f)
    with open("premium.json") as f:
        subs_premium = json.load(f)

    with open("customers.json") as f:
        customers = {c["id"]: c for c in json.load(f)}

    with open("invoices.json") as f:
        invoices = json.load(f)
    im = defaultdict(list)
    for invoice in invoices:
        im[invoice["subscription"]].append(invoice)

    with open("analysis.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            (
                "Plan",
                "Start",
                "End",
                "Created",
                "Status",
                "Coupon",
                "Email",
                "Yearly trial end",
                "Invoices",
            )
        )
        for plan_name, subs in (("basic", subs_basic), ("premium", subs_premium)):
            for sub in subs:
                curr_period_start = pts(sub["current_period_start"])
                curr_period_end = pts(sub["current_period_end"])
                created = pts(sub["created"])
                status = sub["status"]
                discount = sub["discount"]
                trial_end = (
                    curr_period_end
                    if status == "trialing"
                    else curr_period_end.replace(year=curr_period_end.year + 1)
                )
                writer.writerow(
                    (
                        plan_name,
                        curr_period_start.isoformat(),
                        curr_period_end.isoformat(),
                        created.isoformat(),
                        status,
                        discount["coupon"]["id"] if discount else "None",
                        customers[sub["customer"]]["email"],
                        trial_end,
                        ";".join(
                            f'{i["status"]}({i["total"]/100})' for i in im[sub["id"]]
                        ),
                    )
                )


#analyze()
cancel_subscription()
# fetch_customers()
# yes fetch()
# fetch_invoices()
