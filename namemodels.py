import webapp2


import cgi
import datetime
import urllib
import webapp2
import random

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
import jinja2
import os

class Unique(db.Model):
  @classmethod
  def check(cls, scope, value):
    def tx(scope, value):
      key_name = "U%s:%s" % (scope, value,)
      ue = Unique.get_by_key_name(key_name)
      if ue:
        raise UniqueConstraintViolation(scope, value)
      ue = Unique(key_name=key_name)
      ue.put()
    db.run_in_transaction(tx, scope, value)
    
class UniqueConstraintViolation(Exception):
  def __init__(self, scope, value):
    super(UniqueConstraintViolation, self).__init__("Value '%s' is not unique within scope '%s'." % (value, scope, ))

class Prefix(db.Model):
  prefix = db.StringProperty()
  rand_num = db.FloatProperty()
  @classmethod
  def create(cls, prefix):
    Unique.check("prefix", prefix)
    a = Prefix(prefix=prefix, rand_num = random.random())
    a.put()
    return a

class Body(db.Model) :
  body = db.StringProperty()
  rand_num = db.FloatProperty()
  @classmethod
  def create(cls, body):
    Unique.check("body", body)
    a = Body(body=body, rand_num = random.random())
    a.put()
    return a

class Suffix(db.Model):
  suffix = db.StringProperty()
  rand_num = db.FloatProperty()
  @classmethod
  def create(cls, suffix):
    Unique.check("suffix", suffix)
    a = Suffix(suffix=suffix, rand_num = random.random())
    a.put()
    return a

class User(db.Model):
  usage = db.BooleanProperty()
