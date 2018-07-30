import sys

import webapp2

from src.news.cron import NewsCron
from src.news.scrapers.newsscraper import ScraperWeb
from src.news.storage import NewsMetadata, NewsData
from src.scrapers.webscraper import WebScraper
from src.worksheet.main import SheetMakerWeb

sys.path.insert(0, 'lib')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')


app = webapp2.WSGIApplication([
    (r'/', MainPage),
    (r'/news', NewsMetadata),
    (r'/news/(\d+)', NewsData),
    (r'/news/cron', NewsCron),
    (r'/web', WebScraper),
    (r'/scrape', ScraperWeb),
    (r'/worksheet', SheetMakerWeb)
], debug=True)
