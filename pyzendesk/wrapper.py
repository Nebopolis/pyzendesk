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
        self.remote_endpoints = {'requester':'user', 'assignee':'user', 'organization': 'organization'}
        self.all_endpoints = {'ticket':{'plural':'tickets', 'singular':'ticket'}, 'organization':{'plural':'organizations', 'singular':'organization'}}
        self.object_cache = {}

    def get_all(self, member, fetch=False):
        singular = self.all_endpoints[member]['singular']
        plural = self.all_endpoints[member]['plural']
        responses = self.session.get_all(plural)
        objects = itertools.chain.from_iterable(((zenContainer(self, singular, item['id'], data=item) for item in response.json()[plural]) for response in responses))
        if(fetch):
            objects = list(objects)
        return objects





        
def main():
    creds = zenCredentials('z3nbe', 'zendesk@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    z3nbe = Wrapper(creds)
    x = iter(z3nbe.get_all('ticket'))
    # for i in x:
    #     print(i.raw_subject)

    y = iter(z3nbe.get_all('organization', fetch=True))
    for i in x:
        if i.organization_id:
            print(i.organization.created_at)
        print(i.organization_id)

    # for i in x:
    #     if i.organization_id:
    #         print(i.raw_subject)
        # print(i.organization_id)




if __name__ == '__main__':
    main()


