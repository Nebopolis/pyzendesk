from sortedcontainers import SortedList, SortedSet, SortedDict
from Session import Session

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


class zenContainer:

    def __init__(self, wrapper, member, object_id=None, data=None):
        self.raw = data or {}
        if data:
            self.should_refresh = False
        else:
            self.should_refresh = True
        self.wrapper = wrapper
        self.member = member
        self.singular = self.wrapper.all_endpoints[member]['singular']
        self.plural = self.wrapper.all_endpoints[member]['plural']
        if object_id:
            self.endpoint = '{}/{}'.format(self.plural, object_id)
            self.wrapper.object_cache.set(self.endpoint, self)
        else:
            self.endpoint = '{}'.format(self.plural)
        self.url = self.wrapper.session.create_url(self.endpoint)
        self.get()

    def update(self, data):
        if self.id:
            print('put')
            self.wrapper.session.put(self.endpoint, self.raw)
            self.wrapper.expire_cache(self.endpoint)
            self.should_refresh = True
        else:
            print('post')
            self.wrapper.expire_cache(self.endpoint)
            self.wrapper.session.post(self.endpoint, self.raw)
            self.should_refresh = True

    def get(self, cache=True):
        if(self.should_refresh):
            self.should_refresh = False
            if not cache:
                self.wrapper.expire_cache(self.endpoint)
            data = self.wrapper.session.get(self.endpoint).json()[self.singular]
            self.raw.update(data)
        else:
            return self.raw
        return data

    def __getattr__(self,key):
        if(key is 'raw'):
            super().__getattr__(key)
        elif(key is 'should_refresh'):
            return self.raw['should_refresh']
        elif((key in self.raw['wrapper'].all_endpoints)):
            if(key in self.raw):
                return self.raw[key]
            id_key = self.raw['{}_id'.format(key)]
            if not id_key:
                return None
            singular = self.raw['wrapper'].all_endpoints[key]['singular']
            plural = self.raw['wrapper'].all_endpoints[singular]['plural']
            endpoint = '{}/{}'.format(plural, id_key)
            new_obj = self.wrapper.object_cache.get(endpoint)
            if new_obj:
                 self.raw[key] = new_obj
            else:
                new_obj = zenContainer(self.wrapper, singular, object_id=id_key)
                self.raw[key] = new_obj
            return self.raw[key]
        try:
            return self.raw[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if(key is 'raw'):
            super().__setattr__(key, value)
        else:
            self.raw[key] = value

    def __cmp__(self, other):
        if self.raw['id'] > other.raw['id']:
            return 1
        elif self.raw['id'] == other.raw['id']:
            return 0
        elif self.raw['id'] < other.raw['id']:
            return -1

    def __lt__(self, other):
        return self.raw['id'] < other.raw['id']
    
    def __le__(self, other):
        return self.raw['id'] <= other.raw['id']

    def __eq__(self, other):
        return self.raw == other.raw

    def __ne__(self, other):
        return self.raw != other.raw

    def __gt__(self, other):
        return self.raw['id'] > other.raw['id']

    def __ge__(self, other):
        return self.raw['id'] >= other.raw['id']

    def __hash__(self):
        print(self.raw)
        return hash(self.raw['id'])

    def __repr__(self):
        return repr(self.raw)



def main():
    z3nbe = Session('https://z3nbe.zendesk.com/api/v2', user='zendesk@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    ticket = zenContainer(z3nbe,'ticket', 1400)
    print(ticket.organization.name)

if __name__ == '__main__':
    main()
