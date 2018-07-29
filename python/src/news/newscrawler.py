import webapp2
import json
from src.database import googlecloudstorage as db
from src.news.scrapers.newsscraper import NewsScraper
from src.news.feed import Feed

FILE_LOC = 'data.json'


class Newscrawler(webapp2.RequestHandler):
    def get(self):
        data = self.load_articles()
        db.store(json.dumps(data), db.get_filename(FILE_LOC))
        return self.response.write('Success')

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
                        if len(article['lines']) >= 5:
                            articles.append(article)
                    except:
                        pass
            result[topic] = articles
        return result

    @staticmethod
    def get_article(title, url):
        lines = NewsScraper(url).get_text()
        title = title.replace('&apos;', "'")
        return {'title': title, 'url': url, 'lines': lines}

    @staticmethod
    def _load():
        with open('config/newspapers.json') as f:
            return json.load(f)

