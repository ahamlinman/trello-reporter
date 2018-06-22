#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from pprint import pprint
import json
import os

from dateutil.parser import parse as parse_date

from mailer import send_email
from reporter import Reporter
from trello import TrelloClient


def is_card_old(card):
    card_date = parse_date(card['dateLastActivity'])
    return datetime.now(tz=card_date.tzinfo) - card_date > timedelta(days=7)


def format_report(list_name, cards):
    reporter = Reporter()
    reporter.add_section(list_name, [c['name'] for c in cards])

    heading = (
        'The following cards have not been modified in some time. '
        'Please review them.'
    )
    return reporter.format(heading)


def run_report(lists):
    trello_key = os.getenv('TRELLO_KEY')
    trello_token = os.getenv('TRELLO_TOKEN')

    trello = TrelloClient(trello_key, trello_token)
    trello_list = trello.list(lists[0]['listId'])
    all_cards = trello_list['cards']
    list_name = trello_list['name']

    old_cards = filter(is_card_old, all_cards)
    report = format_report(list_name, old_cards)

    email_address = os.getenv('REPORT_EMAIL_ADDRESS')
    if email_address is not None:
        print('(sending mail to {})'.format(email_address))
        result = send_email(email_address, 'Trello Old Cards Report', report)
        pprint(result)
    else:
        print(report)


def lambda_handler(event, context):
    run_report(event)


if __name__ == '__main__':
    with open('lists.json', 'r') as f:
        lists = json.load(f)

    run_report(lists)
