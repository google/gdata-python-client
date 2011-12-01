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

"""Data model classes for the Organization Unit Provisioning API."""


__author__ = 'Gunjan Sharma <gunjansharma@google.com>'


import gdata.apps
import gdata.apps.apps_property_entry
import gdata.apps_property
import gdata.data


# This is required to work around a naming conflict between the Google
# Spreadsheets API and Python's built-in property function
pyproperty = property


# The apps:property name of an organization unit
ORG_UNIT_NAME = 'name'
# The apps:property orgUnitPath of an organization unit
ORG_UNIT_PATH = 'orgUnitPath'
# The apps:property parentOrgUnitPath of an organization unit
PARENT_ORG_UNIT_PATH = 'parentOrgUnitPath'
# The apps:property description of an organization unit
ORG_UNIT_DESCRIPTION = 'description'
# The apps:property blockInheritance of an organization unit
ORG_UNIT_BLOCK_INHERITANCE = 'blockInheritance'
# The apps:property userEmail of a user entry
USER_EMAIL = 'orgUserEmail'
# The apps:property list of users to move
USERS_TO_MOVE = 'usersToMove'
# The apps:property list of moved users
MOVED_USERS = 'usersMoved'
# The apps:property customerId for the domain
CUSTOMER_ID = 'customerId'
# The apps:property name of the customer org unit
CUSTOMER_ORG_UNIT_NAME = 'customerOrgUnitName'
# The apps:property description of the customer org unit
CUSTOMER_ORG_UNIT_DESCRIPTION = 'customerOrgUnitDescription'
# The apps:property old organization unit's path for a user
OLD_ORG_UNIT_PATH = 'oldOrgUnitPath'


class CustomerIdEntry(gdata.apps.apps_property_entry.AppsPropertyEntry):
  """Represents a customerId entry in object form."""

  def GetCustomerId(self):
    """Get the customer ID of the customerId object.

    Returns:
      The customer ID of this customerId object as a string or None.
    """
    return self._GetProperty(CUSTOMER_ID)

  customer_id = pyproperty(GetCustomerId)

  def GetOrgUnitName(self):
    """Get the Organization Unit name of the customerId object.

    Returns:
      The Organization unit name of this customerId object as a string or None.
    """
    return self._GetProperty(ORG_UNIT_NAME)

  org_unit_name = pyproperty(GetOrgUnitName)

  def GetCustomerOrgUnitName(self):
    """Get the Customer Organization Unit name of the customerId object.

    Returns:
      The Customer Organization unit name of this customerId object as a string
      or None.
    """
    return self._GetProperty(CUSTOMER_ORG_UNIT_NAME)

  customer_org_unit_name = pyproperty(GetCustomerOrgUnitName)

  def GetOrgUnitDescription(self):
    """Get the Organization Unit Description of the customerId object.

    Returns:
      The Organization Unit Description of this customerId object as a string
          or None.
    """
    return self._GetProperty(ORG_UNIT_DESCRIPTION)

  org_unit_description = pyproperty(GetOrgUnitDescription)

  def GetCustomerOrgUnitDescription(self):
    """Get the Customer Organization Unit Description of the customerId object.

    Returns:
      The Customer Organization Unit Description of this customerId object
          as a string or None.
    """
    return self._GetProperty(CUSTOMER_ORG_UNIT_DESCRIPTION)

  customer_org_unit_description = pyproperty(GetCustomerOrgUnitDescription)


