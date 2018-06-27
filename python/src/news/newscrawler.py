import webapp2
import json
import os
from google.appengine.api import urlfetch, app_identity
import cloudstorage as gcs
from src.news.scrapers.usatoday import USAToday
from src.news.feed import Feed

SCRAPERS = {
    'usatoday': USAToday
}


class Newscrawler(webapp2.RequestHandler):
    def get(self):
        filename = Newscrawler.get_filename()
        gcs_file = gcs.open(filename)
        contents = gcs_file.read()
        gcs_file.close()
        self.response.write(contents)

    def post(self):
        result = self.load_articles()
        data = self.store(json.dumps(result))
        return self.response.write(json.dumps(data))

    @staticmethod
    def store(data):
        filename = Newscrawler.get_filename()

        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        gcs_file = gcs.open(filename, 'w', content_type='text/plain', retry_params=write_retry_params)
        gcs_file.write(data)
        gcs_file.close()

        return 'Success: {}'.format(data)

    def load_articles(self):
        papers = self._load()
        topics = papers['topics']
        del papers['topics']
        result = {}
        for topic in topics:
            articles = []
            for source, feeds in papers.items():
                feed = Feed(feeds[topic])
                Parser = SCRAPERS[source]
                for title, url in feed.get_articles():
                    try:
                        articles.append(self.get_article(title, url, Parser))
                    except:
                        pass
            result[topic] = articles
        return result

    @staticmethod
    def get_filename():
        bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
        bucket = '/' + bucket_name
        filename = bucket + '/' + "data.json"
        return filename

    @staticmethod
    def get_article(title, url, Parser):
        lines = Parser(url).get_text()
        return {'title': title, 'url': url, 'lines': lines}

    @staticmethod
    def _load():
        with open('config/newspapers.json') as f:
            return json.load(f)

