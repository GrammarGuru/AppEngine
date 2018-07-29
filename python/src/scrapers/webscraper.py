import webapp2
import json
from src.database import googlecloudstorage as db


class WebScraper(webapp2.RequestHandler):
    def get(self):
        files = db.get_files(db.get_filename())
        result = {}
        print(files)
        for file in files['web'].keys():
            title = file.split('.')[0]
            filename = db.get_filename('web/{}'.format(file))
            result[title] = db.get(filename)
        self.response.write(json.dumps(result))
