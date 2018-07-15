# import adal
#
#
# class ApplicationAuthenticationHandler:
#     def __init__(self, app_settings):
#         # TODO sanity check
#         self.tenant_id = app_settings.get('tenant')
#         self.namespace_id = app_settings.get('namespace')
#         self.address = app_settings.get('address')
#         self.resource = app_settings.get('resource')
#         self.client_id = app_settings.get('clientId')
#         self.client_secret = app_settings.get('clientSecret')
#         self.authority = app_settings.get('authority').format(self.tenant_id)
#         self.token = ""
#         self.get_token()
#
#     def get_token(self):
#         # handle existing token by checking for expiration
#         context = adal.AuthenticationContext(self.authority, False)
#         print("AUTHORITY: \n{}".format(self.authority))
#         token_dct = context.acquire_token_with_client_credentials(self.resource, self.client_id, self.client_secret)
#         self.token = token_dct.get('accessToken')
#         # return token
#
#     def sds_headers(self):
#         retval = {"Authorization": "bearer {}".format(self.get_token()),
#                   "Content-type": "application/json",
#                   "Accept": "*/*; q=1"}
#         print("HEADERS: \n{}".format(retval))
#         return retval
#
#         # TODO sanity check