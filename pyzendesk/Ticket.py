__author__ = 'bevans'

import os
import requests
import simplejson as json
from collections import namedtuple
import warnings
import Endpoint
#session = Session.generate(conf1, conf2, conf3...)

Field = namedtuple('Field', 'read_only required post_required post put')
ticket_attributes = {
    'id':                       Field(True,  False, False, False, False),   # Automatically assigned when creating tickets
    'url':                      Field(True,  False, False, False, False),	# The API url of this ticket
    'external_id':              Field(False, False, False, True,  True ),	# A unique external id, you can use this to link Zendesk tickets to local records
    'type':                     Field(False, False, False, True,  True ),	# The type of this ticket, i.e. "problem", "incident", "question" or "task"
    'subject':                  Field(False, False, True,  True,  True ),   # The value of the subject field for this ticket
    'description':              Field(True,  False, False, False, False),	# The first comment on the ticket
    'comment':                  Field(False, True,  True,  True,  True ),   # A comment to be added to the ticket
    'priority':                 Field(False, False, False, True,  True ), 	# Priority, defines the urgency with which the ticket should be addressed: "urgent", "high", "normal", "low"
    'status':                   Field(False, False, False, True,  True ),	# The state of the ticket, "new", "open", "pending", "hold", "solved", "closed"
    'recipient':                Field(True,  False, False, False, False),	# The original recipient e-mail address of the ticket
    'requester_id':             Field(False, False, False, True,  True ),	# The user who requested this ticket
    'submitter_id':             Field(False, False, False, True,  False),	# The user who submitted the ticket; The submitter always becomes the author of the first comment on the ticket.
    'assignee_id':              Field(False, False, False, True,  True ),	# What agent is currently assigned to the ticket
    'organization_id':          Field(True,  False, False, False, False),	# The organization of the requester
    'group_id':                 Field(False, False, False, True,  True ),	# The group this ticket is assigned to
    'collaborator_ids':         Field(False, False, False, True,  True ),	# Who are currently CC'ed on the ticket
    'forum_topic_id':           Field(False, False, False, True,  True ),	# The topic this ticket originated from, if any
    'problem_id':               Field(False, False, False, True,  True ),	# The problem this incident is linked to, if any
    'has_incidents':            Field(True,  False, False, False, False),	# Is true of this ticket has been marked as a problem, false otherwise
    'due_at':                   Field(False, False, False, True,  True ),	# If this is a ticket of type "task" it has a due date. Due date format uses ISO 8601 format.
    'tags': 	                Field(False, False, False, True,  True ), 	# The array of tags applied to this ticket
    'via':                      Field(True,  False, False, False, False),	# This object explains how the ticket was created
    'custom_fields':            Field(False, False, False, True,  True ),	# The custom fields of the ticket
    'satisfaction_rating':      Field(True,  False, False, False, False),   # The satisfaction rating of the ticket, if it exists
    'sharing_agreement_ids':    Field(True,  False, False, False, False),   # The ids of the sharing agreements used for this ticket
    'followup_ids':             Field(True,  False, False, False, False),   # The ids of the followups created from this ticket - only applicable for closed tickets
    'ticket_form_id':           Field(True,  False, False, False, False),	# The id of the ticket form to render for this ticket - only applicable for enterprise accounts
    'brand_id':                 Field(True,  False, False, False, False),	# The id of the brand this ticket is associated with - only applicable for enterprise accounts
    'created_at':               Field(True,  False, False, False, False),	# When this record was created
    'updated_at':               Field(True,  False, False, False, False),	# When this record last got updated
}   

class Ticket():

    def __init__(self, **kwargs):
        for name, value in ticket_attributes.items():
            if value.post_required and not (name in kwargs):
                warnings.warn('Missing required ticket field: ' + name, RuntimeWarning, stacklevel=2)
        for name, value in kwargs.items():
            if not ticket_attributes[name].post:
                warnings.warn('Writing to non-editable field: ' + name, RuntimeWarning, stacklevel=2)
            setattr(self, name, value)
    
    def put():
        print("hello")

def post_ticket(subject, comment, **kwargs):
    ticket = {
        'subject': subject,
        'comment': comment
    }
    ticket.update(kwargs)
    try:
        created = session.post({'ticket', ticket})
        return created
    except AttributeError:
        return None

def encode_ticket(obj):
    if isinstance(obj, Ticket):
        attributes = [a for a in dir(obj) if not a.startswith('__') and not callable(getattr(obj,a))]
        data={}
        for value in attributes:
            attr = getattr(obj, value)
            if isinstance(attr, Ticket):
                attr = encode_ticket(attr)
            data[value] = attr
        return data
    raise TypeError(repr(obj) + " is not JSON serializable")

def main():
    tick = Ticket(subject='Hello World', comment='description')
    print(json.dumps(encode_ticket(tick)))

if __name__ == '__main__':
    main()

