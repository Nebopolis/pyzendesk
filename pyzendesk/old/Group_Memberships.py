import warnings
from Endpoint import Endpoint
from Endpoint import Requester as Endpoint_Requester
from Endpoint import from_properties

__author__ = 'bevans'

class Group_Membership(Endpoint):

    attributes = {
            'id': { 'read_only' },
            'url': { 'read_only' },
            'user_id': { 'post_required', 'post' },
            'group_id': { 'post_required', 'post' },
            'default': { 'post' },
            'created_at': { 'read_only' },
            'updated_at': { 'read_only' },
    }

    def put(self, session):
        warnings.warn('Put request for a create only endpoint group_memberships with ID: ' + self.id, RuntimeWarning, stacklevel=2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Requester(Endpoint_Requester):

    endpoint_name = 'group_membership'
    endpoint_plural = 'group_memberships'
    endpoint_url = 'https://{0}.zendesk.com/api/v2/group_memberships'
    attributes = from_properties(Group_Membership.attributes)

    def from_data(self, json):
        return Group_Membership(**super().from_data(json))

    def __init__(self, session):
        super().__init__(session)


def main():
    from Session import Session
    session = Session('z3nbe', 'bevans@runasroot.net', token='ExYtkWBYio2KwTedfZ1zgDABL4KPZC8mUUau6iwu')
    print(session.group_memberships.get_all(2)[0].user_id)

if __name__ == '__main__':
    main()
