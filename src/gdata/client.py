#!/usr/bin/env python
#
# Copyright (C) 2008, 2009 Google Inc.
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


__author__ = 'j.s@google.com (Jeff Scudder)'


import re
import atom.client
import gdata.service
import atom.http_core
import gdata.gauth


# Old imports
import urllib
import urlparse
import gdata.auth
import atom.service


class Error(Exception):
  pass


class RedirectError(gdata.service.RequestError):
  pass


class CaptchaChallenge(gdata.service.CaptchaRequired):
  captcha_url = None
  captcha_token = None


class ClientLoginTokenMissing(Error):
  pass


class ClientLoginFailed(Error):
  pass


class GDClient(atom.client.AtomPubClient):
  # The gsessionid is used by Google Calendar to prevent redirects.
  __gsessionid = None

  def request(self, method=None, uri=None, auth_token=None,
              http_request=None, converter=None, redirects_remaining=4,
              **kwargs):
    """Make an HTTP request to the server.
    
    See also documentation for atom.client.AtomPubClient.request.

    Args:
      method: str
      uri: atom.http_core.Uri, str, or unicode
      auth_token:
      http_request: (optional) atom.http_core.HttpRequest
      converter: function which takes the body of the response as it's only
                 argument and returns the desired object.
      redirects_remaining: (optional) int, if this number is 0 and the
                           server sends a 302 redirect, the request method
                           will raise an exception. This parameter is used in
                           recursive request calls to avoid an infinite loop.

    Any additional arguments are passed through to 
    atom.client.AtomPubClient.request.

    Returns:
      An HTTP response object (see atom.http_core.HttpResponse for a
      description of the object's interface) if no converter was
      specified. If a converter function was provided, the results of
      calling the converter are returned.
    """
    if isinstance(uri, (str, unicode)):
      uri = atom.http_core.parse_uri(uri)

    # Add the gsession ID to the URL to prevent further redirects.
    if self.__gsessionid is not None:
      uri.query['gsessionid'] = self.__gsessionid

    response = atom.client.AtomPubClient.request(self, method=method, 
        uri=uri, auth_token=auth_token, http_request=http_request, **kwargs)
    # On success, convert the response body using the desired converter 
    # function if present.
    if response.status == 200 or response.status == 201:
      if converter is not None:
        return converter(response.read())
      return response
    elif response.status == 302:
      if redirects_remaining > 0:
        location = response.getheader('Location')
        if location is not None:
          m = re.compile('[\?\&]gsessionid=(\w*)').search(location)
          if m is not None:
            self.__gsessionid = m.group(1)
          # Make a recursive call with the gsession ID in the URI to follow 
          # the redirect.
          return self.request(method=method, uri=uri, auth_token=auth_token,
                              http_request=http_request, converter=converter,
                              redirects_remaining=redirects_remaining-1,
                              **kwargs)
        else:
          raise RedirectError('302 received without Location header %s' % (
              response.read(),))
      else:
        raise RedirectError('Too many redirects from server %s' % (
            response.read(),))
    else:
      raise gdata.service.RequestError('Server responded with %i, %s' % (
          response.status, response.read()))

  Request = request

  def request_client_login_token(self, email, password, service, source,
      account_type='HOSTED_OR_GOOGLE', 
      auth_url='https://www.google.com/accounts/ClientLogin', 
      captcha_token=None, captcha_response=None):
    http_request = atom.http_core.HttpRequest()
    http_request.add_body_part(
        gdata.gauth.generate_client_login_request_body(email=email, 
            password=password, service=service, source=source, 
            account_type=account_type, captcha_token=captcha_token, 
            captcha_response=captcha_response),
        'application/x-www-form-urlencoded')
    http_request.method = 'POST'
    # Set the target URL.
    atom.http_core.parse_uri(auth_url).modify_request(http_request)

    # Use the underlyinh http_client to make the request.
    response = self.http_client.request(http_request)

    response_body = response.read()
    if response.status == 200:
      token_string = gdata.gauth.get_client_login_token_string(response_body)
      if token_string is not None:
        return gdata.gauth.ClientLoginToken(token_string)
      else:
        raise ClientLoginTokenMissing(
            'Recieved a 200 response to client login request,'
            ' but no token was present. %s' % (response_body,))
    elif response.status == 403:
      captcha_challenge = gdata.gauth.get_captcha_challenge(response_body)
      if captcha_challenge:
        challenge = CaptchaChallenge('CAPTCHA required')
        challenge.captcha_url = captcha_challenge['url']
        challenge.captcha_token = captcha_challenge['token']
        raise challenge
      elif response_body.splitlines()[0] == 'Error=BadAuthentication':
        raise gdata.service.BadAuthentication(
            'Incorrect username or password')
      else:
        raise gdata.service.Error('Server responded with a 403 code')
    elif response.status == 302:
      # Google tries to redirect all bad URLs back to
      # http://www.google.<locale>. If a redirect
      # attempt is made, assume the user has supplied an incorrect
      # authentication URL
      raise gdata.service.BadAuthenticationServiceURL(
          'Server responded with a 302 code.')
    else:
      raise ClientLoginFailed(
          'Server responded to ClientLogin request with %i: %s' % (
              response.status, response_body))

  RequestClientLoginToken = request_client_login_token

  def client_login(self, email, password, service, source,
                   account_type='HOSTED_OR_GOOGLE',
                   auth_url='https://www.google.com/accounts/ClientLogin',
                   captcha_token=None, captcha_response=None):
    self.auth_token = self.request_client_login_token(email, password,
        service, source, account_type=account_type, auth_url=auth_url,
        captcha_token=captcha_token, captcha_response=captcha_response)

  ClientLogin = client_login


