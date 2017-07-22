#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from dateutil.parser import parse as parse_date
import os
import requests

def get_cards_from_trello(key, token, list_id):
    url = 'https://api.trello.com/1/lists/{}/cards'.format(list_id)
    params = { 'key': key, 'token': token }

    r = requests.get(url, params=params)
    return r.json()

def is_card_old(card):
    card_date = parse_date(card['dateLastActivity'])
    return datetime.now(tz=card_date.tzinfo) - card_date > timedelta(days=7)

def format_card_email(cards):
    lines = ['• {}'.format(c['name']) for c in cards]
    heading = 'Please review the following Trello cards. They are at least ' \
            'one week old.'

    return '{}\n\n{}'.format(heading, '\n'.join(lines))

trello_key = os.getenv('TRELLO_KEY')
trello_token = os.getenv('TRELLO_TOKEN')
trello_list_id = os.getenv('TRELLO_LIST_ID')

all_cards = get_cards_from_trello(trello_key, trello_token, trello_list_id)
old_cards = filter(is_card_old, all_cards)

print(format_card_email(old_cards))
