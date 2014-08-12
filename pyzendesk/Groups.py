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
from Group_Memberships import Group_Membership
import Group_Memberships

url = 'https://{0}.zendesk.com/api/v2/groups.json'
get_url = 'https://{0}.zendesk.com/api/v2/groups.json?page={1}'
url_id = 'https://{0}.zendesk.com/api/v2/groups/{1}.json'

class Group(Endpoint):

    def post(self, session):
        response = super().post(session, url)
        return response

    def put(self, session):
        response = super().put(session, self.id, url_id)
        return response

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

def get(session, id):
    return session.get_id(url_id, id)

def get_all(session, page=1):
    return session.get_all(get_url, page)

def main():
    session = Session('z3nbe', 'bevans@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
  
    '''
    bacon_ipsum = requests.get('http://baconipsum.com/api/?type=all-meat&sentences=100').json()[0]
    bacon_ipsum = bacon_ipsum.replace('.', '').replace(',', '')
    bacon_ipsum = list(set(bacon_ipsum.split()))
    
    for meat in bacon_ipsum: 
        group = Group(name=meat)
        group.post(session)
    '''
    
    '''
    next_page = 1
    groups = {}

    while(next_page):
        json = get_all(session, next_page).json()
        for group in json['groups']:
            groups[group['id']] = group
        next_page = json['next_page']
        next_page = next_page.rsplit('=', 1)[1] if next_page else None
        print(next_page)
    print(groups)

    agent_id = 727303658

    for group_id in groups:
        membership = Group_Membership(user_id=agent_id, group_id=group_id)
        membership.post(session)
    '''

    next_page = 1
    memberships = {}


    while(next_page):
        json = Group_Memberships.get_all(session, next_page).json()
        for membership in json['group_memberships']:
            memberships[membership['id']] = membership
        next_page = json['next_page']
        next_page = next_page.rsplit('=', 1)[1] if next_page else None
        print(next_page)
    print(memberships)

    pairs = []

    for id, membership in memberships.items():
        pair = [membership['user_id'], membership['group_id']]
        pairs.append(pair)
    print(pairs)

    count = Group_Memberships.get_all(session).json()['count']
    print(count)
    print(len(pairs))




if __name__ == '__main__':
    main()