# Version 1 code.
SCOPE_URL_PARAM_NAME = gdata.service.SCOPE_URL_PARAM_NAME 
# Maps the service names used in ClientLogin to scope URLs. 
CLIENT_LOGIN_SCOPES = gdata.service.CLIENT_LOGIN_SCOPES


class AuthorizationRequired(gdata.service.Error):
  pass


class GDataClient(gdata.service.GDataService):
  """This class is deprecated. 
  
  All functionality has been migrated to gdata.service.GDataService.
  """
  def __init__(self, application_name=None, tokens=None):
    gdata.service.GDataService.__init__(self, source=application_name, 
        tokens=tokens)

  def ClientLogin(self, username, password, service_name, source=None, 
      account_type=None, auth_url=None, login_token=None, login_captcha=None):
    gdata.service.GDataService.ClientLogin(self, username=username, 
        password=password, account_type=account_type, service=service_name,
        auth_service_url=auth_url, source=source, captcha_token=login_token,
        captcha_response=login_captcha)

  def Get(self, url, parser):
    """Simplified interface for Get.

    Requires a parser function which takes the server response's body as
    the only argument.

    Args:
      url: A string or something that can be converted to a string using str.
          The URL of the requested resource.
      parser: A function which takes the HTTP body from the server as it's
          only result. Common values would include str, 
          gdata.GDataEntryFromString, and gdata.GDataFeedFromString.

    Returns: The result of calling parser(http_response_body).
    """
    return gdata.service.GDataService.Get(self, uri=url, converter=parser)

  def Post(self, data, url, parser, media_source=None):
    """Streamlined version of Post.

    Requires a parser function which takes the server response's body as
    the only argument.
    """
    return gdata.service.GDataService.Post(self, data=data, uri=url,
        media_source=media_source, converter=parser)

  def Put(self, data, url, parser, media_source=None):
    """Streamlined version of Put.

    Requires a parser function which takes the server response's body as
    the only argument.
    """
    return gdata.service.GDataService.Put(self, data=data, uri=url,
        media_source=media_source, converter=parser)

  def Delete(self, url):
    return gdata.service.GDataService.Delete(self, uri=url)


ExtractToken = gdata.service.ExtractToken
GenerateAuthSubRequestUrl = gdata.service.GenerateAuthSubRequestUrl    
