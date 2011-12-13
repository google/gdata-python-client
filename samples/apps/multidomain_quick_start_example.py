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
import getpass
import sys
import gdata.apps.multidomain.client

SCOPE = 'https://apps-apis.google.com/a/feeds/user/'
USER_AGENT = 'MultiDomainQuickStartExample'


class UserData(object):
  """Data corresponding to a single user."""

  def __init__(self):
    self.email = ''
    self.first_name = ''
    self.last_name = ''
    self.password = ''
    self.confirm_password = 'temp'
    self.is_admin = ''
    self.hash_function = ''
    self.suspended = ''
    self.change_password = ''
    self.ip_whitelisted = ''
    self.quota = ''


class MultiDomainQuickStartExample(object):
  """Demonstrates all the functions of multidomain user provisioning."""

  def __init__(self, client_id, client_secret, domain):
    """Constructor for the MultiDomainQuickStartExample object.

    Takes a client_id, client_secret and domain to create an object for
    multidomain user provisioning.

    Args:
      client_id: [string] The clientId of the developer.
      client_secret: [string] The clientSecret of the developer.
      domain: [string] The domain on which the functions are to be performed.
    """
    self.client_id = client_id
    self.client_secret = client_secret
    self.domain = domain
    token = gdata.gauth.OAuth2Token(
        client_id=self.client_id, client_secret=self.client_secret,
        scope=SCOPE, user_agent=USER_AGENT)
    uri = token.generate_authorize_url()
    print 'Please visit this URL to authorize the application:'
    print uri
    # Get the verification code from the standard input.
    code = raw_input('What is the verification code? ').strip()
    token.get_access_token(code)
    self.multidomain_client = (
        gdata.apps.multidomain.client.MultiDomainProvisioningClient(
            domain=self.domain, auth_token=token))

  def _PrintUserDetails(self, entry):
    """Prints all the information for a user entry.

       Args:
         entry: [UserEntry] User entry corresponding to a user
    """

    print 'First Name: %s' % (entry.first_name)
    print 'Last Name: %s' % (entry.last_name)
    print 'Email: %s' % (entry.email)
    print 'Is Admin: %s' % (entry.is_admin)
    print 'Is Suspended: %s' % (entry.suspended)
    print 'Change password at next login: %s' % (
        entry.change_password_at_next_login)
    print '\n'

  def _PrintAliasDetails(self, entry):
    """Prints all the information for a user alias entry.

    Args:
      entry: [AliasEntry] Alias entry correspoding to an alias
    """

    print 'User Email: %s' % (entry.user_email)
    print 'Alias Email: %s' % (entry.alias_email)
    print '\n'

  def _GetChoice(self, for_field):
    """Gets a choice for a field.

    Args:
      for_field: [string] The field for which input is to be taken.

    Return:
      True/False/None: Depending on the choice made by the user.
    """
    choice = int(raw_input(('Enter a choice for %s\n'
                            '1-True 2-False 3-Default/Skip: ') % (for_field)))
    if choice == 1:
      return True
    elif choice == 2:
      return False
    return None

  def _TakeUserData(self, function='create'):
    """Takes input data for _UpdateUser and _CreateUser functions.

    Args:
      function: [string] representing the kind of function (create/update)
          from where this function was called.

    Return:
      user_data: [UserData] All data for a user.
    """
    extra_stmt = ''
    if function == 'update':
      extra_stmt = '. Press enter to not update the field'
    user_data = UserData()
    while not user_data.email:
      user_data.email = raw_input('Enter a valid email address'
                                  '(username@domain.com): ')
    while not user_data.first_name:
      user_data.first_name = raw_input(('Enter first name for the user%s: ')
                                       % (extra_stmt))
      if function == 'update':
        break
    while not user_data.last_name:
      user_data.last_name = raw_input(('Enter last name for the user%s: ')
                                      % (extra_stmt))
      if function == 'update':
        break
    while not user_data.password == user_data.confirm_password:
      user_data.password = ''
      while not user_data.password:
        sys.stdout.write(('Enter password for the user%s: ')
                         % (extra_stmt))
        user_data.password = getpass.getpass()
        if function == 'update' and user_data.password.__len__() == 0:
          break
        if user_data.password.__len__() < 8:
          print 'Password must be at least 8 characters long'
          user_data.password = ''
      if function == 'update' and user_data.password.__len__() == 0:
        break
      sys.stdout.write('Confirm password: ')
      user_data.confirm_password = getpass.getpass()

    user_data.is_admin = self._GetChoice('is_admin')
    user_data.hash_function = raw_input('Enter a hash function or None: ')
    user_data.suspended = self._GetChoice('suspended')
    user_data.change_password = self._GetChoice('change_password')
    user_data.ip_whitelisted = self._GetChoice('ip_whitelisted')
    user_data.quota = raw_input('Enter a quota or None: ')

    if user_data.quota == 'None' or not user_data.quota.isdigit():
      user_data.quota = None
    if user_data.hash_function == 'None':
      user_data.hash_function = None
    return user_data

  def _CreateUser(self):
    """Creates a new user account."""

    user_data = self._TakeUserData()
    self.multidomain_client.CreateUser(
        user_data.email, user_data.first_name, user_data.last_name,
        user_data.password, user_data.is_admin,
        hash_function=user_data.hash_function, suspended=user_data.suspended,
        change_password=user_data.change_password,
        ip_whitelisted=user_data.ip_whitelisted, quota=user_data.quota)

  def _UpdateUser(self):
    """Updates a user."""

    user_data = self._TakeUserData('update')
    user_entry = self.multidomain_client.RetrieveUser(user_data.email)
    if user_data.first_name:
      user_entry.first_name = user_data.first_name
    if user_data.last_name:
      user_entry.last_name = user_data.last_name
    if user_data.password:
      user_entry.password = user_data.password
    if not user_data.hash_function is None:
      user_entry.hash_function = user_data.hash_function
    if not user_data.quota is None:
      user_entry.quota = user_entry.quota
    if not user_data.is_admin is None:
      user_entry.is_admin = (str(user_data.is_admin)).lower()
    if not user_data.suspended is None:
      user_entry.suspended = (str(user_data.suspended)).lower()
    if not user_data.change_password is None:
      user_entry.change_password = (str(user_data.change_password)).lower()
    if not user_data.ip_whitelisted is None:
      user_entry.ip_whitelisted = (str(user_data.ip_whitelisted)).lower()

    self.multidomain_client.UpdateUser(user_data.email, user_entry)

  def _RenameUser(self):
    """Renames username of a user."""

    old_email = ''
    new_email = ''
    while not old_email:
      old_email = raw_input('Enter old email address(username@domain.com): ')
    while not new_email:
      new_email = raw_input('Enter new email address(username@domain.com): ')

    self.multidomain_client.RenameUser(old_email, new_email)

  def _RetrieveSingleUser(self):
    """Retrieves a single user."""

    email = ''
    while not email:
      email = raw_input('Enter a valid email address(username@domain.com): ')

    response = self.multidomain_client.RetrieveUser(email)
    self._PrintUserDetails(response)

  def _RetrieveAllUsers(self):
    """Retrieves all users from all the domains."""

    response = self.multidomain_client.RetrieveAllUsers()
    for entry in response.entry:
      self._PrintUserDetails(entry)

  def _DeleteUser(self):
    """Deletes a user."""

    email = ''
    while not email:
      email = raw_input('Enter a valid email address(username@domain.com): ')

    self.multidomain_client.DeleteUser(email)

  def _CreateUserAlias(self):
    """Creates a user alias."""

    email = ''
    alias = ''
    while not email:
      email = raw_input('Enter a valid email address(username@domain.com): ')
    while not alias:
      alias = raw_input('Enter a valid alias email address'
                        '(username@domain.com): ')
    self.multidomain_client.CreateAlias(email, alias)

  def _RetrieveAlias(self):
    """Retrieves a user corresponding to an alias."""

    alias = ''
    while not alias:
      alias = raw_input('Enter a valid alias email address'
                        '(username@domain.com): ')
    response = self.multidomain_client.RetrieveAlias(alias)
    self._PrintAliasDetails(response)

  def _RetrieveAllAliases(self):
    """Retrieves all user aliases for all users."""

    response = self.multidomain_client.RetrieveAllAliases()
    for entry in response.entry:
      self._PrintAliasDetails(entry)

  def _RetrieveAllUserAliases(self):
    """Retrieves all user aliases of a user."""

    email = ''
    while not email:
      email = raw_input('Enter a valid email address(username@domain.com): ')
    response = self.multidomain_client.RetrieveAllUserAliases(email)
    for entry in response.entry:
      self._PrintAliasDetails(entry)

  def _DeleteAlias(self):
    """Deletes a user alias."""

    alias = ''
    while not alias:
      alias = raw_input('Enter a valid alias email address'
                        '(username@domain.com): ')
    self.multidomain_client.DeleteAlias(alias)

  def Run(self):
    """Runs the sample by getting user input and takin appropriate action."""

    #List of all the function and there description
    functions_list = [
        {'function': self._CreateUser,
         'description': 'Create a user'},
        {'function': self._UpdateUser,
         'description': 'Updating a user'},
        {'function': self._RenameUser,
         'description': 'Renaming a user'},
        {'function': self._RetrieveSingleUser,
         'description': 'Retrieve a single user'},
        {'function': self._RetrieveAllUsers,
         'description': 'Retrieve all users in all domains'},
        {'function': self._DeleteUser,
         'description': 'Deleting a User from a domain'},
        {'function': self._CreateUserAlias,
         'description': 'Create a User Alias in a domain'},
        {'function': self._RetrieveAlias,
         'description': 'Retrieve a User Alias in a domain'},
        {'function': self._RetrieveAllAliases,
         'description': 'Retrieve all User Aliases in a Domain'},
        {'function': self._RetrieveAllUserAliases,
         'description': 'Retrieve all User Aliases for a User'},
        {'function': self._DeleteAlias,
         'description': 'Delete a user alias from a domain'}
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
  """Runs the sample using an instance of MultiDomainQuickStartExample."""

  # Parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['client_id=',
                                                  'client_secret=',
                                                  'domain='])
  except getopt.error, msg:
    print ('python multidomain_provisioning_quick_start_example.py'
           '--client_id [clientId] --client_secret [clientSecret]'
           '--domain [domain]')
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
    multidomain_quick_start_example = MultiDomainQuickStartExample(
        client_id, client_secret, domain)
  except gdata.service.BadAuthentication:
    print 'Invalid user credentials given.'
    return

  multidomain_quick_start_example.Run()


if __name__ == '__main__':
  main()
