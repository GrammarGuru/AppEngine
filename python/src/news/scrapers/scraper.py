from google.appengine.api import urlfetch
import re
from bs4 import BeautifulSoup


class Scraper(object):
    def __init__(self, url):
        self.content = self._get_content(url)
        self.soup = BeautifulSoup(self.content, 'html.parser')

    def get_article(self):
        return self.soup.find('html')

    def get_text(self):
        paragraphs = self.get_paragraphs(self.get_article())
        return [line.strip() for p in paragraphs for line in self._split_paragraph(self._clean_text(p.get_text()))]

    @staticmethod
    def get_paragraphs(soup):
        return soup.findAll('p')

    @staticmethod
    def _clean_text(text):
        return text.replace(u'\u00A0', " ").\
            replace(u'\u2019', "'").\
            replace(u'\u2018', "'").\
            encode('ascii', 'ignore')

    @staticmethod
    def _split_paragraph(p):
        return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', p)

    @staticmethod
    def _get_content(url):
        page = urlfetch.fetch(url, 'html.parser')
        return page.content
