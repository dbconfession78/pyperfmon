import requests
import time
import adal
from SdsError import SdsError
import json
from SdsTypeData import SdsTypeData

class RequestManager:
    def __init__(self, client, url, method):
        self.client = client
        self.url = url
        self.method = method
        self.payload = {}
        self.__token = ""
        self.__expiration = 0
        self.content = ""
        self.status = 0


    def __getToken(self):
        if ((self.__expiration - time.time()) > 5 * 60):
            return self.__token

        context = adal.AuthenticationContext(self.client.authority, validate_authority=True)

        token = context.acquire_token_with_client_credentials(
            self.client.resource,
            self.client.clientId,
            self.client.clientSecret)

        if token is None:
            raise Exception("Failed to retrieve AAD Token")

        self.__expiration = float(token['expiresIn']) + time.time()
        self.__token = token['accessToken']
        return self.__token


    def execute(self):
        method_funcs = {'get': requests.get, 'post': requests.post}
        headers =  {
            "Authorization": "bearer %s" % self.__getToken(),
            "Content-type": "application/json",
            "Accept": "*/*; q=1"
        }
        fnc = method_funcs.get(self.method)
        if self.method=='post' or self.method=='put':
            r = fnc(self.url, data=self.payload, headers = headers)
        else:
            r = fnc(self.url, headers=headers)
        self.status = r.status_code
        self.content = r.content
