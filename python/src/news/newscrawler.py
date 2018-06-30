import webapp2
import json
from src.database import googlecloudstorage as db
from src.news.scrapers.scraper import Scraper
from src.news.feed import Feed

FILE_LOC = 'data.json'


class Newscrawler(webapp2.RequestHandler):
    def get(self):
        content = db.get(db.get_filename(FILE_LOC))
        return self.response.write(content)

    def post(self):
        result = self.load_articles()
        data = db.store(json.dumps(result), db.get_filename(FILE_LOC))
        return self.response.write(json.dumps(data))

    def load_articles(self):
        papers = self._load()
        topics = papers['topics']
        del papers['topics']
        result = {}
        for topic in topics:
            articles = []
            for source, feeds in papers.items():
                if topic not in feeds:
                    continue
                feed = Feed(feeds[topic])
                for title, url in feed.get_articles():
                    try:
                        article = self.get_article(title, url)
                        if len(article['lines']) >= 10:
                            articles.append(article)
                    except:
                        pass
            result[topic] = articles
        return result

    @staticmethod
    def get_article(title, url):
        lines = Scraper(url).get_text()
        title = title.replace('&apos;', "'")
        return {'title': title, 'url': url, 'lines': lines}

    @staticmethod
    def _load():
        with open('config/newspapers.json') as f:
            return json.load(f)

