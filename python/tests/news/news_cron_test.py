import json
import unittest

import webtest
from google.appengine.ext import testbed, ndb

import main


class NewsCronTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()
        ndb.get_context().clear_cache()
        self.app = webtest.TestApp(main.app)

    def tearDown(self):
        self.testbed.deactivate()

    def testGet(self):
        with open('config/newspapers.json') as f:
            topics = json.load(f)['topics']

        self.app.get('/news/cron')
