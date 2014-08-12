__author__ = 'bevans'

import os
import requests
import simplejson as json
from collections import namedtuple
import warnings
from json import JSONEncoder

class Endpoint(object):

    def __init__(self, **kwargs):
        self.attributes = Attribute(type(self).__name__).attributes
        for name, value in self.attributes.items():
            if value.post_required and not (name in kwargs):
                warnings.warn('Missing required ticket field: ' + name, RuntimeWarning, stacklevel=2)
        for name, value in kwargs.items():
            if not self.attributes[name].post:
                warnings.warn('Writing to non-editable field: ' + name, RuntimeWarning, stacklevel=2)
            setattr(self, name, value)

    def update(self, json='', session=None):
        if json:
            data = [a for a in self.attributes if a in json]
            for key in data:
                setattr(self, key, json[key])
        elif self.url and session:
            response = session.get_id(self.url, self.id)
            json = response.json()[type(self).__name__.lower()]
            self.update(json)
        else: 
            warnings.warn('Updating object with no valid network ID', RuntimeWarning, stacklevel=2)

    def put(self, session, id, url):
        put_attrs = [a for a in self.attributes if self.attributes[a].put]
        response = session.put(url, self.id, self.serialize(put_attrs))
        if response.status_code == 422:
            print(response.json)
            return response.json
        json = response.json()[type(self).__name__.lower()]
        self.update(json) 

        return response

    def post(self, session, url):
        post_attrs = [a for a in self.attributes if self.attributes[a].post]
        response = session.post(url, self.serialize(post_attrs))
        if response.status_code == 422:
            print(response.json())
            return response.json
        json = response.json()[type(self).__name__.lower()]
        self.update(json)

        return response

    def __encode__(self, attributes=''):
        if not attributes:
            attributes = self.attributes
        if isinstance(self, Endpoint):
            attributes = [a for a in dir(self) if a in attributes]
            data={}
            for value in attributes:
                attr = getattr(self, value)
                if isinstance(attr, Endpoint):
                    attr = attr.__encode__()
                data[value] = attr
            return data
        raise TypeError(repr(self) + " is not JSON serializable")

    def serialize(self, attributes=''):
        data = {}
        data[type(self).__name__.lower()] = self.__encode__(attributes)
        return json.dumps(data);

class Attribute(object):

    Field = namedtuple('Field', 'read_only required post_required post put')

    endpoint_attributes = {
        'Ticket': {
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
        },
        'Group_Membership': {
            'id': { 'read_only' },
            'url': { 'read_only' },
            'user_id': { 'post_required', 'post' },
            'group_id': { 'post_required', 'post' },
            'default': { 'post' },
            'created_at': { 'read_only' },
            'updated_at': { 'read_only' },
        },
        'Group': {
            'id': { 'read_only' },
            'url': { 'read_only' },
            'name': { 'post_required', 'required', 'post', 'put' },
            'deleted': { 'read_only' },
            'created_at': { 'read_only' },
            'updated_at': { 'read_only' },
        },
    }

    def __init__(self, endpoint):
        self.attributes =  {}
        endpoint = self.endpoint_attributes[endpoint]
        for name, value in endpoint.items():
            attribute = {}
            for prop in self.Field._fields:
                attribute[prop] = True if prop in value else False
            self.attributes[name] = self.Field(**attribute)



