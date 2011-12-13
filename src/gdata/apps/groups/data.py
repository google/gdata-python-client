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

"""Data model classes for the Groups Provisioning API."""


__author__ = 'Shraddha gupta <shraddhag@google.com>'


import atom.data
import gdata.apps
import gdata.apps.apps_property_entry
import gdata.apps_property
import gdata.data


# This is required to work around a naming conflict between the Google
# Spreadsheets API and Python's built-in property function
pyproperty = property


# The apps:property groupId of a group entry
GROUP_ID = 'groupId'
# The apps:property groupName of a group entry
GROUP_NAME = 'groupName'
# The apps:property description of a group entry
DESCRIPTION = 'description'
# The apps:property emailPermission of a group entry
EMAIL_PERMISSION = 'emailPermission'
# The apps:property memberId of a group member entry
MEMBER_ID = 'memberId'
# The apps:property memberType of a group member entry
MEMBER_TYPE = 'memberType'
# The apps:property directMember of a group member entry
DIRECT_MEMBER = 'directMember'


class GroupEntry(gdata.apps.apps_property_entry.AppsPropertyEntry):
  """Represents a group entry in object form."""

  def GetGroupId(self):
    """Get groupId of the GroupEntry object.

    Returns:
      The groupId this GroupEntry object as a string or None.
    """
    return self._GetProperty(GROUP_ID)

  def SetGroupId(self, value):
    """Set the groupId of this GroupEntry object.

    Args:
      value: string The new groupId to give this object.
    """
    self._SetProperty(GROUP_ID, value)

  group_id = pyproperty(GetGroupId, SetGroupId)

  def GetGroupName(self):
    """Get the groupName of the GroupEntry object.

    Returns:
      The groupName of this GroupEntry object as a string or None.
    """
    return self._GetProperty(GROUP_NAME)

  def SetGroupName(self, value):
    """Set the groupName of this GroupEntry object.

    Args:
      value: string The new groupName to give this object.
    """
    self._SetProperty(GROUP_NAME, value)

  group_name = pyproperty(GetGroupName, SetGroupName)

  def GetDescription(self):
    """Get the description of the GroupEntry object.

    Returns:
      The description of this GroupEntry object as a string or None.
    """
    return self._GetProperty(DESCRIPTION)

  def SetDescription(self, value):
    """Set the description of this GroupEntry object.

    Args:
      value: string The new description to give this object.
    """
    self._SetProperty(DESCRIPTION, value)

  description = pyproperty(GetDescription, SetDescription)

  def GetEmailPermission(self):
    """Get the emailPermission of the GroupEntry object.

    Returns:
      The emailPermission of this GroupEntry object as a string or None.
    """
    return self._GetProperty(EMAIL_PERMISSION)

  def SetEmailPermission(self, value):
    """Set the emailPermission of this GroupEntry object.

    Args:
      value: string The new emailPermission to give this object.
    """
    self._SetProperty(EMAIL_PERMISSION, value)

  email_permission = pyproperty(GetEmailPermission, SetEmailPermission)

  def __init__(self, group_id=None, group_name=None, description=None,
               email_permission=None, *args, **kwargs):
    """Constructs a new GroupEntry object with the given arguments.

    Args:
      group_id: string identifier of the group.
      group_name: string name of the group.
      description: string (optional) the group description.
      email_permisison: string (optional) permission level of the group.
    """
    super(GroupEntry, self).__init__(*args, **kwargs)
    if group_id:
      self.group_id = group_id
    if group_name:
      self.group_name = group_name
    if description:
      self.description = description
    if email_permission:
      self.email_permission = email_permission


class GroupFeed(gdata.data.GDFeed):
  """Represents a feed of GroupEntry objects."""

  # Override entry so that this feed knows how to type its list of entries.
  entry = [GroupEntry]


class GroupMemberEntry(gdata.apps.apps_property_entry.AppsPropertyEntry):
  """Represents a group member in object form."""

  def GetMemberId(self):
    """Get the memberId of the GroupMember object.

    Returns:
      The memberId of this GroupMember object as a string.
    """
    return self._GetProperty(MEMBER_ID)

  def SetMemberId(self, value):
    """Set the memberId of this GroupMember object.

    Args:
      value: string The new memberId to give this object.
    """
    self._SetProperty(MEMBER_ID, value)

  member_id = pyproperty(GetMemberId, SetMemberId)

  def GetMemberType(self):
    """Get the memberType(User, Group) of the GroupMember object.

    Returns:
      The memberType of this GroupMember object as a string or None.
    """
    return self._GetProperty(MEMBER_TYPE)

  def SetMemberType(self, value):
    """Set the memberType of this GroupMember object.

    Args:
      value: string The new memberType to give this object.
    """
    self._SetProperty(MEMBER_TYPE, value)

  member_type = pyproperty(GetMemberType, SetMemberType)

  def GetDirectMember(self):
    """Get the directMember of the GroupMember object.

    Returns:
      The directMember of this GroupMember object as a bool or None.
    """
    return self._GetProperty(DIRECT_MEMBER)

  def SetDirectMember(self, value):
    """Set the memberType of this GroupMember object.

    Args:
      value: string The new memberType to give this object.
    """
    self._SetProperty(DIRECT_MEMBER, value)

  direct_member = pyproperty(GetDirectMember, SetDirectMember)

  def __init__(self, member_id=None, member_type=None,
               direct_member=None, *args, **kwargs):
    """Constructs a new GroupMemberEntry object with the given arguments.

    Args:
      member_id: string identifier of group member object.
      member_type: string (optional) member type of group member object.
      direct_member: bool (optional) if group member object is direct member.
      args: The other parameters to pass to gdata.entry.GDEntry constructor.
      kwargs: The other parameters to pass to gdata.entry.GDEntry constructor.
    """
    super(GroupMemberEntry, self).__init__(*args, **kwargs)
    if member_id:
      self.member_id = member_id
    if member_type:
      self.member_type = member_type
    if direct_member:
      self.direct_member = direct_member


class GroupMemberFeed(gdata.data.GDFeed):
  """Represents a feed of GroupMemberEntry objects."""

  # Override entry so that this feed knows how to type its list of entries.
  entry = [GroupMemberEntry]

