import json
import requests

from requests.exceptions import RequestException


class CrossengageClient(object):
    """
    Client for Crossengage public API. Support create_user, update_user, delete_user API calls.
    usage:
     from crossengage.client import CrossengageClient
     client = CrossengageClient(client_token='Place your token here')
     try:
         r = client.create_user(payload={'here_payload_key': 'here_payload_value'})
         if r.success:
             # do you magic here
         else:
             # some went wrong, see r.errors
     except Exception as e:
         print 'Create user Error: ' % e
    """
    API_URL = 'https://api.crossengage.io'

    API_VERSION = '1'

    USER_ENDPOINT = '/users/'

    REQUEST_PUT = 'put'

    REQUEST_DELETE = 'delete'

    def __init__(self, client_token):
        self.client_token = client_token
        self.requests = requests
        self.request_url = ''
        self.headers = {}

    def create_user(self, payload):
        # type: (dict) -> dict
        """
        Create User given its id.
        :param payload: dict of payload (email, id, firstName, lastName, birthday, createdAt, gender)
        :return: json dict response, for example: {"status_code": 200, "id":"123", "xngGlobalUserId": "xng-id",
         "success": "true}
        """
        return self.__sync_user(payload=payload, request_type=self.REQUEST_PUT)

    def update_user(self, payload):
        # type: (dict) -> dict
        """
        Update User given its id.
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

        response = {}

        try:
            if request_type == self.REQUEST_PUT:
                r = self.requests.put(self.request_url, data=json.dumps(payload), headers=self.headers)
                response = r.json()
            else:
                r = self.requests.delete(self.request_url, data=json.dumps(payload), headers=self.headers)
                if r.status_code == 204:
                    response['success'] = True
            response['status_code'] = r.status_code

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
        if 'client_error' not in response:
            response['client_error'] = ''

        return response
