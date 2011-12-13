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

"""Sample for the Orgunits Provisioning API to demonstrate all methods.

Usage:
  $ python orgunit_quick_start_example.py

You can also specify the  user credentials from the command-line

  $ python orgunit_quick_start_example.py
    --client_id [client_id] --client_secret [client_scret] --domain [domain]

You can get help for command-line arguments as

  $ python orgunit_quick_start_example.py --help
"""

__author__ = 'Shraddha Gupta <shraddhag@google.com>'

import getopt
import sys
import gdata.apps.client
from gdata.apps.organization.client import OrganizationUnitProvisioningClient
import gdata.client
import gdata.gauth

SCOPE = 'https://apps-apis.google.com/a/feeds/policies/'
USER_AGENT = 'OrgUnitProvisioningQuickStartExample'


class OrgUnitProvisioning(object):
  """Demonstrates all the functions of org units provisioning."""

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
    self.client = OrganizationUnitProvisioningClient(
        domain=self.domain, auth_token=self.token)

  def _PrintCustomerIdDetails(self, entry):
    """Prints the attributes for a CustomerIdEntry.

    Args:
      entry: [gdata.apps.organization.data.CustomerIdEntry]
    """
    print '\nCustomer Id: %s' % (entry.customer_id)
    print 'Org unit name: %s' % (entry.org_unit_name)
    print 'Customer org unit name: %s' % (entry.customer_org_unit_name)
    print 'Org unit description: %s' % (entry.org_unit_description)
    print 'Customer org unit description: %s' % (
        entry.customer_org_unit_description)

  def _PrintOrgUnitDetails(self, entry):
    """Prints the attributes for a OrgUnitEntry.

    Args:
      entry: [gdata.apps.organization.data.OrgUnitEntry]
    """
    if entry:
      print '\nOrg unit name: %s' % (entry.org_unit_name)
      print 'Org unit path: %s' % (entry.org_unit_path)
      print 'Parent org unit path: %s' % (entry.parent_org_unit_path)
      print 'organization unit description: %s' % (entry.org_unit_description)
      print 'Block inheritance flag: %s' % (entry.org_unit_block_inheritance)
    else:
      print 'null entry'

  def _PrintOrgUserDetails(self, entry):
    """Prints the attributes for a OrgUserEntry.

    Args:
      entry: [gdata.apps.organization.data.OrgUserEntry]
    """
    if entry:
      print 'Org user email: %s' % (entry.user_email)
      print 'Org unit path: %s' % (entry.org_unit_path)
    else:
      print 'null entry'

  def _GetChoice(self, for_field):
    """Gets input for boolean fields.
    
    Args:
      for_value : string field for which input is required

    Returns:
      boolean input for the given field
    """
    choice = raw_input(('(Optional) Enter a choice for %s\n'
                        '1-True 2-False ') % (for_field))
    if choice == '1':
      return True
    return False

  def _GetOrgUnitPath(self):
    """Gets org_unit_path from user.

    Returns:
      string org_unit_path entered by the user
    """

    org_unit_path = raw_input('Enter the org unit path ')
    if org_unit_path is None:
      print 'Organization path missing\n'
      return
    return org_unit_path

  def _RetrieveCustomerId(self):
    """Retrieves Groups Apps account customerId.

    Returns:
      CustomerIdEntry
    """

    response = self.client.RetrieveCustomerId()
    self._PrintCustomerIdDetails(response)
    return response

  def _CreateOrgUnit(self, customer_id):
    """Creates a new org unit.
    
    Args:
      customer_id : string customer_id of organization
    """
    name = raw_input('Enter a name for organization: ')
    parent_org_unit_path = raw_input('(default "/")'
        'Enter full path of the parentental tree: ')
    description = raw_input('(Optional) Enter description of organization: ')
    block_inheritance = self._GetChoice('(default: False) block_inheritance: ')
    if not parent_org_unit_path:
      parent_org_unit_path = '/'
    try:
      orgunit_entry = self.client.CreateOrgUnit(
          customer_id=customer_id, name=name,
          parent_org_unit_path=parent_org_unit_path,
          description=description, block_inheritance=block_inheritance)
      self._PrintOrgUnitDetails(orgunit_entry)
      print 'Org unit Created'
    except gdata.client.RequestError, e:
      print e.reason, e.body
      return

  def _UpdateOrgUnit(self, customer_id):
    """Updates an org unit.
    
    Args:
      customer_id : string customer_id of organization
    """
    org_unit_path = self._GetOrgUnitPath()
    if org_unit_path is None:
      return
    try:
      org_unit_entry = self.client.RetrieveOrgUnit(customer_id=customer_id,
          org_unit_path=org_unit_path)
      print self._PrintOrgUnitDetails(org_unit_entry)
      attributes = {1: 'org_name', 2: 'parent_org_unit_path', 3: 'description',
                    4: 'block_inheritance'}
      print attributes
      while True:
        attr = int(raw_input('\nEnter number(1-4) of attribute to be updated'))
        updated_val = raw_input('Enter updated value ')
        if attr == 1:
          org_unit_entry.org_unit_name = updated_val
        if attr == 2:
          org_unit_entry.parent_org_unit_path = updated_val
        if attr == 3:
          org_unit_entry.org_unit_description = updated_val
        if attr == 4:
          org_unit_entry.login.org_unit_block_inheritance = updated_val
        choice = raw_input('\nDo you want to update more attributes y/n')
        if choice != 'y':
          break
      self.client.UpdateOrgUnit(customer_id=customer_id,
          org_unit_path=org_unit_path, org_unit_entry=org_unit_entry)
      print 'Updated Org unit'
    except gdata.client.RequestError, e:
      print e.reason, e.body
      return

  def _RetrieveOrgUnit(self, customer_id):
    """Retrieves a single org unit.
    
    Args:
      customer_id : string customer_id of organization
    """
    org_unit_path = self._GetOrgUnitPath()
    if org_unit_path is None:
      return
    try:
      response = self.client.RetrieveOrgUnit(customer_id=customer_id,
          org_unit_path=org_unit_path)
      self._PrintOrgUnitDetails(response)
    except gdata.client.RequestError, e:
      print e.reason, e.body
      return

  def _RetrieveAllOrgUnits(self, customer_id):
    """Retrieves all org units.
    
    Args:
      customer_id : string customer_id of organization
    """    
    try:
      response = self.client.RetrieveAllOrgUnits(customer_id=customer_id)
      for entry in response.entry:
        self._PrintOrgUnitDetails(entry)
    except gdata.client.RequestError, e:
      print e.reason, e.body
      return

  def _RetrieveSubOrgUnits(self, customer_id):
    """Retrieves all sub org units of an org unit.
    
    Args:
      customer_id : string customer_id of organization
    """
    org_unit_path = self._GetOrgUnitPath()
    if org_unit_path is None:
      return
    try:
      response = self.client.RetrieveSubOrgUnits(customer_id=customer_id,
          org_unit_path=org_unit_path)
      if not response.entry:
        print 'No Sub organization units'
        return
      for entry in response.entry:
        self._PrintOrgUnitDetails(entry)
    except gdata.client.RequestError, e:
      print e.reason, e.body
      return

  def _MoveUsers(self, customer_id):
    """Moves users to an org unit.
    
    Args:
      customer_id : string customer_id of organization
    """
    org_unit_path = self._GetOrgUnitPath()
    if org_unit_path is None:
      return
    users = []
    while True:
      user = raw_input('Enter user email address ')
      if user:
        users.append(user)
      else:
        break
    if users is None:
      print 'No users given to move'
      return
    try:
      self.client.MoveUserToOrgUnit(customer_id=customer_id,
          org_unit_path=org_unit_path, users_to_move=users)
      print 'Moved users'
      print users
    except gdata.client.RequestError, e:
      print e.reason, e.body
      return

  def _DeleteOrgUnit(self, customer_id):
    """Deletes an org unit.
    
    Args:
      customer_id : string customer_id of organization
    """
    org_unit_path = self._GetOrgUnitPath()
    if org_unit_path is None:
      return
    try:
      self.client.DeleteOrgUnit(customer_id=customer_id,
          org_unit_path=org_unit_path)
      print 'OrgUnit Deleted'
    except gdata.client.RequestError, e:
      print e.reason, e.body
      return

  def _UpdateOrgUser(self, customer_id):
    """Updates the orgunit of an org user.
    
    Args:
      customer_id : string customer_id of organization
    """
    org_unit_path = self._GetOrgUnitPath()
    user_email = raw_input('Enter the email address')
    if None in (org_unit_path, user_email):
      print 'Organization path and email are both required\n'
      return
    try:
      org_user_entry = self.client.UpdateOrgUser(customer_id=customer_id,
          user_email=user_email, org_unit_path=org_unit_path)
      print 'Updated org unit for user'
      print self._PrintOrgUserDetails(org_user_entry)
    except gdata.client.RequestError, e:
      print e.reason, e.body
      return

  def _RetrieveOrgUser(self, customer_id):
    """Retrieves an organization user.
    
    Args:
      customer_id : string customer_id of organization
    """
    user_email = raw_input('Enter the email address ')
    if user_email is None:
      print 'Email address missing\n'
      return
    try:
      response = self.client.RetrieveOrgUser(customer_id=customer_id,
          user_email=user_email)
      self._PrintOrgUserDetails(response)
    except gdata.client.RequestError, e:
      print e.reason, e.body
      return

  def _RetrieveOrgUnitUsers(self, customer_id):
    """Retrieves all org users of an org unit.
    
    Args:
      customer_id : string customer_id of organization
    """
    org_unit_path = self._GetOrgUnitPath()
    if org_unit_path is None:
      return
    try:
      response = self.client.RetrieveOrgUnitUsers(customer_id=customer_id,
          org_unit_path=org_unit_path)
      if not response.entry:
        print 'No users in this organization'
        return
      for entry in response.entry:
        self._PrintOrgUserDetails(entry)
    except gdata.client.RequestError, e:
      print e.reason, e.body
      return

  def _RetrieveAllOrgUsers(self, customer_id):
    """Retrieves all org users.
    
    Args:
      customer_id : string customer_id of organization
    """
    try:
      response = self.client.RetrieveAllOrgUsers(customer_id=customer_id)
      for entry in response.entry:
        self._PrintOrgUserDetails(entry)
    except gdata.client.RequestError, e:
      print e.reason, e.body
      return

  def Run(self):
    """Runs the sample by getting user input and taking appropriate action."""

    self._AuthorizeClient()
    # CustomerId is required to perform any opertaion on org unit
    # Retrieve customerId beforehand.
    customer_id_entry = self._RetrieveCustomerId()
    customer_id = customer_id_entry.customer_id

    # List of all the functions and their descriptions
    functions_list = [
        {'function': self._CreateOrgUnit,
         'description': 'Create an org unit'},
        {'function': self._UpdateOrgUnit,
         'description': 'Update an org unit'},
        {'function': self._RetrieveOrgUnit,
         'description': 'Retrieve an org unit'},
        {'function': self._RetrieveAllOrgUnits,
         'description': 'Retrieve all org units'},
        {'function': self._RetrieveSubOrgUnits,
         'description': 'Retrieve sub org unit of a given org unit'},
        {'function': self._MoveUsers,
         'description': 'Move users to an org unit'},
        {'function': self._DeleteOrgUnit,
         'description': 'Delete an org unit'},
        {'function': self._UpdateOrgUser,
         'description': 'Update org unit of a user'},
        {'function': self._RetrieveOrgUser,
         'description': 'Retrieve an org user '},
        {'function': self._RetrieveOrgUnitUsers,
         'description': 'Retrieve users of an org unit'},
        {'function': self._RetrieveAllOrgUsers,
         'description': 'Retrieve all org users'}
    ]
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
      functions_list[choice-1]['function'](customer_id=customer_id)


def main():
  """A menu driven application to demo all methods of org unit provisioning."""

  usage = ('python orgunit_quick_start_example.py '
           '--client_id [clientId] --client_secret [clientSecret] '
           '--domain [domain]')
  # Parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['client_id=',
                                                  'client_secret=',
                                                  'domain='])
  except getopt.error:
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
    orgunit_provisioning = OrgUnitProvisioning(
        client_id, client_secret, domain)
  except gdata.service.BadAuthentication:
    print 'Invalid user credentials given.'
    return

  orgunit_provisioning.Run()


if __name__ == '__main__':
  main()
