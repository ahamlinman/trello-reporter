#!/usr/bin/env python3

from trelloclient import TrelloClient
import os

trello_key = os.getenv('TRELLO_KEY')
trello_token = os.getenv('TRELLO_TOKEN')
trello_list_id = os.getenv('TRELLO_LIST_ID')

client = TrelloClient(trello_key, trello_token)
print(client.get_cards_from_list(trello_list_id))
