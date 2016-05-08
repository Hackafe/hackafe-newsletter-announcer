#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import logging
import trello
import pprint
from datetime import *
from time import *
from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler

pp = pprint.PrettyPrinter(indent=4)

PUBLIC_EVENTS_LABEL_IDS = set([
        "565af8f0fb396fe706bec112",
        "54648a0274d650d567a72353",
        "54648a0274d650d567a72355",
        "54648a0274d650d567a72356",
        "565af54bfb396fe706bebf3d",
        "566aca77fb396fe706d2928a",
])


def get_public_events_for_this_week():
    events_board = trello.get_board('5384d9bf0737263537b5e3a4')
    now = datetime.now()
    one_week_from_now = now + timedelta(weeks = 1)
    month = now.strftime('%B %Y')
    events_list = [l for l in events_board if l['name'] == month][0]

    events_for_the_month = trello.get_cards(events_list['id'])

    events_for_this_week = [e for e in events_for_the_month
            if due(e) >= now and due(e) <= one_week_from_now]

    public_events = [e for e
            in events_for_this_week
            if len(e['idLabels']) > 0 and set(e['idLabels']).issubset(PUBLIC_EVENTS_LABEL_IDS)]
    return public_events

def due(event):
    return datetime(*strptime(event['due'], '%Y-%m-%dT%H:%M:%S.%fZ')[0:6])



def run_scheduler():
    logging.basicConfig()
    scheduler = BlockingScheduler()
    scheduler.add_job(get_public_events_for_this_week, 'cron', day_of_week='sun', hour='23')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    print get_public_events_for_this_week()
