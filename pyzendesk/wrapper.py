from zenContainer import zenList, zenContainer
from Session import Session
from RequestQueue import RequestQueue, BasicCache
import itertools

class zenCredentials():

    base_url = 'https://{}.zendesk.com/api/v2'

    def __init__(self, subdomain, user, password='', token=''):
        if token:
            password = token
            user = user + '/token'
        self.auth = (user, password)
        self.subdomain = subdomain

    def create_url(self, endpoint, params = None, page = None):
        param_string = params or []
        param_string = param_string if type(param_string) is list else [param_string]
        if(page):
            param_string.append('page={}'.format(page))
        param_string = '&'.join(param_string)
        url = '{}/{}?{}'.format(self.base_url, endpoint, param_string)
        return url.format(self.subdomain)

class Wrapper:

    def __init__(self, credentials):
        self.credentials = credentials
        self.queue = RequestQueue(request_limit=600)
        self.session = Session(self.credentials, self.queue)
        self.plural = 'tickets'
        self.singular = 'ticket'
        self.remote_endpoints = {'requester':'user', 'assignee':'user', 'organization': 'organization'}

    def get_all(self):
        responses = self.session.get_all(self.plural)
        objects = itertools.chain.from_iterable(((zenContainer(self, 'ticket', ticket['id'], data=ticket) for ticket in response.json()[self.plural]) for response in responses))
        return objects

    def get(self, id, cache=True):
        location = '{}/{}'.format(self.plural, id)
        url = self.session.create_url(location)
        if not cache:
            self.queue.cache.delete(url)
        data = self.session.get(endpoint).json()[self.singular]


        
def main():
    creds = zenCredentials('z3nbe', 'zendesk@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    z3nbe = Wrapper(creds)
    x = iter(z3nbe.get_all())
    print(next(x))
    for i in x:
        print(i.raw_subject)

if __name__ == '__main__':
    main()


