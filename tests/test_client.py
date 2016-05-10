import unittest

from mock import Mock
from requests import RequestException

from crossengage.client import CrossengageClient


class DummyRequest(object):
    def __init__(self):
        self.status_code = 200
        self.text = 'Some text'

    def put(self, request_url, data, headers):
        return self

    def delete(self, request_url, data, headers):
        return self

    @staticmethod
    def json():
        return {'success': True, 'errors': ''}


class DummyRequestException(object):
    def __init__(self):
        self.status_code = 200

    def put(self, request_url, data, headers):
        raise RequestException('Something went wrong')

    @staticmethod
    def json():
        return {'success': True, 'errors': ''}


class TestCrossengageClient(unittest.TestCase):
    def setUp(self):
        self.client = CrossengageClient(client_token='SOME_TOKEN')
        self.payload = {
            'email': 'email@example.com',
            'id': '1234',
            'firstName': 'Firstname',
            'lastName': 'Lastname',
            'birthday': '1991-11-07',
            'createdAt': '2015-10-02T08:23:53Z',
            'gender': 'male',
        }

    def test_init(self):
        self.assertEqual(self.client.client_token, 'SOME_TOKEN')
        self.assertIsNotNone(self.client.requests)
        self.assertEqual(self.client.request_url, '')
        self.assertEqual(self.client.headers, {})

    def test_create_update_user(self):
        self.client.requests = DummyRequest()
        response = self.client.create_user(payload=self.payload)

        self.assertEqual('https://api.crossengage.io/users/1234', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], 200)
        self.assertEqual(response['errors'], '')
        self.assertEqual(response['client_error'], '')
        self.assertEqual(response['success'], True)

    def test_create_update_user_request_exception(self):
        self.client.requests = DummyRequestException()
        response = self.client.create_user(payload=self.payload)

        self.assertEqual('https://api.crossengage.io/users/1234', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], 0)
        self.assertEqual(response['errors'], '')
        self.assertEqual(response['client_error'], 'Something went wrong')
        self.assertEqual(response['success'], False)

    def test_delete_user(self):
        payload = {
            'id': '1',
        }
        dummy_request = DummyRequest()
        dummy_request.status_code = 204
        self.client.requests = dummy_request
        response = self.client.delete_user(payload)

        self.assertEqual('https://api.crossengage.io/users/1', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], 204)
        self.assertEqual(response['errors'], '')
        self.assertEqual(response['client_error'], '')
        self.assertEqual(response['success'], True)
