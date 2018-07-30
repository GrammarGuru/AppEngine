import unittest

from google.appengine.ext import testbed, ndb

from src.news.storage import Category, Article

CATEGORY_TITLE = 'Category'
TITLE = 'Article'
URL = 'www.url.com'
LINES = [{'line': 'I like cats.'}]
ARTICLES = [{'url': URL, 'title': TITLE, 'lines': LINES}]


class NewsStoreTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        ndb.get_context().clear_cache()
        Category.create_category(CATEGORY_TITLE, ARTICLES)

    def tearDown(self):
        self.testbed.deactivate()

    def testCategory(self):
        category = Category.query().fetch()[0]
        self.assertEquals(category.title, CATEGORY_TITLE)
        self.assertEquals(category.articles[0]['title'], TITLE)
        self.assertEquals(category.articles[0]['url'], URL)

    def testArticleFromCategory(self):
        category = Category.query().fetch()[0]
        key = category.articles[0]
        article = Article.get_by_id(key['id'])

        self.assertEquals(article.lines, LINES)
