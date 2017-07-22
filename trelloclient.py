import requests

class TrelloClient:
    API_BASE = 'https://api.trello.com/1'

    def __init__(self, key, token):
        self.key = key
        self.token = token

    def get_cards_from_list(self, list_id):
        url = '{}/lists/{}/cards'.format(self.API_BASE, list_id)
        params = { 'key': self.key, 'token': self.token }

        r = requests.get(url, params=params)
        return r.json()
