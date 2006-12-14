#!/usr/bin/python2.4
#
# Copyright 2006 Google Inc. All Rights Reserved.

"""GDataClient provides CRUD ops. and programmatic login for GData services.

  Error: A base exception class for all exceptions in the gdata_client
         module.

  CaptchaRequired: This exception is thrown when a login attempt results in a
                   captcha challenge from the ClientLogin service. When this
                   exception is thrown, the captcha_token and captcha_url are
                   set to the values provided in the server's response.

  BadAuthentication: Thrown when a login attempt is made with an incorrect
                     username or password.

  NotAuthenticated: Thrown if an operation requiring authentication is called
                    before a user has authenticated.

  NonAuthSubToken: Thrown if a method to modify an AuthSub token is used when
                   the user is either not authenticated or is authenticated
                   through programmatic login.

  GDataClient: Encapsulates user credentials needed to perform insert, update
               and delete operations with the GData API. An instance can
               perform user authentication, query, insertion, deletion, and 
               update.
"""

__author__ = 'api.jscudder (Jeffrey Scudder)'

import httplib
import urllib


PROGRAMMATIC_AUTH_LABEL = 'GoogleLogin auth'
AUTHSUB_AUTH_LABEL = 'AuthSub token'


class Error(Exception):
  pass


class CaptchaRequired(Error):
  pass


class BadAuthentication(Error):
  pass


class NotAuthenticated(Error):
  pass


class NonAuthSubToken(Error):
  pass


