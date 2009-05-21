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


"""Provides a client to interact with Google Data API servers.

This module is used for version 2 of the Google Data APIs and is currently
experimental. This module may change in backwards incompatible ways before
the release of version 2.0.0. The primary class in this module is GDClient.

  GDClient: handles auth and CRUD operations when communicating with servers.
  GDataClient: deprecated client for version one services. Will be removed.
  create_converter: uses a prototype object to create a converter function.
"""


__author__ = 'j.s@google.com (Jeff Scudder)'


import re
import atom.client
import atom.core
import gdata.service
import atom.http_core
import gdata.gauth
import gdata.data


# Old imports
import urllib
import urlparse
import gdata.auth
import atom.service


class Error(Exception):
  pass


class RequestError(gdata.service.RequestError):
  status = None
  reason = None
  body = None
  headers = None


class RedirectError(RequestError):
  pass


class CaptchaChallenge(gdata.service.CaptchaRequired):
  captcha_url = None
  captcha_token = None


class ClientLoginTokenMissing(Error):
  pass


class ClientLoginFailed(RequestError):
  pass


class UnableToUpgradeToken(Error):
  pass


class Unauthorized(Error):
  pass


class BadAuthenticationServiceURL(RedirectError,
    gdata.service.BadAuthenticationServiceURL):
  pass


def v2_entry_from_response(response):
  """Experimental converter which gets an Atom entry from the response."""
  return gdata.data.entry_from_string(response.read(), version=2)


def v2_feed_from_response(response):
  """Experimental converter which gets an Atom feed from the response."""
  return gdata.data.feed_from_string(response.read(), version=2)


def create_converter(obj):
  """Experimental: Generates a converter function for this object's class.

  When updating an entry, the returned object should usually be of the same
  type as the original entry. Since the client's request method takes a
  converter funtion as an argument, we need a function which will parse the
  XML using the desired class.

  Returns:
    A function which takes an XML string as the only parameter and returns an
    object of the same type as obj.
  """
  return lambda response: atom.core.xml_element_from_string(
      response.read(), obj.__class__, version=2, encoding='UTF-8')


def error_from_response(message, http_response, error_class, response_body=None):
  """Creates a new exception and sets the HTTP information in the error.
  
  Args:
   message: str human readable message to be displayed if the exception is
            not caught.
   http_response: The response from the server, contains error information.
   error_class: The exception to be instantiated and populated with
                information from the http_response
   response_body: str (optional) specify if the response has already been read
                  from the http_response object.
  """
  if response_body is None:
    body = http_response.read()
  else:
    body = response_body
  error = error_class('%s: %i, %s' % (message, http_response.status, body))
  error.status = http_response.status
  error.reason = http_response.reason
  error.body = body
  error.headers = http_response.getheaders()
  return error


