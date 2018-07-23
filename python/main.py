import sys
import webapp2
from src.news.newscrawler import Newscrawler
from src.news.newsstorage import NewsStore
from src.news.scrapers.newsscraper import ScraperWeb
from src.images.imagecrawler import ImageCrawler
from src.scrapers.webscraper import WebScraper

sys.path.insert(0, 'lib')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

    def post(self):
        self.response.write(self.request.get('data'))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/getNews', NewsStore),
    ('/getWeb', WebScraper),
    ('/crawlNews', Newscrawler),
    ('/crawlImages', ImageCrawler),
    ('/scrape', ScraperWeb)
], debug=True)
