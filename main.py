#!/usr/bin/env python3

from datetime import datetime, timedelta
from pprint import pprint
import argparse
import json
import os

from dateutil.parser import parse as parse_date

from mailer import send_email
from reporter import Reporter
from trello import TrelloClient


def older_than(date_str, delta_spec):
    date = parse_date(date_str)
    return datetime.now(tz=date.tzinfo) - date > timedelta(**delta_spec)


def build_report(config, trello):
    reporter = Reporter()

    for list_spec in config["lists"]:
        trello_list = trello.list(list_spec["listId"])
        old_cards = [
            card
            for card in trello_list["cards"]
            if older_than(card["dateLastActivity"], list_spec["timeDelta"])
        ]

        if not old_cards:
            continue

        reporter.add_section(trello_list["name"], [card["name"] for card in old_cards])

    if not reporter.sections:
        return None

    return reporter.format(config["heading"])


def run_report(config, email=False):
    trello = TrelloClient(os.getenv("TRELLO_KEY"), os.getenv("TRELLO_TOKEN"))
    report_text = build_report(config, trello)

    if report_text is None:
        print("(nothing to report)")
        return

    if email:
        result = send_email(config["emailAddress"], config["subject"], report_text)
        pprint(result)
    else:
        print(report_text)


def lambda_handler(event, _context):
    run_report(event, True)


def main():
    parser = argparse.ArgumentParser(description="Report on old Trello cards.")
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        metavar="FILE",
        help="path to the JSON config file " "(default: config.json)",
    )
    parser.add_argument(
        "--email",
        action="store_true",
        help="send an email instead of printing the report",
    )
    args = parser.parse_args()

    with open(args.config, "r") as config_file:
        config = json.load(config_file)

    run_report(config, args.email)


if __name__ == "__main__":
    main()
