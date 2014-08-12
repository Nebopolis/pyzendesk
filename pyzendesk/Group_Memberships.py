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

url = 'https://{0}.zendesk.com/api/v2/group_memberships.json'
get_url = 'https://{0}.zendesk.com/api/v2/group_memberships.json?page={1}'
url_id = 'https://{0}.zendesk.com/api/v2/group_memberships/{1}.json'

class Group_Membership(Endpoint):

    def post(self, session):
        response = super().post(session, url)
        return response

    def put(self, session):
        warnings.warn('Put request for a create only endpoint group_memberships with ID: ' + self.id, RuntimeWarning, stacklevel=2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

def get(session, id):
    return session.get_id(url_id, id)

def get_all(session, page=1):
    return session.get_all(get_url, page)

def main():
    session = Session('z3nbe', 'bevans@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    print(get_all(session, 2).json())

if __name__ == '__main__':
    main()

