import webapp2
import json
from src.database import googlecloudstorage as db


class NewsStore(webapp2.RequestHandler):
    def get(self):
        bucket = db.get_filename()
        files = db.get_files(bucket)
        return self.response.write(json.dumps(files))

    def post(self):
        filename = db.get_filename(self.request.get('file'))
        content = db.get(filename)
        return self.response.write(content)
