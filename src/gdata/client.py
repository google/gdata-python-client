#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
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


__author__ = 'api.jscudder (Jeff Scudder)'


import urllib
import urlparse
import gdata.auth
import gdata.service
import atom.service


SCOPE_URL_PARAM_NAME = 'authsub_token_scope'
# Maps the service names used in ClientLogin to scope URLs. 
CLIENT_LOGIN_SCOPES = {
    'cl': 'http://www.google.com/calendar/feeds/', # Google Calendar
    'gbase': 'http://www.google.com/base/feeds/', # Google Base
    'blogger': 'http://www.blogger.com/feeds/', # Blogger
    'codesearch': 'http://www.google.com/codesearch/feeds/', # Google Code Search
    'cp': 'http://www.google.com/m8/feeds/', # Contacts API
    'finance': 'http://finance.google.com/finance/feeds/', # Google Finance
    'health': 'https://www.google.com/health/feeds/', # Google Health
    'writely': 'http://docs.google.com/feeds/documents/', # Documents List API
    'lh2': 'http://picasaweb.google.com/data/feed/api/', # Picasa Web Albums
    'apps': 'https://www.google.com/a/feeds/', # Google Apps Provisioning API
    'wise': 'http://spreadsheets.google.com/feeds/', # Spreadsheets Data API
    'sitemaps': 'https://www.google.com/webmasters/tools/feeds/', # Google Webmaster Tools
    'youtube': 'http://gdata.youtube.com/feeds/api/'} # YouTube


class AuthorizationRequired(gdata.service.Error):
  pass


class GDataClient(gdata.service.GDataService):

  def __init__(self, application_name=None, tokens=None):
    gdata.service.GDataService.__init__(self, source=application_name)
    # dict which uses the scope URL as the key, and the token as the value.
    self.tokens = tokens or {}

  def ClientLogin(self, username, password, service_name, source=None, 
      account_type=None, auth_url=None, login_token=None, login_captcha=None):
    gdata.service.GDataService.ClientLogin(self, username=username, 
        password=password, account_type=account_type, service=service_name,
        auth_service_url=auth_url, source=source, captcha_token=login_token,
        captcha_response=login_captcha)
    self.tokens[CLIENT_LOGIN_SCOPES[service_name]] = self.auth_token

  def UpgradeAndStoreAuthSubToken(self, token, scopes):
    self.auth_token = token
    self.UpgradeToSessionToken()
    self.StoreAuthSubToken(service.auth_token, scopes)

  def StoreAuthSubToken(self, token, scopes):
    for scope in scopes:
      self.tokens[scope] = token

  def FindTokenForScope(self, url):
    # Attempt a direct match lookup first.
    if url in self.tokens:
      return self.tokens[url]
    # If the scope is not an exact match, look for a scope which is broader
    # than the current request.
    else:
      for scope in self.tokens:
        if url.startswith(scope):
          return self.tokens[scope]
    return None

  def RemoveTokenForScope(self, url):
    if url in self.tokens:
      del self.tokens[url]
    else:
      for scope in self.tokens:
        if url.startswith(scope):
          del self.tokens[scope]
          return

  def Get(self, url, parser):
    token = self.FindTokenForScope(url)
    if token:
      self.auth_token = token
      try:
        return gdata.service.GDataService.Get(self, uri=url, converter=parser)
      except gdata.service.RequestError, inst:
        if inst[0]['status'] == 403 or inst[0]['status'] == 401:
          self.RemoveTokenForScope(url)
        raise
    else:
      return gdata.service.GDataService.Get(self, uri=url, converter=parser)

  def Post(self, data, url, parser, media_source=None):
    token = self.FindTokenForScope(url)
    if token:
      self.auth_token = token
      try:
        return gdata.service.GDataService.Post(self, data=data, uri=url, 
            media_source=media_source, converter=parser)
      except gdata.service.RequestError, inst:
        if inst[0]['status'] == 403 or inst[0]['status'] == 401:
          self.RemoveTokenForScope(url)
        raise
    else:
      raise AuthorizationRequired('Cannot Post to %s without an authorization token' % url)

  def Put(self, data, url, parser):
    token = self.FindTokenForScope(url)
    if token:
      self.auth_token = token
      try:
        return gdata.service.GDataService.Put(self, data=data, uri=url, 
          converter=parser)
      except gdata.service.RequestError, inst:
        if inst[0]['status'] == 403 or inst[0]['status'] == 401:
          self.RemoveTokenForScope(url)
        raise
    else:
      raise AuthorizationRequired('Cannot Put to %s without an authorization token' % url)

  def Delete(self, url):
    token = self.FindTokenForScope(url)
    if token:
      self.auth_token = token
      try:
        return gdata.service.GDataService.Delete(self, uri=url)
      except gdata.service.RequestError, inst:
        if inst[0]['status'] == 403 or inst[0]['status'] == 401:
          self.RemoveTokenForScope(url)
        raise
    else:
      raise AuthorizationRequired('Cannot Delete %s without an authorization token' % url)

    
