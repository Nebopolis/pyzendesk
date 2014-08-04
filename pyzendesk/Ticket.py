__author__ = 'bevans'

import os
import requests
import simplejson as json
from collections import namedtuple
import warnings
from json import JSONEncoder
from Endpoint import Endpoint
from Endpoint import Attribute


class Ticket(Endpoint):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

def main():
    tick = Ticket(subject='Hello World', comment='description')
    print(tick.serialize())
    
if __name__ == '__main__':
    main()

