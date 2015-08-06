from Endpoint import Endpoint
from Endpoint import from_properties
from Endpoint import Requester as Endpoint_Requester

__author__ = 'bevans'

class Group(Endpoint):

    attributes = {
            'id': { 'read_only' },
            'url': { 'read_only' },
            'name': { 'post_required', 'required', 'post', 'put' },
            'deleted': { 'read_only' },
            'created_at': { 'read_only' },
            'updated_at': { 'read_only' },
        }

    def post(self, session):
        response = super().post(session, url)
        return response

    def put(self, session):
        response = super().put(session, self.id, url_id)
        return response

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Requester(Endpoint_Requester):

    endpoint_name = 'group'
    endpoint_plural = 'groups'
    endpoint_url = 'https://{0}.zendesk.com/api/v2/groups'
    attributes = from_properties(Group.attributes)

    def from_data(self, json):
        return Group(**super().from_data(json))

    def __init__(self, session):
        super().__init__(session)


def main():
    from Session import Session
    session = Session('z3nbe', 'bevans@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    memberships = session.groups.get_all()
    print([membership.name for membership in memberships])

if __name__ == '__main__':
    main()
