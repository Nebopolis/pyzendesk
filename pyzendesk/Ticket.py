__author__ = 'bevans'

import os
import requests
import simplejson as json
from collections import namedtuple
import warnings
from json import JSONEncoder
from Endpoint import Endpoint
from Endpoint import Attribute
from Session import Session


url = 'https://{0}.zendesk.com/api/v2/tickets.json'
url_id = 'https://{0}.zendesk.com/api/v2/tickets/{1}.json'

class Ticket(Endpoint):

    def post(self, session):
        response = super().post(session, url)
        self.comment = '' #comment has now been posted, clear it out to prevent duplciate comments
        return response

    def put(self, session):
        response = super().put(session, self.id, url_id)
        self.comment = '' #comment has now been posted, clear it out to prevent duplciate comments
        return response

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

def get(session, id):
    return session.get_id(url_id, id)

def get_all(session, id):
    return session.get_all(url)

def main():
    session = Session('z3nbe', 'bevans@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    tick = Ticket(subject='Hello World', comment={'body':'description'})
    tick.post(session)
    tick.update(session=session)
    tick.put(session)
    print(tick.id)

if __name__ == '__main__':
    main()

