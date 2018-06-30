import webapp2
import json
import datetime
from google.appengine.api import urlfetch
from src.database import googlecloudstorage as db

URL = 'https://newsapi.org/v2/everything?sources=national-geographic&apiKey={}&from={}&to={}&pageSize={}'
FILE_LOC = 'images.json'


class ImageCrawler(webapp2.RequestHandler):
    def get(self):
        content = db.get(db.get_filename(FILE_LOC))
        return self.response.write(content)

    def post(self):
        data = get_images()
        result = db.store(json.dumps(data), db.get_filename(FILE_LOC))
        return self.response.write(json.dumps(result))


def get_images(page_size=100):
    from_date, to_date = get_week()
    response = urlfetch.fetch(URL.format(get_api_key(), from_date, to_date, page_size))
    articles = json.loads(response.content)
    return [article['urlToImage'] for article in articles['articles'] if article['urlToImage'] is not None]


def get_week():
    end = datetime.datetime.now()
    begin = end - datetime.timedelta(days=7)
    return format_data(begin), format_data(end)


def format_data(date):
    return '{}-{:02d}-{:02d}'.format(date.year, date.month, date.day)


def get_api_key():
    with open('config/newsapi.json') as f:
        return json.load(f)['key']