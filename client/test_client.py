# -*-coding:utf-8-*-
# @auth ivan
# @time 2016-11-9 10:26:27
# @goal test the client & provider

from django.shortcuts import render
from django.http import HttpResponse

from client import Client
import utils

import json
import requests
s = requests.session()

url1 = 'U_R_L// oauth/get_authorization_code/?'
url2 = 'U_R_L// oauth/get_token_key/?'
url3 = 'U_R_L// oauth/refresh_token/?'

MOCK_CLIENT_ID = 'abc123456789'
MOCK_CLIENT_SECRET = 'MNBVCXZLKJHGFDSAPOIUYTREWQ'
MOCK_REDIRECT_URI = 'U_R_L// myapp/oauth_endpoint/'
MOCK_AUTHORIZATION_CODE = 'poiuytrewqlkjhgfdsamnbvcxz0987654321'
MOCK_REFRESH_TOKEN = 'uhbygvtfcrdxeszokmijn'


class MockClient(Client):
    def http_post(self, url, data=None):
        if url.startswith('U_R_L// oauth2/token'):
            return self.mock_provider_get_token_from_post_data(data)
        raise Exception('Test fail')

class_client = MockClient(client_id=MOCK_CLIENT_ID,
                          client_secret=MOCK_CLIENT_SECRET,
                          authorization_uri='U_R_L// oauth2/auth',
                          token_uri='U_R_L// oauth2/token',
                          redirect_uri=MOCK_REDIRECT_URI + '?param=123')


def test_get_authorization_code(request):
    uri = class_client.get_authorization_code_uri(scope='example')

    result = utils.url_query_params(uri)
    uri = utils.build_url(url1, result)

    response = s.get(uri)
    redirect = response.content
    return HttpResponse(redirect)


def get_token_from_post_data(request):
    data = {'code': MOCK_AUTHORIZATION_CODE,
            'scope': 'example',
            'grant_type': 'authorization_code',
            'client_id': MOCK_CLIENT_ID,
            'client_secret': MOCK_CLIENT_SECRET,
            'redirect_uri': MOCK_REDIRECT_URI
            }
    uri = utils.build_url(url2, data)

    response = s.get(uri)
    redirect = response.content
    return HttpResponse(redirect)


def refresh_token(request):
    data = {
        'grant_type': 'refresh_token',
        'client_id': MOCK_CLIENT_ID,
        'client_secret': MOCK_CLIENT_SECRET,
        'refresh_token': MOCK_REFRESH_TOKEN,
        'scope': 'example'
    }
    uri = utils.build_url(url3, data)

    response = s.get(uri)
    redirect = response.content
    return HttpResponse(redirect)