class GDataClient(object):
  """Contains elements needed for GData login and CRUD request headers.

  Maintains additional headers (tokens for example) needed for the GData 
  services to allow a user to perform inserts, updates, and deletes.
  """

  def __init__(self, email=None, password=None, service=None, source=None,
               server=None, additional_headers=None): 
    """Creates an object of type GDataClient.

    Args:
      email: string (optional) The user's email address, used for
             authentication.
      password: string (optional) The user's password.
      service: string (optional) The desired service for which credentials
               will be obtained.
      source: string (optional) The name of the user's application.
      server: string (optional) The name of the server to which a connection
              will be opened. Default value: 'base.google.com'.
      additional_headers: dictionary (optional) Any additional headers which 
                          should be included with CRUD operations.
    """

    self.email = email
    self.password = password
    self.service = service
    self.source =  source
    self.server = server
    self.additional_headers = additional_headers
    self.__auth_token = None
    self.__auth_type = None
    self.__captcha_token = None
    self.__captcha_url = None
 
  # Define properties for GDataClient
  def _SetAuthSubToken(self, auth_token):
    """Sets the token sent in requests to an AuthSub token.

    Only use this method if you have received a token from the AuthSub 
    service. The auth_token is set automatically when ProgrammaticLogin()
    is used. See documentation for Google AuthSub here:
    http://code.google.com/apis/accounts/AuthForWebApps.html .

    Args:
      auth_token: string The token returned by the AuthSub service.
    """

    self.__auth_token = auth_token
    # The auth token is only set externally when using AuthSub authentication,
    # so set the auth_type to indicate AuthSub.
    self.__auth_type = AUTHSUB_AUTH_LABEL

  def __SetAuthSubToken(self, auth_token):
    self._SetAuthSubToken(auth_token)

  def _GetAuthToken(self):
    """Returns the auth token used for authenticating requests.

    Returns:
      string
    """

    return self.__auth_token

  def __GetAuthToken(self):
    return self._GetAuthToken()

  auth_token = property(__GetAuthToken, __SetAuthSubToken,
      doc="""Get or set the token used for authentication.""")

  def _GetCaptchaToken(self):
    """Returns a captcha token if the most recent login attempt generated one.

    The captcha token is only set if the Programmatic Login attempt failed 
    because the Google service issued a captcha challenge.

    Returns:
      string
    """

    return self.__captcha_token

  def __GetCaptchaToken(self):
    return self._GetCaptchaToken()

  captcha_token = property(__GetCaptchaToken,
      doc="""Get the captcha token for a login request.""")

  def _GetCaptchaURL(self):
    """Returns the URL of the captcha image if a login attempt generated one.
     
    The captcha URL is only set if the Programmatic Login attempt failed
    because the Google service issued a captcha challenge.

    Returns:
      string
    """

    return self.__captcha_url

  def __GetCaptchaURL(self):
    return self._GetCaptchaURL()

  captcha_url = property(__GetCaptchaURL,
      doc="""Get the captcha URL for a login request.""")

  # Authentication operations

  def ProgrammaticLogin(self, captcha_token=None, captcha_response=None):
    """Authenticates the user and sets the GData Auth token.

    Login retreives a temporary auth token which must be used with all
    requests to GData services. The auth token is stored in the GData client
    object.

    Login is also used to respond to a captcha challenge. If the user's login
    attempt failed with a CaptchaRequired error, the user can respond by
    calling Login with the captcha token and the answer to the challenge.

    Args:
      captcha_token: string (optional) The identifier for the captcha challenge
                     which was presented to the user.
      captcha_response: string (optional) The user's answer to the captch 
                        challenge.

    Raises:
      CaptchaRequired if the login service will require a captcha response
      BadAuthentication if the login service rejected the username or password
      Error if the login service responded with a 403 different from the above
    """

    # Create a POST body containing the user's credentials.
    if captcha_token and captcha_response:
      # Send the captcha token and response as part of the POST body if the
      # user is responding to a captch challenge.
      request_body = urllib.urlencode({'Email': self.email,
                                       'Passwd': self.password,
                                       'service': self.service,
                                       'source': self.source,
                                       'logintoken': captcha_token,
                                       'logincaptcha': captcha_response})
    else:
      request_body = urllib.urlencode({'Email': self.email,
                                       'Passwd': self.password,
                                       'service': self.service,
                                       'source': self.source})

    # Open a connection to the authentication server.
    auth_connection = httplib.HTTPSConnection('www.google.com')

    # Begin the POST request to the client login service.
    auth_connection.putrequest('POST', '/accounts/ClientLogin')
    # Set the required headers for an Account Authentication request.
    auth_connection.putheader('Content-type',
                              'application/x-www-form-urlencoded')
    auth_connection.putheader('Content-Length',str(len(request_body)))
    auth_connection.endheaders()

    auth_connection.send(request_body)

    # Process the response and throw exceptions if the login request did not
    # succeed.
    auth_response = auth_connection.getresponse()

    if auth_response.status == 200:
      response_body = auth_response.read()
      for response_line in response_body.splitlines():
        if response_line.startswith('Auth='):
          self.__auth_token = response_line.lstrip('Auth=')
          self.__auth_type = PROGRAMMATIC_AUTH_LABEL
          # Get rid of any residual captcha information because the request
          # succeeded.
          self.__captcha_token = None
          self.__captcha_url = None

    elif auth_response.status == 403:
      response_body = auth_response.read()
      # Examine each line to find the error type and the captcha token and
      # captch URL if they are present.
      for response_line in response_body.splitlines():
        if response_line.startswith('Error='):
          error_line = response_line
        elif response_line.startswith('CaptchaToken='):
          self.__captcha_token = response_line.lstrip('CaptchaToken=')
        elif response_line.startswith('CaptchaUrl='):
          self.__captcha_url = 'https://www.google.com/accounts/Captcha%s' % (
                               response_line.lstrip('CaptchaUrl='))
      

      # Raise an exception based on the error type in the 403 response.
      # In cases where there was no captcha challenge, remove any previous
      # captcha values.
      if error_line == 'Error=CaptchaRequired':
        raise CaptchaRequired, 'Captcha Required'
      elif error_line == 'Error=BadAuthentication':
        self.__captcha_token = None
        self.__captcha_url = None
        raise BadAuthentication, 'Incorrect username or password'
      else:
        self.__captcha_token = None
        self.__captcha_url = None
        raise Error, 'Server responded with a 403 code' 

  def GenerateAuthSubURL(self, next, scope, secure=False, session=True):
    """Generate a URL at which the user will login and be redirected back.

    Users enter their credentials on a Google login page and a token is sent
    to the URL specified in next. See documentation for AuthSub login at:
    http://code.google.com/apis/accounts/AuthForWebApps.html

    Args:
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
                                    'secure': secure, 'session': session})
    return 'https://www.google.com/accounts/AuthSubRequest?%s' % request_params

  def UpgradeToSessionToken(self):
    """Upgrades a single use AuthSub token to a session token.

    Raises:
      NonAuthSubToken if the user's auth token is not an AuthSub token
    """
    
    if self.__auth_type != AUTHSUB_AUTH_LABEL: 
      raise NonAuthSubToken

    upgrade_connection = httplib.HTTPSConnection('www.google.com')
    upgrade_connection.putrequest('GET', '/accounts/AuthSubSessionToken')
    
    upgrade_connection.putheader('Content-Type',
	                         'application/x-www-form-urlencoded')
    upgrade_connection.putheader('Authorization', '%s=%s' %
        (self.__auth_type, self.__auth_token))
    upgrade_connection.endheaders()

    response = upgrade_connection.getresponse()

    response_body = response.read()
    if response.status == 200:
      for response_line in response_body.splitlines():
        if response_line.startswith('Token='):
          self.__auth_token = response_line.lstrip('Token=')

  def RevokeAuthSubToken(self):
    """Revokes an existing AuthSub token.

    Raises:
      NonAuthSubToken if the user's auth token is not an AuthSub token
    """

    if self.__auth_type != AUTHSUB_AUTH_LABEL:
      raise NonAuthSubToken
    
    revoke_connection = httplib.HTTPSConnection('www.google.com')
    revoke_connection.putrequest('GET', '/accounts/AuthSubRevokeToken')
    
    revoke_connection.putheader('Content-Type', 
	                        'application/x-www-form-urlencoded')
    revoke_connection.putheader('Authorization', '%s=%s' %
            (self.__auth_type, self.__auth_token))
    revoke_connection.endheaders()

    response = revoke_connection.getresponse()
    if response.status == 200:
      self.__auth_type = None
      self.__auth_token = None

  # CRUD operations
  def Get(self, uri, extra_headers=None):
    """Query the GData API with the given URI

    The uri is the portion of the URI after the server value 
    (ex: www.google.com).

    To perform a query against Google Base, set the server to 
    'base.google.com' and set the uri to '/base/feeds/...', where ... is 
    your query. For example, to find snippets for all digital cameras uri 
    should be set to: '/base/feeds/snippets?bq=digital+camera'

    Args:
      uri: string The query in the form of a URI. Example:
           '/base/feeds/snippets?bq=digital+camera'.
      extra_headers: dictionary (optional) Extra HTTP headers to be included
                     in the GET request. These headers are in addition to 
                     those stored in the client's additional_headers property.
                     The client automatically sets the Content-Type and 
                     Authorization headers.

    Returns:
      httplib.HTTPResponse The server's response to the GET request.
    """

    query_connection = httplib.HTTPConnection(self.server)
    query_connection.putrequest('GET', uri)

    query_connection.putheader('Content-Type','application/atom+xml')
    # Authorization headers are required if the user is querying their
    # own items feed, so include the auth_token if it is present.
    if self.__auth_token:
      query_connection.putheader('Authorization', '%s=%s' %
          (self.__auth_type, self.__auth_token))
    # Add any additional headers held in the client
    if isinstance(self.additional_headers, dict):
      for header in self.additional_headers:
        query_connection.putheader(header, self.additional_headers[header])
    if isinstance(extra_headers, dict):
      for header in extra_headers:
        query_connection.putheader(header, extra_headers[header])
    query_connection.endheaders()

    return query_connection.getresponse() 

  def Post(self, uri, data, extra_headers=None):
    """Insert data into a GData service at the given URI.

    Args:
      uri: string The location (feed) to which the data should be inserted. 
           Example: '/base/feeds/items'. 
      data: string The xml to be sene to the uri. 
      extra_headers: dict (optional) HTTP headers which are to be included. 
                     The client automatically sets the Content-Type,
                     Authorization, and Content-Length headers.

    Returns:
      httplib.HTTPResponse Server's response to the POST request.
    """

    insert_connection = httplib.HTTPConnection(self.server)
    insert_connection.putrequest('POST', uri)

    insert_connection.putheader('Content-Type','application/atom+xml')
    insert_connection.putheader('Authorization', '%s=%s' %
        (self.__auth_type, self.__auth_token))
    if isinstance(self.additional_headers, dict):
      for header in self.additional_headers:
        insert_connection.putheader(header, self.additional_headers[header])
    if isinstance(extra_headers, dict):
      for header in extra_headers:
        insert_connection.putheader(header, extra_headers[header])
    insert_connection.putheader('Content-Length',str(len(data)))
    insert_connection.endheaders()

    insert_connection.send(data)

    return insert_connection.getresponse()

  def Put(self, uri, data, extra_headers=None):
    """Updates an entry at the given URI.
     
    Args:
      uri: string A URI indicating entry to which the update will be applied.
           Example: '/base/feeds/items/ITEM-ID'
      data: string The XML containing the updated data.
      extra_headers: dict (optional) HTTP headers which are to be included.
                     The client automatically sets the Content-Type,
                     Authorization, and Content-Length headers.
  
    Returns:
      httplib.HTTPResponse Server's response to the PUT request.
    """
    
    update_connection = httplib.HTTPConnection(self.server)
    update_connection.putrequest('PUT', uri)

    update_connection.putheader('Content-Type','application/atom+xml')
    update_connection.putheader('Authorization', '%s=%s' %
        (self.__auth_type, self.__auth_token))
    if isinstance(self.additional_headers, dict):
      for header in self.additional_headers:
        update_connection.putheader(header, self.additional_headers[header])
    if isinstance(extra_headers, dict):
      for header in extra_headers:
        update_connection.putheader(header, extra_headers[header])
    update_connection.putheader('Content-Length',str(len(data)))
    update_connection.endheaders()

    update_connection.send(data)

    return update_connection.getresponse()

  def Delete(self, uri, extra_headers=None):
    """Deletes the entry at the given URI.

    Args:
      uri: string The URI of the entry to be deleted. Example: 
           '/base/feeds/items/ITEM-ID'
      extra_headers: dict (optional) HTTP headers which are to be included.
                     The client automatically sets the Content-Type and
                     Authorization headers.

    Returns:
      httplib.HTTPResponse Server's response to the DELETE request.
    """
 
    delete_connection = httplib.HTTPConnection(self.server)
    delete_connection.putrequest('DELETE', uri)
    delete_connection.putheader('Content-Type','application/atom+xml')
    delete_connection.putheader('Authorization', '%s=%s' %
        (self.__auth_type, self.__auth_token))    
    if isinstance(self.additional_headers, dict):
      for header in self.additional_headers:
        delete_connection.putheader(header, self.additional_headers[header])
    if isinstance(extra_headers, dict):
      for header in extra_headers:
        delete_connection.putheader(header, extra_headers[header])
    delete_connection.endheaders()

    return delete_connection.getresponse()

