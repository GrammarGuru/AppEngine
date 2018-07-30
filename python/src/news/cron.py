import webapp2

from src.news.crawler import load_articles
from src.news.storage import Category


class NewsCron(webapp2.RequestHandler):
    def get(self):
        data = load_articles()
        for title, articles in data.items():
            Category.create_category(title, articles)
        self.response.write('Success')