def ExtractToken(url, scopes_included_in_next=True):
  """Gets the AuthSub token from the current page's URL.

  Designed to be used on the URL that the browser is sent to after the user
  authorizes this application at the page given by GenerateAuthSubRequestUrl.

  Args:
    url: The current page's URL. It should contain the token as a URL 
        parameter. Example: 'http://example.com/?...&token=abcd435'
    scopes_included_in_next: If True, this function looks for a scope value
        associated with the token. The scope is a URL parameter with the
        key set to SCOPE_URL_PARAM_NAME. This parameter should be present
        if the AuthSub request URL was generated using 
        GenerateAuthSubRequestUrl with include_scope_in_next set to True.

  Returns: 
    A tuple containing the token string and a list of scope strings for which
    this token should be valid. If the scope was not included in the URL, the
    tuple will contain (token, None).
  """
  parsed = urlparse.urlparse(url)
  token = gdata.auth.AuthSubTokenFromUrl(parsed[4])
  scopes = None
  if scopes_included_in_next:
    for pair in parsed[4].split('&'):
      if pair.startswith('%s=' % SCOPE_URL_PARAM_NAME):
        scopes = urllib.unquote_plus(pair.split('=')[1])
  return (token, scopes.split(' '))


def GenerateAuthSubRequestUrl(next, scopes, hd='default', secure=False,
    session=True, request_url='http://www.google.com/accounts/AuthSubRequest', 
    include_scopes_in_next=True):
  """Creates a URL to request an AuthSub token to access Google services.

  For more details on AuthSub, see the documentation here: 
  http://code.google.com/apis/accounts/docs/AuthSub.html

  Args:
    next: The URL where the browser should be sent after the user authorizes
        the application. This page is responsible for receiving the token
        which is embeded in the URL as a parameter.
    scopes: The base URL to which access will be granted. Example: 
        'http://www.google.com/calendar/feeds' will grant access to all
        URLs in the Google Calendar data API. If you would like a token for
        multiple scopes, pass in a list of URL strings.
    hd: The domain to which the user's account belongs. This is set to the
        domain name if you are using Google Apps. Example: 'example.org' 
        Defaults to 'default'
    secure: If set to True, all requests should be signed. The default is
        False.
    session: If set to True, the token received by the 'next' URL can be
        upgraded to a multiuse session token. If session is set to False, the
        token may only be used once and cannot be upgraded. Default is True.
    request_url: The base of the URL to which the user will be sent to 
        authorize this application to access their data. The default is
        'http://www.google.com/accounts/AuthSubRequest'.
    include_scopes_in_next: Boolean if set to true, the 'next' parameter will
        be modified to include the requested scope as a URL parameter. The 
        key for the next's scope parameter will be SCOPE_URL_PARAM_NAME. The
        benefit of including the scope URL as a parameter to the next URL, is
        that the page which receives the AuthSub token will be able to tell
        which URLs the token grants access to.

  Returns:
    A URL string to which the browser should be sent.
  """
  if isinstance(scopes, list):
    scope = ' '.join(scopes)
  else:
    scope = scopes
  if include_scopes_in_next:
    if next.find('?') > -1:
      next += '&%s' % urllib.urlencode({SCOPE_URL_PARAM_NAME:scope})
    else:
      next += '?%s' % urllib.urlencode({SCOPE_URL_PARAM_NAME:scope})
  return gdata.auth.GenerateAuthSubUrl(next=next, scope=scope, secure=secure, session=session, 
      request_url=request_url, domain=hd)
