from sortedcontainers import SortedList, SortedSet, SortedDict

class zenList:
    def __init__(self, data=None):
        self.data = SortedDict()
        for item in data: 
            self.data[item.id] = item

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

    def __init__(self, data=None):
        self.raw = data or {}
    
    def __getattr__(self,key):
        if(key is 'raw'):
            super().__getattr__(key)
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
    test1 = zenContainer()
    test1.id = 1234
    test1.name = 'hello'
    test2 = zenContainer()
    test2.id = 3214
    test2.name = 'world'
    test = zenList([test1, test2])
    print(test)
    print(test[1])
    print(test(slice(2000,7000)))
    for item in test(slice(2000, 7000)):
        print(item.name)

if __name__ == '__main__':
    main()
