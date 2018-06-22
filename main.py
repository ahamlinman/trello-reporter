#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from pprint import pprint
import json
import os

from dateutil.parser import parse as parse_date

from mailer import send_email
from reporter import Reporter
from trello import TrelloClient


def older_than(date_str, delta_spec):
    date = parse_date(date_str)
    return datetime.now(tz=date.tzinfo) - date > timedelta(**delta_spec)


def run_report(config):
    trello_key = os.getenv('TRELLO_KEY')
    trello_token = os.getenv('TRELLO_TOKEN')

    trello = TrelloClient(trello_key, trello_token)
    reporter = Reporter()
    for list_spec in config['lists']:
        trello_list = trello.list(list_spec['listId'])

        old_cards = [
            card for card in trello_list['cards']
            if older_than(card['dateLastActivity'], list_spec['timeDelta'])
        ]
        if len(old_cards) == 0:
            continue

        reporter.add_section(
            trello_list['name'],
            [card['name'] for card in old_cards]
        )

    if len(reporter.sections) == 0:
        print('(no old cards)')
        return

    heading = (
        'The following cards have not been acted upon in some time. '
        'Please review them.'
    )
    report_text = reporter.format(heading)

    email_address = os.getenv('REPORT_EMAIL_ADDRESS')
    if email_address is not None:
        print('(sending mail to {})'.format(email_address))
        result = send_email(
            email_address,
            'Trello Old Cards Report',
            report_text
        )
        pprint(result)
    else:
        print(report_text)


def lambda_handler(event, context):
    run_report(event)


if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    run_report(config)
