"""Provides OAuth authorization. Main components are:
 * OAuthClient - provides logic for 3-legged OAuth protocol,
 * OAuthDanceHandler - wrapper for OAuthClient for handling OAuth requests,
 * OAuthHandler - from this handler should inherit all other handlers that want
      to be authenticated and have access to BloggerService. Be sure that you
      added @requiredOAuth on top of your request method (i.e. post, get).

Request tokens are stored in OAuthRequestToken (explicite) and access tokens are
stored in TokenCollection (implicit) provided by gdata.alt.appengine.

Heavily used resources and ideas from:
 * http://github.com/tav/tweetapp,
 * Examples of OAuth from GData Python Client written by Eric Bidelman.
"""

__author__ = ('wiktorgworek (Wiktor Gworek), '
              'e.bidelman (Eric Bidelman)')

import os
import gdata.auth
import gdata.client
import gdata.alt.appengine
import gdata.blogger.service

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

SETTINGS = {
  'APP_NAME': 'YOUR_APPLICATION_NAME',
  'CONSUMER_KEY': 'YOUR_CONSUMER_KEY',
  'CONSUMER_SECRET': 'YOUR_CONSUMER_SECRET',
  'SIG_METHOD': gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
  'SCOPES': gdata.service.CLIENT_LOGIN_SCOPES['blogger']
}

# ------------------------------------------------------------------------------
# Data store models.
# ------------------------------------------------------------------------------

class OAuthRequestToken(db.Model):
  """Stores OAuth request token."""

  token_key = db.StringProperty(required=True)
  token_secret = db.StringProperty(required=True)
  created = db.DateTimeProperty(auto_now_add=True)

# ------------------------------------------------------------------------------
# OAuth client.
# ------------------------------------------------------------------------------

class OAuthClient(object):

  __public__ = ('request_token', 'callback', 'revoke_token')

  def __init__(self, handler):
    self.handler = handler
    self.blogger = gdata.blogger.service.BloggerService(
        source=SETTINGS['APP_NAME'])
    self.blogger.SetOAuthInputParameters(SETTINGS['SIG_METHOD'],
        SETTINGS['CONSUMER_KEY'], consumer_secret=SETTINGS['CONSUMER_SECRET'])
    gdata.alt.appengine.run_on_appengine(self.blogger)

  def has_access_token(self):
    """Checks if there is an access token in token store."""
    access_token = self.blogger.token_store.find_token(
        '%20'.join(SETTINGS['SCOPES']))
    return isinstance(access_token, gdata.auth.OAuthToken)

  def request_token(self):
    """Fetches a request token and redirects the user to the approval page."""

    if users.get_current_user():
      # 1.) REQUEST TOKEN STEP. Provide the data scope(s) and the page we'll
      # be redirected back to after the user grants access on the approval page.
      req_token = self.blogger.FetchOAuthRequestToken(
          scopes=SETTINGS['SCOPES'],
          oauth_callback=self.handler.request.uri.replace(
              'request_token', 'callback'))

      # When using HMAC, persist the token secret in order to re-create an
      # OAuthToken object coming back from the approval page.
      db_token = OAuthRequestToken(token_key = req_token.key,
          token_secret=req_token.secret)
      db_token.put()

      # 2.) APPROVAL STEP.  Redirect to user to Google's OAuth approval page.
      self.handler.redirect(self.blogger.GenerateOAuthAuthorizationURL())

  def callback(self):
    """Invoked after we're redirected back from the approval page."""

    oauth_token = gdata.auth.OAuthTokenFromUrl(self.handler.request.uri)
    if oauth_token:
      # Find request token saved by put() method.
      db_token = OAuthRequestToken.all().filter(
          'token_key =', oauth_token.key).fetch(1)[0]
      oauth_token.secret = db_token.token_secret
      oauth_token.oauth_input_params = self.blogger.GetOAuthInputParameters()
      self.blogger.SetOAuthToken(oauth_token)

      # 3.) Exchange the authorized request token for an access token
      oauth_verifier = self.handler.request.get(
          'oauth_verifier', default_value='')
      access_token = self.blogger.UpgradeToOAuthAccessToken(
          oauth_verifier=oauth_verifier)

      # Remember the access token in the current user's token store
      if access_token and users.get_current_user():
        self.blogger.token_store.add_token(access_token)
      elif access_token:
        self.blogger.current_token = access_token
        self.blogger.SetOAuthToken(access_token)

    self.handler.redirect('/')

  def revoke_token(self):
    """Revokes the current user's OAuth access token."""

    try:
      self.blogger.RevokeOAuthToken()
    except gdata.service.RevokingOAuthTokenFailed:
      pass
    except gdata.service.NonOAuthToken:
      pass

    self.blogger.token_store.remove_all_tokens()
    self.handler.redirect('/')

# ------------------------------------------------------------------------------
# Request handlers.
# ------------------------------------------------------------------------------

class OAuthDanceHandler(webapp.RequestHandler):
  """Handler for the 3 legged OAuth dance.

  This handler is responsible for fetching an initial OAuth request token,
  redirecting the user to the approval page.  When the user grants access, they
  will be redirected back to this GET handler and their authorized request token
  will be exchanged for a long-lived access token."""

  def __init__(self):
    super(OAuthDanceHandler, self).__init__()
    self.client = OAuthClient(self)

  def get(self, action=''):
    if action in self.client.__public__:
      self.response.out.write(getattr(self.client, action)())
    else:
      self.response.out.write(self.client.request_token())

class OAuthHandler(webapp.RequestHandler):
  """All handlers requiring OAuth should inherit from this class."""

  def __init__(self):
    super(OAuthHandler, self).__init__()
    self.client = OAuthClient(self)

def requiresOAuth(fun):
  """Decorator for request handlers to gain authentication via OAuth.
     Must be used in a handler that inherits from OAuthHandler."""
  def decorate(self, *args, **kwargs):
    if self.client.has_access_token():
      try:
        fun(self, *args, **kwargs)
      except gdata.service.RequestError, error:
        if error.code in [401, 403]:
          self.redirect('/oauth/request_token')
        else:
          raise
    else:
      self.redirect('/oauth/request_token')
  return decorate
