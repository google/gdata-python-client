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

"""GroupsClient simplifies Groups Provisioning API calls.

GroupsClient extends gdata.client.GDClient to ease interaction
with the Group Provisioning API.  These interactions include the
ability to create, retrieve, update and delete groups.
"""


__author__ = 'Shraddha gupta <shraddhag@google.com>'


import urllib
import gdata.apps.groups.data
import gdata.client


# Multidomain URI templates
# The strings in this template are eventually replaced with the API version,
# and Google Apps domain name respectively.
GROUP_URI_TEMPLATE = '/a/feeds/group/%s/%s'
GROUP_MEMBER = 'member'


class GroupsProvisioningClient(gdata.client.GDClient):
  """Client extension for the Google Group Provisioning API service.

  Attributes:
    host: string The hostname for the Group Provisioning API service.
    api_version: string The version of the MultiDomain Provisioning API.
  """

  host = 'apps-apis.google.com'
  api_version = '2.0'
  auth_service = 'apps'
  auth_scopes = gdata.gauth.AUTH_SCOPES['apps']
  ssl = True

  def __init__(self, domain, auth_token=None, **kwargs):
    """Constructs a new client for the Groups Provisioning API.

    Args:
      domain: string The Google Apps domain with Group Provisioning.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the email settings.
      kwargs: The other parameters to pass to the gdata.client.GDClient
          constructor.
    """
    gdata.client.GDClient.__init__(self, auth_token=auth_token, **kwargs)
    self.domain = domain

  def make_group_provisioning_uri(
      self, feed_type=None, group_id=None, member_id=None, params=None):

    """Creates a resource feed URI for the Groups Provisioning API.

    Using this client's Google Apps domain, create a feed URI for group
    provisioning in that domain. If an email address is provided, return a
    URI for that specific resource.  If params are provided, append them as GET
    params.

    Args:
      feed_type: string groupmember for groupmember feed else None
      group_id: string (optional) The identifier of group for which to
      make a feed URI.
      member_id: string (optional) The identifier of group member for which to
      make a feed URI.
      params: dict (optional) key -> value params to append as GET vars to the
          URI. Example: params={'start': 'my-resource-id'}

    Returns:
      A string giving the URI for group provisioning for this client's
          Google Apps domain.
    """
    uri = GROUP_URI_TEMPLATE % (self.api_version, self.domain)
    if group_id:
      uri += '/' + group_id
    if feed_type is GROUP_MEMBER:
      uri += '/' + feed_type
    if member_id:
      uri += '/' + member_id
    if params:
      uri += '?' + urllib.urlencode(params)
    return uri

  MakeGroupProvisioningUri = make_group_provisioning_uri

  def make_group_member_uri(self, group_id, member_id=None, params=None):
    """Creates a resource feed URI for the Group Member Provisioning API."""

    return self.make_group_provisioning_uri(GROUP_MEMBER, group_id=group_id,
        member_id=member_id, params=params)

  MakeGroupMembersUri = make_group_member_uri

  def retrieve_all_groups(self, **kwargs):
    """Retrieves all groups for the given domain.

    Args:
      kwargs: The other parameters to pass to gdata.client.GDClient.GetFeed()

    Returns:
      A gdata.apps.groups.data.GDFeed of the group users
    """
    uri = self.MakeGroupProvisioningUri()
    return self.GetFeed(uri,
        desired_class=gdata.apps.groups.data.GroupFeed, **kwargs)

  RetrieveAllGroups = retrieve_all_groups

  def retrieve_group(self, group_id, **kwargs):
    """Retrieves a single group in the domain.

    Args:
      group_id: string groupId of the group to be retrieved
      kwargs: other parameters to pass to gdata.client.GDClient.GetEntry()

    Returns:
      A gdata.apps.groups.data.GroupEntry representing the group
    """
    uri = self.MakeGroupProvisioningUri(group_id=group_id)
    print uri
    return self.GetEntry(uri,
        desired_class=gdata.apps.groups.data.GroupEntry, **kwargs)

  RetrieveGroup = retrieve_group

  def create_group(self, group_id, group_name,
      description=None, email_permission=None, **kwargs):
    """Creates a group in the domain with the given properties.

    Args:
      group_id: string identifier of the group.
      group_name: string name of the group.
      description: string (optional) description of the group.
      email_permission: string (optional) email permission level for the group.
      kwargs: other parameters to pass to gdata.client.GDClient.post().

    Returns:
      A gdata.apps.groups.data.GroupEntry of the new group
    """
    new_group = gdata.apps.groups.data.GroupEntry(group_id=group_id,
        group_name=group_name, description=description,
        email_permission=email_permission)
    return self.post(new_group, self.MakeGroupProvisioningUri(),
                     **kwargs)

  CreateGroup = create_group

  def update_group(self, group_id, group_entry, **kwargs):
    """Updates the group with the given groupID.

    Args:
      group_id: string identifier of the group.
      group_entry: GroupEntry The group entry with updated values.
      kwargs: The other parameters to pass to gdata.client.GDClient.put()

    Returns:
      A gdata.apps.groups.data.GroupEntry representing the group
    """
    return self.update(group_entry,
                       uri=self.MakeGroupProvisioningUri(group_id=group_id),
                       **kwargs)

  UpdateGroup = update_group

  def delete_group(self, group_id, **kwargs):
    """Deletes the group with the given groupId.

    Args:
      group_id: string groupId of the group to delete.
      kwargs: The other parameters to pass to gdata.client.GDClient.delete()
    """
    self.delete(self.MakeGroupProvisioningUri(group_id=group_id), **kwargs)

  DeleteGroup = delete_group

  def retrieve_all_members(self, group_id, **kwargs):
    """Retrieves group members of the group.

    Args:
      group_id: string groupId of the group whose members are retrieved
      kwargs: The other parameters to pass to gdata.client.GDClient.GetFeed()

    Returns:
      A gdata.apps.groups.data.GDFeed of the GroupMember entries
    """
    uri = self.MakeGroupMembersUri(group_id=group_id)
    return self.GetFeed(uri,
        desired_class=gdata.apps.groups.data.GroupMemberFeed, **kwargs)

  RetrieveAllMembers = retrieve_all_members

  def retrieve_group_member(self, group_id, member_id, **kwargs):
    """Retrieves a group member with the given id from given group.

    Args:
      group_id: string groupId of the group whose member is retrieved
      member_id: string memberId of the group member retrieved
      kwargs: The other parameters to pass to gdata.client.GDClient.GetEntry()

    Returns:
      A gdata.apps.groups.data.GroupEntry representing the group member
    """
    uri = self.MakeGroupMembersUri(group_id=group_id, member_id=member_id)
    return self.GetEntry(uri,
        desired_class=gdata.apps.groups.data.GroupMemberEntry, **kwargs)

  RetrieveGroupMember = retrieve_group_member

  def add_member_to_group(self, group_id, member_id, member_type=None,
      direct_member=None, **kwargs):
    """Adds a member with the given id to the group.

    Args:
      group_id: string groupId of the group where member is added
      member_id: string memberId of the member added
      member_type: string (optional) type of member(user or group)
      direct_member: bool (optional) if member is a direct member
      kwargs: The other parameters to pass to gdata.client.GDClient.post().

    Returns:
      A gdata.apps.groups.data.GroupMemberEntry of the group member
    """
    member = gdata.apps.groups.data.GroupMemberEntry(member_id=member_id,
        member_type=member_type, direct_member=direct_member)
    return self.post(member, self.MakeGroupMembersUri(group_id=group_id),
        **kwargs)

  AddMemberToGroup = add_member_to_group

  def remove_member_from_group(self, group_id, member_id, **kwargs):
    """Remove member from the given group.

    Args:
      group_id: string groupId of the group
      member_id: string memberId of the member to be removed
      kwargs: The other parameters to pass to gdata.client.GDClient.delete()
    """
    self.delete(
        self.MakeGroupMembersUri(group_id=group_id, member_id=member_id),
        **kwargs)

  RemoveMemberFromGroup = remove_member_from_group
