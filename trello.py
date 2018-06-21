#!/usr/bin/env python3

import requests


class TrelloClient:
    def __init__(self, key, token):
        self.key = key
        self.token = token

    def cards_in_list(self, list_id):
        url = 'https://api.trello.com/1/lists/{}/cards'.format(list_id)
        params = {'key': self.key, 'token': self.token}

        r = requests.get(url, params=params)
        return r.json()
