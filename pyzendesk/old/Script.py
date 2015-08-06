import collections
import requests

class URL:

    def __init__(self, base_url, get_all, get_id):
        self.base_url = base_url
        self.get_all = get_all
        self.get_id = get_id

class Session:


    def __init__(self, subdomain, user, password='', token=''):
        self.subdomain = subdomain
        self.user = user
        if password and not token:
            self.password = password
        if token:
            self.password = token
            self.user = user + '/token'

    @property
    def tickets(self):
        return Tickets(self.subdomain, self.user, self.password)

    def auth(self):
        return (self.user, self.password)


class Tickets:

    base_url = 'https://{0}.zendesk.com/api/v2/tickets'
    all_url = '.json'
    id_url = '/{0}.json'

    def __init__(self, subdomain, user, password):
        self.base_url = self.base_url.format(subdomain)
        self.user = user
        self.password = password

    def get_all(self, page=1):
        url = self.base_url + self.all_url
        response = requests.get(url, auth=(self.user, self.password))
        print(response.status_code)
        return response

class Requester:

    def __init__(self, session, endpoint):
        self.session = session
        self.endpoint = endpoint

    def get_all(self, page=1):
        url = self.base_url + self.get_all
        print(url);
        response = requests.get(url, auth=self.session.auth())
        print(response.status_code)
        return response

    def get(self, ID):
        url = self.endpoint.base_url + self.endpoint.get_id
        print(url);
        response = requests.get(url, auth=self.session.auth())
        print(response.status_code)
        return response



def main():
    session = Session('z3nbe', 'bevans@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    print(session.tickets.get_all().json())

if __name__ == '__main__':
    main()
