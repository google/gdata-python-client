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

"""Sample to demonstrate the Email Settings API's labels and filters creation.
   The sample creates labels and filters corresponding to festivals,
   which are some days ahead.
"""

__author__ = 'Gunjan Sharma <gunjansharma@google.com>'

from datetime import date
from datetime import datetime
import getopt
import random
import sys
import time
import gdata.apps.client
import gdata.apps.emailsettings.client


SCOPES = ['https://apps-apis.google.com/a/feeds/emailsettings/2.0/',
          'https://apps-apis.google.com/a/feeds/user/']
FESTIVALS_LIST = [
    {
        'name': 'Christmas',
        'date': '25/12',
        'tags': ['Merry Christmas', 'Happy Christmas',
                 'Happy X-mas', 'Merry X-mas']
    },
    {
        'name': 'Halloween',
        'date': '31/10',
        'tags': ['Happy Halloween', 'Trick or Treat', 'Guise']
    },
    {
        'name': 'Sankranti',
        'date': '14/01',
        'tags': ['Makar Sankranti', 'Happy Sankranti']
    },
    {
        'name': 'New Year',
        'date': '31/12',
        'tags': ['Happy New Year', 'New Year Best Wishes']
    }]
# Number of days left before a festival should be less than MAX_DAY_LEFT
# to be considered for filter creation.
MAX_DAYS_LEFT = 15
# Maximum retries to be done for exponential back-off
MAX_RETRIES = 6


class FestivalSettingsException(Exception):
  """Exception class for FestivalSettings to show appropriate error message."""

  def __init__(self, message):
    """Create new FestivalSettingsException with appropriate error message."""
    super(FestivalSettingsException, self).__init__(message)


class FestivalSettings(object):
  """Sample demonstrating how to create filter and label for domain's user."""

  def __init__(self, consumer_key, consumer_secret, domain):
    """Create a new FestivalSettings object configured for a domain.

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

    Access to the two APIs needs to be authorized,
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

  def _CreateLabelsFiltersForUser(self, username):
    """Creates labels and filters for a domain's user.

    Args:
      username: [string] The user's username to create labels and filters for.
    """
    today = date.today()

    for festival in FESTIVALS_LIST:
      d = datetime.strptime(festival['date'], '%d/%m').date()
      d = d.replace(year=today.year)
      days_left = (d - today).days
      d = d.replace(year=today.year+1)
      days_left_next_year = (d - today).days
      if ((0 <= days_left <= MAX_DAYS_LEFT) or
          (0 <= days_left_next_year <= MAX_DAYS_LEFT)):
        self._CreateFestivalSettingsForUser(username, festival, 1)

  def _CreateFestivalSettingsForUser(self, username, festival, tries):
    """Creates the festival wishes labels and filters for a domain's user.

    Args:
      username: [string] The user's username to create labels and filters for.
      festival: [dictionary] The details for the festival.
      tries: Number of times the operation has been retried.
    """
    label_name = festival['name'] + ' Wishes'
    try:
      self.email_settings_client.CreateLabel(username=username,
                                             name=label_name)
      for tag in festival['tags']:
        self.email_settings_client.CreateFilter(username=username,
                                                has_the_word=tag,
                                                label=label_name)
    except gdata.client.RequestError, e:
      if e.status == 503 and tries < MAX_RETRIES:
        time.sleep(2 ^ tries + random.randint(0, 10))
        self._CreateFestivalSettingsForUser(username, festival, tries+1)

  def Run(self):
    """Handles the flow of the sample.
    Asks application user for whom to create the festival wishes
    labels and filters.
    """
    print 'Whom would you like to create labels for?'
    print ('1 - For all user in the domain.'
           '(WARNING: May take a long time depending on your domain size.)')
    print '2 - Single user'

    choice = raw_input('Enter your choice: ').strip()
    if choice.isdigit():
      choice = int(choice)

    if choice == 1:
      users = self.provisioning_client.RetrieveAllUsers()
      for user in users.entry:
        self._CreateLabelsFiltersForUser(user.login.user_name)
    elif choice == 2:
      username = raw_input('Enter a valid username: ')
      self._CreateLabelsFiltersForUser(username)
    else:
      print 'Invalid choice'
      return
    print 'Labels and Filters created successfully'


def PrintUsageString():
  """Prints the correct call for running the sample."""
  print ('python emailsettings_labels_filters.py'
         '--consumer_key [ConsumerKey] --consumer_secret [ConsumerSecret]'
         '--domain [domain]')


def main():
  """Runs the sample using an instance of FestivalSettings."""

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

  festival_wishes_labels = FestivalSettings(
      consumer_key, consumer_secret, domain)
  try:
    festival_wishes_labels.Authorize()
  except gdata.client.RequestError, e:
    if e.status == 400:
      raise FestivalSettingsException('Invalid consumer credentials')
    else:
      raise FestivalSettingsException('Unknown server error')
    sys.exit(1)

  try:
    festival_wishes_labels.Run()
  except gdata.client.RequestError, e:
    if e.status == 403:
      raise FestivalSettingsException('Invalid Domain')
    elif e.status == 400:
      raise FestivalSettingsException('Invalid username')
    else:
      print e.reason
      raise FestivalSettingsException('Unknown error')


if __name__ == '__main__':
  main()
