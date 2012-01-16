#!/usr/bin/python
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

"""Search users with a given pattern and move to a new organization.

Sample to move users to a new organization based on a pattern using
the User Provisioning and Organization Provisioning APIs.

Usage:
  $ python search_organize_users.py
"""

__author__ = 'Shraddha Gupta <shraddhag@google.com>'

from optparse import OptionParser
import re
from gdata.apps.client import AppsClient
from gdata.apps.organization.client import OrganizationUnitProvisioningClient
import gdata.gauth

BATCH_SIZE = 25
SCOPES = ('https://apps-apis.google.com/a/feeds/user/ '
          'https://apps-apis.google.com/a/feeds/policies/')
USER_AGENT = 'SearchAndOrganizeUsers'


class SearchAndOrganizeUsers(object):
  """Search users with a pattern and move them to organization."""

  def __init__(self, client_id, client_secret, domain):
    """Create a new SearchAndOrganizeUsers object configured for a domain.
    
    Args:
      client_id: [string] The clientId of the developer.
      client_secret: [string] The clientSecret of the developer.
      domain: [string] The domain on which the functions are to be performed.
    """
    self.client_id = client_id
    self.client_secret = client_secret
    self.domain = domain

  def AuthorizeClient(self):
    """Authorize the clients for making API requests."""
    self.token = gdata.gauth.OAuth2Token(
        client_id=self.client_id, client_secret=self.client_secret,
        scope=SCOPES, user_agent=USER_AGENT)
    uri = self.token.generate_authorize_url()
    print 'Please visit this URL to authorize the application:'
    print uri
    # Get the verification code from the standard input.
    code = raw_input('What is the verification code? ').strip()
    self.token.get_access_token(code)
    self.user_client = AppsClient(domain=self.domain, auth_token=self.token)
    self.org_client = OrganizationUnitProvisioningClient(
        domain=self.domain, auth_token=self.token)

  def OrganizeUsers(self, customer_id, org_unit_path, pattern):
    """Find users with given pattern and move to an organization in batches.

    Args:
      customer_id: [string] customer_id to make calls to Organization API.
      org_unit_path: [string] path of organization unit where users are moved
      pattern: [regex object] regex to match with users
    """
    users = self.user_client.RetrieveAllUsers()
    matched_users = []
    # Search the users that match given pattern
    for user in users.entry:
      if (pattern.search(user.login.user_name) or
          pattern.search(user.name.given_name) or
          pattern.search(user.name.family_name)):
        user_email = '%s@%s' % (user.login.user_name, self.domain)
        matched_users.append(user_email)
    # Maximum BATCH_SIZE users can be moved at one time
    # Split users into batches of BATCH_SIZE and move in batches
    for i in xrange(0, len(matched_users), BATCH_SIZE):
      batch_to_move = matched_users[i: i + BATCH_SIZE]
      self.org_client.MoveUserToOrgUnit(customer_id,
          org_unit_path, batch_to_move)
    print 'Number of users moved = %d' % len(matched_users)

  def Run(self, org_unit_path, regex):
    self.AuthorizeClient()
    customer_id_entry = self.org_client.RetrieveCustomerId()
    customer_id = customer_id_entry.customer_id
    pattern = re.compile(regex)
    print 'Moving Users with the pattern %s' % regex
    self.OrganizeUsers(customer_id, org_unit_path, pattern)


def main():
  usage = 'Usage: %prog [options]'
  parser = OptionParser(usage=usage)
  parser.add_option('--DOMAIN',
                    help='Google Apps Domain, e.g. "domain.com".')
  parser.add_option('--CLIENT_ID',
                    help='Registered CLIENT_ID of Domain.')
  parser.add_option('--CLIENT_SECRET',
                    help='Registered CLIENT_SECRET of Domain.')
  parser.add_option('--ORG_UNIT_PATH',
                    help='Orgunit path of organization where to move users.')
  parser.add_option('--PATTERN',
                    help='Pattern to search in users')
  (options, args) = parser.parse_args()

  if not (options.DOMAIN and options.CLIENT_ID and options.CLIENT_SECRET
      and options.ORG_UNIT_PATH and options.PATTERN):
    parser.print_help()
    return

  sample = SearchAndOrganizeUsers(options.CLIENT_ID, options.CLIENT_SECRET,
      options.DOMAIN)
  sample.Run(options.ORG_UNIT_PATH, options.PATTERN)


if __name__ == '__main__':
  main()
