#!/usr/bin/env python3

import requests


class TrelloClient:
    def __init__(self, key, token):
        self.key = key
        self.token = token

    def list(self, list_id):
        url = f'https://api.trello.com/1/lists/{list_id}'
        params = {
            'key': self.key,
            'token': self.token,
            'fields': 'name',
            'cards': 'open',
            'card_fields': 'name,dateLastActivity'
        }

        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()
