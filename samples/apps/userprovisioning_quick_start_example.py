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

"""Sample for the User Provisioning API to demonstrate all methods.

Usage:
  $ python userprovisioning_quick_start_example.py

You can also specify the  user credentials from the command-line

  $ python userprovisioning_quick_start_example.py
    --client_id [client_id] --client_secret [client_scret] --domain [domain]

You can get help for command-line arguments as

  $ python userprovisioning_quick_start_example.py --help
"""

__author__ = 'Shraddha Gupta <shraddhag@google.com>'

import getopt
import getpass
import sys
import gdata.apps.client

SCOPE = 'https://apps-apis.google.com/a/feeds/user/'
USER_AGENT = 'UserProvisioningQuickStartExample'


class UserProvisioning(object):
  """Demonstrates all the functions of user provisioning."""

  def __init__(self, client_id, client_secret, domain):
    """
    Args:
      client_id: [string] The clientId of the developer.
      client_secret: [string] The clientSecret of the developer.
      domain: [string] The domain on which the functions are to be performed.
    """
    self.client_id = client_id
    self.client_secret = client_secret
    self.domain = domain

  def _AuthorizeClient(self):
    """Authorize the client for making API requests."""

    self.token = gdata.gauth.OAuth2Token(
        client_id=self.client_id, client_secret=self.client_secret,
        scope=SCOPE, user_agent=USER_AGENT)
    uri = self.token.generate_authorize_url()
    print 'Please visit this URL to authorize the application:'
    print uri
    # Get the verification code from the standard input.
    code = raw_input('What is the verification code? ').strip()
    self.token.get_access_token(code)
    self.client = gdata.apps.client.AppsClient(
        domain=self.domain, auth_token=self.token)

  def _PrintUserDetails(self, entry):
    """Prints the attributes for a user entry.

    Args:
      entry: [UserEntry] User entry corresponding to a user
    """
    print '\nGiven Name: %s' % (entry.name.given_name)
    print 'Family Name: %s' % (entry.name.family_name)
    print 'Username: %s' % (entry.login.user_name)
    print 'Is Admin: %s' % (entry.login.admin)
    print 'Is Suspended: %s' % (entry.login.suspended)
    print 'Change password at next login: %s\n' % (
        entry.login.change_password)

  def _PrintNicknameDetails(self, entry):
    """Prints the attributes for a user nickname entry.

    Args:
      entry: [NicknameEntry]
    """
    print 'Username: %s' % (entry.login.user_name)
    print 'Nickname: %s\n' % (entry.nickname.name)

  def _GetChoice(self, for_value):
    choice = raw_input(('(Optional) Enter a choice for %s\n'
                        '1-True 2-False ') % (for_value))
    if choice == '1':
      return True
    return False

  def _CreateUser(self):
    """Creates a new user account."""

    user_name = given_name = family_name = password = None
    confirm_password = ''
    while not user_name:
      user_name = raw_input('Enter a new username: ')
    while not given_name:
      given_name = raw_input('Enter given name for the user: ')
    while not family_name:
      family_name = raw_input('Enter family name for the user: ')
    while not password == confirm_password:
      password = ''
      while not password:
        sys.stdout.write('Enter password for the user: ')
        password = getpass.getpass()
        if password.__len__() == 0:
          break
        if password.__len__() < 8:
          print 'Password must be at least 8 characters long'
          password = ''
      sys.stdout.write('Confirm password: ')
      confirm_password = getpass.getpass()

    is_admin = self._GetChoice('is_admin ')
    hash_function = raw_input('(Optional) Enter a hash function ')
    suspended = self._GetChoice('suspended ')
    change_password = self._GetChoice('change_password ')
    quota = raw_input('(Optional) Enter a quota ')

    if quota == 'None' or not quota.isdigit():
      quota = None
    user_entry = self.client.CreateUser(
        user_name=user_name, given_name=given_name, family_name=family_name,
        password=password, admin=is_admin, suspended=suspended,
        password_hash_function=hash_function,
        change_password=change_password)
    self._PrintUserDetails(user_entry)
    print 'User Created'

  def _UpdateUser(self):
    """Updates a user."""

    user_name = raw_input('Enter the username ')
    if user_name is None:
      print 'Username missing\n'
      return
    user_entry = self.client.RetrieveUser(user_name=user_name)
    print self._PrintUserDetails(user_entry)

    attributes = {1: 'given_name', 2: 'family_name', 3: 'user_name',
                  4: 'suspended', 5: 'is_admin'}
    print attributes
    attr = int(raw_input('\nEnter number(1-5) of attribute to be updated '))

    updated_val = raw_input('Enter updated value ')
    if attr == 1:
      user_entry.name.given_name = updated_val
    if attr == 2:
      user_entry.name.family_name = updated_val
    if attr == 3:
      user_entry.login.user_name = updated_val
    if attr == 4:
      user_entry.login.suspended = updated_val
    if attr == 5:
      user_entry.login.admin = updated_val

    updated = self.client.UpdateUser(user_entry.login.user_name, user_entry)
    self._PrintUserDetails(updated)

  def _RetrieveSingleUser(self):
    """Retrieves a single user."""

    user_name = raw_input('Enter the username ')
    if user_name is None:
      print 'Username missing\n'
      return
    response = self.client.RetrieveUser(user_name=user_name)
    self._PrintUserDetails(response)

  def _RetrieveAllUsers(self):
    """Retrieves all users from all the domains."""

    response = self.client.RetrieveAllUsers()
    for entry in response.entry:
      self._PrintUserDetails(entry)

  def _DeleteUser(self):
    """Deletes a user."""

    user_name = raw_input('Enter the username ')
    if user_name is None:
      print 'Username missing\n'
      return

    self.client.DeleteUser(user_name=user_name)
    print 'User Deleted'

  def _CreateNickname(self):
    """Creates a user alias."""

    user_name = raw_input('Enter the username ')
    nickname = raw_input('Enter a nickname for user ')
    if None in (user_name, nickname):
      print 'Username/Nickname missing\n'
      return
    nickname = self.client.CreateNickname(
        user_name=user_name, nickname=nickname)
    print nickname
    print 'Nickname Created'

  def _RetrieveNickname(self):
    """Retrieves a nickname entry."""

    nickname = raw_input('Enter the username ')
    if nickname is None:
      print 'Nickname missing\n'
      return
    response = self.client.RetrieveNickname(nickname=nickname)
    self._PrintNicknameDetails(response)

  def _RetrieveUserNicknames(self):
    """Retrieves all nicknames of a user."""

    user_name = raw_input('Enter the username ')
    if user_name is None:
      print 'Username missing\n'
      return
    response = self.client.RetrieveNicknames(user_name=user_name)
    for entry in response.entry:
      self._PrintNicknameDetails(entry)

  def _DeleteNickname(self):
    """Deletes a nickname."""

    nickname = raw_input('Enter the username ')
    if nickname is None:
      print 'Nickname missing\n'
      return
    self.client.DeleteNickname(nickname=nickname)
    print 'Nickname deleted'

  def Run(self):
    """Runs the sample by getting user input and taking appropriate action."""

    # List of all the functions and their descriptions
    functions_list = [
        {'function': self._CreateUser,
         'description': 'Create a user'},
        {'function': self._UpdateUser,
         'description': 'Update a user'},
        {'function': self._RetrieveSingleUser,
         'description': 'Retrieve a single user'},
        {'function': self._RetrieveAllUsers,
         'description': 'Retrieve all users'},
        {'function': self._DeleteUser,
         'description': 'Delete a user'},
        {'function': self._CreateNickname,
         'description': 'Create a nickname'},
        {'function': self._RetrieveNickname,
         'description': 'Retrieve a nickname'},
        {'function': self._RetrieveUserNicknames,
         'description': 'Retrieve all nicknames for a user'},
        {'function': self._DeleteNickname,
         'description': 'Delete a nickname'}
    ]
    self._AuthorizeClient()
    while True:
      print '\nChoose an option:\n0 - to exit'
      for i in range (0, len(functions_list)):
        print '%d - %s' % ((i+1), functions_list[i]['description'])
      choice = int(raw_input())
      if choice == 0:
        break
      if choice < 0 or choice > 11:
        print 'Not a valid option!'
        continue
      functions_list[choice-1]['function']()


def main():
  """A menu driven application to demo all methods of user provisioning."""

  usage = ('python userprovisioning_quick_start_example.py '
           '--client_id [clientId] --client_secret [clientSecret] '
           '--domain [domain]')
  # Parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['client_id=',
                                                  'client_secret=',
                                                  'domain='])
  except getopt.error, msg:
    print 'Usage: %s' % usage
    return

  client_id = None
  client_secret = None
  domain = None
  # Parse options
  for option, arg in opts:
    if option == '--client_id':
      client_id = arg
    elif option == '--client_secret':
      client_secret = arg
    elif option == '--domain':
      domain = arg

  if None in (client_id, client_secret, domain):
    print 'Usage: %s' % usage
    return

  try:
    user_provisioning = UserProvisioning(client_id, client_secret, domain)
  except gdata.service.BadAuthentication:
    print 'Invalid user credentials given.'
    return

  user_provisioning.Run()


if __name__ == '__main__':
  main()
