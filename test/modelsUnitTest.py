import unittest
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext import testbed

import models

def GetPrefix(entity_key):
  # Get entity from memcache if available, from datastore if not.
  prefix = memcache.get(entity_key)
  if prefix is not None:
    return entity
  prefix = models.Prefix.get(entity_key)
  return prefix

class TestUnique(unittest.TestCase):
  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Next, declare which service stubs you want to use.
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    
  def tearDown(self):
    self.testbed.deactivate()
    
  def testCheck(self):
    try:
        models.Unique.check('test1', 'value1')
    except models.UniqueConstraintViolation:
        self.fail("Should not cause exception")
    #check that the instance was inserted properly
    self.assertEqual(1, len(models.Unique.all().fetch(2)))
    try:
        models.Unique.check('test1', 'value2')
    except models.UniqueConstraintViolation:
        self.fail("Should not cause exception")
    self.assertEqual(2, len(models.Unique.all().fetch(3)))
    
    try:
        models.Unique.check('test1', 'value1')
        self.fail("Should cause exception")
    except models.UniqueConstraintViolation:
        pass
    try:
        models.Unique.check('test1', 'value2')
        self.fail("Should cause exception")
    except models.UniqueConstraintViolation:
        pass
    
    try:
        models.Unique.check('test2', 'value1')
    except models.UniqueConstraintViolation:
        self.fail("Should not cause exception")
    try:
        models.Unique.check('test2', 'value2')
    except models.UniqueConstraintViolation:
        self.fail("Should not cause exception")
    
    try:
        models.Unique.check('test2', 'value1')
        self.fail("Should cause exception")
    except models.UniqueConstraintViolation:
        pass
    try:
        models.Unique.check('test2', 'value2')
        self.fail("Should cause exception")
    except models.UniqueConstraintViolation:
        pass

class TestPrefix(unittest.TestCase):
  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Next, declare which service stubs you want to use.
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    
  def tearDown(self):
    self.testbed.deactivate()
    
  def testCreate(self):
    test1p = models.Prefix.create('test1')
    self.assertEqual(1, len(models.Prefix.all().fetch(2)))
    test1f = models.Prefix.create('test1')
    self.assertEqual(1, len(models.Prefix.all().fetch(2)))
    self.assertIsNone(test1f)
    test2p = models.Prefix.create('test2')
    self.assertEqual(2, len(models.Prefix.all().fetch(3)))
    test2f = models.Prefix.create('test2')
    self.assertEqual(2, len(models.Prefix.all().fetch(3)))
    self.assertIsNone(test2f)
    
    self.assertNotEqual(test1p.rand_num, test2p.rand_num)

  def testGetRandom(self):
    test1 = models.Prefix.getRandom()
    self.assertEqual('Missing-', test1)
    models.Prefix.create('test2')
    test2 = models.Prefix.getRandom()
    self.assertEqual('test2', test2)  
    models.Prefix.create('test3')
    count = 0
    test3 = ''
    while count<20 and test3!='test3':
        test3 = models.Prefix.getRandom() 
    if count>20:
        self.fail('Did not fetch new value randomly')

class TestBody(unittest.TestCase):
  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Next, declare which service stubs you want to use.
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    
  def tearDown(self):
    self.testbed.deactivate()
    
  def testCreate(self):
    test1p = models.Body.create('test1')
    self.assertEqual(1, len(models.Body.all().fetch(2)))
    test1f = models.Body.create('test1')
    self.assertEqual(1, len(models.Body.all().fetch(2)))
    self.assertIsNone(test1f)
    test2p = models.Body.create('test2')
    self.assertEqual(2, len(models.Body.all().fetch(3)))
    test2f = models.Body.create('test2')
    self.assertEqual(2, len(models.Body.all().fetch(3)))
    self.assertIsNone(test2f)
    
    self.assertNotEqual(test1p.rand_num, test2p.rand_num)

  def testGetRandom(self):
    test1 = models.Body.getRandom()
    self.assertEqual('Body', test1)
    models.Body.create('test2')
    test2 = models.Body.getRandom()
    self.assertEqual('test2', test2)  
    models.Body.create('test3')
    count = 0
    test3 = ''
    while count<20 and test3!='test3':
        test3 = models.Body.getRandom() 
    if count>20:
        self.fail('Did not fetch new value randomly')

