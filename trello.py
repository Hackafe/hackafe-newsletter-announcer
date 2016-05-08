#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import requests

TRELLO_API_ROOT = "https://api.trello.com/1/"

def get_board(board_id):
    board_url = "%s/boards/%s/lists" % (TRELLO_API_ROOT, board_id)
    res = requests.get(board_url)
    print board_url
    return res.json()

def get_cards(list_id):
    cards_url = "%s/lists/%s/cards" % (TRELLO_API_ROOT, list_id)
    res = requests.get(cards_url)
    return res.json()

