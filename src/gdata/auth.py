#/usr/bin/python
#
# Copyright (C) 2007 Google Inc.
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


import re
import urllib
import atom.http_interface


__author__ = 'api.jscudder (Jeff Scudder)'


PROGRAMMATIC_AUTH_LABEL = 'GoogleLogin auth='
AUTHSUB_AUTH_LABEL = 'AuthSub token='


def GenerateClientLoginRequestBody(email, password, service, source, 
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


def GenerateClientLoginAuthToken(http_body):
  """Returns the token value to use in Authorization headers.

  Reads the token from the server's response to a Client Login request and
  creates header value to use in requests.

  Args:
    http_body: str The body of the server's HTTP response to a Client Login
        request
 
  Returns:
    The value half of an Authorization header.
  """
  token = get_client_login_token(http_body)
  if token:
    return 'GoogleLogin auth=%s' % token
  return None


def get_client_login_token(http_body):
  """Returns the token value for a ClientLoginToken.

  Reads the token from the server's response to a Client Login request and
  creates the token value string to use in requests.

  Args:
    http_body: str The body of the server's HTTP response to a Client Login
        request
 
  Returns:
    The token value for a ClientLoginToken.
  """
  for response_line in http_body.splitlines():
    if response_line.startswith('Auth='):
      # Strip off the leading Auth= and return the Authorization value.
      return response_line[5:]
  return None


def GetCaptchChallenge(http_body, 
    captcha_base_url='http://www.google.com/accounts/'):
  """Returns the URL and token for a CAPTCHA challenge issued bu the server.

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


def GenerateAuthSubUrl(next, scope, secure=False, session=True, 
    request_url='https://www.google.com/accounts/AuthSubRequest',
    domain='default'):
  """Generate a URL at which the user will login and be redirected back.

  Users enter their credentials on a Google login page and a token is sent
  to the URL specified in next. See documentation for AuthSub login at:
  http://code.google.com/apis/accounts/AuthForWebApps.html

  Args:
    request_url: str The beginning of the request URL. This is normally
        'http://www.google.com/accounts/AuthSubRequest' or 
        '/accounts/AuthSubRequest'
    next: string The URL user will be sent to after logging in.
    scope: string The URL of the service to be accessed.
    secure: boolean (optional) Determines whether or not the issued token
            is a secure token.
    session: boolean (optional) Determines whether or not the issued token
             can be upgraded to a session token.
  """
  # Translate True/False values for parameters into numeric values acceoted
  # by the AuthSub service.
  if secure:
    secure = 1
  else:
    secure = 0

  if session:
    session = 1
  else:
    session = 0

  request_params = urllib.urlencode({'next': next, 'scope': scope,
                                     'secure': secure, 'session': session, 
                                     'hd': domain})
  if request_url.find('?') == -1:
    return '%s?%s' % (request_url, request_params)
  else:
    # The request URL already contained url parameters so we should add
    # the parameters using the & seperator
    return '%s&%s' % (request_url, request_params)


def AuthSubTokenFromUrl(url):
  """Extracts the AuthSub token from the URL. 

  Used after the AuthSub redirect has sent the user to the 'next' page and
  appended the token to the URL. This function returns the value to be used
  in the Authorization header. 

  Args:
    url: str The URL of the current page which contains the AuthSub token as
        a URL parameter.
  """
  token = TokenFromUrl(url)
  if token:
    return 'AuthSub token=%s' % token
  return None


def TokenFromUrl(url):
  """Extracts the AuthSub token from the URL.

  Returns the raw token value.

  Args:
    url: str The URL or the query portion of the URL string (after the ?) of
        the current page which contains the AuthSub token as a URL parameter.
  """
  if url.find('?') > -1:
    query_params = url.split('?')[1]
  else:
    query_params = url
  for pair in query_params.split('&'):
    if pair.startswith('token='):
      return pair[6:]
  return None


def AuthSubTokenFromHttpBody(http_body):
  """Extracts the AuthSub token from an HTTP body string.

  Used to find the new session token after making a request to upgrade a 
  single use AuthSub token.

  Args:
    http_body: str The repsonse from the server which contains the AuthSub 
        key. For example, this function would find the new session token
        from the server's response to an upgrade token request.

  Returns:
    The header value to use for Authorization which contains the AuthSub
    token.
  """
  token_value = TokenFromHttpBody(http_body)
  if token_value:
    return 'AuthSub token=%s' % token_value
  return None


def TokenFromHttpBody(http_body):
  """Extracts the AuthSub token from an HTTP body string.

  Used to find the new session token after making a request to upgrade a 
  single use AuthSub token.

  Args:
    http_body: str The repsonse from the server which contains the AuthSub 
        key. For example, this function would find the new session token
        from the server's response to an upgrade token request.

  Returns:
    The raw token value to use in an AuthSubToken object.
  """
  for response_line in http_body.splitlines():
    if response_line.startswith('Token='):
      # Strip off Token= and return the token value string.
      return response_line[6:]
  return None


class ClientLoginToken(atom.http_interface.GenericToken):
  """Stores the Authorization header in auth_header and adds to requests.

  This token will add it's Authorization header to an HTTP request
  as it is made. Ths token class is simple but
  some Token classes must calculate portions of the Authorization header
  based on the request being made, which is why the token is responsible
  for making requests via an http_client parameter.

  Args:
    auth_header: str The value for the Authorization header.
    scopes: list of str or atom.url.Url specifying the beginnings of URLs
        for which this token can be used. For example, if scopes contains
        'http://example.com/foo', then this token can be used for a request to
        'http://example.com/foo/bar' but it cannot be used for a request to
        'http://example.com/baz'
  """
  def __init__(self, auth_header=None, scopes=None):
    self.auth_header = auth_header
    self.scopes = scopes or []

  def __str__(self):
    return self.auth_header

  def perform_request(self, http_client, operation, url, data=None,
                      headers=None):
    """Sets the Authorization header and makes the HTTP request."""
    if headers is None:
      headers = {'Authorization':self.auth_header}
    else:
      headers['Authorization'] = self.auth_header
    return http_client.request(operation, url, data=data, headers=headers)

  def get_token_string(self):
    """Removes PROGRAMMATIC_AUTH_LABEL to give just the token value."""
    return self.auth_header[len(PROGRAMMATIC_AUTH_LABEL):]

  def set_token_string(self, token_string):
    self.auth_header = '%s%s' % (PROGRAMMATIC_AUTH_LABEL, token_string)
  
  def valid_for_scope(self, url):
    """Tells the caller if the token authorizes access to the desired URL.

    Since the generic token doesn't add an auth header, it is not valid for
    any scope.
    """
    for scope in self.scopes:
      scope = str(scope)
      url = str(url)
      if url.startswith(scope):
        return True
    return False

class AuthSubToken(ClientLoginToken):
  def get_token_string(self):
    """Removes AUTHSUB_AUTH_LABEL to give just the token value."""
    return self.auth_header[len(AUTHSUB_AUTH_LABEL):]

  def set_token_string(self, token_string):
    self.auth_header = '%s%s' % (AUTHSUB_AUTH_LABEL, token_string)


#TODO: Add classes for SecureAuthSubToken and OAuthToken.
