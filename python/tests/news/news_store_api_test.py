import json
import unittest

import webtest
from google.appengine.ext import testbed, ndb

import main
from src.news.storage import Category

CATEGORY_TITLE = 'Category'
TITLE = 'Article'
URL = 'www.url.com'
LINES = [{'line': 'I like cats.'}]
ARTICLES = [{'url': URL, 'title': TITLE, 'lines': LINES}]


class NewsApiTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_urlfetch_stub()
        ndb.get_context().clear_cache()
        key = Category.create_category(CATEGORY_TITLE, ARTICLES)
        self.article_id = key.get().articles[0]['id']
        self.app = webtest.TestApp(main.app)

    def tearDown(self):
        self.testbed.deactivate()

    def testGet(self):
        response = self.app.get('/news')
        category = json.loads(response.normal_body.encode('utf-8'))[CATEGORY_TITLE]

        self.assertEqual(response.status_int, 200)
        self.assertEqual(category[0]['url'], URL)
        self.assertEqual(category[0]['title'], TITLE)
        self.assertEqual(response.content_type, 'application/json')

    def testGetByURL(self):
        response = self.app.get('/news/{}'.format(self.article_id))
        response_body = json.loads(response.normal_body.encode('utf-8'))

        self.assertEqual(response.status_int, 200)
        self.assertEqual(response_body, LINES)
        self.assertEqual(response.content_type, 'application/json')
