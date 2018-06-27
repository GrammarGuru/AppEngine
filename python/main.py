import sys
import webapp2
from src.news.main import Scraper

sys.path.insert(0, 'lib')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')

    def post(self):
        self.response.write(self.request.get('data'))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/scrape', Scraper)
], debug=True)