import sys
import webapp2
from src.news.newscrawler import Newscrawler
from src.news.newsstorage import NewsStore
from src.news.scrapers.scraper import ScraperWeb
from src.images.imagecrawler import ImageCrawler
from src.worksheets.main import SheetMakerWeb

sys.path.insert(0, 'lib')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/getNews', NewsStore),
    ('/crawlNews', Newscrawler),
    ('/crawlImages', ImageCrawler),
    ('/scrape', ScraperWeb),
    ('/worksheet', SheetMakerWeb)
], debug=True)
