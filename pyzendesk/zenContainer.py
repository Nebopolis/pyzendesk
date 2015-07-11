from sortedcontainers import SortedList, SortedSet, SortedDict
from Session import Session

class zenList:
    def __init__(self, data=None):
        self.data = SortedDict(data)

    def __repr__(self):
        return repr(self.data)


    def __call__(self, key):
        if type(key) == slice:
            start = key.start or 0
            stop = key.stop or 0
            step = key.step or 1
            return [self.data[index] for index in self.data.keys() if index in range(start, stop, step)]
        return self.data[key]

    def __getitem__(self, key):
        return self.data.values()[key]



class zenContainer:

    def __init__(self, wrapper, member, id=None, endpoint=None, data=None):
        if data:
            self.raw = data
        self.raw = data or {}
        self.remote_endpoints = wrapper.remote_endpoints
        self.session = wrapper.session
        if data:
            self.should_refresh = False
        else:
            self.should_refresh = True
        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = '{}s/{}'.format(member, id)
        self.member = member
        self.url = self.session.create_url(self.endpoint)

    def update(self, data):
        if self.id:
            print('put')
        else:
            print('post')

    def fetch(self, cache=True):
        self.raw.update(self.session.get(self.endpoint).json()[self.member])
        self.should_refresh = False


    def __getattr__(self,key):
        if(self.raw['should_refresh']):
            self.fetch()
        if(key is 'session'):
            super().__getattr__(key)
        elif(key is 'raw'):
            super().__getattr__(key)
        elif(key is 'should_refresh'):
            return self.raw['should_refresh']
        elif((key in self.raw['remote_endpoints'])):
            if(key in self.raw):
                return self.raw[key]
            id_key = self.raw['{}_id'.format(key)]
            if not id_key:
                return None
            member = self.raw['remote_endpoints'][key]
            endpoint = '{}s/{}.json'.format(member, id_key)
            self.raw[key] = zenContainer(self.session, member, id_key)
            return self.raw[key]
        try:
            return self.raw[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if(key is 'session'):
            super().__setattr__(key, value)
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
