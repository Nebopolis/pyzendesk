__author__ = 'bevans'

import os
import requests
import simplejson as json
from collections import namedtuple
import warnings

session = Session.generate(conf1, conf2, conf3...)

Field = namedtuple('Field', 'required read_only')
ticket_attributes = {
    'id': Field(True, False),                       # Automatically assigned when creating tickets
    'url': Field(True, False),	 	 	            # The API url of this ticket
    'external_id': Field(False, False),	 	 	    # A unique external id, you can use this to link Zendesk tickets to local records
    'type': Field(False, False),	                # The type of this ticket, i.e. "problem", "incident", "question" or "task"
    'subject': Field(False, False),		            # The value of the subject field for this ticket
    'description': Field(True, False),	  	        # The first comment on the ticket
    'priority': Field(False, False), 	            # Priority, defines the urgency with which the ticket should be addressed: "urgent", "high", "normal", "low"
    'status': Field(False, False),		            # The state of the ticket, "new", "open", "pending", "hold", "solved", "closed"
    'recipient': Field(True, False),	  	        # The original recipient e-mail address of the ticket
    'requester_id': Field(False, True),	            # The user who requested this ticket
    'submitter_id': Field(False, False),		    # The user who submitted the ticket; The submitter always becomes the author of the first comment on the ticket.
    'assignee_id': Field(False, False),	 	        # What agent is currently assigned to the ticket
    'organization_id': Field(True, False),	        # The organization of the requester
    'group_id': Field(False, False),	 	        # The group this ticket is assigned to
    'collaborator_ids': Field(False, False),	    # Who are currently CC'ed on the ticket
    'forum_topic_id': Field(False, False),	  	    # The topic this ticket originated from, if any
    'problem_id': Field(False, False),	  	        # The problem this incident is linked to, if any
    'has_incidents': Field(True, False),		    # Is true of this ticket has been marked as a problem, false otherwise
    'due_at': Field(False, False),	 	            # If this is a ticket of type "task" it has a due date. Due date format uses ISO 8601 format.
    'tags': 	Field(False, False), 	            # The array of tags applied to this ticket
    'via': Field(True, False),	  	                # This object explains how the ticket was created
    'custom_fields': Field(False, False),	        # The custom fields of the ticket
    'satisfaction_rating': Field(True, False),      # The satisfaction rating of the ticket, if it exists
    'sharing_agreement_ids': Field(True, False),    # The ids of the sharing agreements used for this ticket
    'followup_ids': Field(True, False),		        # The ids of the followups created from this ticket - only applicable for closed tickets
    'ticket_form_id': Field(True, False),	        # The id of the ticket form to render for this ticket - only applicable for enterprise accounts
    'brand_id': Field(True, False),	                # The id of the brand this ticket is associated with - only applicable for enterprise accounts
    'created_at': Field(True, False),	 		    # When this record was created
    'updated_at': Field(True, False),	 	        # When this record last got updated
}


class Ticket:

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
        for name, value in ticket_attributes.items():
            if value.required and getattr(self, name) is None:
                warnings.warn('Missing required ticket field', RuntimeWarning, stacklevel=2)

    def put

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
