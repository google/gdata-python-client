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

"""Create group and update settings using two APIs.

Sample to use the Groups Settings API in google-api-python client library
http://code.google.com/p/google-api-python-client/source/checkout
with the Groups Provisioning API in gdata-python-client library
http://code.google.com/p/gdata-python-client/source/checkout to create a
group and update its settings.

Usage:
  $ python create_update_group.py
"""

__author__ = 'Shraddha Gupta <shraddhag@google.com>'

import os
import pprint
import sys

from apiclient.discovery import build
import gdata.apps.groups.client
import gflags
import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run


# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = 'client_secrets.json'

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console <https://code.google.com/apis/console>.

""" % os.path.join(os.path.dirname(__file__), CLIENT_SECRETS)

# Request a token for the scope of two APIs:
# Groups Provisioning and Groups Settings APIs
SCOPES = ('https://apps-apis.google.com/a/feeds/groups/ '
          'https://www.googleapis.com/auth/apps.groups.settings')

FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope=SCOPES,
    message=MISSING_CLIENT_SECRETS_MESSAGE)
FLAGS = gflags.FLAGS


def GetOAuth2Token(client_id, client_secret, access_token, refresh_token):
  """Get the OAuth 2.0 token to be used with the Groups Provisioning API.

  Args:
    client_id: String client_id of the installed application
    client_secret: String client_secret of the installed application
    access_token: String access token obtained from OAuth 2.0 server flow
    refresh_token: String refresh token obtained with access token

  Returns:
    token: String OAuth 2.0 token adapted for the Groups Provisioning API.
  """
  token = gdata.gauth.OAuth2Token(client_id=client_id,
                                  client_secret=client_secret,
                                  scope=SCOPES,
                                  access_token=access_token,
                                  refresh_token=refresh_token,
                                  user_agent='create-manage-group-sample')
  return token


def CreateAndUpdateGroup(http, groups_client, domain):
  """Create a group and update its settings.

  Args:
    http: httplib2.Http authorized object
    groups_client: gdata.apps.groups.client.GroupsProvisioningClient
                  authorized group provisioning client
    domain: String domain name
  """
  group_id = raw_input('Enter the group id: ')
  group_name = raw_input('Enter the group name: ')
  group_description = raw_input('Enter the group description: ')
  email_permission = raw_input('Enter the email permission: ')

  if not (group_id and group_name):
    print 'One or more required fields missing: group id, group name'
    sys.exit(1)

  new_group = groups_client.CreateGroup(group_id=group_id,
      group_name=group_name, description=group_description,
      email_permission=email_permission)
  print 'Group Created %s' % new_group.group_id
  print 'Name: %s\nDescription %s\nEmail Permission %s' % (
      new_group.group_name, new_group.description, new_group.email_permission)

  group_id = '%s@%s' % (new_group.group_id, domain)
  service = build('groupssettings', 'v1', http=http)
  # Get the resource 'group' from the set of resources of the API.
  group_resource = service.groups()

  body = {'showInGroupDirectory': True,
          'whoCanViewGroup': 'ALL_IN_DOMAIN_CAN_VIEW',
          'whoCanViewMembership': 'ALL_IN_DOMAIN_CAN_VIEW'}
  # Update the group properties
  g = group_resource.update(groupUniqueId=group_id, body=body).execute()
  print '\nUpdated Access Permissions to the group\n'
  pprint.pprint(g)


def main(argv):
  """Demonstrates creation of a group and updation of its settings."""
  storage = Storage('group.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    print 'Credentials are invalid or do not exist.'
    credentials = run(FLOW, storage)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with the valid credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  domain = raw_input('Enter the domain: ')

  # Create an OAuth 2.0 token suitable for use with the GData client library
  oauth2token = GetOAuth2Token(credentials.client_id,
                               credentials.client_secret,
                               credentials.access_token,
                               credentials.refresh_token)
  groups_client = oauth2token.authorize(
      gdata.apps.groups.client.GroupsProvisioningClient(domain=domain))
  CreateAndUpdateGroup(http, groups_client, domain)


if __name__ == '__main__':
  main(sys.argv)
