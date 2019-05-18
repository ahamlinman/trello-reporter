import requests


class TrelloClient:
    def __init__(self, key, token):
        self.key = key
        self.token = token

    def list(self, list_id):
        url = f"https://api.trello.com/1/lists/{list_id}"
        params = {
            "key": self.key,
            "token": self.token,
            "fields": "name",
            "cards": "open",
            "card_fields": "name,dateLastActivity",
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
