# -*-coding:utf-8-*-
# @auth ivan
# @time 2016-11-9 10:26:27
# @goal test the client & provider

from django.shortcuts import render
from django.http import HttpResponse

from provider import AuthorizationProvider
import utils

import requests

MOCK_CLIENT_ID = 'abc123456789'
MOCK_CLIENT_SECRET = 'MNBVCXZLKJHGFDSAPOIUYTREWQ'
MOCK_REDIRECT_URI = 'http://yiyin.site:8082/myapp/oauth_endpoint/'
MOCK_AUTHORIZATION_CODE = 'poiuytrewqlkjhgfdsamnbvcxz0987654321'
MOCK_REFRESH_TOKEN = 'uhbygvtfcrdxeszokmijn'


class MockAuthorizationProvider(AuthorizationProvider):
    def validate_client_id(self, client_id):
        return client_id == MOCK_CLIENT_ID

    def validate_client_secret(self, client_id, client_secret):
        return client_id == MOCK_CLIENT_ID and client_secret == MOCK_CLIENT_SECRET

    def validate_scope(self, client_id, scope):
        requested_scopes = scope.split()
        if client_id == MOCK_CLIENT_ID and requested_scopes == ['example']:
            return True
        return False

    def validate_redirect_uri(self, client_id, redirect_uri):
        return redirect_uri.startswith(MOCK_REDIRECT_URI)

    def from_authorization_code(self, client_id, code, scope):
        if code == MOCK_AUTHORIZATION_CODE:
            return {'session': '12345'}
        return None

    def from_refresh_token(self, client_id, refresh_token, scope):
        if refresh_token == MOCK_REFRESH_TOKEN:
            return {'session': '56789'}
        return None

    def validate_access(self):
        return True

    def persist_authorization_code(self, client_id, code, scope):
        pass

    def persist_token_information(self, client_id, scope, access_token,
                                  token_type, expires_in, refresh_token,
                                  data):
        pass

    def discard_authorization_code(self, client_id, code):
        pass

    def discard_refresh_token(self, client_id, refresh_token):
        pass
class_provider = MockAuthorizationProvider()


def test_get_authorization_code(request):
    result = {}
    for i in request.GET:
        result[i] = request.GET[i]

    uri = 'http://yiyin.site:8082/oauth2/auth?'
    uri = utils.build_url(uri, result)
    response = class_provider.get_authorization_code_from_uri(uri)
    redirect = response.headers['Location']
    print redirect
    return HttpResponse(redirect)


def get_token_from_post_data(request):
    result = {}
    for i in request.GET:
        result[i] = request.GET[i]

    result = class_provider.get_token_from_post_data(result)
    return HttpResponse(result)


def refresh_token(request):
    result = {}
    for i in request.GET:
        result[i] = request.GET[i]

    result = class_provider.refresh_token(grant_type=result['grant_type'],
                                          client_id=result['client_id'],
                                          client_secret=result['client_secret'],
                                          refresh_token=result['refresh_token'],
                                          scope=result['scope'])
    result = result.content
    return HttpResponse(result)

