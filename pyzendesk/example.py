from zenContainer import zenCredentials
from Wrapper import Wrapper

creds = zenCredentials('z3nbe', 'zendesk@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
z3nbe = Wrapper(creds)

for ticket in z3nbe.tickets:
    print(ticket.description)
    if ticket.organization:
    	print(ticket.organization.name)
