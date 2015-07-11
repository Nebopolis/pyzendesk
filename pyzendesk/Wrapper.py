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


class Endpoint:
    def __init__(self, member, wrapper):
        self.member = member
        self.wrapper = wrapper

    def get_all(self, fetch=False):
        data = self.wrapper.get_all(self.member, fetch)
        return data

    def get(self, object_id):
        return self.wrapper.get(member, object_id)

    def __call__(self, key):
        return self.get(key)

    def endpoint(self, key):
        return '{}/{}'.format(self.wrapper.all_endpoints[self.member]['plural'], key)

    def __getitem__(self, key):
        try:
            self.count
        except NameError:
            self.count = session.count(self.endpoint(key))
        if type(key) == slice:
            start = key.start or 0
            stop = key.stop or 0
            step = key.step or 1
            if(len(range(start, stop, step)) > self.count/100):
                self.get_all(fetch=True)
            return [self.get(index) for index in range(start, stop, step)]
        return self.get(key)

    def __iter__(self):
        return self.get_all()


class Wrapper: 

    def __init__(self, credentials):
        self.credentials = credentials
        self.queue = RequestQueue(request_limit=600)
        self.session = Session(self.credentials, self.queue)
        self.all_endpoints = {'ticket':{'plural':'tickets', 'singular':'ticket'}, 
                            'organization':{'plural':'organizations', 'singular':'organization'},
                            'requester': {'plural':'users','singular':'user'},
                            'user': {'plural':'users','singular':'user'},
                            'assignee': {'plural':'users','singular':'user'}}
        self.object_cache = BasicCache()
        self.tickets = Endpoint('ticket', self)
        self.organizations = Endpoint('organization', self)
        self.users = Endpoint('user', self)

    def get_all(self, member, fetch=False):
        singular = self.all_endpoints[member]['singular']
        plural = self.all_endpoints[member]['plural']
        responses = self.session.get_all(plural)
        objects = itertools.chain.from_iterable(((zenContainer(self, singular, item['id'], data=item) for item in response.json()[plural]) for response in responses))
        if(fetch):
            objects = list(objects)
        return objects

    def get(self, member, object_id, cache=True):
        singular = self.all_endpoints[member]['singular']
        plural = self.all_endpoints[member]['plural']
        endpoint = '{}/{}'.format(self.plural, object_id)
        if not cache:
            self.expire_cache(endpoint)
        new_obj = self.object_cache.get(endpoint)
        if new_obj:
            return new_obj
        return zenContainer(self, singular, object_id)

    def expire_cache(endpoint):
        cache_url = self.credentials.create_url(endpoint)
        self.queue.cache.delete(cache_url)
        self.object_cache.delete(endpoint)

        
def main():
    creds = zenCredentials('z3nbe', 'zendesk@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    z3nbe = Wrapper(creds)

    for user in z3nbe.users:
        print(user.name)
        if user.organization_id:
            print(user.organization.name)

if __name__ == '__main__':
    main()