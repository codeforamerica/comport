# -*- coding: utf-8 -*-
import base64
import json

class ComportTestClient:
    ''' Stateful client for Comport Flask test client.
    '''

    def __init__(self, client):
        ''' Create a new client, with flask test_client instance.
        '''
        self.client = client
        self.response_data = None
        self.status_code = None

    def make_auth_header(self, username, password):
        ''' Create and return an authorization header.
        '''
        bytes_credentials = '{un}:{pw}'.format(un=username, pw=password).encode()
        encoded_credentials = base64.b64encode(bytes_credentials).decode()
        return {'Authorization': 'Basic {credentials}'.format(credentials=encoded_credentials)}

    def post_json(self, path, data, username, password):
        ''' Convert the passed data to JSON, post it to the passed path, with the passed auth.
        '''
        # create the auth header
        post_headers = self.make_auth_header(username, password)

        # post the response
        response = self.client.post('/data/heartbeat', data=json.dumps(data), content_type='application/json', headers=post_headers)

        # save response values
        self.status_code = response.status_code
        self.response_data = json.loads(response.data.decode())
