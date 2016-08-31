import unittest

from mock import Mock

from crossengage.client import CrossengageClient
from requests import RequestException


class DummyRequest(object):
    def __init__(self):
        self.status_code = 200
        self.text = 'Some text'
        self.request = Mock()

    def put(self, request_url, data, headers):
        return self

    def delete(self, request_url, data, headers):
        return self

    def post(self, request_url, data, headers):
        return self

    def get(self, request_url, headers):
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
        self.user = {
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

    def test_update_user(self):
        self.client.requests = DummyRequest()
        response = self.client.update_user(self.user)

        self.assertEqual('https://api.crossengage.io/users/1234', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], 200)
        self.assertEqual(response['errors'], '')
        self.assertEqual(response['success'], True)

    def test_update_user_request_exception(self):
        self.client.requests = DummyRequestException()
        response = self.client.update_user(self.user)

        self.assertEqual('https://api.crossengage.io/users/1234', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], 0)
        self.assertEqual(response['success'], False)

    def test_delete_user(self):
        user = {
            'id': '1',
        }
        dummy_request = DummyRequest()
        dummy_request.status_code = 204
        self.client.requests = dummy_request
        response = self.client.delete_user(user)

        self.assertEqual('https://api.crossengage.io/users/1', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], 204)

    def test_add_user_attribute(self):
        dummy_request = DummyRequest()
        dummy_request.status_code = 200
        self.client.requests = dummy_request
        response = self.client.add_user_attribute(
            attribute_name='attr_name',
            attribute_type=CrossengageClient.ATTRIBUTE_ARRAY,
            nested_type=CrossengageClient.ATTRIBUTE_STRING
        )

        self.assertEqual('https://api.crossengage.io/users/attributes', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], 200)
        self.assertEqual(response['errors'], '')
        self.assertEqual(response['success'], True)

    def test_list_user_attributes(self):
        dummy_request = DummyRequest()
        dummy_request.status_code = 200
        self.client.requests = dummy_request
        response = self.client.list_user_attributes(offset=0, limit=10)

        self.assertEqual('https://api.crossengage.io/users/attributes?offset=0&limit=10', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], 200)
        self.assertEqual(response['errors'], '')
        self.assertEqual(response['success'], True)

    def test_delete_user_attributes(self):
        dummy_request = DummyRequest()
        dummy_request.status_code = 204
        self.client.requests = dummy_request
        response = self.client.delete_user_attribute(attribute_id=123)

        self.assertEqual('https://api.crossengage.io/users/attributes/123', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], 204)

    def test_send_events(self):
        dummy_request = DummyRequest()
        dummy_request.status_code = 202
        self.client.requests = dummy_request

        events = [{'foo': 'bar'}, {'xpto': 123}]
        response = self.client.send_events(self.user, events)

        self.assertEqual('https://api.crossengage.io/events', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], 204)
