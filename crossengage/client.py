import json

import requests


class CrossengageClient(object):
    """
    Client for Crossengage public API.
    usage:
     import client
     client = CrossengageClient(your_token)
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

    USER_URL = '/users/'

    def __init__(self, client_token):
        self.client_token = client_token
        self.requests = requests
        self.request_url = ''
        self.headers = {}

    def create_user(self, payload):
        """
        Create User given its id.
        :param payload: dict of payload (email, id, firstName, lastName, birthday ..)
        :return: json response, for example: {"id":"123", "xngGlobalUserId": "xng-id", "success": "true}
        """
        return self.__sync_user(payload, put_type=True)

    def update_user(self, payload):
        """
        Update User given its id.
        :param payload: dict of payload (email, id, firstName, lastName, birthday ..)
        :return: json response, for example: {"id":"123", "xngGlobalUserId": "xng-id", "success": "true}
        """
        return self.__sync_user(payload, put_type=True)

    def delete_user(self, payload):
        """
        Delete User given its id.
        :param payload: dict of payload (id only)
        :return: status code
        """
        return self.__sync_user(payload, put_type=False)

    def __sync_user(self, payload, put_type):
        self.request_url = self.API_URL + self.USER_URL + payload['id']
        response = self.__create_request(payload, put_type)
        return response

    def __create_request(self, payload, put_type=True):
        self.headers = {
            'X-XNG-AuthToken': self.client_token,
            'X-XNG-ApiVersion': '1',
            'Content-Type': 'application/json',
        }

        if put_type:
            r = self.requests.put(
                self.request_url,
                data=json.dumps(payload),
                headers=self.headers
            )
            return r.json()

        r = self.requests.delete(
            self.request_url,
            data=json.dumps(payload),
            headers=self.headers
        )

        return r.status_code
