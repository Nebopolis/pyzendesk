class ZendeskList:
    def __init__(self, endpoint):
        generate_properties(endpoint)


class ZendeskObject:
    def __init__(self, endpoint):


class ZendeskSession:
    def __init__(self, endpoint):




def main():
    #example of api usage
    z3nbe = Session('z3nbe', limit=100)
    z3nbe.vault.password = 'testpw' #omit to instead require password at command line to run

    z3nbe.credentials = z3nbe.vault(user='user@user.test', type='oauth', grant='read write') or \ 
                        z3nbe.vault.grant_oauth(user='user@user.test',grant='read write')

    for ticket in z3nbe.tickets:
        print(ticket.description)

    ticket = z3nbe.tickets(450)  #allow numeric indexing (lookup by ID)
    print(test_ticket.assignee.name) #automatically look up sub-objects based on ID in parent object
    print(test_ticket.requester.orginization.name) #look up sub objects recursively as long as is needed

    ticket_list = z3nbe.tickets[50:100] #allow range indexting (lookup second 50 in pagination default sort)
    ticket_exports = z3nbe.exports.tickets(0, -1)[::2] #get every other ticket from the beginning of time using the incremental endpoint
    user_list = ticket_list.users #create a generator array if asked for a sub-object of a list
    search = z3nbe.search('hello date:>12-19-2013') #allow searching with arbitrary querries.  
    user_search = search.users #'lazy mapping' - only go as deep as is needed to find an array of the requested objects 
                               #in this case would only return the users found in the search and not any users from
                               #tickets in the search
    user_expanded_search = search.user | search.tickets.users #combine a list of users within tickets and users returned from a search

    #how to both allow indexing by depth (10th element) and ID (#10) especially with a diffrent type of sort
    #perhaps:

    ticket_list = z3nbe.tickets(range(50,100)) #get all tickets between ID 50 and ID 100
    ticket = z3nbe.ticket[10] #get the 10th ticket in this list
    ticket_list = z3nbe.tickets([14,55,666])
    ticket = z3nbe.ticket[2] #ticket 111

    tickets(id)            #get a specific ticket
    tickets([id])          #get a list of tickets
    tickets([id])[:slice]  #filter by collection of IDs, then slice the resulting list
    tickets[:slice]        #make a slice across the entire list of tickets tickets()[:slice] is the same thing
    tickets[10]            #get the 10th ticket in the default sort order of tickets
    tickets[-1]            #get the last ticket

    tickets([id]/id).delete()
    tickets([id]/id).put()
    tickets([id]/id).get()
    tickets.get()           #load all tickets

    ticket_list = z3nbe.tickets('commenter:bevans@zendesk.com') | z3nbe.tickets[::4] #union of set of tickets commented on by
                                                                                     #bevans, and every fourth ticket

    full_history = ticket_list.audits.get()



    collection = z3nbe.tickets(range(50,100))
    collection.get()
    collection[0].description
    z3nbe.tickets(range(0,1000000000))
    descriptions = [ticket.description for ticket in collection]


    **_id

    ticket.** 

    z3nbe.**(id)

    userid = z3nbe.tickets(11).assignee_id
    user_name = z3nbe.users(userid).name

    name = z3nbe.tickets(11).assignee.name


    ***_id

    requester 


{
  "id":               35436,
  "url":              "https://company.zendesk.com/api/v2/tickets/35436.json",
  "external_id":      "ahg35h3jh",
  "created_at":       "2009-07-20T22:55:29Z",
  "updated_at":       "2011-05-05T10:38:52Z",
  "type":             "incident",
  "subject":          "Help, my printer is on fire!",
  "raw_subject":      "{{dc.printer_on_fire}}",
  "description":      "The fire is very colorful.",
  "priority":         "high",
  "status":           "open",
  "recipient":        "support@company.com",
  "requester_id":     "https://company.zendesk.com/api/v2/users/20978392.json",
  "submitter_id":     "https://company.zendesk.com/api/v2/users/76872.json",
  "assignee_id":      235323,
  "organization_id":  509974,
  "group_id":         98738,
  "collaborator_ids": [35334, 234],
  "forum_topic_id":   72648221,
  "problem_id":       9873764,
  "has_incidents":    false,
  "due_at":           null,
  "tags":             ["enterprise", "other_tag"],
  "via": {
    "channel": "web"
  },
  "custom_fields": [
    {
      "id":    27642,
      "value": "745"
    },
    {
      "id":    27648,
      "value": "yes"
    }
  ],
  "satisfaction_rating": {
    "id": 1234,
    "score": "good",
    "comment": "Great support!"
  },
  "sharing_agreement_ids": [84432]
}


