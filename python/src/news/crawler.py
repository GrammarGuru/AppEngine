import json

from src.news.feed import Feed
from src.news.scrapers.newsscraper import NewsScraper

FILE_LOC = 'data.json'


def load_articles(size=12):
    papers = _load()
    topics = papers['topics']
    del papers['topics']
    result = {}
    for topic in topics:
        articles = []
        for source, feeds in papers.items():
            if topic not in feeds:
                continue
            feed = Feed(feeds[topic])
            for title, url in feed.get_articles(size):
                try:
                    article = get_article(title, url)
                    if len(article['lines']) >= 5:
                        articles.append(article)
                except:
                    pass
        result[topic] = articles
    return result


def get_article(title, url):
    lines = NewsScraper(url).get_text()
    title = title.replace('&apos;', "'")
    return {'title': title, 'url': url, 'lines': lines}


def _load():
    with open('config/newspapers.json') as f:
        return json.load(f)
