import json

import webapp2
from google.appengine.ext import ndb


class Category(ndb.Model):
    title = ndb.StringProperty()
    articles = ndb.JsonProperty()

    @classmethod
    def create_category(cls, title, articles):
        keys = [Article.create_article(article['lines']) for article in articles]
        articles = [{
            'title': article['title'],
            'url': article['url'],
            'id': key.id()} for key, article in zip(keys, articles)]
        return cls(title=title, articles=articles).put()


class Article(ndb.Model):
    lines = ndb.JsonProperty()

    @classmethod
    def create_article(cls, lines):
        return cls(lines=lines).put()


class NewsMetadata(webapp2.RequestHandler):
    def get(self):
        data = Category.query()
        result = {category.title: category.articles for category in data}
        self.response.headers['Content-Type'] = 'application/json'
        return self.response.write(json.dumps(result))


class NewsData(webapp2.RequestHandler):
    def get(self, article_id):
        data = Article.get_by_id(int(article_id))

        self.response.headers['Content-Type'] = 'application/json'
        return self.response.write(json.dumps(data.lines))