class OrgUnitEntry(gdata.apps.apps_property_entry.AppsPropertyEntry):
  """Represents an OrganizationUnit in object form."""

  def GetOrgUnitName(self):
    """Get the Organization Unit name of the OrganizationUnit object.

    Returns:
      The Organization unit name of this OrganizationUnit object as a string
      or None.
    """
    return self._GetProperty(ORG_UNIT_NAME)

  def SetOrgUnitName(self, value):
    """Set the Organization Unit name of the OrganizationUnit object.

    Args:
      value: [string] The new Organization Unit name to give this object.
    """
    self._SetProperty(ORG_UNIT_NAME, value)

  org_unit_name = pyproperty(GetOrgUnitName, SetOrgUnitName)

  def GetOrgUnitPath(self):
    """Get the Organization Unit Path of the OrganizationUnit object.

    Returns:
      The Organization Unit Path of this OrganizationUnit object as a string
          or None.
    """
    return self._GetProperty(ORG_UNIT_PATH)

  def SetOrgUnitPath(self, value):
    """Set the Organization Unit path of the OrganizationUnit object.

    Args:
      value: [string] The new Organization Unit path to give this object.
    """
    self._SetProperty(ORG_UNIT_PATH, value)

  org_unit_path = pyproperty(GetOrgUnitPath, SetOrgUnitPath)

  def GetParentOrgUnitPath(self):
    """Get the Parent Organization Unit Path of the OrganizationUnit object.

    Returns:
      The Parent Organization Unit Path of this OrganizationUnit object
      as a string or None.
    """
    return self._GetProperty(PARENT_ORG_UNIT_PATH)

  def SetParentOrgUnitPath(self, value):
    """Set the Parent Organization Unit path of the OrganizationUnit object.

    Args:
      value: [string] The new Parent Organization Unit path
             to give this object.
    """
    self._SetProperty(PARENT_ORG_UNIT_PATH, value)

  parent_org_unit_path = pyproperty(GetParentOrgUnitPath, SetParentOrgUnitPath)

  def GetOrgUnitDescription(self):
    """Get the Organization Unit Description of the OrganizationUnit object.

    Returns:
      The Organization Unit Description of this OrganizationUnit object
      as a string or None.
    """
    return self._GetProperty(ORG_UNIT_DESCRIPTION)

  def SetOrgUnitDescription(self, value):
    """Set the Organization Unit Description of the OrganizationUnit object.

    Args:
      value: [string] The new Organization Unit Description
             to give this object.
    """
    self._SetProperty(ORG_UNIT_DESCRIPTION, value)

  org_unit_description = pyproperty(GetOrgUnitDescription,
                                    SetOrgUnitDescription)

  def GetOrgUnitBlockInheritance(self):
    """Get the block_inheritance flag of the OrganizationUnit object.

    Returns:
      The the block_inheritance flag of this OrganizationUnit object
      as a string or None.
    """
    return self._GetProperty(ORG_UNIT_BLOCK_INHERITANCE)

  def SetOrgUnitBlockInheritance(self, value):
    """Set the block_inheritance flag of the OrganizationUnit object.

    Args:
      value: [string] The new block_inheritance flag to give this object.
    """
    self._SetProperty(ORG_UNIT_BLOCK_INHERITANCE, value)

  org_unit_block_inheritance = pyproperty(GetOrgUnitBlockInheritance,
                                          SetOrgUnitBlockInheritance)

  def GetMovedUsers(self):
    """Get the moved users of the OrganizationUnit object.

    Returns:
      The the moved users of this OrganizationUnit object as a string or None.
    """
    return self._GetProperty(MOVED_USERS)

  def SetUsersToMove(self, value):
    """Set the Users to Move of the OrganizationUnit object.

    Args:
      value: [string] The comma seperated list of users to move
             to give this object.
    """
    self._SetProperty(USERS_TO_MOVE, value)

  move_users = pyproperty(GetMovedUsers, SetUsersToMove)

  def __init__(
      self, org_unit_name=None, org_unit_path=None,
      parent_org_unit_path=None, org_unit_description=None,
      org_unit_block_inheritance=None, move_users=None, *args, **kwargs):
    """Constructs a new OrganizationUnit object with the given arguments.

    Args:
      org_unit_name: string (optional) The organization unit name
          for the object.
      org_unit_path: string (optional) The organization unit path
          for the object.
      parent_org_unit_path: string (optional) The parent organization unit path
          for the object.
      org_unit_description: string (optional) The organization unit description
          for the object.
      org_unit_block_inheritance: boolean (optional) weather or not inheritance
          from the organization unit is blocked.
      move_users: string (optional) comma seperated list of users to move.
      args: The other parameters to pass to gdata.entry.GDEntry constructor.
      kwargs: The other parameters to pass to gdata.entry.GDEntry constructor.
    """
    super(OrgUnitEntry, self).__init__(*args, **kwargs)
    if org_unit_name:
      self.org_unit_name = org_unit_name
    if org_unit_path:
      self.org_unit_path = org_unit_path
    if parent_org_unit_path:
      self.parent_org_unit_path = parent_org_unit_path
    if org_unit_description:
      self.org_unit_description = org_unit_description
    if org_unit_block_inheritance is not None:
      self.org_unit_block_inheritance = str(org_unit_block_inheritance)
    if move_users:
      self.move_users = move_users


