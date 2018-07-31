import json
import unittest
from io import BytesIO

import webtest
from google.appengine.ext import testbed

import main
from src.worksheet.create_worksheet import create_worksheet

TITLE = 'test'
LINES = [
    'I like cats.',
    'I am big.',
    'I jumped over a fence.'
]
REMOVE_COMMAS = True
SOURCES = []
with open('tests/worksheet/pos.json') as f:
    POS = json.load(f)


class WorksheetTest(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_urlfetch_stub()
        self.app = webtest.TestApp(main.app)

    def tearDown(self):
        self.testbed.deactivate()

    def testSheet(self):
        sheet, key = create_worksheet(TITLE, LINES, SOURCES, REMOVE_COMMAS, POS)
        self.assertIsInstance(sheet, BytesIO)
        self.assertIsInstance(key, BytesIO)

    def testApi(self):
        response = self.app.post_json('/worksheet', {
            'title': TITLE,
            'lines': LINES,
            'sources': SOURCES,
            'removeCommas': REMOVE_COMMAS,
            'pos': POS
        }).normal_body

        self.assertEquals(len(response.split(b', key: ')), 2)
