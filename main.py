#!/usr/bin/env python3

import requests
import os

def get_cards_from_trello(key, token, list_id):
    url = 'https://api.trello.com/1/lists/{}/cards'.format(list_id)
    params = { 'key': key, 'token': token }

    r = requests.get(url, params=params)
    return r.json()

trello_key = os.getenv('TRELLO_KEY')
trello_token = os.getenv('TRELLO_TOKEN')
trello_list_id = os.getenv('TRELLO_LIST_ID')

print(get_cards_from_list(trello_key, trello_token, trello_list_id))
