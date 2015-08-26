from zenContainer import zenContainer, Endpoint, zenCredentials
from Session import Session
from RequestQueue import RequestQueue, BasicCache
import itertools


class Wrapper: 

    def __init__(self, credentials):
        self.credentials = credentials
        self.queue = RequestQueue(request_limit=600)
        self.session = Session(self.credentials, self.queue)
        self.object_cache = BasicCache()

        self.all_endpoints = {'ticket':{'plural':'tickets', 'singular':'ticket'}, 
                            'organization':{'plural':'organizations', 'singular':'organization'},
                            'requester': {'plural':'users','singular':'user'},
                            'user': {'plural':'users','singular':'user'},
                            'assignee': {'plural':'users','singular':'user'},
                            'audit': {'plural': 'audits', 'singular': 'audit'}}
                            
        self.tickets = Endpoint('ticket', self)
        self.organizations = Endpoint('organization', self)
        self.users = Endpoint('user', self)

    def get_all(self, member, fetch=False, singular=None, plural=None):
        singular = singular or self.all_endpoints[member]['singular']
        plural = plural or self.all_endpoints[member]['plural']
        responses = self.session.get_all(plural)
        objects = itertools.chain.from_iterable(((zenContainer(self, singular, item['id'], data=item) for item in response.json()[member]) for response in responses))
        if(fetch):
            objects = list(objects)
        return objects

    def get(self, member, object_id, cache=True):
        singular = self.all_endpoints[member]['singular']
        plural = self.all_endpoints[member]['plural']
        endpoint = '{}/{}'.format(plural, object_id)
        if not cache:
            self.expire_cache(endpoint)
        new_obj = self.object_cache.get(endpoint)
        if new_obj:
            return new_obj
        return zenContainer(self, singular, object_id)

    def expire_cache(self, endpoint):
        cache_url = self.credentials.create_url(endpoint)
        self.queue.cache.delete(cache_url)
        self.object_cache.delete(endpoint)

        
def main():
    creds = zenCredentials('z3nbe', 'zendesk@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    z3nbe = Wrapper(creds)

    for user in z3nbe.users:
        print(user)
    for organization in z3nbe.organizations:
        print(organization)
    for ticket in z3nbe.tickets:
        print(ticket)

if __name__ == '__main__':
    main()