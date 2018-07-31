import sys

import webapp2

from src.news.crawler import NewsCrawler

sys.path.insert(0, 'lib')

app = webapp2.WSGIApplication([
    (r'/newscrawler', NewsCrawler),
], debug=True)
