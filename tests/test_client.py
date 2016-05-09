import unittest

from mock import Mock

from crossengage.client import CrossengageClient


class TestCrossengageClient(unittest.TestCase):
    def setUp(self):
        self.client = CrossengageClient(client_token='SOME_TOKEN')

    def test_init(self):
        self.assertEqual(self.client.client_token, 'SOME_TOKEN')
        self.assertIsNotNone(self.client.requests)
        self.assertEqual(self.client.request_url, '')
        self.assertEqual(self.client.headers, {})

    def test_create_user(self):
        payload = {
            'email': 'email@example.com',
            'id': '1234',
            'firstName': 'Firstname',
            'lastName': 'Lastname',
            'birthday': '1991-11-07',
            'createdAt': '2015-10-02T08:23:53Z',
            'gender': 'male',
        }
        self.client.requests = Mock()
        self.client.requests.put.json.return_value = {'success': 'true'}
        self.client.create_user(payload=payload)

        self.assertEqual('https://api.crossengage.io/users/1234', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')

    def test_update_user(self):
        payload = {
            'email': 'email@example.com',
            'id': '1235',
            'firstName': 'Firstname2',
            'lastName': 'Lastname2',
            'birthday': '1991-11-07',
            'createdAt': '2015-10-02T08:23:53Z',
            'gender': 'male',
        }
        self.client.requests = Mock()
        self.client.requests.put.json.return_value = {'success': 'true'}
        self.client.create_user(payload=payload)

        self.assertEqual('https://api.crossengage.io/users/1235', self.client.request_url)
        self.assertEqual(self.client.headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.headers['Content-Type'], 'application/json')
