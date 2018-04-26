import json
import logging

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

     r = client.send_events(
        user={'here_user_key': 'here_user_value'},
        events=[{'foo': 'bar'}, {'alpha': 'beta'}])

     if r['success']:
         print r
     else:
         print r['errors']

    """
    API_URL = 'https://api.crossengage.io'
    API_VERSION = '1'

    USER_ENDPOINT = '/users/'
    EVENTS_ENDPOINT = '/events'
    BULK_ENDPOINT = '/users/batch'

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
        self.headers = {
            'X-XNG-AuthToken': self.client_token,
            'X-XNG-ApiVersion': self.API_VERSION,
            'Content-Type': 'application/json',
        }

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

    def delete_user_by_xng_id(self, user):
        # type: (dict) -> dict
        """
        Delete User given its xngId.
        :param user: dict of payload (xng_id)
        :return: json dict response, for example: {"status_code": 200}
        """
        self.request_url = self.API_URL + self.USER_ENDPOINT + 'xngId/' + user['xngId']
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

    def add_nested_user_attribute(self, parent_name, attribute_name, attribute_type):
        """
        Add new nested user attribute.
        :param parent_name: parent name of attribute
        :param attribute_name: name of new nested attribute
        :param attribute_type: type of new nested attribute
        :return: json dict response, for example: {"id": 123, "name":"traits.foobar", "attributeType": "ARRAY",
         "success": "true}
        """
        self.request_url = self.API_URL + self.USER_ENDPOINT + 'attributes'
        payload = {
            'name': attribute_name,
            'attributeType': attribute_type,
            'parentName': parent_name
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

    def send_events(self, events, email=None, user_id=None, business_unit=None):
        """
        Send up to 50 events for a given user.
        :param email: user email
        :param events: list of event payloads
        :param business_unit: businessUnit of user in crossengage
        :param user_id: id of user in your database
        :return: json dict response, for example: {"status_code": 200}
        """
        self.request_url = "{}{}".format(self.API_URL + self.EVENTS_ENDPOINT)

        if email is None and user_id is None:
            raise ValueError('email or external_id required for sending events')

        payload = {
            "id": user_id,
            "email": email,
            "events": events
        }

        if business_unit is not None:
            payload['businessUnit'] = business_unit

        return self.__create_request(payload, self.REQUEST_POST)

    def batch_process(self, delete_list=[], update_list=[]):
        """
        Delete or Update up to 1000 users in batch.
        :param delete_list: user that should get deleted
        :param update_list: user that should get updated
        :return: integer status_code, json dict response
        {
          "updated": [
            {
              "id": "fb85fe50-a528-11e7-abc4-cec278b6b50a",
              "xngId": "088818b3-445e-41a6-a7e1-cf86c8cdfbe4",
              "success": false,
              "errors": [
                {
                  "field": "id",
                  "type": "NOT_NULL"
                },
                {
                  "field": "email",
                  "type": "WRONG_FORMAT"
                }
              ]
            }
          ],
          "deleted": [
            {
              "id": "78ad0e3e-19e6-4ec1-84a7-b2c860c05387",
              "xngId": "ae86796f-8aca-4f65-a5dc-dea9a269f2a5",
              "success": false,
              "errors": [
                {
                  "field": "id",
                  "type": "NOT_NULL"
                },
                {
                  "field": "email",
                  "type": "WRONG_FORMAT"
                }
              ]
            }
          ]
        }
        """
        self.request_url = self.API_URL + self.BULK_ENDPOINT
        payload = {
            'updated': update_list,
            'deleted': delete_list,
        }

        r = self.requests.post(
            self.request_url,
            data=json.dumps(payload),
            headers=self.headers
        )

        return r.status_code, r.json()

    def __create_request(self, payload, request_type):
        r = '{}'
        try:
            if request_type == self.REQUEST_PUT:
                r = self.requests.put(self.request_url, data=json.dumps(payload), headers=self.headers)

            if request_type == self.REQUEST_GET:
                r = self.requests.get(self.request_url, headers=self.headers)

            if request_type == self.REQUEST_POST:
                r = self.requests.post(self.request_url, data=json.dumps(payload), headers=self.headers)

            if request_type == self.REQUEST_DELETE:
                r = self.requests.delete(self.request_url, data=json.dumps(payload), headers=self.headers)

            response = {}
            if r.text != '':
                response = r.json()

            response['status_code'] = r.status_code

            logging.debug("Request object", extra={
                'crossengage_url': r.request.url,
                'crossengage_headers': r.request.headers,
                'crossengage_body': r.request.body
            })

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
