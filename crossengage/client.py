import json
import requests

from requests.exceptions import RequestException


class CrossengageClient(object):
    """
    Client for Crossengage public API. Support create_user, update_user, delete_user, create_attribute,
    delete_attribute API calls.

    Usage:

     from crossengage.client import CrossengageClient
     client = CrossengageClient(client_token='Place your token here')
     r = client.update_user(payload={'here_payload_key': 'here_payload_value'})

     r = client.delete_user(payload={'here_payload_key': 'here_payload_value'})

     r = client.add_user_attribute(
             attribute_name='our_new_attribute',
             attribute_type=client.ATTRIBUTE_ARRAY,
             nested_type=client.ATTRIBUTE_STRING
         )

     r = client.list_user_attributes(offset=0, limit=10)

     r = client.delete_user_attribute(attribute_id=123)

     if r['success']:
         # do you magic here
         print r
     else:
         # some went wrong, see r.errors
         print r['client_error']
         print r['errors']

    """
    API_URL = 'https://api.crossengage.io'
    API_VERSION = '1'

    USER_ENDPOINT = '/users/'

    REQUEST_GET = 'get'
    REQUEST_PUT = 'put'
    REQUEST_DELETE = 'delete'
    REQUEST_POST = 'post'

    ATTRIBUTE_STRING = 'STRING'
    ATTRIBUTE_DATETIME = 'DATETIME'
    ATTRIBUTE_FLOAT = 'FLOAT'
    ATTRIBUTE_INTEGER = 'INTEGER'
    ATTRIBUTE_BOOLEAN = 'BOOLEAN'
    ATTRIBUTE_ARRAY = 'ARRAY'
    ATTRIBUTE_OBJECT = 'OBJECT'

    def __init__(self, client_token):
        self.client_token = client_token
        self.requests = requests
        self.request_url = ''
        self.headers = {}

    def update_user(self, payload):
        # type: (dict) -> dict
        """
        Create / Update User given its id.
        :param payload: dict of payload (email, id, firstName, lastName, birthday, createdAt, gender)
        :return: json dict response, for example: {"status_code": 200, "id":"123", "xngGlobalUserId": "xng-id",
         "success": "true}
        """
        return self.__sync_user(payload=payload, request_type=self.REQUEST_PUT)

    def delete_user(self, payload):
        # type: (dict) -> dict
        """
        Delete User given its id.
        :param payload: dict of payload (id)
        :return: json dict response, for example: {"status_code": 200}
        """
        return self.__sync_user(payload=payload, request_type=self.REQUEST_DELETE)

    def add_user_attribute(self, attribute_name, attribute_type, nested_type):
        """
        Add new user attribute.
        :param attribute_name: name of new attribute
        :param attribute_type: type of new attribute
        :param nested_type: nested_type of new attribute
        :return: json dict response, for example: {"id": 123, "name":"traits.foobar", "attributeType": "ARRAY",
         "success": "true}
        """
        self.request_url = self.API_URL + self.USER_ENDPOINT + 'attributes'
        payload = {
            'name': 'traits.' + attribute_name,
            'attributeType': attribute_type,
            'nestedType': nested_type
        }
        return self.__create_request(payload, self.REQUEST_POST)

    def list_user_attributes(self, offset, limit):
        """
            List of user attributes.
            :param offset: request offset
            :param limit: request limit
            :return: json dict response, for example: {"attributes": [{"id": 1234, "name": "traits.name",
            "attributeType": "STRING" }], "total": "1"}
        """
        self.request_url = self.API_URL + self.USER_ENDPOINT + 'attributes'
        payload = {
            'offset': offset,
            'limit': limit,
        }
        return self.__create_request(payload, self.REQUEST_GET)

    def delete_user_attribute(self, attribute_id):
        """
            Delete user attribute.
            :param attribute_id: id of attribute
            :return: response N/A or error_response
            """
        self.request_url = self.API_URL + self.USER_ENDPOINT + 'attributes/' + str(attribute_id)
        payload = {}
        return self.__create_request(payload, self.REQUEST_DELETE)

    def __sync_user(self, payload, request_type):
        if 'id' in payload:
            self.request_url = self.API_URL + self.USER_ENDPOINT + payload['id']
            return self.__create_request(payload, request_type)

        return {'success': False, 'client_error': 'Missing id in payload', 'errors': ''}

    def __create_request(self, payload, request_type):
        self.headers = {
            'X-XNG-AuthToken': self.client_token,
            'X-XNG-ApiVersion': self.API_VERSION,
            'Content-Type': 'application/json',
        }

        r = '{}'
        try:
            if request_type == self.REQUEST_PUT:
                r = self.requests.put(self.request_url, data=json.dumps(payload), headers=self.headers)

            if request_type == self.REQUEST_GET:
                r = self.requests.get(self.request_url, data=json.dumps(payload), headers=self.headers)

            if request_type == self.REQUEST_POST:
                r = self.requests.post(self.request_url, data=json.dumps(payload), headers=self.headers)

            if request_type == self.REQUEST_DELETE:
                r = self.requests.delete(self.request_url, data=json.dumps(payload), headers=self.headers)

            response = r.json()
            response['status_code'] = r.status_code
            response['client_error'] = ''

            if response['status_code'] == 200 or response['status_code'] == 204:
                response['success'] = True

        except RequestException as e:
            # handle all requests HTTP exceptions
            response = {'client_error': e.message}
        except Exception as e:
            # handle all exceptions which can be on API side
            response = {'client_error': (e.message + '. Response: ' + r.text)}

        if 'errors' not in response:
            response['errors'] = ''
        if 'status_code' not in response:
            response['status_code'] = 0
        if 'success' not in response:
            response['success'] = False

        return response
