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

"""Sample to demonstrate the Email Audit API's email monitoring functions.

The sample demonstrates the creating, updating, retrieving and deleting of
email monitors.
"""

__author__ = 'Gunjan Sharma <gunjansharma@google.com>'

from datetime import datetime
import getopt
import re
import sys
import gdata
from gdata.apps.audit.service import AuditService


class EmailMonitoringException(Exception):
  """Exception class for EmailMonitoring, shows appropriate error message."""


class EmailMonitoring(object):
  """Sample demonstrating how to perform CRUD operations on email monitor."""

  def __init__(self, consumer_key, consumer_secret, domain):
    """Create a new EmailMonitoring object configured for a domain.

    Args:
      consumer_key: A string representing a consumerKey.
      consumer_secret: A string representing a consumerSecret.
      domain: A string representing the domain to work on in the sample.
    """
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.domain = domain
    self._Authorize()

  def _Authorize(self):
    """Asks the domain's admin to authorize access to the apps Apis."""
    self.service = AuditService(domain=self.domain, source='emailAuditSample')
    self.service.SetOAuthInputParameters(
        gdata.auth.OAuthSignatureMethod.HMAC_SHA1,
        self.consumer_key, self.consumer_secret)
    request_token = self.service.FetchOAuthRequestToken()
    self.service.SetOAuthToken(request_token)
    auth_url = self.service.GenerateOAuthAuthorizationURL()
    print auth_url
    raw_input('Manually go to the above URL and authenticate.'
              'Press Return after authorization.')
    self.service.UpgradeToOAuthAccessToken()

  def _CheckUsername(self, username):
    """Checks if a given username is valid or not.

    Args:
      username: A string to check for validity.

    Returns:
      True if username is valid, False otherwise.
    """
    if len(username) > 64:
      print 'Username length should be less than 64'
      return False
    pattern = re.compile('[^\w\.\+-_\']+')
    return not bool(pattern.search(username))

  def _GetValidUsername(self, typeof):
    """Takes a valid username as input.

    Args:
      typeof: A string representing the type of user.

    Returns:
      A valid string corresponding to username.
    """
    username = ''
    while not username:
      username = raw_input('Enter a valid %s username: ' % typeof)
      if not self._CheckUsername(username):
        print 'Invalid username'
        username = ''
    return username

  def _GetValidDate(self, is_neccessary):
    """Takes a valid date as input in 'yyyy-mm-dd HH:MM' format.

    Args:
      is_neccessary: A boolean denoting if a non empty value is needed.

    Returns:
      A valid string corresponding to date.
    """
    date = ''
    extra_stmt = ''
    if not is_neccessary:
      extra_stmt = '. Press enter to skip.'
    while not date:
      date = raw_input(
          'Enter a valid date as (yyyy-mm-dd HH:MM)%s:' % extra_stmt)
      if not (date and is_neccessary):
        return date
      try:
        datetime.strptime(date, '%Y-%m-%d %H:%M')
        return date
      except ValueError:
        print 'Not a valid date!'
        date = ''

  def _GetBool(self, name):
    """Takes a boolean value as input.

    Args:
      name: A string for which input is to be taken.

    Returns:
      A boolean for an entity represented by name.
    """
    choice = raw_input(
        'Enter your choice (t/f) for %s (defaults to False):' % name).strip()
    if choice == 't':
      return True
    return False

  def _CreateEmailMonitor(self):
    """Creates/Updates an email monitor."""
    src_user = self._GetValidUsername('source')
    dest_user = self._GetValidUsername('destination')
    end_date = self._GetValidDate(True)
    start_date = self._GetValidDate(False)
    incoming_headers = self._GetBool('incoming headers')
    outgoing_headers = self._GetBool('outgoing headers')
    drafts = self._GetBool('drafts')
    drafts_headers = False
    if drafts:
      drafts_headers = self._GetBool('drafts headers')
    chats = self._GetBool('chats')
    chats_headers = False
    if chats:
      self._GetBool('chats headers')
    self.service.createEmailMonitor(
        src_user, dest_user,
        end_date, start_date,
        incoming_headers, outgoing_headers,
        drafts, drafts_headers,
        chats, chats_headers)
    print 'Email monitor created/updated successfully!\n'

  def _RetrieveEmailMonitor(self):
    """Retrieves all email monitors for a user."""
    src_user = self._GetValidUsername('source')
    monitors = self.service.getEmailMonitors(src_user)
    for monitor in monitors:
      for key in monitor.keys():
        print '%s ----------- %s' % (key, monitor.get(key))
      print ''
    print 'Email monitors retrieved successfully!\n'

  def _DeleteEmailMonitor(self):
    """Deletes an email monitor."""
    src_user = self._GetValidUsername('source')
    dest_user = self._GetValidUsername('destination')
    self.service.deleteEmailMonitor(src_user, dest_user)
    print 'Email monitor deleted successfully!\n'

  def Run(self):
    """Handles the flow of the sample."""
    functions_list = [
        {
            'function': self._CreateEmailMonitor,
            'description': 'Create a email monitor for a domain user'
        },
        {
            'function': self._CreateEmailMonitor,
            'description': 'Update a email monitor for a domain user'
        },
        {
            'function': self._RetrieveEmailMonitor,
            'description': 'Retrieve all email monitors for a domain user'
        },
        {
            'function': self._DeleteEmailMonitor,
            'description': 'Delete a email monitor for a domain user'
        }
    ]

    while True:
      print 'What would you like to do? Choose an option:'
      print '0 - To exit'
      for i in range (0, len(functions_list)):
        print '%d - %s' % ((i + 1), functions_list[i].get('description'))
      choice = raw_input('Enter your choice: ').strip()
      if choice.isdigit():
        choice = int(choice)
      if choice == 0:
        break
      if choice < 0 or choice > len(functions_list):
        print 'Not a valid option!'
        continue
      try:
        functions_list[choice - 1].get('function')()
      except gdata.apps.service.AppsForYourDomainException, e:
        if e.error_code == 1301:
          print '\nError: Invalid username!!\n'
        else:
          raise e


def PrintUsageString():
  """Prints the correct call for running the sample."""
  print ('python email_audit_email_monitoring.py '
         '--consumer_key [ConsumerKey] --consumer_secret [ConsumerSecret] '
         '--domain [domain]')


def main():
  """Runs the sample using an instance of EmailMonitoring."""

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

  try:
    email_monitoring = EmailMonitoring(
        consumer_key, consumer_secret, domain)
    email_monitoring.Run()
  except gdata.apps.service.AppsForYourDomainException, e:
    raise EmailMonitoringException('Invalid Domain')
  except gdata.service.FetchingOAuthRequestTokenFailed, e:
    raise EmailMonitoringException('Invalid consumer credentials')
  except Exception, e:
    if e.args[0].get('status') == 503:
      raise EmailMonitoringException('Server busy')
    elif e.args[0].get('status') == 500:
      raise EmailMonitoringException('Internal server error')
    else:
      raise EmailMonitoringException('Unknown error')


if __name__ == '__main__':
  main()
