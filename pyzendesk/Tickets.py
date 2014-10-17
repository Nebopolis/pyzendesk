from Endpoint import Endpoint
from Endpoint import from_properties
from Endpoint import Requester as Endpoint_Requester

__author__ = 'bevans'

class Ticket(Endpoint):

    attributes = {
            'id': { 'read_only' },
            'url': { 'read_only' },
            'external_id': { 'post', 'put' },
            'type': { 'post', 'put' },
            'subject': { 'post_required', 'post','put' },
            'description': { 'read_only' },
            'comment': { 'required', 'post_required', 'post', 'put' },
            'priority': { 'post', 'put' },
            'status': { 'post', 'put' },
            'recipient': { 'read_only' },
            'requester_id': { 'post', 'put' },
            'submitter_id': { 'post' },
            'assignee_id': { 'post', 'put' },
            'organization_id': { 'read_only' },
            'group_id': { 'post', 'put' },
            'collaborator_ids': { 'post', 'put' },
            'forum_topic_id': { 'post', 'put' },
            'problem_id': { 'post', 'put' },
            'has_incidents': { 'read_only' },
            'due_at': { 'post', 'put' },
            'tags': { 'post', 'put' },
            'via': { 'read_only' },
            'custom_fields': { 'post', 'put' },
            'satisfaction_rating': { 'read_only' },
            'sharing_agreement_ids': { 'read_only' },
            'followup_ids': { 'read_only' },
            'ticket_form_id': { 'read_only' },
            'brand_id': { 'read_only' },
            'created_at': { 'read_only' },
            'updated_at': { 'read_only' },
    }

    def post(self, session):
        response = super().post(session, url)
        self.comment = '' #comment has now been posted, clear it out to prevent duplciate comments
        return response

    def put(self, session):
        response = super().put(session, self.id, url_id)
        self.comment = '' #comment has now been posted, clear it out to prevent duplciate comments
        return response

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Requester(Endpoint_Requester):

    endpoint_name = 'ticket'
    endpoint_plural = 'tickets'
    endpoint_url = 'https://{0}.zendesk.com/api/v2/tickets'
    attributes = from_properties(Ticket.attributes)

    def from_data(self, json):
        return Ticket(**super().from_data(json))

    def __init__(self, session):
        super().__init__(session)

def main():
    from Session import Session
    session = Session(
                    'z3nbe',
                    'bevans@runasroot.net',
                    token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    print(session.tickets.get(1).subject)

if __name__ == '__main__':
    main()
