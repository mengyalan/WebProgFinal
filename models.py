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
    Unique.check("prefix", prefix)
    a = Prefix(prefix=prefix, rand_num=random.random())
    a.put()
    return a
  @classmethod
  def get(cls):
    rand_num = random.random()
    prefix = Prefix.all().order('rand_num').filter('rand_num >=', rand_num).get()
    if prefix is None:
      prefix = Prefix.all().order('rand_num').get()
    if prefix is None:
        return "Missing-"
    return prefix.prefix

class Body(db.Model) :
  body = db.StringProperty()
  rand_num = db.FloatProperty()
  @classmethod
  def create(cls, body):
    Unique.check("body", body)
    a = Body(body=body, rand_num=random.random())
    a.put()
    return a
  @classmethod
  def get(cls):
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
    Unique.check("suffix", suffix)
    a = Suffix(suffix=suffix, rand_num=random.random())
    a.put()
    return a
  @classmethod
  def get(cls):
    rand_num = random.random()
    suffix = Suffix.all().order('rand_num').filter('rand_num >=', rand_num).get()
    if suffix is None:
      suffix = Suffix.all().order('rand_num').get()
    if suffix is None:
        return "-Error"
    return suffix.suffix

class User(db.Model):
  usage = db.BooleanProperty()

  @classmethod
  def check(cls, name):
    if name is None:
        return True
    user = User.get_by_key_name(name)
    if user is None:
        user = User(key_name=name, usage=True)
        user.put()
        return False
    elif user.usage:
        return True
    else:
        user.usage = True
        user.put()
    return False
  @classmethod
  def set(cls, name, state):
    if name is None:
        return
    user = User.get_by_key_name(name)
    if user is None:
        user = User(key_name=name)
    user.usage = state
    user.put()
  @classmethod
  def reset(cls):
      query = User.all()
      entries = query.fetch(1000)
      db.delete(entries)

try:
    Prefix.create('atri')
except UniqueConstraintViolation:
    pass
try:
    Prefix.create('nigri')
except UniqueConstraintViolation:
    pass
try:
    Prefix.create('melano')
except UniqueConstraintViolation:
    pass
try:
    Prefix.create('cerule')
except UniqueConstraintViolation:
    pass
try:
    Prefix.create('cyano')
except UniqueConstraintViolation:
    pass
try:
    Prefix.create('viridi')
except UniqueConstraintViolation:
    pass

try:
    Body.create('rostr')
except UniqueConstraintViolation:
    pass
try:
    Body.create('rhyncho')
except UniqueConstraintViolation:
    pass
try:
    Body.create('ungui')
except UniqueConstraintViolation:
    pass
try:
    Body.create('chelo')
except UniqueConstraintViolation:
    pass
try:
    Body.create('onycho')
except UniqueConstraintViolation:
    pass
try:
    Body.create('pedi')
except UniqueConstraintViolation:
    pass

try:
    Suffix.create('saurus')
except UniqueConstraintViolation:
    pass
try:
    Suffix.create('raptor')
except UniqueConstraintViolation:
    pass
try:
    Suffix.create('don')
except UniqueConstraintViolation:
    pass
try:
    Suffix.create('ceratops')
except UniqueConstraintViolation:
    pass
try:
    Suffix.create('stuthio')
except UniqueConstraintViolation:
    pass
try:
    Suffix.create('nyx')
except UniqueConstraintViolation:
    pass