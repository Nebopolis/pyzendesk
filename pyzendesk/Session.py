import requests
from RequestQueue import RequestQueue

__author__ = 'bevans'


class Session:

    def __init__(self, base_url, user, password='', token=''):
        self.queue = RequestQueue(request_limit=600)
        self.base_url = base_url
        if password and not token:
            password = password
        if token:
            password = token
            user = user + '/token'
        self.session = requests.Session()
        self.session.auth = (user, password)

    def create_url(self, endpoint, params = None, page = 1):
        param_string = params or []
        param_string = param_string if type(param_string) is list else [param_string]
        param_string.append('page={}'.format(page))
        param_string = '&'.join(param_string)
        url = '{}/{}?{}'.format(self.base_url, endpoint, param_string)
        return url

    def get(self, endpoint, params = None, page = None):
        url = self.create_url(endpoint, params)
        response = self.queue.process((url, self.session.get))
        return next(response)

    def get_all(self, endpoint, params = None):
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
        responses = self.queue.process([(self.create_url(endpoint, params, page),self.session.get) for page in range(1,page_count + 1)])
        return responses

    def post(self, endpoint, json):
        url = self.create_url(endpoint)
        headers = {'Accept':'application/json', 'Content-Type':'application/json'}
        response = self.queue.process((url, lambda url: self.session.post(url, data=json, headers=headers)))
        return next(response)

    def put(self, endpoint, json):
        url = self.create_url(endpoint)
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