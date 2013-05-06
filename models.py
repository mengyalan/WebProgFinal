import webapp2


import cgi
import datetime
import urllib
import webapp2
import random

from google.appengine.ext import db

class Unique(db.Model):
  @classmethod
  def check(cls, scope, value):
    # Checks whether the value is a unique value or not.
    # Code from http://squeeville.com/2009/01/30/add-a-unique-constraint-to-google-app-engine/
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
    super(UniqueConstraintViolation, self).__init__("Value '%s' is not unique within scope '%s'." % (value, scope,))

class Prefix(db.Model):
  prefix = db.StringProperty()
  rand_num = db.FloatProperty()
  
  @classmethod
  def create(cls, prefix):
    # Creates a new prefix. Method ensures uniqueness
    try:
        Unique.check("prefix", prefix)
    except UniqueConstraintViolation:
        return None
    a = Prefix(prefix=prefix, rand_num=random.random())
    a.put()
    return a

  @classmethod
  def getRandom(cls):
    # Gets a random prefix from the datastore. Returns string
    rand_num = random.random()
    prefix = Prefix.all().order('rand_num').filter('rand_num >=', rand_num).get()
    if prefix is None:
      prefix = Prefix.all().order('rand_num').get()
    if prefix is None:
        return "Missing-"
    return prefix.prefix

class Body(db.Model):
  body = db.StringProperty()
  rand_num = db.FloatProperty()
  
  @classmethod
  def create(cls, body):
    # Creates a new word-body. Method ensures uniqueness
    try:
        Unique.check("body", body)
    except UniqueConstraintViolation:
        return None
    a = Body(body=body, rand_num=random.random())
    a.put()
    return a

  @classmethod
  def getRandom(cls):
    # Gets a random word-body from the datastore. Returns string
    rand_num = random.random()
    body = Body.all().order('rand_num').filter('rand_num >=', rand_num).get()
    if body is None:
      body = Body.all().order('rand_num').get()
    if body is None:
        return "Body"
    return body.body

class Suffix(db.Model):
  suffix = db.StringProperty()
  rand_num = db.FloatProperty()
  
  @classmethod
  def create(cls, suffix):
    # Creates a new suffix. Method ensures uniqueness
    try:
        Unique.check("suffix", suffix)
    except UniqueConstraintViolation:
        return None
    a = Suffix(suffix=suffix, rand_num=random.random())
    a.put()
    return a

  @classmethod
  def getRandom(cls):
    # Gets a random suffix from the datastore. Returns string
    rand_num = random.random()
    suffix = Suffix.all().order('rand_num').filter('rand_num >=', rand_num).get()
    if suffix is None:
      suffix = Suffix.all().order('rand_num').get()
    if suffix is None:
        return "-Error"
    return suffix.suffix

class User(db.Model):
  usage = db.BooleanProperty()
  RESET_AMOUNT = 1000
  
  @classmethod
  def isNotAvailable(cls, name):
    # Returns whether a nickname is available or not.
    # Returns True if the name is in use. False otherwise.
    if name is None:
        return True
    user = User.get_by_key_name(name)
    if user is None:
        user = User(key_name=name, usage=False)
        user.put()
    return user.usage

  @classmethod
  def claim(cls, name):
    # Claims a nickname in the datastore, setting its
    # usage flag to true.
    if name is None:
        return
    user = User.get_by_key_name(name)
    if user is None:
        user = User(key_name=name)
    user.usage = True
    user.put()
    
  @classmethod
  def release(cls, name):
    # Releases a nickname in the datastore, setting its
    # usage flag to false.
    if name is None:
        return
    user = User.get_by_key_name(name)
    if user is None:
        user = User(key_name=name)
    user.usage = False
    user.put()
    
  @classmethod
  def reset(cls):
      # Resets a quantity of elements in the datastore.
      # Use after multiple failed queries.
      query = User.all()
      entries = query.fetch(cls.RESET_AMOUNT)
      db.delete(entries)

Prefix.create('atri')
Prefix.create('nigri')
Prefix.create('melano')
Prefix.create('cerule')
Prefix.create('cyano')
Prefix.create('viridi')

Body.create('rostr')
Body.create('rhyncho')
Body.create('ungui')
Body.create('chelo')
Body.create('onycho')
Body.create('pedi')

Suffix.create('saurus')
Suffix.create('raptor')
Suffix.create('don')
Suffix.create('ceratops')
Suffix.create('stuthio')
Suffix.create('nyx')
