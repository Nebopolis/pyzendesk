import requests
from RequestQueue import RequestQueue

__author__ = 'bevans'


class Session:

    def __init__(self, creds, queue):
        self.queue = queue
        self.session = requests.Session()
        self.auth = creds
        self.session.auth = creds.auth
        self.create_url = creds.create_url


    def get(self, endpoint, params = None, page = None):
        url = self.auth.create_url(endpoint, params)
        response = self.queue.process((url, self.session.get))
        return next(response)

    def count(self, endpoint, params = None):
        first_page = self.get(endpoint, params)
        count = first_page.json()['count']
        try:
            page_count = first_page.json()['page_count']
        except KeyError:
            if count > 100:
                page_count = count // 100
                if count % 100 > 0:
                    page_count = page_count + 1
            else:
                page_count = 1
        return page_count

    def get_all(self, endpoint, params = None):
        page_count = self.count(endpoint, params)
        responses = self.queue.process([(self.auth.create_url(endpoint, params, page),self.session.get) for page in range(1,page_count + 1)])
        return responses

    def post(self, endpoint, json):
        url = self.auth.create_url(endpoint)
        headers = {'Accept':'application/json', 'Content-Type':'application/json'}
        response = self.queue.process((url, lambda url: self.session.post(url, data=json, headers=headers)))
        return next(response)

    def put(self, endpoint, json):
        url = self.auth.create_url(endpoint)
        headers = {'Accept':'application/json', 'Content-Type':'application/json'}
        response = self.queue.process((url, lambda url: self.session.put(url, data=json, headers=headers)))
        return next(response)



def main():
    z3nbe = Session('https://z3nbe.zendesk.com/api/v2', user='zendesk@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    tickets = z3nbe.get_all('tickets')
    for ticket in tickets:
        print(ticket)
    

if __name__ == '__main__':
    main()