#!/usr/bin/env python
#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# This module is used for version 2 of the Google Data APIs.


import urllib
import atom.http_core


__author__ = 'j.s@google.com (Jeff Scudder)'


PROGRAMMATIC_AUTH_LABEL = 'GoogleLogin auth='
AUTHSUB_AUTH_LABEL = 'AuthSub token='

# ClientLogin functions and classes.
def generate_client_login_request_body(email, password, service, source, 
    account_type='HOSTED_OR_GOOGLE', captcha_token=None, 
    captcha_response=None):
  """Creates the body of the autentication request

  See http://code.google.com/apis/accounts/AuthForInstalledApps.html#Request
  for more details.

  Args:
    email: str
    password: str
    service: str
    source: str
    account_type: str (optional) Defaul is 'HOSTED_OR_GOOGLE', other valid
        values are 'GOOGLE' and 'HOSTED'
    captcha_token: str (optional)
    captcha_response: str (optional)

  Returns:
    The HTTP body to send in a request for a client login token.
  """
  # Create a POST body containing the user's credentials.
  request_fields = {'Email': email,
                    'Passwd': password,
                    'accountType': account_type,
                    'service': service,
                    'source': source}
  if captcha_token and captcha_response:
    # Send the captcha token and response as part of the POST body if the
    # user is responding to a captch challenge.
    request_fields['logintoken'] = captcha_token
    request_fields['logincaptcha'] = captcha_response
  return urllib.urlencode(request_fields)


GenerateClientLoginRequestBody = generate_client_login_request_body


def get_client_login_token_string(http_body):
  """Returns the token value for a ClientLoginToken.

  Reads the token from the server's response to a Client Login request and
  creates the token value string to use in requests.

  Args:
    http_body: str The body of the server's HTTP response to a Client Login
        request
 
  Returns:
    The token value string for a ClientLoginToken.
  """
  for response_line in http_body.splitlines():
    if response_line.startswith('Auth='):
      # Strip off the leading Auth= and return the Authorization value.
      return response_line[5:]
  return None


GetClientLoginTokenString = get_client_login_token_string


def get_captcha_challenge(http_body, 
    captcha_base_url='http://www.google.com/accounts/'):
  """Returns the URL and token for a CAPTCHA challenge issued by the server.

  Args:
    http_body: str The body of the HTTP response from the server which 
        contains the CAPTCHA challenge.
    captcha_base_url: str This function returns a full URL for viewing the 
        challenge image which is built from the server's response. This
        base_url is used as the beginning of the URL because the server
        only provides the end of the URL. For example the server provides
        'Captcha?ctoken=Hi...N' and the URL for the image is
        'http://www.google.com/accounts/Captcha?ctoken=Hi...N'

  Returns:
    A dictionary containing the information needed to repond to the CAPTCHA
    challenge, the image URL and the ID token of the challenge. The 
    dictionary is in the form:
    {'token': string identifying the CAPTCHA image,
     'url': string containing the URL of the image}
    Returns None if there was no CAPTCHA challenge in the response.
  """
  contains_captcha_challenge = False
  captcha_parameters = {}
  for response_line in http_body.splitlines():
    if response_line.startswith('Error=CaptchaRequired'):
      contains_captcha_challenge = True
    elif response_line.startswith('CaptchaToken='):
      # Strip off the leading CaptchaToken=
      captcha_parameters['token'] = response_line[13:]
    elif response_line.startswith('CaptchaUrl='):
      captcha_parameters['url'] = '%s%s' % (captcha_base_url,
          response_line[11:])
  if contains_captcha_challenge:
    return captcha_parameters
  else:
    return None


GetCaptchaChallenge = get_captcha_challenge


class ClientLoginToken(object):

  def __init__(self, token_string):
    self.token_string = token_string

  def modify_request(self, http_request):
    http_request.headers['Authorization'] = '%s%s' % (PROGRAMMATIC_AUTH_LABEL,
        self.token_string)

  ModifyRequest = modify_request


# AuthSub functions and classes.
def _to_uri(str_or_uri):
  if isinstance(str_or_uri, (str, unicode)):
    return atom.http_core.Uri.parse_uri(str_or_uri)
  return str_or_uri

