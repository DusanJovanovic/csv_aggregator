import json
import unittest
from app import app

class BasicTests(unittest.TestCase): 

    # test client
    app = app.test_client()
    app.testing = True
    headers = {}


    @classmethod
    def setUpClass(cls):
        pass 

    @classmethod
    def tearDownClass(cls):
        pass 

    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestHome(BasicTests):

    def test_home(self):
        response = self.app.get('/') 

        # assert the status code and data of the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 'Hello, Friend!')


class TestUploader(BasicTests):

    def test_uploader(self):
        response = self.app.post('/api/uploader') 

        # assert the status code and data of the response
        self.assertEqual(response.data, "Hello World!!!")
