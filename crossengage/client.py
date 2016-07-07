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
     r = client.update_user(user={'here_user_key': 'here_user_value'})

     r = client.delete_user(user={'here_user_key': 'here_user_value'})

     r = client.add_user_attribute(
             attribute_name='our_new_attribute',
             attribute_type=client.ATTRIBUTE_ARRAY,
             nested_type=client.ATTRIBUTE_STRING
         )

     r = client.list_user_attributes(offset=0, limit=10)

     r = client.delete_user_attribute(attribute_id=123)

     if r['success']:
         print r
     else:
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

    def update_user(self, user):
        # type: (dict) -> dict
        """
        Create / Update User given its id.
        :param user: dict of payload (email, id, firstName, lastName, birthday, createdAt, gender)
        :return: json dict response, for example: {"status_code": 200, "id":"123", "xngGlobalUserId": "xng-id",
         "success": "true}
        """
        self.request_url = self.API_URL + self.USER_ENDPOINT + user['id']
        return self.__create_request(payload=user, request_type=self.REQUEST_PUT)

    def update_users_bulk(self, users):
        # type: (list) -> dict
        """
        Create / Update User bulk.
        :param users: list of user dicts [(email, id, firstName, lastName, birthday, createdAt, gender)]
        :return: json dict response
        """
        payload = {'updated': users}
        self.request_url = self.API_URL + self.USER_ENDPOINT + 'batch'
        return self.__create_request(payload=payload, request_type=self.REQUEST_POST)

    def delete_user(self, user):
        # type: (dict) -> dict
        """
        Delete User given its id.
        :param user: dict of payload (id)
        :return: json dict response, for example: {"status_code": 200}
        """
        self.request_url = self.API_URL + self.USER_ENDPOINT + user['id']
        return self.__create_request(payload=user, request_type=self.REQUEST_DELETE)

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
        self.request_url = self.API_URL + self.USER_ENDPOINT + 'attributes?offset=' + str(offset) + '&limit=' + str(
            limit)
        return self.__create_request(None, self.REQUEST_GET)

    def delete_user_attribute(self, attribute_id):
        """
            Delete user attribute.
            :param attribute_id: id of attribute
            :return: response N/A or error_response
            """
        self.request_url = self.API_URL + self.USER_ENDPOINT + 'attributes/' + str(attribute_id)
        payload = {}
        return self.__create_request(payload, self.REQUEST_DELETE)

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
                response = r.json()

            if request_type == self.REQUEST_GET:
                r = self.requests.get(self.request_url, headers=self.headers)
                response = r.json()

            if request_type == self.REQUEST_POST:
                r = self.requests.post(self.request_url, data=json.dumps(payload), headers=self.headers)
                response = r.json()

            if request_type == self.REQUEST_DELETE:
                r = self.requests.delete(self.request_url, data=json.dumps(payload), headers=self.headers)
                response = {}

            response['status_code'] = r.status_code

        except RequestException as e:
            # handle all requests HTTP exceptions
            response = {'success': False, 'errors': {'connection_error': e.message}}
        except Exception as e:
            # handle all exceptions which can be on API side
            response = {'success': False, 'errors': {'client_error': e.message + '. Response: ' + r.text}}

        if 'status_code' not in response:
            response['status_code'] = 0

        if response['status_code'] == 500:
            response['success'] = False
            response['errors'] = {'server_error': response['message']}

        return response