class OrgUnitFeed(gdata.data.GDFeed):
  """Represents a feed of OrgUnitEntry objects."""

  # Override entry so that this feed knows how to type its list of entries.
  entry = [OrgUnitEntry]


class OrgUserEntry(gdata.apps.apps_property_entry.AppsPropertyEntry):
  """Represents an OrgUser in object form."""

  def GetUserEmail(self):
    """Get the user email address of the OrgUser object.

    Returns:
      The user email address of this OrgUser object as a string or None.
    """
    return self._GetProperty(USER_EMAIL)

  def SetUserEmail(self, value):
    """Set the user email address of this OrgUser object.

    Args:
      value: string The new user email address to give this object.
    """
    self._SetProperty(USER_EMAIL, value)

  user_email = pyproperty(GetUserEmail, SetUserEmail)

  def GetOrgUnitPath(self):
    """Get the Organization Unit Path of the OrgUser object.

    Returns:
      The Organization Unit Path of this OrgUser object as a string or None.
    """
    return self._GetProperty(ORG_UNIT_PATH)

  def SetOrgUnitPath(self, value):
    """Set the Organization Unit path of the OrgUser object.

    Args:
      value: [string] The new Organization Unit path to give this object.
    """
    self._SetProperty(ORG_UNIT_PATH, value)

  org_unit_path = pyproperty(GetOrgUnitPath, SetOrgUnitPath)

  def GetOldOrgUnitPath(self):
    """Get the Old Organization Unit Path of the OrgUser object.

    Returns:
      The Old Organization Unit Path of this OrgUser object as a string
      or None.
    """
    return self._GetProperty(OLD_ORG_UNIT_PATH)

  def SetOldOrgUnitPath(self, value):
    """Set the Old Organization Unit path of the OrgUser object.

    Args:
      value: [string] The new Old Organization Unit path to give this object.
    """
    self._SetProperty(OLD_ORG_UNIT_PATH, value)

  old_org_unit_path = pyproperty(GetOldOrgUnitPath, SetOldOrgUnitPath)

  def __init__(
      self, user_email=None, org_unit_path=None,
      old_org_unit_path=None, *args, **kwargs):
    """Constructs a new OrgUser object with the given arguments.

    Args:
      user_email: string (optional) The user email address for the object.
      org_unit_path: string (optional) The organization unit path
          for the object.
      old_org_unit_path: string (optional) The old organization unit path
          for the object.
      args: The other parameters to pass to gdata.entry.GDEntry constructor.
      kwargs: The other parameters to pass to gdata.entry.GDEntry constructor.
    """
    super(OrgUserEntry, self).__init__(*args, **kwargs)
    if user_email:
      self.user_email = user_email
    if org_unit_path:
      self.org_unit_path = org_unit_path
    if old_org_unit_path:
      self.old_org_unit_path = old_org_unit_path


class OrgUserFeed(gdata.data.GDFeed):
  """Represents a feed of OrgUserEntry objects."""

  # Override entry so that this feed knows how to type its list of entries.
  entry = [OrgUserEntry]