def generate_auth_sub_url(next, scopes, secure=False, session=True,
    request_url=atom.http_core.parse_uri(
        'https://www.google.com/accounts/AuthSubRequest'),
    domain='default', scopes_param_prefix='auth_sub_scopes'):
  """Constructs a URI for requesting a multiscope AuthSub token.

  The generated token will contain a URL parameter to pass along the
  requested scopes to the next URL. When the Google Accounts page
  redirects the broswser to the 'next' URL, it appends the single use
  AuthSub token value to the URL as a URL parameter with the key 'token'.
  However, the information about which scopes were requested is not
  included by Google Accounts. This method adds the scopes to the next
  URL before making the request so that the redirect will be sent to
  a page, and both the token value and the list of scopes for which the token
  was requested.

  Args:
    next: atom.http_core.Uri or string The URL user will be sent to after
          authorizing this web application to access their data.
    scopes: list containint strings or atom.http_core.Uri objects. The URLs
            of the services to be accessed.
    secure: boolean (optional) Determines whether or not the issued token
            is a secure token.
    session: boolean (optional) Determines whether or not the issued token
             can be upgraded to a session token.
    request_url: atom.http_core.Uri or str The beginning of the request URL.
                 This is normally 
                 'http://www.google.com/accounts/AuthSubRequest' or
                 '/accounts/AuthSubRequest'
    domain: The domain which the account is part of. This is used for Google
            Apps accounts, the default value is 'default' which means that
            the requested account is a Google Account (@gmail.com for
            example)
    scopes_param_prefix: str (optional) The requested scopes are added as a
                         URL parameter to the next URL so that the page at
                         the 'next' URL can extract the token value and the
                         valid scopes from the URL. The key for the URL
                         parameter defaults to 'auth_sub_scopes'

  Returns:
    An atom.http_core.Uri which the user's browser should be directed to in
    order to authorize this application to access their information.
  """
  if isinstance(next, (str, unicode)):
    next = atom.http_core.Uri.parse_uri(next)
  scopes_string = ' '.join([str(scope) for scope in scopes])
  next.query[scopes_param_prefix] = scopes_string

  if isinstance(request_url, (str, unicode)):
    request_url = atom.http_core.Uri.parse_uri(request_url)
  request_url.query['next'] = str(next)
  request_url.query['scope'] = scopes_string
  if session:
    request_url.query['session'] = '1'
  else:
    request_url.query['session'] = '0'
  if secure:
    request_url.query['secure'] = '1'
  else:
    request_url.query['secure'] = '0'
  request_url.query['hd'] = domain
  return request_url


def auth_sub_string_from_url(url, scopes_param_prefix='auth_sub_scopes'):
  """Finds the token string (and scopes) after the browser is redirected.

  After the Google Accounts AuthSub pages redirect the user's broswer back to
  the web application (using the 'next' URL from the request) the web app must
  extract the token from the current page's URL. The token is provided as a
  URL parameter named 'token' and if generate_auth_sub_url was used to create
  the request, the token's valid scopes are included in a URL parameter whose
  name is specified in scopes_param_prefix.

  Args:
    url: atom.url.Url or str representing the current URL. The token value
         and valid scopes should be included as URL parameters.
    scopes_param_prefix: str (optional) The URL parameter key which maps to
                         the list of valid scopes for the token.

  Returns:
    A tuple containing the token value as a string, and a tuple of scopes 
    (as atom.http_core.Uri objects) which are URL prefixes under which this
    token grants permission to read and write user data.
    (token_string, (scope_uri, scope_uri, scope_uri, ...))
    If no scopes were included in the URL, the second value in the tuple is
    None. If there was no token param in the url, the tuple returned is 
    (None, None)
  """
  if isinstance(url, (str, unicode)):
    url = atom.http_core.Uri.parse_uri(url)
  if 'token' not in url.query:
    return (None, None)
  token = url.query['token']
  # TODO: decide whether no scopes should be None or ().
  scopes = None # Default to None for no scopes.
  if scopes_param_prefix in url.query:
    scopes = tuple(url.query[scopes_param_prefix].split(' '))
  return (token, scopes)


AuthSubStringFromUrl = auth_sub_string_from_url


def auth_sub_string_from_body(http_body):
  """Extracts the AuthSub token from an HTTP body string.

  Used to find the new session token after making a request to upgrade a
  single use AuthSub token.

  Args:
    http_body: str The repsonse from the server which contains the AuthSub
        key. For example, this function would find the new session token
        from the server's response to an upgrade token request.

  Returns:
    The raw token value string to use in an AuthSubToken object.
  """
  for response_line in http_body.splitlines():
    if response_line.startswith('Token='):
      # Strip off Token= and return the token value string.
      return response_line[6:]
  return None


class AuthSubToken(object):

  def __init__(self, token_string, scopes=None):
    self.token_string = token_string
    self.scopes = scopes

  def modify_request(self, http_request):
    http_request.headers['Authorization'] = '%s%s' % (AUTHSUB_AUTH_LABEL,
        self.token_string)

  ModifyRequest = modify_request

  def from_url(str_or_uri):
    """Creates a new AuthSubToken using information in the URL.
    
    Uses auth_sub_string_from_url.

    Args:
      str_or_uri: The current page's URL (as a str or atom.http_core.Uri)
                  which should contain a token query parameter since the
                  Google auth server redirected the user's browser to this
                  URL.
    """
    token_and_scopes = auth_sub_string_from_url(str_or_uri)
    return AuthSubToken(token_and_scopes[0], token_and_scopes[1])

  from_url = staticmethod(from_url)
  FromUrl = from_url

  def _upgrade_token(self, http_body):
    """Replaces the token value with a session token from the auth server.
    
    Uses the response of a token upgrade request to modify this token. Uses
    auth_sub_string_from_body.
    """
    self.token_string = auth_sub_string_from_body(http_body)
