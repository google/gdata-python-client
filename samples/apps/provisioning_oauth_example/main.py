#!/usr/bin/python2.4
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Sample app for Google Apps Provisioning API using OAuth.

  ProvisioningOAuthSample: Demonstrates the use of the Provisioning API with
  OAuth in a Google App Engine app.
"""


__author__ = 'pti@google.com (Prashant Tiwari)'


import json
import os
import atom.http_interface
import gdata.apps.service
import gdata.auth
from django.utils import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from gdata.apps.service import AppsForYourDomainException


INIT = {
    'APP_NAME': 'googlecode-provisioningtester-v1',
    'SCOPES': ['https://apps-apis.google.com/a/feeds']
}

secret = None

class MainPage(webapp.RequestHandler):
  """Defines the entry point for the App Engine app"""
  def get(self):
    global service
    try:
      service
    except:
      self.redirect('/login')
      return

    oauth_token = None
    json = None
    if self.request.get('two_legged_oauth'):
      two_legged_oauth = True
      app_title = 'Provisioning API Sample (2-legged OAuth)'
      start_over_text = 'Start over'
    else:
      two_legged_oauth = False
      app_title = 'Provisioning API Sample (3-legged OAuth)'
      start_over_text = 'Revoke token'

    try:
      if service:
        oauth_token = service.token_store.find_token('%20'.join(INIT['SCOPES']))
        if isinstance(oauth_token, gdata.auth.OAuthToken) or isinstance(
            oauth_token, atom.http_interface.GenericToken):
          user_feed = service.RetrieveAllUsers()
          json = get_json_from_feed(user_feed)
      else:
        self.redirect('/login')
        return
    except AppsForYourDomainException, e:
      # Usually a Forbidden (403) when signed-in user isn't the admin.
      self.response.out.write(e.args[0].get('body'))
    else:
      template_values = {
          'oauth_token': oauth_token,
          'json': json,
          'two_legged_oauth': two_legged_oauth,
          'start_over_text': start_over_text,
          'app_title': app_title
      }

      path = os.path.join(os.path.dirname(__file__), 'index.html')
      self.response.out.write(template.render(path, template_values))


def get_json_from_feed(user_feed):
  """Constructs and returns a JSON object from the given feed object
  
  Args:
    user_feed: A gdata.apps.UserFeed object
  
  Returns:
    A JSON object containing the first and last names of the domain users
  """
  json = []
  for entry in user_feed.entry:
    json.append({'given_name': entry.name.given_name,
                 'family_name': entry.name.family_name,
                 'username': entry.login.user_name,
                 'admin': entry.login.admin
                })
  return simplejson.dumps(json)


class DoLogin(webapp.RequestHandler):
  """Brings up the app's login page"""
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'login.html')
    self.response.out.write(template.render(path, None))


class DoAuth(webapp.RequestHandler):
  """Handles the entire OAuth flow for the app"""
  def post(self):
    global service
    global secret
    # Get instance of the AppsService for the given consumer_key (domain)
    service = gdata.apps.service.AppsService(source=INIT['APP_NAME'],
                                             domain=self.request.get('key'))
    two_legged_oauth = False
    if self.request.get('oauth') == 'two_legged_oauth':
      two_legged_oauth = True
    service.SetOAuthInputParameters(
        signature_method=gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
        consumer_key=self.request.get('key'),
        consumer_secret=self.request.get('secret'),
        two_legged_oauth=two_legged_oauth)

    if two_legged_oauth:
      # Redirect to MainPage if 2-legged OAuth is requested
      self.redirect('/?two_legged_oauth=true')
      return

    request_token = service.FetchOAuthRequestToken(
        scopes=INIT['SCOPES'], oauth_callback=self.request.uri)
    secret = request_token.secret
    service.SetOAuthToken(request_token)
    # Send user to Google authorization page
    google_auth_page_url = service.GenerateOAuthAuthorizationURL()
    self.redirect(google_auth_page_url)

  def get(self):
    global service
    global secret
    # Extract the OAuth request token from the URL
    oauth_token = gdata.auth.OAuthTokenFromUrl(self.request.uri)
    if oauth_token:
      oauth_token.secret = secret
      oauth_token.oauth_input_params = service.GetOAuthInputParameters()
      service.SetOAuthToken(oauth_token)
      # Exchange the request token for an access token
      oauth_verifier = self.request.get('oauth_verifier', default_value='')
      access_token = service.UpgradeToOAuthAccessToken(
          oauth_verifier=oauth_verifier)
      # Store access_token to the service token_store for later access
      if access_token:
        service.current_token = access_token
        service.SetOAuthToken(access_token)

    self.redirect('/')


class DoStartOver(webapp.RequestHandler):
  """Revokes the OAuth token if needed and starts over"""
  def get(self):
    global service
    two_legged_oauth = self.request.get('two_legged_oauth')
    # Revoke the token for 3-legged OAuth
    if two_legged_oauth != 'True':
      try:
        service.RevokeOAuthToken()
      except gdata.service.RevokingOAuthTokenFailed:
        pass
      except gdata.service.NonOAuthToken:
        pass
      finally:
        service.token_store.remove_all_tokens()

    service = None
    self.redirect('/')


application = webapp.WSGIApplication([('/', MainPage),
                                      ('/do_auth', DoAuth),
                                      ('/start_over', DoStartOver),
                                      ('/login', DoLogin)],
                                      debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