class GDClient(atom.client.AtomPubClient):
  """Communicates with Google Data servers to perform CRUD operations.

  This class is currently experimental and may change in backwards
  incompatible ways.

  This class exists to simplify the following three areas involved in using
  the Google Data APIs.

  CRUD Operations:

  The client provides a generic 'request' method for making HTTP requests.
  There are a number of convenience methods which are built on top of
  request, which include get_feed, get_entry, get_next, post, update, and
  delete. These methods contact the Google Data servers.

  Auth:

  Reading user-specific private data requires authorization from the user as
  do any changes to user data. An auth_token object can be passed into any
  of the HTTP requests to set the Authorization header in the request.

  You may also want to set the auth_token member to a an object which can
  use modify_request to set the Authorization header in the HTTP request.

  If you are authenticating using the email address and password, you can
  use the client_login method to obtain an auth token and set the
  auth_token member.

  If you are using browser redirects, specifically AuthSub, you will want
  to use gdata.gauth.AuthSubToken.from_url to obtain the token after the
  redirect, and you will probably want to updgrade this since use token
  to a multiple use (session) token using the upgrade_token method.

  API Versions:

  This client is multi-version capable and can be used with Google Data API
  version 1 and version 2. The version should be specified by setting the
  api_version member to a string, either '1' or '2'. 
  """

  # The gsessionid is used by Google Calendar to prevent redirects.
  __gsessionid = None
  api_version = None

  def request(self, method=None, uri=None, auth_token=None,
              http_request=None, converter=None, desired_class=None,
              redirects_remaining=4, **kwargs):
    """Make an HTTP request to the server.
    
    See also documentation for atom.client.AtomPubClient.request.

    If a 302 redirect is sent from the server to the client, this client
    assumes that the redirect is in the form used by the Google Calendar API.
    The same request URI and method will be used as in the original request,
    but a gsessionid URL parameter will be added to the request URI with
    the value provided in the server's 302 redirect response. If the 302
    redirect is not in the format specified by the Google Calendar API, a
    RedirectError will be raised containing the body of the server's
    response.

    The method calls the client's modify_request method to make any changes
    required by the client before the request is made. For example, a
    version 2 client could add a GData-Version: 2 header to the request in
    its modify_request method.

    Args:
      method: str The HTTP verb for this request, usually 'GET', 'POST', 
              'PUT', or 'DELETE'
      uri: atom.http_core.Uri, str, or unicode The URL being requested.
      auth_token: An object which sets the Authorization HTTP header in its
                  modify_request method. Recommended classes include 
                  gdata.gauth.ClientLoginToken and gdata.gauth.AuthSubToken
                  among others.
      http_request: (optional) atom.http_core.HttpRequest
      converter: function which takes the body of the response as it's only
                 argument and returns the desired object.
      desired_class: class descended from atom.core.XmlElement to which a
                     successful response should be converted. If there is no
                     converter function specified (converter=None) then the
                     desired_class will be used in calling the
                     atom.core.xml_element_from_string function. If neither
                     the desired_class nor the converter is specified, an
                     HTTP reponse object will be returned.
      redirects_remaining: (optional) int, if this number is 0 and the
                           server sends a 302 redirect, the request method
                           will raise an exception. This parameter is used in
                           recursive request calls to avoid an infinite loop.

    Any additional arguments are passed through to 
    atom.client.AtomPubClient.request.

    Returns:
      An HTTP response object (see atom.http_core.HttpResponse for a
      description of the object's interface) if no converter was
      specified and no desired_class was specified. If a converter function
      was provided, the results of calling the converter are returned. If no
      converter was specified but a desired_class was provided, the response
      body will be converted to the class using 
      atom.core.xml_element_from_string.
    """
    if isinstance(uri, (str, unicode)):
      uri = atom.http_core.Uri.parse_uri(uri)

    # Add the gsession ID to the URL to prevent further redirects.
    # TODO: If different sessions are using the same client, there will be a
    # multitude of redirects and session ID shuffling.
    # If the gsession ID is in the URL, adopt it as the standard location.
    if uri is not None and uri.query is not None and 'gsessionid' in uri.query:
      self.__gsessionid = uri.query['gsessionid']
    # The gsession ID could also be in the HTTP request.
    elif (http_request is not None and http_request.uri is not None
          and http_request.uri.query is not None
          and 'gsessionid' in http_request.uri.query):
      self.__gsessionid = http_request.uri.query['gsessionid']
    # If the gsession ID is stored in the client, and was not present in the
    # URI then add it to the URI.
    elif self.__gsessionid is not None:
      uri.query['gsessionid'] = self.__gsessionid

    http_request = self.modify_request(http_request)

    response = atom.client.AtomPubClient.request(self, method=method, 
        uri=uri, auth_token=auth_token, http_request=http_request, **kwargs)
    # On success, convert the response body using the desired converter 
    # function if present.
    if response is None:
      return None
    if response.status == 200 or response.status == 201:
      if converter is not None:
        return converter(response)
      elif desired_class is not None:
        if self.api_version is not None:
          return atom.core.xml_element_from_string(response.read(),
              desired_class, version=self.api_version)
        else:
          # No API version was specified, so allow xml_element_from_string to
          # use the default version.
          return atom.core.xml_element_from_string(response.read(),
              desired_class)
      else:
        return response
    # TODO: move the redirect logic into the Google Calendar client once it
    # exists since the redirects are only used in the calendar API.
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
                              desired_class=desired_class,
                              redirects_remaining=redirects_remaining-1,
                              **kwargs)
        else:
          raise error_from_response('302 received without Location header',
                                    response, RedirectError)
      else:
        raise error_from_response('Too many redirects from server', 
                                  response, RedirectError)
    elif response.status == 401:
      raise error_from_response('Unauthorized - Server responded with',
                                response, Unauthorized)
    # If the server's response was not a 200, 201, 302, or 401, raise an 
    # exception.
    else:
      raise error_from_response('Server responded with', response,
                                RequestError)

  Request = request

  def request_client_login_token(self, email, password, service, source,
      account_type='HOSTED_OR_GOOGLE', 
      auth_url=atom.http_core.Uri.parse_uri(
          'https://www.google.com/accounts/ClientLogin'), 
      captcha_token=None, captcha_response=None):
    # Set the target URL.
    http_request = atom.http_core.HttpRequest(uri=auth_url, method='POST')
    http_request.add_body_part(
        gdata.gauth.generate_client_login_request_body(email=email, 
            password=password, service=service, source=source, 
            account_type=account_type, captcha_token=captcha_token, 
            captcha_response=captcha_response),
        'application/x-www-form-urlencoded')

    # Use the underlying http_client to make the request.
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
        raise error_from_response('Server responded with a 403 code',
                                  response, RequestError, response_body)
    elif response.status == 302:
      # Google tries to redirect all bad URLs back to
      # http://www.google.<locale>. If a redirect
      # attempt is made, assume the user has supplied an incorrect
      # authentication URL
      raise error_from_response('Server responded with a redirect',
                                response, BadAuthenticationServiceURL,
                                response_body)
    else:
      raise error_from_response('Server responded to ClientLogin request',
                                response, ClientLoginFailed, response_body)

  RequestClientLoginToken = request_client_login_token

  def client_login(self, email, password, service, source,
                   account_type='HOSTED_OR_GOOGLE',
                   auth_url='https://www.google.com/accounts/ClientLogin',
                   captcha_token=None, captcha_response=None):
    self.auth_token = self.request_client_login_token(email, password,
        service, source, account_type=account_type, auth_url=auth_url,
        captcha_token=captcha_token, captcha_response=captcha_response)

  ClientLogin = client_login

  def upgrade_token(self, token=None, url=atom.http_core.Uri.parse_uri(
      'https://www.google.com/accounts/AuthSubSessionToken')):
    """Asks the Google auth server for a multi-use AuthSub token.

    For details on AuthSub, see:
    http://code.google.com/apis/accounts/docs/AuthSub.html
    
    Args:
      token: gdata.gauth.AuthSubToken (optional) If no token is passed in, 
             the client's auth_token member is used to request the new token.
             The token object will be modified to contain the new session 
             token string.
      url: str or atom.http_core.Uri (optional) The URL to which the token
           upgrade request should be sent. Defaults to: 
           https://www.google.com/accounts/AuthSubSessionToken

    Returns:
      The upgraded gdata.gauth.AuthSubToken object.
    """
    # Default to using the auth_token member if no token is provided.
    if token is None:
      token = self.auth_token
    # We cannot upgrade a None token.
    if token is None:
      raise UnableToUpgradeToken('No token was provided.')
    if not isinstance(token, gdata.gauth.AuthSubToken):
      raise UnableToUpgradeToken(
          'Cannot upgrade the token because it is not an AuthSubToken object.')
    http_request = atom.http_core.HttpRequest(uri=url, method='GET')
    token.modify_request(http_request)
    # Use the lower level HttpClient to make the request.
    response = self.http_client.request(http_request)
    if response.status == 200:
      token._upgrade_token(response.read())
      return token
    else:
      raise UnableToUpgradeToken(
          'Server responded to token upgrade request with %s: %s' % (
              response.status, response.read()))

  UpgradeToken = upgrade_token

  def modify_request(self, http_request):
    """Adds or changes request before making the HTTP request.
    
    This client will add the API version if it is specified. 
    Subclasses may override this method to add their own request 
    modifications before the request is made.
    """
    atom.client.AtomPubClient.modify_request(self, http_request)
    if self.api_version is not None:
      if http_request is None:
        http_request = atom.http_core.HttpRequest()
      http_request.headers['GData-Version'] = self.api_version
    return http_request

  ModifyRequest = modify_request

  def get_feed(self, uri, auth_token=None, converter=None, 
               desired_class=gdata.data.GFeed, **kwargs):
    return self.request(method='GET', uri=uri, auth_token=auth_token,
                        converter=converter, desired_class=desired_class,
                        **kwargs)

  GetFeed = get_feed

  def get_entry(self, uri, auth_token=None, converter=None,
                desired_class=gdata.data.GEntry, **kwargs):
    return self.request(method='GET', uri=uri, auth_token=auth_token,
                        converter=converter, desired_class=desired_class,
                        **kwargs)

  GetEntry = get_entry

  def get_next(self, feed, auth_token=None, converter=None, 
               desired_class=None, **kwargs):
    """Fetches the next set of results from the feed. 
    
    When requesting a feed, the number of entries returned is capped at a
    service specific default limit (often 25 entries). You can specify your
    own entry-count cap using the max-results URL query parameter. If there
    are more results than could fit under max-results, the feed will contain
    a next link. This method performs a GET against this next results URL.

    Returns:
      A new feed object containing the next set of entries in this feed.
    """
    if converter is None and desired_class is None:
      desired_class = feed.__class__
    return self.get_feed(feed.get_next_url(), auth_token=auth_token,
                         converter=converter, desired_class=desired_class,
                         **kwargs)

  GetNext = get_next

  # TODO: add a refresh method to re-fetch the entry/feed from the server
  # if it has been updated.

  def post(self, entry, uri, auth_token=None, converter=None, 
           desired_class=None, **kwargs):
    if converter is None and desired_class is None:
      desired_class = entry.__class__
    http_request = atom.http_core.HttpRequest()
    http_request.add_body_part(entry.to_string(), 'application/atom+xml')
    return self.request(method='POST', uri=uri, auth_token=auth_token,
                        http_request=http_request, converter=converter,
                        desired_class=desired_class, **kwargs)

  Post = post

  def update(self, entry, auth_token=None, force=False, **kwargs):
    """Edits the entry on the server by sending the XML for this entry.
    
    Performs a PUT and converts the response to a new entry object with a
    matching class to the entry passed in.

    Args:
      entry:
      auth_token:
      force: boolean stating whether an update should be forced. Defaults to
             False. Normally, if a change has been made since the passed in
             entry was obtained, the server will not overwrite the entry since
             the changes were based on an obsolete version of the entry.
             Setting force to True will cause the update to silently
             overwrite whatever version is present.

    Returns:
      A new Entry object of a matching type to the entry which was passed in.
    """
    http_request = atom.http_core.HttpRequest()
    http_request.add_body_part(entry.to_string(), 'application/atom+xml')
    # Include the ETag in the request if this is version 2 of the API.
    if self.api_version and self.api_version.startswith('2'):
      if force:
        http_request.headers['If-Match'] = '*'
      elif hasattr(entry, 'etag') and entry.etag:
        http_request.headers['If-Match'] = entry.etag
    return self.request(method='PUT', uri=entry.get_edit_url(), 
                        auth_token=auth_token, http_request=http_request, 
                        desired_class=entry.__class__, **kwargs)

  Update = update

  def delete(self, entry, auth_token=None, force=False, **kwargs):
    http_request = atom.http_core.HttpRequest()
    # Include the ETag in the request if this is version 2 of the API.
    if self.api_version and self.api_version.startswith('2'):
      if force:
        http_request.headers['If-Match'] = '*'
      elif hasattr(entry, 'etag') and entry.etag:
        http_request.headers['If-Match'] = entry.etag
    return self.request(method='DELETE', uri=entry.get_edit_url(), 
                        http_request=http_request, auth_token=auth_token,
                        **kwargs)

  Delete = delete

  #TODO: implement batch requests.
  #def batch(feed, uri, auth_token=None, converter=None, **kwargs):
  #  pass

class GDQuery(atom.http_core.Uri):

  def _get_text_query(self):
    return self.query['q']

  def _set_text_query(self, value):
    self.query['q'] = value

  text_query = property(_get_text_query, _set_text_query, 
      doc='The q parameter for searching for an exact text match on content')
    



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
