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

"""Sample to list all the members of a group.

The sample demonstrates how to get all members from a group (say Group1)
including members from groups that are members of Group1. It recursively finds
the members of groups that are the member of given group and lists them.
"""

__author__ = 'Shraddha Gupta <shraddhag@google.com>'

from optparse import OptionParser
import gdata.apps.groups.client


SCOPE = 'https://apps-apis.google.com/a/feeds/groups/'
USER_AGENT = 'ListUserMembersFromGroup'


def GetAuthToken(client_id, client_secret):
  """Get an OAuth 2.0 access token using the given client_id and client_secret.

  Client_id and client_secret can be found on the API Access tab on the
  Google APIs Console <http://code.google.com/apis/console>.

  Args:
    client_id: String, client id of the developer.
    client_secret: String, client secret of the developer.

  Returns:
    token: String, authorized OAuth 2.0 token.
  """
  token = gdata.gauth.OAuth2Token(
      client_id=client_id, client_secret=client_secret,
      scope=SCOPE, user_agent=USER_AGENT)
  uri = token.generate_authorize_url()
  print 'Please visit this URL to authorize the application:'
  print uri
  # Get the verification code from the standard input.
  code = raw_input('What is the verification code? ').strip()
  token.get_access_token(code)
  return token


def ListAllMembers(group_client, group_id):
  """Lists all members including members of sub-groups.

  Args:
    group_client: gdata.apps.groups.client.GroupsProvisioningClient instance.
    group_id: String, identifier of the group from which members are listed.

  Returns:
    members_list: List containing the member_id of group members.
  """
  members_list = []
  try:
    group_members = group_client.RetrieveAllMembers(group_id)
    for member in group_members.entry:
      if member.member_type == 'Group':
        temp_list = ListAllMembers(group_client, member.member_id)
        members_list.extend(temp_list)
      else:
        members_list.append(member.member_id)
  except gdata.client.RequestError, e:
    print 'Request error: %s %s %s' % (e.status, e.reason, e.body)
  return members_list


def main():
  """Demonstrates retrieval of members of a group."""
  usage = ('Usage: %prog --DOMAIN <domain> --CLIENT_ID <client_id> '
           '--CLIENT_SECRET <client_secret> --GROUP_ID <group_id> ')
  parser = OptionParser(usage=usage)
  parser.add_option('--DOMAIN',
                    help='Google Apps Domain, e.g. "domain.com".')
  parser.add_option('--CLIENT_ID',
                    help='Registered CLIENT_ID of Domain.')
  parser.add_option('--CLIENT_SECRET',
                    help='Registered CLIENT_SECRET of Domain.')
  parser.add_option('--GROUP_ID',
                    help='Group identifier of the group to list members from.')
  (options, args) = parser.parse_args()

  if not (options.DOMAIN and options.CLIENT_ID and options.CLIENT_SECRET
          and options.GROUP_ID):
    parser.print_help()
    return

  group_client = gdata.apps.groups.client.GroupsProvisioningClient(
      domain=options.DOMAIN)
  token = GetAuthToken(options.CLIENT_ID, options.CLIENT_SECRET)
  token.authorize(group_client)

  members_list = ListAllMembers(group_client, options.GROUP_ID)
  no_duplicate_members_list = list(set(members_list))
  print 'User members of the group %s are: ' % options.GROUP_ID
  print no_duplicate_members_list


if __name__ == '__main__':
  main()
