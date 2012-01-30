#!/usr/bin/python2.4
#
# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Apps marketplace sample app.

Demonstartes how to use provisoining data in marketplace apps.
"""

__author__ = 'Gunjan Sharma <gunjansharma@google.com>'

import logging
import os
import re
import urllib
from urlparse import urlparse
from django.utils import simplejson as json
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from appengine_utilities.sessions import Session
from gdata.apps.client import AppsClient
from gdata.apps.groups.client import GroupsProvisioningClient
from gdata.apps.organization.client import OrganizationUnitProvisioningClient
import gdata.auth

CONSUMER_KEY = '965697648820.apps.googleusercontent.com'
CONSUMER_SECRET = '3GBNP4EJykV7wq8tuN0LTFLr'


class TwoLeggedOauthTokenGenerator(webapp.RequestHandler):
  def Get2loToken(self):
    user = users.get_current_user()
    return gdata.gauth.TwoLeggedOAuthHmacToken(
        CONSUMER_KEY, CONSUMER_SECRET, user.email())


class MainHandler(TwoLeggedOauthTokenGenerator):
  """Handles initial get request and post request to '/' URL."""

  def get(self):
    """Handels the get request for the MainHandler.

    It checks if a the user is logged in and also that he belogs to the domain,
    if not redirects it to the login page else to the index.html page.
    """
    domain = self.request.get('domain')
    if not domain:
      self.response.out.write(
          'Missing required params. To use the app start with following URL: '
          'http://domain-mgmt.appspot.com?from=google&domain=yourdomain.com')
      return
    user = users.get_current_user()
    if user and self.CheckEmail(user):
      logging.debug('logged in user: %s', user.email())
      session = Session()
      session['domain'] = domain
    else:
      self.redirect('/_ah/login_required?' +
                    urllib.urlencode((self.request.str_params)))

    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path, {}))

  def CheckEmail(self, user):
    """Performs basic validation of the supplied email address.

    Args:
      user: A User object corresponding to logged in user.

    Returns:
      True if user is valid, False otherwise.
    """
    domain = urlparse(user.federated_identity()).hostname
    m = re.search('.*@' + domain, user.email())
    if m:
      return True
    else:
      return False

  def post(self):
    """Handels the get request for the MainHandler.

    Retrieves a list of all of the domain's users and sends it
    to the Client as a JSON object.
    """
    users_list = []
    session = Session()
    domain = session['domain']
    client = AppsClient(domain=domain)
    client.auth_token = self.Get2loToken()
    client.ssl = True
    feed = client.RetrieveAllUsers()
    for entry in feed.entry:
      users_list.append(entry.login.user_name)
    self.response.out.write(json.dumps(users_list))


class UserDetailsHandler(TwoLeggedOauthTokenGenerator):
  """Handles get request to '/getdetails' URL."""

  def get(self, username):
    """Handels the get request for the UserDetailsHandler.

    Sends groups, organization unit and nicknames for the user
    in a JSON object.

    Args:
      username: A string denoting the user's username.
    """
    session = Session()
    domain = session['domain']
    if not domain:
      self.redirect('/')
    details = {}
    details['groups'] = self.GetGroups(domain, username)
    details['orgunit'] = self.GetOrgunit(domain, username)
    details['nicknames'] = self.GetNicknames(domain, username)
    data = json.dumps(details)
    logging.debug('Sending data...')
    logging.debug(data)
    self.response.out.write(data)
    logging.debug('Data sent successfully')

  def GetGroups(self, domain, username):
    """Retrieves a list of groups for the given user.

    Args:
      domain: A string determining the user's domain.
      username: A string denoting the user's username.

    Returns:
      A list of dicts of groups with their name and ID if successful.
      Otherwise a list with single dict entry containing error message.
    """
    try:
      groups_client = GroupsProvisioningClient(domain=domain)
      groups_client.auth_token = self.Get2loToken()
      groups_client.ssl = True
      feed = groups_client.RetrieveGroups(username, True)
      groups = []
      for entry in feed.entry:
        group = {}
        group['name'] = entry.group_name
        group['id'] = entry.group_id
        groups.append(group)
      return groups
    except:
      return [{'name': 'An error occured while retriving Groups for the user',
               'id': 'An error occured while retriving Groups for the user'}]

  def GetOrgunit(self, domain, username):
    """Retrieves the Org Unit corresponding to the user.

    Args:
      domain: A string determining the user's domain.
      username: A string denoting the user's username.

    Returns:
      A dict of orgunit having its name and path if successful.
      Otherwise a dict entry containing error message.
    """
    try:
      ouclient = OrganizationUnitProvisioningClient(domain=domain)
      ouclient.auth_token = self.Get2loToken()
      ouclient.ssl = True
      customer_id = ouclient.RetrieveCustomerId().customer_id
      entry = ouclient.RetrieveOrgUser(customer_id, username + '@' + domain)
      oupath = entry.org_unit_path
      orgunit = {}
      if not oupath:
        orgunit['name'] = 'MAIN ORG UNIT'
        orgunit['path'] = '/'
        return orgunit
      entry = ouclient.RetrieveOrgUnit(customer_id, oupath)
      orgunit['name'] = entry.org_unit_name
      orgunit['path'] = entry.org_unit_path
      return orgunit
    except:
      return {'name': 'An error occured while retriving OrgUnit for the user.',
              'path': 'An error occured while retriving OrgUnit for the user.'}

  def GetNicknames(self, domain, username):
    """Retrieves the list of all the nicknames for the user.

    Args:
      domain: A string determining the user's domain.
      username: A string denoting the user's username.

    Returns:
      A list of user's nicknames if successful.
      Otherwise a list with a single entry containing error message.
    """
    try:
      client = AppsClient(domain=domain)
      client.auth_token = self.Get2loToken()
      client.ssl = True
      feed = client.RetrieveNicknames(username)
      nicknames = []
      for entry in feed.entry:
        nicknames.append(entry.nickname.name)
      return nicknames
    except:
      return ['An error occured while retriving Nicknames for the user.']


class OpenIDHandler(webapp.RequestHandler):
  def get(self):
    """Begins the OpenID flow for the supplied domain."""
    domain = self.request.get('domain')
    self.redirect(users.create_login_url(
        dest_url='https://domain-mgmt.appspot.com?domain=' + domain,
        _auth_domain=None,
        federated_identity=domain))


def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/getdetails/(.*)',
                                         UserDetailsHandler),
                                        ('/_ah/login_required', OpenIDHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
