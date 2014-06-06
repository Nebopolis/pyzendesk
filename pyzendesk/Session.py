import requests

__author__ = 'bevans'

subdomain = ''
url = ''
user = ''
pwd = ''



class Session:
    
    def __init__(subdomain,user,pwd):
        

def checkCreds(subdomain='z3nbe',user='bevans@zendesk.com',pwd='Oo87GVNSxuuN'):
    url = 'https://{0}.zendesk.com/api/v2/tickets.json'.format(subdomain)
    response = requests.get(url, auth=(user,pwd))
    print(response.status_code)
    return response
    
    
    
    