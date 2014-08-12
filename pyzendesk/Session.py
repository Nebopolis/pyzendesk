import requests

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

    def get_all(self, url, page=1):
        url = url.format(self.subdomain, page)
        print(url);
        response = requests.get(url, auth=(self.user,self.password))
        print(response.status_code)
        return response

    def get(self, url):
        response = requests.get(url, auth=(self.user,self.password))
        print(response.status_code)
        return response

    def get_id(self, url, id):
        url = url.format(self.subdomain, id)
        response = requests.get(url, auth=(self.user,self.password))
        print(response.status_code)
        return response

    def post(self, url, json):
        url = url.format(self.subdomain)
        headers = {'Accept':'application/json', 'Content-Type':'application/json'}
        response = requests.post(url, auth=(self.user,self.password), data=json, headers=headers)
        print(response.status_code)
        return response

    def put(self, url, id, json):
        url = url.format(self.subdomain, id)
        headers = {'Accept':'application/json', 'Content-Type':'application/json'}
        response = requests.put(url, auth=(self.user,self.password), data=json, headers=headers)
        print(response.status_code)
        return response


def checkCreds(subdomain='z3nbe',user='bevans@zendesk.com',pwd='Oo87GVNSxuuN'):
    url = 'https://{0}.zendesk.com/api/v2/tickets.json'.format(subdomain)
    response = requests.get(url, auth=(user,pwd))
    print(response.status_code)
    return response
    
    
    
    