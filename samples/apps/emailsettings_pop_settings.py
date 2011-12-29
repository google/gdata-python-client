#!/usr/bin/python2.4
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Demonstrates Email Settings API's POP settings.
   Enables POP for all of the domain's users for all messages and
   archives Gmail's copy.
"""

__author__ = 'Gunjan Sharma <gunjansharma@google.com>'

import getopt
import sys
import gdata.apps.client
import gdata.apps.emailsettings.client


SCOPES = ['https://apps-apis.google.com/a/feeds/emailsettings/2.0/',
          'https://apps-apis.google.com/a/feeds/user/']


class PopSettingsException(Exception):
  """Exception class for PopSettings to show appropriate error message."""

  def __init__(self, message):
    """Create a new PopSettingsException with the appropriate error message."""
    super(PopSettingsException, self).__init__(message)


class PopSettings(object):
  """Sample demonstrating how to enable POP for all of a domain's users."""

  def __init__(self, consumer_key, consumer_secret, domain):
    """Create a new PopSettings object configured for a domain.

    Args:
      consumer_key: [string] The consumerKey of the domain.
      consumer_secret: [string] The consumerSecret of the domain.
      domain: [string] The domain whose user's POP settings to be changed.
    """
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.domain = domain

  def Authorize(self):
    """Asks the domain's admin to authorize.

       Access to two APIs needs to be authorized,
       provisioning users and Gmail settings.
       The function creates clients for both APIs.
    """
    self.email_settings_client = (
        gdata.apps.emailsettings.client.EmailSettingsClient(
            domain=self.domain))
    self.provisioning_client = gdata.apps.client.AppsClient(domain=self.domain)
    request_token = self.email_settings_client.GetOAuthToken(
        SCOPES, None, self.consumer_key, consumer_secret=self.consumer_secret)
    print request_token.GenerateAuthorizationUrl()
    raw_input('Manually go to the above URL and authenticate.'
              'Press Return after authorization.')
    access_token = self.email_settings_client.GetAccessToken(request_token)
    self.email_settings_client.auth_token = access_token
    self.provisioning_client.auth_token = access_token

  def UpdateDomainUsersPopSettings(self):
    """Updates POP settings for all of the domain's users."""
    users = self.provisioning_client.RetrieveAllUsers()
    for user in users.entry:
      self.email_settings_client.UpdatePop(username=user.login.user_name,
                                           enable=True,
                                           enable_for='ALL_MAIL',
                                           action='ARCHIVE')


def PrintUsageString():
  """Prints the correct call for running the sample."""
  print ('python emailsettings_pop_settings.py'
         '--consumer_key [ConsumerKey] --consumer_secret [ConsumerSecret]'
         '--domain [domain]')


def main():
  """Updates POP settings for all of the domain's users
     using the Email Settings API.
  """
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['consumer_key=',
                                                  'consumer_secret=',
                                                  'domain='])
  except getopt.error, msg:
    PrintUsageString()
    sys.exit(1)

  consumer_key = ''
  consumer_secret = ''
  domain = ''
  for option, arg in opts:
    if option == '--consumer_key':
      consumer_key = arg
    elif option == '--consumer_secret':
      consumer_secret = arg
    elif option == '--domain':
      domain = arg

  if not (consumer_key and consumer_secret and domain):
    print 'Requires exactly three flags.'
    PrintUsageString()
    sys.exit(1)

  pop_settings = PopSettings(
      consumer_key, consumer_secret, domain)
  try:
    pop_settings.Authorize()
    pop_settings.UpdateDomainUsersPopSettings()
  except gdata.client.RequestError, e:
    if e.status == 403:
      raise PopSettingsException('Invalid Domain')
    elif e.status == 400:
      raise PopSettingsException('Invalid consumer credentials')
    elif e.status == 503:
      raise PopSettingsException('Server busy')
    else e.status == 500:
      raise PopSettingsException('Internal server error')
    else:
      raise PopSettingsException('Unknown error')


if __name__ == '__main__':
  main()
