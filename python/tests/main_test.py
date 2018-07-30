import unittest

import webtest

import main


class HomeTest(unittest.TestCase):
    def setUp(self):
        self.app = webtest.TestApp(main.app)

    def testHelloWorldHandler(self):
        response = self.app.get('/')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.normal_body, 'Hello, World!')
        self.assertEqual(response.content_type, 'text/plain')
