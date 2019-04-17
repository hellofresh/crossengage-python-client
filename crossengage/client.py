from __future__ import absolute_import

import json
import logging

import requests
from requests.exceptions import RequestException

from crossengage.utils import update_dict


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
    API_VERSIONS = {
        "v1": "1",
        "v2": "2"
    }

    AUTH_HEADER = 'X-XNG-AuthToken'
    API_VERSION_HEADER = 'X-XNG-ApiVersion'

    USER_ENDPOINT = 'users'
    USER_BULK_ENDPOINT = "{0}/batch".format(USER_ENDPOINT)
    TRACK_USER_TASK_ENDPOINT = "{0}/track".format(USER_ENDPOINT)
    EVENTS_ENDPOINT = 'events'
    OPTOUT_ENDPOINT = 'optout-status'

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
        self.default_headers = {
            self.AUTH_HEADER: self.client_token,
            self.API_VERSION_HEADER: self.API_VERSIONS["v1"],
            'Content-Type': 'application/json',
        }

    def get_user(self, user):
        # type: (dict) -> dict
        """
        Fetch User by id.
        :param user: dict of payload (id, email, businessUnit, firstName, lastName, birthday, createdAt, gender)
        :return: json dict response, for example:
            {
                "status_code": 200,
                "email": "john.doe@crossengage.io",
                "id": "fb85fe50-a528-11e7-abc4-cec278b6b50a",
                "xngId": "123e4567-e89b-12d3-a456-426655440000",
                "firstName": "John",
                "lastName": "Doe",
                "birthday": "1982-08-30",
                "createdAt": "2015-10-02T08:23:53Z",
                "gender": "male"
            }
        """
        self.request_url = "{0}/{1}/{2}".format(self.API_URL, self.USER_ENDPOINT, user['id'])
        return self.__create_request(payload={}, request_type=self.REQUEST_GET, version="v2")

    def update_user(self, user):
        # type: (dict) -> dict
        """
        Create / Update User given its id.
        :param user: dict of payload (email, id, firstName, lastName, birthday, createdAt, gender)
        :return: json dict response, for example: {"status_code": 200, "id":"123", "xngGlobalUserId": "xng-id",
         "success": "true}
        """
        self.request_url = "{0}/{1}/{2}".format(self.API_URL, self.USER_ENDPOINT, user['id'])
        return self.__create_request(payload=user, request_type=self.REQUEST_PUT, version="v1")

    def update_user_async(self, user):
        # type: (dict) -> dict
        """
        Create / Update User given its id and email.
        :param user: dict of payload (id, email, businessUnit, firstName, lastName, birthday, createdAt, gender)
        :return: json dict response, for example:
          {"status_code": 202, "trackingId": "2e312089-a987-45c6-adbd-b904bc4dfc97"}
        """
        self.request_url = "{0}/{1}".format(self.API_URL, self.USER_ENDPOINT)
        return self.__create_request(payload=user, request_type=self.REQUEST_PUT, version="v2")

    def update_users_bulk(self, users):
        # type: (list) -> dict
        """
        Warning! Deprecated method, use batch_process instead.
        Create / Update User bulk.
        :param users: list of user dicts [(email, id, firstName, lastName, birthday, createdAt, gender)]
        :return: json dict response
        """
        payload = {'updated': users}
        self.request_url = "{0}/{1}".format(self.API_URL, self.USER_BULK_ENDPOINT)
        return self.__create_request(payload=payload, request_type=self.REQUEST_POST, version="v1")

    def delete_user(self, user):
        # type: (dict) -> dict
        """
        Delete User given its id.
        :param user: dict of payload (id)
        :return: json dict response, for example: {"status_code": 200}
        """
        self.request_url = "{0}/{1}/{2}".format(self.API_URL, self.USER_ENDPOINT, user['id'])
        return self.__create_request(payload=user, request_type=self.REQUEST_DELETE, version="v1")

    def delete_user_async(self, user):
        # type: (dict) -> dict
        """
        Delete User given its id.
        :param user: dict of payload (id)
        :return: json dict response, for example:
            {"status_code": 202, "trackingId": "2e312089-a987-45c6-adbd-b904bc4dfc97"}
        """
        self.request_url = "{0}/{1}/{2}".format(self.API_URL, self.USER_ENDPOINT, user['id'])
        return self.__create_request(payload=user, request_type=self.REQUEST_DELETE, version="v2")

    def delete_user_by_xng_id(self, user):
        # type: (dict) -> dict
        """
        Delete User given its xngId.
        :param user: dict of payload (xng_id)
        :return: json dict response, for example: {"status_code": 200}
        """
        self.request_url = "{0}/{1}/xngId/{2}".format(self.API_URL, self.USER_ENDPOINT, user['xngId'])
        return self.__create_request(payload=user, request_type=self.REQUEST_DELETE, version="v1")

    def add_user_attribute(self, attribute_name, attribute_type, nested_type):
        """
        Add new user attribute.
        :param attribute_name: name of new attribute
        :param attribute_type: type of new attribute
        :param nested_type: nested_type of new attribute
        :return: json dict response, for example: {"id": 123, "name":"traits.foobar", "attributeType": "ARRAY",
         "success": "true}
        """
        self.request_url = "{0}/{1}/attributes".format(self.API_URL, self.USER_ENDPOINT)
        payload = {
            'name': 'traits.' + attribute_name,
            'attributeType': attribute_type,
            'nestedType': nested_type
        }
        return self.__create_request(payload, self.REQUEST_POST, version="v1")

    def add_nested_user_attribute(self, parent_name, attribute_name, attribute_type):
        """
        Add new nested user attribute.
        :param parent_name: parent name of attribute
        :param attribute_name: name of new nested attribute
        :param attribute_type: type of new nested attribute
        :return: json dict response, for example: {"id": 123, "name":"traits.foobar", "attributeType": "ARRAY",
         "success": "true}
        """
        self.request_url = "{0}/{1}/attributes".format(self.API_URL, self.USER_ENDPOINT)
        payload = {
            'name': attribute_name,
            'attributeType': attribute_type,
            'parentName': parent_name
        }
        return self.__create_request(payload, self.REQUEST_POST, version="v1")

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
        self.request_url = "{0}/{1}/attributes?offset={2}&limit={3}".format(
            self.API_URL, self.USER_ENDPOINT, offset, limit)
        return self.__create_request(None, self.REQUEST_GET, version="v1")

    def delete_user_attribute(self, attribute_id):
        """
            Delete user attribute.
            :param attribute_id: id of attribute
            :return: response N/A or error_response
            """
        self.request_url = "{0}/{1}/attributes/{2}".format(self.API_URL, self.USER_ENDPOINT, attribute_id)
        payload = {}
        return self.__create_request(payload, self.REQUEST_DELETE, version="v1")

    def send_events(self, events, email=None, user_id=None, business_unit=None):
        """
        Send up to 50 events for a given user.
        :param email: user email
        :param events: list of event payloads
        :param business_unit: businessUnit of user in crossengage
        :param user_id: id of user in your database
        :return: json dict response, for example: {"status_code": 200}
        """
        self.request_url = "{0}/{1}".format(self.API_URL, self.EVENTS_ENDPOINT)

        if email is None and user_id is None:
            raise ValueError('email or external_id required for sending events')

        payload = {
            "events": events
        }

        if email is not None:
            payload['email'] = email

        if user_id is not None:
            payload['id'] = user_id

        if business_unit is not None:
            payload['businessUnit'] = business_unit

        return self.__create_request(payload, self.REQUEST_POST, version="v1")

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
        self.request_url = "{0}/{1}".format(self.API_URL, self.USER_BULK_ENDPOINT)
        payload = {
            'updated': update_list,
            'deleted': delete_list,
        }

        r = self.requests.post(
            self.request_url,
            data=json.dumps(payload),
            headers=self.default_headers,
            timeout=30
        )

        return r.status_code, r.json()

    def batch_process_async(self, delete_list=[], update_list=[]):
        """
        Create, Update or Delete up to 1000 users in batch.
        :param delete_list: users that should be deleted
        :param update_list: users that should be created or updated
        :return integer status_code, json dict response
            202, {"trackingId": "2e312089-a987-45c6-adbd-b904bc4dfc97"}
        """
        headers = update_dict(self.default_headers, {self.API_VERSION_HEADER: self.API_VERSIONS["v2"]})
        self.request_url = "{0}/{1}".format(self.API_URL, self.USER_BULK_ENDPOINT)

        payload = {
            'updated': update_list,
            'deleted': delete_list,
        }

        r = self.requests.post(self.request_url, data=json.dumps(payload), headers=headers, timeout=30)

        return r.status_code, r.json()

    def track_user_task(self, tracking_id):
        # type: (dict) -> dict
        """
        Create / Update User given its id.
        :param user: dict of payload (email, id, firstName, lastName, birthday, createdAt, gender)
        :return integer status_code, json dict response
            200, { "stage": "PROCESSED", "total": 2, "success": 1, "error": 1 }
        """
        headers = update_dict(self.default_headers, {self.API_VERSION_HEADER: self.API_VERSIONS["v2"]})
        self.request_url = "{0}/{1}/{2}".format(self.API_URL, self.TRACK_USER_TASK_ENDPOINT, tracking_id)

        r = self.requests.get(self.request_url, headers=headers, timeout=30)

        try:
            body = r.json()
        except ValueError:
            body = None

        return r.status_code, body

    def get_user_opt_out_status(self, user_id):
        # type: (str) -> dict
        """
        Fetch User Opt-Out status by id.
        :param user_id: User external ID
        :return: json dict response, for example:
            {
                "optOut": false
            }
        """
        self.request_url = "{0}/{1}/{2}/{3}".format(self.API_URL, self.USER_ENDPOINT, user_id, self.OPTOUT_ENDPOINT)
        return self.__create_request(payload={}, request_type=self.REQUEST_GET, version="v1")

    def update_user_opt_out_status(self, user_id, channel_name):
        # type: (str, str) -> dict
        """
        Fetch User Opt-Out status by id.
        :param user_id: User ID
        :param channel_name: Name of the channel to opt out user from. It has to be one of MAIL, BROWSER_NOTIFICATION,
                             ONSITE_DISPLAY, EXIT_INTENT, PUSH_NOTIFICATION, DIRECT_MAIL or SMS
        :return: json dict response, for example:
            {
                "optOut": true
            }
        """
        self.request_url = "{0}/{1}/{2}/{3}?channelType={4}".format(
            self.API_URL, self.USER_ENDPOINT, user_id, self.OPTOUT_ENDPOINT, channel_name
        )
        return self.__create_request(payload={"optOut": True}, request_type=self.REQUEST_PUT, version="v1")

    def update_user_opt_in_status(self, user_id, channel_name):
        # type: (str, str) -> dict
        """
        Fetch User Opt-In status by id.
        :param user_id: User ID
        :param channel_name: Name of the channel to opt in user to. It has to be one of MAIL, BROWSER_NOTIFICATION,
                             ONSITE_DISPLAY, EXIT_INTENT, PUSH_NOTIFICATION, DIRECT_MAIL or SMS
        :return: json dict response, for example:
            {
                "optOut": false
            }
        """
        self.request_url = "{0}/{1}/{2}/{3}?channelType={4}".format(
            self.API_URL, self.USER_ENDPOINT, user_id, self.OPTOUT_ENDPOINT, channel_name
        )
        return self.__create_request(payload={"optOut": False}, request_type=self.REQUEST_PUT, version="v1")

    def __create_request(self, payload, request_type, version):
        headers = update_dict(self.default_headers, {self.API_VERSION_HEADER: self.API_VERSIONS[version]})
        try:
            if request_type == self.REQUEST_PUT:
                r = self.requests.put(self.request_url, data=json.dumps(payload), headers=headers, timeout=30)

            if request_type == self.REQUEST_GET:
                r = self.requests.get(self.request_url, headers=headers, timeout=30)

            if request_type == self.REQUEST_POST:
                r = self.requests.post(self.request_url, data=json.dumps(payload), headers=headers, timeout=30)

            if request_type == self.REQUEST_DELETE:
                r = self.requests.delete(self.request_url, data=json.dumps(payload), headers=headers, timeout=30)

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
            response = {'success': False, 'errors': {'connection_error': str(e)}}
        except Exception as e:
            # handle all exceptions which can be on API side
            response = {'success': False, 'errors': {'client_error': str(e)}}

        if 'status_code' not in response:
            response['status_code'] = 0

        if response['status_code'] == 500:
            response['success'] = False
            response['errors'] = {'server_error': 'error on crossengage side'}

        if response['status_code'] > 202:
            response['success'] = False

        return response
