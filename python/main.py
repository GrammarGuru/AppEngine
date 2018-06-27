import sys
import webapp2
from src.news.newscrawler import Newscrawler
from src.news.scrapers.scraper import ScraperWeb

sys.path.insert(0, 'lib')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

    def post(self):
        self.response.write(self.request.get('data'))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/getNews', Newscrawler),
    ('/scrape', ScraperWeb)
], debug=True)