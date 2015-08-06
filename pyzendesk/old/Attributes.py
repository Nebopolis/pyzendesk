__author__ = 'bevans'

import os
import requests
import simplejson as json
from collections import namedtuple
import warnings
from json import JSONEncoder
from Endpoint import Endpoint

class Attribute(object):

    Field = namedtuple('Field', 'read_only required post_required post put')

    attributes = {
        'id':                       Field(True,  False, False, False, False),   # Automatically assigned when creating tickets
        'url':                      Field(True,  False, False, False, False),   # The API url of this ticket
        'external_id':              Field(False, False, False, True,  True ),   # A unique external id, you can use this to link Zendesk tickets to local records
        'type':                     Field(False, False, False, True,  True ),   # The type of this ticket, i.e. "problem", "incident", "question" or "task"
        'subject':                  Field(False, False, True,  True,  True ),   # The value of the subject field for this ticket
        'description':              Field(True,  False, False, False, False),   # The first comment on the ticket
        'comment':                  Field(False, True,  True,  True,  True ),   # A comment to be added to the ticket
        'priority':                 Field(False, False, False, True,  True ),   # Priority, defines the urgency with which the ticket should be addressed: "urgent", "high", "normal", "low"
        'status':                   Field(False, False, False, True,  True ),   # The state of the ticket, "new", "open", "pending", "hold", "solved", "closed"
        'recipient':                Field(True,  False, False, False, False),   # The original recipient e-mail address of the ticket
        'requester_id':             Field(False, False, False, True,  True ),   # The user who requested this ticket
        'submitter_id':             Field(False, False, False, True,  False),   # The user who submitted the ticket; The submitter always becomes the author of the first comment on the ticket.
        'assignee_id':              Field(False, False, False, True,  True ),   # What agent is currently assigned to the ticket
        'organization_id':          Field(True,  False, False, False, False),   # The organization of the requester
        'group_id':                 Field(False, False, False, True,  True ),   # The group this ticket is assigned to
        'collaborator_ids':         Field(False, False, False, True,  True ),   # Who are currently CC'ed on the ticket
        'forum_topic_id':           Field(False, False, False, True,  True ),   # The topic this ticket originated from, if any
        'problem_id':               Field(False, False, False, True,  True ),   # The problem this incident is linked to, if any
        'has_incidents':            Field(True,  False, False, False, False),   # Is true of this ticket has been marked as a problem, false otherwise
        'due_at':                   Field(False, False, False, True,  True ),   # If this is a ticket of type "task" it has a due date. Due date format uses ISO 8601 format.
        'tags':                     Field(False, False, False, True,  True ),   # The array of tags applied to this ticket
        'via':                      Field(True,  False, False, False, False),   # This object explains how the ticket was created
        'custom_fields':            Field(False, False, False, True,  True ),   # The custom fields of the ticket
        'satisfaction_rating':      Field(True,  False, False, False, False),   # The satisfaction rating of the ticket, if it exists
        'sharing_agreement_ids':    Field(True,  False, False, False, False),   # The ids of the sharing agreements used for this ticket
        'followup_ids':             Field(True,  False, False, False, False),   # The ids of the followups created from this ticket - only applicable for closed tickets
        'ticket_form_id':           Field(True,  False, False, False, False),   # The id of the ticket form to render for this ticket - only applicable for enterprise accounts
        'brand_id':                 Field(True,  False, False, False, False),   # The id of the brand this ticket is associated with - only applicable for enterprise accounts
        'created_at':               Field(True,  False, False, False, False),   # When this record was created
        'updated_at':               Field(True,  False, False, False, False),   # When this record last got updated_at
    }   

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            attribute = {}
            for prop in self.Field._fields:
                attribute[prop] = True if prop in value else False
            print( attribute )



def main():
    tick = Ticket(subject='Hello World', comment='description')
    print(tick.serialize())

if __name__ == '__main__':
    main()


    attributes = {
        'id':                       Endpoint.Field(True,  False, False, False, False),   # Automatically assigned when creating tickets
        'url':                      Endpoint.Field(True,  False, False, False, False),   # The API url of this ticket
        'external_id':              Endpoint.Field(False, False, False, True,  True ),   # A unique external id, you can use this to link Zendesk tickets to local records
        'type':                     Endpoint.Field(False, False, False, True,  True ),   # The type of this ticket, i.e. "problem", "incident", "question" or "task"
        'subject':                  Endpoint.Field(False, False, True,  True,  True ),   # The value of the subject field for this ticket
        'description':              Endpoint.Field(True,  False, False, False, False),   # The first comment on the ticket
        'comment':                  Endpoint.Field(False, True,  True,  True,  True ),   # A comment to be added to the ticket
        'priority':                 Endpoint.Field(False, False, False, True,  True ),   # Priority, defines the urgency with which the ticket should be addressed: "urgent", "high", "normal", "low"
        'status':                   Endpoint.Field(False, False, False, True,  True ),   # The state of the ticket, "new", "open", "pending", "hold", "solved", "closed"
        'recipient':                Endpoint.Field(True,  False, False, False, False),   # The original recipient e-mail address of the ticket
        'requester_id':             Endpoint.Field(False, False, False, True,  True ),   # The user who requested this ticket
        'submitter_id':             Endpoint.Field(False, False, False, True,  False),   # The user who submitted the ticket; The submitter always becomes the author of the first comment on the ticket.
        'assignee_id':              Endpoint.Field(False, False, False, True,  True ),   # What agent is currently assigned to the ticket
        'organization_id':          Endpoint.Field(True,  False, False, False, False),   # The organization of the requester
        'group_id':                 Endpoint.Field(False, False, False, True,  True ),   # The group this ticket is assigned to
        'collaborator_ids':         Endpoint.Field(False, False, False, True,  True ),   # Who are currently CC'ed on the ticket
        'forum_topic_id':           Endpoint.Field(False, False, False, True,  True ),   # The topic this ticket originated from, if any
        'problem_id':               Endpoint.Field(False, False, False, True,  True ),   # The problem this incident is linked to, if any
        'has_incidents':            Endpoint.Field(True,  False, False, False, False),   # Is true of this ticket has been marked as a problem, false otherwise
        'due_at':                   Endpoint.Field(False, False, False, True,  True ),   # If this is a ticket of type "task" it has a due date. Due date format uses ISO 8601 format.
        'tags':                     Endpoint.Field(False, False, False, True,  True ),   # The array of tags applied to this ticket
        'via':                      Endpoint.Field(True,  False, False, False, False),   # This object explains how the ticket was created
        'custom_fields':            Endpoint.Field(False, False, False, True,  True ),   # The custom fields of the ticket
        'satisfaction_rating':      Endpoint.Field(True,  False, False, False, False),   # The satisfaction rating of the ticket, if it exists
        'sharing_agreement_ids':    Endpoint.Field(True,  False, False, False, False),   # The ids of the sharing agreements used for this ticket
        'followup_ids':             Endpoint.Field(True,  False, False, False, False),   # The ids of the followups created from this ticket - only applicable for closed tickets
        'ticket_form_id':           Endpoint.Field(True,  False, False, False, False),   # The id of the ticket form to render for this ticket - only applicable for enterprise accounts
        'brand_id':                 Endpoint.Field(True,  False, False, False, False),   # The id of the brand this ticket is associated with - only applicable for enterprise accounts
        'created_at':               Endpoint.Field(True,  False, False, False, False),   # When this record was created
        'updated_at':               Endpoint.Field(True,  False, False, False, False),   # When this record last got updated_at
    }   

