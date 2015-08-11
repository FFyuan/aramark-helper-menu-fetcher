'''
Created on Aug 11, 2015
@author: yuanx
'''
from endpoints_proto_datastore.ndb.model import EndpointsModel
from google.appengine.ext import ndb

class Period(EndpointsModel):
    """ Period, contains some Categories """
    _message_fields_schema = ("entityKey", "selectDate", "name")
    selectDate = ndb.StringProperty()
    name = ndb.StringProperty()

class Category(EndpointsModel):
    """ Category, contains some dishes"""
    _message_fields_schema = ("entityKey", "parent", "name")
    parent = ndb.StringProperty()
    name = ndb.StringProperty()

class Dish(EndpointsModel):
    """ Dish. """
    _message_fields_schema = ("entityKey", "parent", "name")
    parent = ndb.StringProperty()
    name = ndb.StringProperty()
