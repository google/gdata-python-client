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

__author__ = 'Gunjan Sharma <gunjansharma@google.com>'

import getopt
import sys
import gdata.apps.groups.client
import gdata.apps.groups.data

SCOPE = 'https://apps-apis.google.com/a/feeds/groups/'
USER_AGENT = 'GroupsQuickStartExample'


class GroupsQuickStartExample(object):
  """Demonstrates all the functions of Groups provisioning."""

  def __init__(self, client_id, client_secret, domain):
    """Constructor for the GroupsQuickStartExample object.

    Takes a client_id, client_secret and domain needed to create an object for
    groups provisioning.

    Args:
      client_id: [string] The clientId of the developer.
      client_secret: [string] The clientSecret of the developer.
      domain: [string] The domain on which the functions are to be performed.
    """
    self.client_id = client_id
    self.client_secret = client_secret
    self.domain = domain

  def CreateGroupsClient(self):
    """Creates a groups provisioning client using OAuth2.0 flow."""
    token = gdata.gauth.OAuth2Token(
        client_id=self.client_id, client_secret=self.client_secret,
        scope=SCOPE, user_agent=USER_AGENT)
    uri = token.generate_authorize_url()
    print 'Please visit this URL to authorize the application:'
    print uri
    # Get the verification code from the standard input.
    code = raw_input('What is the verification code? ').strip()
    token.get_access_token(code)
    self.groups_client = gdata.apps.groups.client.GroupsProvisioningClient(
        domain=self.domain, auth_token=token)

  def _GetValidGroupId(self):
    """Takes a valid group email address as input.

    Return:
      group_id: [string] a valid group email address
    """
    group_id = ''
    while not group_id:
      group_id = raw_input('Enter a valid group email address'
                           '(group@domain.com): ')
    return group_id

  def _GetValidMemberId(self):
    """Takes a valid member email address as input.

    Return:
      member_id: [string] a valid member email address
    """
    member_id = ''
    while not member_id:
      member_id = raw_input('Enter a valid member email address'
                            '(username@domain.com): ')
    return member_id

  def _PrintGroupDetails(self, group_entry):
    """Print all the details of a group.

    Args:
      group_entry: [GroupEntry] contains all the data about the group.
    """
    print 'Group ID: ' + group_entry.group_id
    print 'Group Name: ' + group_entry.group_name
    print 'Description: ' + group_entry.description
    print 'Email Permissions: ' + group_entry.email_permission
    print ''

  def _PrintMemberDetails(self, member_entry):
    """Print all the details of a group member.

    Args:
      member_entry: [GroupMemberEntry] contains all the data about the group member.
    """
    print 'Member ID: ' + member_entry.member_id
    print 'Member Type: ' + member_entry.member_type
    print 'Is Direct Member: ' + member_entry.direct_member
    print ''

  def _TakeGroupData(self, function='create'):
    """Takes input data for _UpdateGroup and _CreateGroup functions.

    Args:
      function: [string] representing the kind of function (create/update)
          from where this function was called.

    Return:
      group_data: [gdata.apps.groups.data.GroupEntry] All data for a group.
    """
    email_permission_options = ['Owner', 'Member', 'Domain', 'Anyone']
    extra_stmt = ''
    if function == 'update':
      extra_stmt = '. Press enter to not update the field'
    group_data = gdata.apps.groups.data.GroupEntry()
    group_data.group_id = self._GetValidGroupId()
    while not group_data.group_name:
      group_data.group_name = raw_input('Enter name for the group%s: '
                                        % extra_stmt)
      if function == 'update':
        break
    group_data.description = raw_input('Enter description for the group%s: '
                                       % extra_stmt)

    print ('Choose an option for email permission%s:'
           % extra_stmt)
    i = 1
    for option in email_permission_options:
      print '%d - %s' % (i, option)
      i += 1
    choice = (raw_input())
    if not choice:
      choice = -1
    choice = int(choice)
    if choice > 0 and choice <= len(email_permission_options):
      group_data.email_permission = email_permission_options[choice-1]

    return group_data

  def _CreateGroup(self):
    """Creates a new group."""
    group_data = self._TakeGroupData()
    self.groups_client.CreateGroup(group_data.group_id,
                                   group_data.group_name,
                                   group_data.description,
                                   group_data.email_permission)

  def _UpdateGroup(self):
    """Updates an existing group."""
    group_data = self._TakeGroupData(function='update')
    group_entry = self.groups_client.RetrieveGroup(group_data.group_id)
    if group_data.group_name:
      group_entry.group_name = group_data.group_name
    if group_data.description:
      group_entry.description = group_data.description
    if group_data.email_permission:
      group_entry.email_permission = group_data.email_permission

    self.groups_client.UpdateGroup(group_data.GetGroupId(), group_entry)

  def _RetrieveSingleGroup(self):
    """Retrieves a single group."""
    group_id = self._GetValidGroupId()
    group_entry = self.groups_client.RetrieveGroup(group_id)
    self._PrintGroupDetails(group_entry)

  def _RetrieveAllGroupsForMember(self):
    """Retrieves all the groups the user is a member of."""
    member_id = self._GetValidMemberId()
    direct_only = raw_input('Write true/false for direct_only: ')
    if direct_only == 'true':
      direct_only = True
    else:
      direct_only = False
    groups_feed = self.groups_client.RetrieveGroups(member_id, direct_only)
    for entry in groups_feed.entry:
      self._PrintGroupDetails(entry)

  def _RetrieveAllGroups(self):
    """Retrieves all the groups in a domain."""
    groups_feed = self.groups_client.RetrieveAllGroups()
    for entry in groups_feed.entry:
      self._PrintGroupDetails(entry)

  def _DeleteGroup(self):
    """Delete a group."""
    group_id = self._GetValidGroupId()
    self.groups_client.DeleteGroup(group_id)

  def _AddMemberToGroup(self):
    """Add a member to a particular group."""
    group_id = self._GetValidGroupId()
    member_id = self._GetValidMemberId()
    self.groups_client.AddMemberToGroup(group_id, member_id)

  def _RetrieveSingleMember(self):
    """Retrieve a single member from a group."""
    group_id = self._GetValidGroupId()
    member_id = self._GetValidMemberId()
    member_entry = self.groups_client.RetrieveGroupMember(group_id, member_id)
    self._PrintMemberDetails(member_entry)

  def _RetrieveAllMembersOfGroup(self):
    """Retrieve all the members of a group."""
    group_id = self._GetValidGroupId()
    members_feed = self.groups_client.RetrieveAllMembers(group_id)
    for entry in members_feed.entry:
      self._PrintMemberDetails(entry)

  def _RemoveMemberFromGroup(self):
    """Remove a member from a group."""
    group_id = self._GetValidGroupId()
    member_id = self._GetValidMemberId()
    self.groups_client.RemoveMemberFromGroup(group_id, member_id)

  def Run(self):
    """Runs the sample by getting user input and takin appropriate action."""
    #List of all the function and there description
    functions_list = [
        {'function': self._CreateGroup,
         'description': 'Create a Group'},
        {'function': self._UpdateGroup,
         'description': 'Updating a Group'},
        {'function': self._RetrieveSingleGroup,
         'description': 'Retrieve a single Group'},
        {'function': self._RetrieveAllGroupsForMember,
         'description': 'Retrieve all Groups for a member'},
        {'function': self._RetrieveAllGroups,
         'description': 'Retrieve all Groups in a domain'},
        {'function': self._DeleteGroup,
         'description': 'Deleting a Group from a domain'},
        {'function': self._AddMemberToGroup,
         'description': 'Add a member to a Group'},
        {'function': self._RetrieveSingleMember,
         'description': 'Retrieve a member of a group'},
        {'function': self._RetrieveAllMembersOfGroup,
         'description': 'Retrieve all members of a group'},
        {'function': self._RemoveMemberFromGroup,
         'description': 'Delete a member from a Group'}
    ]

    while True:
      print 'Choose an option:\n0 - to exit'
      for i in range (0, len(functions_list)):
        print '%d - %s' % ((i+1), functions_list[i]['description'])
      choice = int(raw_input())
      if choice == 0:
        break
      if choice < 0 or choice > len(functions_list):
        print 'Not a valid option!'
        continue
      functions_list[choice-1]['function']()


def main():
  """Runs the sample using an instance of GroupsQuickStartExample."""
  # Parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['client_id=',
                                                  'client_secret=',
                                                  'domain='])
  except getopt.error, msg:
    print ('python groups_provisioning_quick_start_example.py'
           ' --client_id [clientId] --client_secret [clientSecret]'
           ' --domain [domain]')
    sys.exit(2)

  client_id = ''
  client_secret = ''
  domain = ''
  # Parse options
  for option, arg in opts:
    if option == '--client_id':
      client_id = arg
    elif option == '--client_secret':
      client_secret = arg
    elif option == '--domain':
      domain = arg

  while not client_id:
    client_id = raw_input('Please enter a clientId: ')
  while not client_secret:
    client_secret = raw_input('Please enter a clientSecret: ')
  while not domain:
    domain = raw_input('Please enter domain name (example.com): ')

  try:
    groups_quick_start_example = GroupsQuickStartExample(
        client_id, client_secret, domain)
  except gdata.service.BadAuthentication:
    print 'Invalid user credentials given.'
    return

  groups_quick_start_example.CreateGroupsClient()
  groups_quick_start_example.Run()


if __name__ == '__main__':
  main()