class TestSuffix(unittest.TestCase):
  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Next, declare which service stubs you want to use.
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    
  def tearDown(self):
    self.testbed.deactivate()
    
  def testCreate(self):
    test1p = models.Suffix.create('test1')
    self.assertEqual(1, len(models.Suffix.all().fetch(2)))
    test1f = models.Suffix.create('test1')
    self.assertEqual(1, len(models.Suffix.all().fetch(2)))
    self.assertIsNone(test1f)
    test2p = models.Suffix.create('test2')
    self.assertEqual(2, len(models.Suffix.all().fetch(3)))
    test2f = models.Suffix.create('test2')
    self.assertEqual(2, len(models.Suffix.all().fetch(3)))
    self.assertIsNone(test2f)
    
    self.assertNotEqual(test1p.rand_num, test2p.rand_num)

  def testGetRandom(self):
    test1 = models.Suffix.getRandom()
    self.assertEqual('-Error', test1)
    models.Suffix.create('test2')
    test2 = models.Suffix.getRandom()
    self.assertEqual('test2', test2)  
    models.Suffix.create('test3')
    count = 0
    test3 = ''
    while count<20 and test3!='test3':
        test3 = models.Suffix.getRandom() 
    if count>20:
        self.fail('Did not fetch new value randomly')

class TestUser(unittest.TestCase):
  def setUp(self):
    # First, create an instance of the Testbed class.
    self.testbed = testbed.Testbed()
    # Then activate the testbed, which prepares the service stubs for use.
    self.testbed.activate()
    # Next, declare which service stubs you want to use.
    self.testbed.init_datastore_v3_stub()
    self.testbed.init_memcache_stub()
    
  def tearDown(self):
    self.testbed.deactivate()
    
  def testClaim(self):
    self.assertEqual(0, len(models.User.all().fetch(2)))
    
    models.User.claim('test1')
    self.assertEqual(1, len(models.User.all().fetch(2)))
    self.assertTrue(models.User.get_by_key_name('test1').usage)
    
    models.User.release('test2')
    models.User.claim('test2')
    self.assertEqual(2, len(models.User.all().fetch(3)))
    self.assertTrue(models.User.get_by_key_name('test2').usage)

  def testRelease(self):
    self.assertEqual(0, len(models.User.all().fetch(2)))
    
    models.User.release('test1')
    self.assertEqual(1, len(models.User.all().fetch(2)))
    self.assertFalse(models.User.get_by_key_name('test1').usage)
    
    models.User.claim('test2')
    models.User.release('test2')
    self.assertEqual(2, len(models.User.all().fetch(3)))
    self.assertFalse(models.User.get_by_key_name('test2').usage)
    
  def testIsNotAvailable(self):
    self.assertTrue(models.User.isNotAvailable(None))
    self.assertFalse(models.User.isNotAvailable('test1'))
    self.assertFalse(models.User.get_by_key_name('test1').usage)
    models.User.claim('test2')
    self.assertTrue(models.User.isNotAvailable('test2'))
    models.User.release('test3')    
    self.assertFalse(models.User.isNotAvailable('test3'))
    
  def testReset(self):
    self.assertEqual(0, len(models.User.all().fetch(2)))
    models.User.claim('test1')
    models.User.claim('test2')
    models.User.claim('test3')
    models.User.claim('test4')
    models.User.claim('test5')
    models.User.claim('test6')
    self.assertLess(0, len(models.User.all().fetch(6)))
    models.User.reset()
    self.assertEqual(0, len(models.User.all().fetch(2)))
  
if __name__ == '__main__':
    unittest.main()