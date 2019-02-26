import json
import unittest
import sys
sys.path.append('../')
from app import app

# response json for the requests with the missing data
response_mising_asset = {
	'code': 3,
	'error': 'Missing data',
	'details': {
		'data': [
            {'asset1': ['1/13/2018', '1/27/2018']},
            {'asset2': ['2/27/2018']},
            {'asset4': ['3/12/2018']},
        ]

	}
}

# response json for the requests with the gap in the date
response_date_gap = {
	'code': 2,
	'error': 'Missing dates',
	'details': {
		'dates': [
            '1/16/2018',
            '1/17/2018',
            '1/18/2018',
            '1/19/2018',
            '7/13/2018',
            '4/11/2019',
            '4/12/2019',
        ]
	}
}


class BasicTests(unittest.TestCase): 

    # test client
    app = app.test_client()
    app.testing = True
    headers = {'Content-type': 'multipart/form-data'}


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
        self.assertEqual(response.data, b'Hello, Friend!')


class TestUploader(BasicTests):

    def test_uploader_200(self):
        file_ = open('data/test_data.csv', 'rb')
        response = self.app.post(
            '/api/uploader',
            headers=self.headers,
            data={
                'data': file_,
                'aggregation': 'week',
            }
        ) 
        print(response.data)
        # assert the status code and data of the 
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'2018-01-07,4151.0,4660.0,3906.0,3363.0', response.data)
    

    def test_bad_column_name(self):
        file_ = open('data/test_bad_format1.csv', 'rb')
        response = self.app.post(
            '/api/uploader',
            headers=self.headers,
            data={
                'data': file_,
                'aggregation': 'week',
            }
        ) 
        result = json.loads(response.data)
        # assert the status code and data of the response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result, {'code': 1, 'error': 'Wrong format'})
    

    def test_bad_date_value(self):
        file_ = open('data/test_bad_format2.csv', 'rb')
        response = self.app.post(
            '/api/uploader',
            headers=self.headers,
            data={
                'data': file_,
                'aggregation': 'week',
            }
        ) 
        result = json.loads(response.data)
        # assert the status code and data of the response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result, {'code': 1, 'error': 'Wrong format'})
    

    def test_bad_asset_value(self):
        file_ = open('data/test_bad_format3.csv', 'rb')
        response = self.app.post(
            '/api/uploader',
            headers=self.headers,
            data={
                'data': file_,
                'aggregation': 'week',
            }
        ) 
        result = json.loads(response.data)
        # assert the status code and data of the response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result, {'code': 1, 'error': 'Wrong format'})
    

    def test_no_asset_columns(self):
        file_ = open('data/test_bad_format4.csv', 'rb')
        response = self.app.post(
            '/api/uploader',
            headers=self.headers,
            data={
                'data': file_,
                'aggregation': 'week',
            }
        ) 
        result = json.loads(response.data)
        # assert the status code and data of the response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result, {'code': 1, 'error': 'Wrong format'})
    

    def test_no_asset_title(self):
        file_ = open('data/test_bad_format5.csv', 'rb')
        response = self.app.post(
            '/api/uploader',
            headers=self.headers,
            data={
                'data': file_,
                'aggregation': 'week',
            }
        ) 
        result = json.loads(response.data)
        # assert the status code and data of the response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result, {'code': 1, 'error': 'Wrong format'})
    

    def test_missing_asset_value(self):
        file_ = open('data/test_data_missing_dates.csv', 'rb')
        response = self.app.post(
            '/api/uploader',
            headers=self.headers,
            data={
                'data': file_,
                'aggregation': 'week',
            }
        ) 
        result = json.loads(response.data)
        # assert the status code and data of the response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result, response_date_gap)
    

    def test_date_gap(self):
        file_ = open('data/test_data_missing_asset_data.csv', 'rb')
        response = self.app.post(
            '/api/uploader',
            headers=self.headers,
            data={
                'data': file_,
                'aggregation': 'week',
            }
        ) 
        result = json.loads(response.data)
        # assert the status code and data of the response
        self.assertEqual(response.status_code, 422)
        self.assertEqual(result, response_mising_asset)
