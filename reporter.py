#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from pprint import pprint
import os

from dateutil.parser import parse as parse_date

from mailer import send_email
from trello import TrelloClient


def is_card_old(card):
    card_date = parse_date(card['dateLastActivity'])
    return datetime.now(tz=card_date.tzinfo) - card_date > timedelta(days=7)


def format_card_list(cards):
    lines = ['• {}'.format(c['name']) for c in cards]
    return '\n'.join(lines)


def format_report(cards):
    heading = (
        'Please review the following Trello cards. They are at least one week '
        'old.'
    )

    return '{}\n\n{}'.format(heading, format_card_list(cards))


def run_report():
    trello_key = os.getenv('TRELLO_KEY')
    trello_token = os.getenv('TRELLO_TOKEN')
    trello_list_id = os.getenv('TRELLO_LIST_ID')

    trello = TrelloClient(trello_key, trello_token)
    all_cards = trello.cards_in_list(trello_list_id)

    old_cards = filter(is_card_old, all_cards)
    report = format_report(old_cards)

    email_address = os.getenv('REPORT_EMAIL_ADDRESS')
    if email_address is not None:
        print('(sending mail to {})'.format(email_address))
        result = send_email(email_address, 'Trello Old Cards Report', report)
        pprint(result)
    else:
        print(report)


def lambda_handler(event, context):
    run_report()


if __name__ == '__main__':
    run_report()
