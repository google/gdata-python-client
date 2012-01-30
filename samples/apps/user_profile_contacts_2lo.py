#!/usr/bin/python
#
# Copyright 2012 Google Inc. All Rights Reserved.
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

"""Sample to retrieve profile and contacts of a domain user.

The sample uses 2-legged OAuth to authorize clients of User Provisioning
and Contacts API and retrieves user's profile and contacts.
"""

__author__ = 'Shraddha Gupta <shraddhag@google.com>'

from optparse import OptionParser
import gdata.apps.client
import gdata.contacts.client
import gdata.gauth


class UserProfileAndContactsSample(object):
  """Class to demonstrate retrieval of domain user's profile and contacts."""

  def __init__(self, consumer_key, consumer_secret):
    """Creates a new UserProfileAndContactsSample object for a domain.

    Args:
      consumer_key: String, consumer key of the domain.
      consumer_secret: String, consumer secret of the domain.
    """
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.domain = consumer_key

  def TwoLOAuthorize(self, admin_id):
    """Authorize clients of User Provisioning and Contacts API using 2LO.

    Args:
      admin_id: String, admin username for 2LO with the Provisioning API.
    """
    requestor_id = '%s@%s' % (admin_id, self.consumer_key)
    two_legged_oauth_token = gdata.gauth.TwoLeggedOAuthHmacToken(
        self.consumer_key, self.consumer_secret, requestor_id)

    self.apps_client = gdata.apps.client.AppsClient(domain=self.domain)
    self.apps_client.auth_token = two_legged_oauth_token

    self.contacts_client = gdata.contacts.client.ContactsClient(
        domain=self.domain)
    self.contacts_client.auth_token = two_legged_oauth_token

  def PrintProfile(self, profile):
    """Prints the contents of a profile entry.

    Args:
      profile: gdata.contacts.data.ProfileEntry.
    """
    for email in profile.email:
      if email.primary == 'true':
        print 'Email: %s (primary)' % email.address
      else:
        print 'Email: %s' % email.address
    if profile.name:
      print 'Name: %s' % profile.name.full_name.text
    if profile.nickname:
      print 'Nickname: %s' % profile.nickname.text
    if profile.occupation:
      print 'Occupation: %s' % profile.occupation.text
    if profile.gender:
      print 'Gender: %s' % profile.gender.value
    if profile.birthday:
      print 'Birthday: %s' % profile.birthday.when
    for phone_number in profile.phone_number:
      print 'Phone Number: %s' % phone_number.text

  def GetProfile(self, admin_id, user_id):
    """Retrieves the profile of a user.

    Args:
      admin_id: String, admin username.
      user_id: String, user whose profile is retrieved.

    Returns:
      profile_entry: gdata.contacts.data.ProfileEntry.
    """
    requestor_id = '%s@%s' % (admin_id, self.domain)
    self.contacts_client.auth_token.requestor_id = requestor_id
    entry_uri = '%s/%s' % (self.contacts_client.GetFeedUri('profiles'),
                           user_id)
    profile_entry = self.contacts_client.GetProfile(entry_uri)
    return profile_entry

  def GetContacts(self, user_id):
    """Retrieves the contacts of a user.

    Args:
      user_id: String, user whose contacts are retrieved.

    Returns:
      contacts: List of strings containing user contacts.
    """
    requestor_id = '%s@%s' % (user_id, self.domain)
    self.contacts_client.auth_token.requestor_id = requestor_id
    contacts = []
    try:
      contact_feed = self.contacts_client.GetContacts()
      for contact_entry in contact_feed.entry:
        contacts.append(contact_entry.title.text)
    except gdata.client.Unauthorized, e:
      print 'Error: %s %s' % (e.status, e.reason)
    return contacts

  def Run(self, admin_id, user_id):
    """Retrieves profile and contacts of a user.

    Args:
      admin_id: String, admin username.
      user_id: String, user whose information is retrieved.
    """
    self.TwoLOAuthorize(admin_id)
    print 'Profile of user: %s' % user_id
    profile = self.GetProfile(admin_id, user_id)
    self.PrintProfile(profile)
    user = self.apps_client.RetrieveUser(user_id)
    print 'Is admin: %s' % user.login.admin
    print 'Suspended: %s' % user.login.suspended
    contacts = self.GetContacts(user_id)
    print '\nContacts of user '
    for contact in contacts:
      print contact


def main():
  """Demonstrates retrieval of domain user's profile and contacts using 2LO."""

  usage = ('Usage: %prog --consumer_key <consumer_key> '
           '--consumer_secret <consumer_secret> --admin_id <admin_id> '
           '--user_id=<user_id> ')
  parser = OptionParser(usage=usage)
  parser.add_option('--consumer_key',
                    help='Domain name is also consumer key.')
  parser.add_option('--consumer_secret',
                    help='Consumer secret of the domain.')
  parser.add_option('--admin_id',
                    help='Username of admin.')
  parser.add_option('--user_id',
                    help='Username of domain user.')
  (options, args) = parser.parse_args()

  if (not options.consumer_key or not options.consumer_secret
      or not options.admin_id or not options.user_id):
    parser.print_help()
    return 1
  sample = UserProfileAndContactsSample(options.consumer_key,
                                        options.consumer_secret)
  sample.Run(options.admin_id, options.user_id)


if __name__ == '__main__':
  main()
