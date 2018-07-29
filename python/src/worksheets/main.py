import webapp2
import logging
import json
from .create_worksheet import create_worksheet


class SheetMakerWeb(webapp2.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        logging.info(body['lines'])
        sheet, keys = create_worksheet(body['title'], body['lines'], body['sources'], body['removeCommas'], body['pos'])
        self.response.write(sheet.getvalue())
        self.response.write(', ')
        self.response.write(keys.getvalue())
