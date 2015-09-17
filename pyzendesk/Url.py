
class Request:
    def __init__(self, url, credentials = None, data = None):
        self.url = url
        self.credentials = credentials
        self.data = data

def put(requests):
    return requests

def post(requests):
    return requests

def get(requests):
    return requests

class Credentials:
    def __init__(self, username, password = None, token = None):    
        if token:
            password = token
            user = user + '/token'
        self.auth = (user, password)
        self.subdomain = subdomain


class Account:
    def __init__(self, subdomain, credentials = None, cache = None):
        self.subdomain   = subdomain
        self.credentials = credentials
        self.cache       = cache
        self.url = 'https://{}.zendesk.com/api/v2'.format(subdomain)


class Endpoint(object):
    def __init__(self, base = None, item = None, items = [], params = None):
        self.base = base
        self.items = items
        if type(item) is tuple:
            self.plural = True
            self.url = base.url + "/{}"
            self.items.append(item)
        else:
            self.url = "{}/{}".format(base.url, item)
        self.item = item
        self.params = params

    def __call__(self, key):
        self.params[self.url] = key
        return(self)

    def __getitem__(self, key):
        if type(key)is slice:
            start = key.start or 1
            step = key.step or 1
            if key.stop:
                return Endpoint(self, tuple(range(start, stop, step)), self.items, self.params)
            else:
                return Endpoint(self, '[[{}:all:{}]]'.format(start,step), self.items, self.params)
        return Endpoint(self, key, self.items, self.params)

    def __getattr__(self, key):
        return Endpoint(self, key, self.items, self.params)

    def __iter__(self):
        return self.base()

    def __repr__(self):
        return self.url

    def urls(self):
        if not self.items:
            return [self.url]
        items = list(reversed(self.items))
        elements = items.pop()
        while(items):
            elements2 = items.pop()
            elements = [(element, item) for element in elements for item in elements2]
        if len(self.items) > 1:
            return [self.url.format(*path) for path in elements]
        else:
            return [self.url.format(path) for path in elements]
        

z3nbe = Account('z3nbe')
test = Endpoint(z3nbe, 'tickets')
z3nbe.tickets = test

print(z3nbe.tickets[1000:]['organization', 'assignee', 'requester'].urls())