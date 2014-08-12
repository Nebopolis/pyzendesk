import requests
from Ticket import Requester as Ticket_Requester

__author__ = 'bevans'

class Session:

    def __init__(self, subdomain,user,password='',token=''):
        self.subdomain = subdomain
        self.user = user
        if password and not token:
            self.password = password
        if token:
            self.password = token
            self.user = user + '/token'

    def get(self, url):
        response = requests.get(url, auth=(self.user,self.password))
        print(response.status_code)
        return response

    def post(self, url, json):
        headers = {'Accept':'application/json', 'Content-Type':'application/json'}
        response = requests.post(url, auth=(self.user,self.password), data=json, headers=headers)
        print(response.status_code)
        return response

    def put(self, url, json):
        headers = {'Accept':'application/json', 'Content-Type':'application/json'}
        response = requests.put(url, auth=(self.user,self.password), data=json, headers=headers)
        print(response.status_code)
        return response

    @property
    def tickets(self):
        return Ticket_Requester(self)

def checkCreds(subdomain='z3nbe',user='bevans@zendesk.com',pwd='Oo87GVNSxuuN'):
    url = 'https://{0}.zendesk.com/api/v2/tickets.json'.format(subdomain)
    response = requests.get(url, auth=(user,pwd))
    print(response.status_code)
    return response




