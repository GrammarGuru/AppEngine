# coding=utf-8
import webapp2
import json
from google.appengine.api import urlfetch
import re
from bs4 import BeautifulSoup


class Scraper(object):
    def __init__(self, url):
        self.content = self._get_content(url)
        self.soup = BeautifulSoup(self.content, 'html.parser')

    def get_article(self):
        article = self.soup.find('article')
        if article is None:
            return self.soup.find('html')
        return article

    def get_text(self):
        paragraphs = self.get_paragraphs(self.get_article())
        result = []
        for p in paragraphs:
            p = self._clean_text(p.get_text())
            if self.is_good_paragraph(p):
                result.append(p)
        return result

    @staticmethod
    def get_paragraphs(soup):
        return soup.findAll('p')

    @staticmethod
    def is_good_paragraph(p):
        lines = Scraper._split_paragraph(p)
        return len(lines) >= 2

    @staticmethod
    def _clean_text(text):
        text = text.replace(u'\u00A0', " ")
        text = text.replace(u'\u2019', "'")
        text = text.replace(u'\u2018', "'")
        text = text.encode('ascii', 'ignore')

        loc_pattern = re.compile(r'([A-Z]+[ ,.]?)+[ ,]+')
        result = re.match(loc_pattern, text)
        if result is not None:
            text = text[result.span()[1]:]
        return text.strip()

    @staticmethod
    def _split_paragraph(p):
        return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', p)

    @staticmethod
    def _get_content(url):
        page = urlfetch.fetch(url, 'html.parser')
        return page.content


class ScraperWeb(webapp2.RequestHandler):
    def post(self):
        response = Scraper(self.request.get('url')).get_text()
        self.response.write(json.dumps(response))
