import json
import unittest

from mock import Mock
from requests import RequestException, codes

from crossengage.client import CrossengageClient


class DummyRequest(object):
    def __init__(self):
        self.status_code = codes.ok
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
        self.status_code = codes.ok

    def put(self, request_url, data, headers):
        raise RequestException('Something went wrong')

    @staticmethod
    def json():
        return {'success': True, 'errors': ''}


class TestCrossengageClient(unittest.TestCase):

    CROSSENGAGE_URL = "https://api.crossengage.io/"

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
        self.default_headers_api_v1 = {
            'X-XNG-AuthToken': 'SOME_TOKEN',
            'X-XNG-ApiVersion': '1',
            'Content-Type': 'application/json',
        }

        self.default_headers_api_v2 = {
            'X-XNG-AuthToken': 'SOME_TOKEN',
            'X-XNG-ApiVersion': '2',
            'Content-Type': 'application/json',
        }

    def test_init(self):
        self.assertEqual(self.client.client_token, 'SOME_TOKEN')
        self.assertIsNotNone(self.client.requests)
        self.assertEqual(self.client.request_url, '')
        self.assertEqual(self.client.default_headers, {
            'X-XNG-AuthToken': 'SOME_TOKEN',
            'X-XNG-ApiVersion': '1',
            'Content-Type': 'application/json',
        })

    def test_get_user(self):
        expected_response = self.user.copy()
        expected_response.update({"status_code": codes.ok})
        response = Mock(status_code=codes.ok)
        response.json.return_value = expected_response
        requests = Mock()
        requests.get.return_value = response

        self.client.requests = requests
        result = self.client.get_user(self.user)

        requests.get.assert_called_once_with(
            self.client.request_url,
            headers=self.default_headers_api_v2
        )
        self.assertEqual(expected_response, result)

    def test_update_user(self):
        self.client.requests = DummyRequest()
        response = self.client.update_user(self.user)

        self.assertEqual(self.CROSSENGAGE_URL + 'users/1234', self.client.request_url)
        self.assertEqual(self.client.default_headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.default_headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], codes.ok)
        self.assertEqual(response['errors'], '')
        self.assertEqual(response['success'], True)

    def test_update_user_request_exception(self):
        self.client.requests = DummyRequestException()
        response = self.client.update_user(self.user)

        self.assertEqual(self.CROSSENGAGE_URL + 'users/1234', self.client.request_url)
        self.assertEqual(self.client.default_headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.default_headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], 0)
        self.assertEqual(response['success'], False)

    def test_update_users_bulk(self):
        response = Mock(
            status_code=codes.ok,
            text='{"updated": [{"id": "updated_id","xngId": "updated_xngId","success": true}],'
                 '"deleted": [{"id": "deleted_id","xngId": "deleted_xngId","success": true}]}')

        response.json.return_value = json.loads(response.text)

        users = [{'email': 'email@sample.com', 'attribute_key': 'attribute_value'}]
        payload = {'updated': users}

        requests = Mock()
        requests.post.return_value = response
        self.client.requests = requests

        response = self.client.update_users_bulk(users)

        requests.post.assert_called_once_with(
            self.CROSSENGAGE_URL + 'users/batch',
            data=json.dumps(payload),
            headers={
                'X-XNG-AuthToken': 'SOME_TOKEN',
                'X-XNG-ApiVersion': '1',
                'Content-Type': 'application/json',
            }
        )

        self.assertEqual(response['status_code'], codes.ok)
        self.assertEqual(response['updated'][0]['id'], 'updated_id')
        self.assertEqual(response['updated'][0]['success'], True)

    def test_update_users_bulk_bad_request(self):
        response = Mock(
            status_code=codes.bad_request,
            text='{"updated": [{"id": "updated_id","xngId": "updated_xngId","success": false,'
                 '"errors": [{"field": "id","type": "NOT_NULL"},{"field": "email","type": "WRONG_FORMAT"}]}],'
                 '"deleted": [{"id": "deleted_id","xngId": "deleted_xngId","success": false,'
                 '"errors": [{"field": "id","type": "NOT_NULL"},{"field": "email","type": "WRONG_FORMAT"}]}]}')

        response.json.return_value = json.loads(response.text)

        users = [{'email': 'email@sample.com', 'attribute_key': 'attribute_value'}]
        payload = {'updated': users}

        requests = Mock()
        requests.post.return_value = response
        self.client.requests = requests

        response = self.client.update_users_bulk(users)

        requests.post.assert_called_once_with(
            self.CROSSENGAGE_URL + 'users/batch',
            data=json.dumps(payload),
            headers={
                'X-XNG-AuthToken': 'SOME_TOKEN',
                'X-XNG-ApiVersion': '1',
                'Content-Type': 'application/json',
            }
        )

        self.assertEqual(response['status_code'], codes.bad_request)
        self.assertEqual(response['updated'][0]['id'], 'updated_id')
        self.assertEqual(response['updated'][0]['success'], False)
        self.assertEqual(response['success'], False)

    def test_delete_user(self):
        user = {
            'id': '1',
        }
        dummy_request = DummyRequest()
        dummy_request.status_code = codes.no_content
        self.client.requests = dummy_request
        response = self.client.delete_user(user)

        self.assertEqual(self.CROSSENGAGE_URL + 'users/1', self.client.request_url)
        self.assertEqual(self.client.default_headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.default_headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.default_headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], codes.no_content)

    def test_delete_user_by_xng_id(self):
        user = {
            'xngId': '1',
        }
        dummy_request = DummyRequest()
        dummy_request.status_code = codes.no_content
        self.client.requests = dummy_request
        response = self.client.delete_user_by_xng_id(user)

        self.assertEqual(self.CROSSENGAGE_URL + 'users/xngId/1', self.client.request_url)
        self.assertEqual(self.client.default_headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.default_headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.default_headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], codes.no_content)

    def test_add_user_attribute(self):
        dummy_request = DummyRequest()
        dummy_request.status_code = codes.ok
        self.client.requests = dummy_request
        response = self.client.add_user_attribute(
            attribute_name='attr_name',
            attribute_type=CrossengageClient.ATTRIBUTE_ARRAY,
            nested_type=CrossengageClient.ATTRIBUTE_STRING
        )

        self.assertEqual(self.CROSSENGAGE_URL + 'users/attributes', self.client.request_url)
        self.assertEqual(self.client.default_headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.default_headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.default_headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], codes.ok)
        self.assertEqual(response['errors'], '')
        self.assertEqual(response['success'], True)

    def test_add_nested_user_attribute(self):
        dummy_request = DummyRequest()
        dummy_request.status_code = codes.ok
        self.client.requests = dummy_request
        response = self.client.add_nested_user_attribute(
            parent_name='parent_attribute',
            attribute_name='main_attribute',
            attribute_type=CrossengageClient.ATTRIBUTE_STRING
        )

        self.assertEqual(self.CROSSENGAGE_URL + 'users/attributes', self.client.request_url)
        self.assertEqual(self.client.default_headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.default_headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.default_headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], codes.ok)
        self.assertEqual(response['errors'], '')
        self.assertEqual(response['success'], True)

    def test_list_user_attributes(self):
        dummy_request = DummyRequest()
        dummy_request.status_code = codes.ok
        self.client.requests = dummy_request
        response = self.client.list_user_attributes(offset=0, limit=10)

        self.assertEqual(self.CROSSENGAGE_URL + 'users/attributes?offset=0&limit=10', self.client.request_url)
        self.assertEqual(self.client.default_headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.default_headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.default_headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], codes.ok)
        self.assertEqual(response['errors'], '')
        self.assertEqual(response['success'], True)

    def test_delete_user_attributes(self):
        dummy_request = DummyRequest()
        dummy_request.status_code = codes.no_content
        self.client.requests = dummy_request
        response = self.client.delete_user_attribute(attribute_id=123)

        self.assertEqual(self.CROSSENGAGE_URL + 'users/attributes/123', self.client.request_url)
        self.assertEqual(self.client.default_headers['X-XNG-AuthToken'], 'SOME_TOKEN')
        self.assertEqual(self.client.default_headers['X-XNG-ApiVersion'], '1')
        self.assertEqual(self.client.default_headers['Content-Type'], 'application/json')

        self.assertEqual(response['status_code'], codes.no_content)

    def test_send_events_with_user_id(self):
        response = Mock(status_code=codes.accepted, text='{"success": true, "errors": ""}')
        response.json.return_value = {'success': True, 'errors': ''}

        events = [{'foo': 'bar'}, {'xpto': 123}]
        payload = {
            'events': events,
            'id': 'some_id',
            'businessUnit': 'de',
        }

        requests = Mock()
        requests.post.return_value = response
        self.client.requests = requests

        response = self.client.send_events(user_id='some_id', business_unit='de', events=events)

        requests.post.assert_called_once_with(self.CROSSENGAGE_URL + 'events', data=json.dumps(payload), headers={
            'X-XNG-AuthToken': 'SOME_TOKEN',
            'X-XNG-ApiVersion': '1',
            'Content-Type': 'application/json',
        })

        self.assertEqual(response['status_code'], codes.accepted)

    def test_send_events_with_email(self):
        response = Mock(status_code=codes.accepted, text='{"success": true, "errors": ""}')
        response.json.return_value = {'success': True, 'errors': ''}

        events = [{'foo': 'bar'}, {'xpto': 123}]
        payload = {
            'events': events,
            'email': 'email@sample.com',
        }

        requests = Mock()
        requests.post.return_value = response
        self.client.requests = requests

        response = self.client.send_events(email='email@sample.com', events=events)

        requests.post.assert_called_once_with(self.CROSSENGAGE_URL + 'events', data=json.dumps(payload), headers={
            'X-XNG-AuthToken': 'SOME_TOKEN',
            'X-XNG-ApiVersion': '1',
            'Content-Type': 'application/json',
        })

        self.assertEqual(response['status_code'], codes.accepted)

    def test_send_events_value_error(self):
        events = [{'foo': 'bar'}, {'xpto': 123}]
        self.client.requests = Mock()
        self.assertRaises(ValueError, self.client.send_events, events=events)

    def test_send_events_request_exception_raised(self):
        response = Mock(status_code=codes.accepted, text='{"success": true, "errors": ""}')
        response.json.return_value = {'success': True, 'errors': ''}

        events = [{'foo': 'bar'}, {'xpto': 123}]
        payload = {
            'events': events,
            'email': 'email@sample.com',
        }

        requests = Mock()
        requests.post.side_effect = RequestException('exception raised')
        self.client.requests = requests

        response = self.client.send_events(email='email@sample.com', events=events)

        requests.post.assert_called_once_with(self.CROSSENGAGE_URL + 'events', data=json.dumps(payload), headers={
            'X-XNG-AuthToken': 'SOME_TOKEN',
            'X-XNG-ApiVersion': '1',
            'Content-Type': 'application/json',
        })

        self.assertEqual(response['success'], False)
        self.assertEqual(response['errors'], {'connection_error': 'exception raised'})

    def test_send_events_exception_raised(self):
        response = Mock(status_code=codes.accepted, text='{???}')
        response.json.return_value = {'success': True, 'errors': ''}

        events = [{'foo': 'bar'}, {'xpto': 123}]
        payload = {
            'events': events,
            'email': 'email@sample.com',
        }

        requests = Mock()
        requests.post.side_effect = Exception('exception raised')
        self.client.requests = requests

        response = self.client.send_events(email='email@sample.com', events=events)

        requests.post.assert_called_once_with(self.CROSSENGAGE_URL + 'events', data=json.dumps(payload), headers={
            'X-XNG-AuthToken': 'SOME_TOKEN',
            'X-XNG-ApiVersion': '1',
            'Content-Type': 'application/json',
        })

        self.assertEqual(response['success'], False)
        self.assertEqual(response['errors'], {'client_error': 'exception raised'})

    def test_send_events_internal_server_error_response(self):
        response = Mock(status_code=codes.server_error, text='Something went wrong')
        response.json.return_value = {}

        events = [{'foo': 'bar'}, {'xpto': 123}]
        payload = {
            'events': events,
            'email': 'email@sample.com',
        }

        requests = Mock()
        requests.post.return_value = response
        self.client.requests = requests

        response = self.client.send_events(email='email@sample.com', events=events)

        requests.post.assert_called_once_with(self.CROSSENGAGE_URL + 'events', data=json.dumps(payload), headers={
            'X-XNG-AuthToken': 'SOME_TOKEN',
            'X-XNG-ApiVersion': '1',
            'Content-Type': 'application/json',
        })

        self.assertEqual(response['success'], False)
        self.assertEqual(response['errors'], {'server_error': 'error on crossengage side'})

    def test_send_events_bad_request_error_response(self):
        response = Mock(status_code=codes.bad_request, text='{}')
        response.json.return_value = {
            'id': 'some_id',
            'xngId': 'some_xngid',
            'email': 'email+sample.com',
            'businessUnit': 'unit',
            'success': False,
            'errors': [
                {
                    'field': 'email',
                    'type': 'WRONG_VALUE',
                }
            ],
        }

        events = [{'foo': 'bar'}, {'xpto': 123}]
        payload = {
            'events': events,
            'email': 'email+sample.com',
        }

        requests = Mock()
        requests.post.return_value = response
        self.client.requests = requests

        response = self.client.send_events(email='email+sample.com', events=events)

        requests.post.assert_called_once_with(self.CROSSENGAGE_URL + 'events', data=json.dumps(payload), headers={
            'X-XNG-AuthToken': 'SOME_TOKEN',
            'X-XNG-ApiVersion': '1',
            'Content-Type': 'application/json',
        })

        self.assertEqual(response['success'], False)
        self.assertEqual(response['errors'], [
            {
                'field': 'email',
                'type': 'WRONG_VALUE',
            }
        ])

    def test_batch_process(self):
        response = Mock(
            status_code=codes.ok,
            text='{"updated": [{"id": "updated_id","xngId": "updated_xngId","success": true}],'
                 '"deleted": [{"id": "deleted_id","xngId": "deleted_xngId","success": true}]}')

        response.json.return_value = json.loads(response.text)

        updated_user = {'id': 'updated_id', 'email': 'updated@sample.com', 'attribute_key': 'value'}
        deleted_user = {'id': 'deleted_id', 'email': 'deleted@sample.com', 'attribute_key': 'value'}
        payload = {'updated': [updated_user], 'deleted': [deleted_user]}

        requests = Mock()
        requests.post.return_value = response
        self.client.requests = requests

        result = self.client.batch_process(
            delete_list=[deleted_user],
            update_list=[updated_user],
        )

        requests.post.assert_called_once_with(
            self.CROSSENGAGE_URL + 'users/batch',
            data=json.dumps(payload),
            headers=self.default_headers_api_v1
        )

        self.assertEqual(result, (codes.ok, json.loads(response.text)))

    def test_update_user_async(self):
        expected_response = {"status_code": codes.accepted, "trackingId": "2e312089-a987-45c6-adbd-b904bc4dfc97"}
        response = Mock(status_code=codes.accepted)
        response.json.return_value = expected_response
        requests = Mock()
        requests.put.return_value = response

        self.client.requests = requests
        result = self.client.update_user_async(self.user)

        requests.put.assert_called_once_with(
            self.CROSSENGAGE_URL + 'users',
            data=json.dumps(self.user),
            headers=self.default_headers_api_v2
        )
        self.assertEqual(expected_response, result)

    def test_delete_user_async(self):
        expected_response = {"status_code": codes.accepted, "trackingId": "2e312089-a987-45c6-adbd-b904bc4dfc97"}
        response = Mock(status_code=codes.accepted)
        response.json.return_value = expected_response
        requests = Mock()
        requests.delete.return_value = response

        self.client.requests = requests
        result = self.client.delete_user_async(self.user)

        requests.delete.assert_called_once_with(
            self.CROSSENGAGE_URL + 'users/' + self.user['id'],
            data=json.dumps(self.user),
            headers=self.default_headers_api_v2
        )
        self.assertEqual(expected_response, result)

    def test_batch_process_async(self):
        expected_body = {"trackingId": "2e312089-a987-45c6-adbd-b904bc4dfc97"}
        response = Mock(status_code=codes.accepted)

        response.json.return_value = expected_body

        updated_user = {'id': 'updated_id', 'email': 'updated@sample.com', 'attribute_key': 'value'}
        deleted_user = {'id': 'deleted_id', 'email': 'deleted@sample.com', 'attribute_key': 'value'}
        payload = {'updated': [updated_user], 'deleted': [deleted_user]}

        requests = Mock()
        requests.post.return_value = response
        self.client.requests = requests

        result = self.client.batch_process_async(
            delete_list=[deleted_user],
            update_list=[updated_user],
        )

        requests.post.assert_called_once_with(
            self.CROSSENGAGE_URL + 'users/batch',
            data=json.dumps(payload),
            headers=self.default_headers_api_v2
        )

        self.assertEqual(result, (codes.accepted, expected_body))

    def test_track_user_task_ok(self):
        """Crossengage returns status code 200"""
        # GIVEN
        expected_body = {"stage": "PROCESSED", "total": 2, "success": 1, "error": 1}

        response = Mock(status_code=codes.ok)
        response.json.return_value = expected_body

        requests = Mock()
        requests.get.return_value = response
        self.client.requests = requests

        # WHEN
        result = self.client.track_user_task("trackingId")

        # THEN
        requests.get.assert_called_once_with(
            self.CROSSENGAGE_URL + 'users/track/trackingId',
            headers=self.default_headers_api_v2
        )

        self.assertEqual(result, (codes.ok, expected_body))

    def test_track_user_task_not_found(self):
        """Crossengage returns status code 404"""
        # GIVEN
        response = Mock(status_code=codes.not_found)
        response.json.return_value = ValueError

        requests = Mock()
        requests.get.return_value = response
        self.client.requests = requests

        # WHEN
        result = self.client.track_user_task("trackingId")

        # THEN
        requests.get.assert_called_once_with(
            self.CROSSENGAGE_URL + 'users/track/trackingId',
            headers=self.default_headers_api_v2
        )

        self.assertEqual(result, (codes.not_found, None))
