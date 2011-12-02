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

"""OrganizationUnitProvisioningClient simplifies OrgUnit Provisioning API calls.

OrganizationUnitProvisioningClient extends gdata.client.GDClient to ease
interaction with the Google Organization Unit Provisioning API.
These interactions include the ability to create, retrieve, update and delete
organization units, move users within organization units, retrieve customerId
and update and retrieve users in organization units.
"""


__author__ = 'Gunjan Sharma <gunjansharma@google.com>'


import urllib
import gdata.apps.organization.data
import gdata.client

CUSTOMER_ID_URI_TEMPLATE = '/a/feeds/customer/%s/customerId'

# OrganizationUnit URI templates
# The strings in this template are eventually replaced with the feed type
# (orgunit/orguser), API version and Google Apps domain name, respectively.
ORGANIZATION_UNIT_URI_TEMPLATE = '/a/feeds/%s/%s/%s'

# The value for orgunit requests
ORGANIZATION_UNIT_FEED = 'orgunit'
# The value for orguser requests
ORGANIZATION_USER_FEED = 'orguser'


class OrganizationUnitProvisioningClient(gdata.client.GDClient):
  """Client extension for the Google Org Unit Provisioning API service.

  Attributes:
    host: string The hostname for the MultiDomain Provisioning API service.
    api_version: string The version of the MultiDomain Provisioning API.
  """

  host = 'apps-apis.google.com'
  api_version = '2.0'
  auth_service = 'apps'
  auth_scopes = gdata.gauth.AUTH_SCOPES['apps']
  ssl = True

  def __init__(self, domain, auth_token=None, **kwargs):
    """Constructs a new client for the Organization Unit Provisioning API.

    Args:
      domain: string The Google Apps domain with Organization Unit
          Provisioning.
      auth_token: (optional) gdata.gauth.ClientLoginToken, AuthSubToken, or
          OAuthToken which authorizes this client to edit the Organization
          Units.
    """
    gdata.client.GDClient.__init__(self, auth_token=auth_token, **kwargs)
    self.domain = domain

  def make_organization_unit_provisioning_uri(
      self, feed_type, customer_id, org_unit_path_or_user_email=None,
      params=None):

    """Creates a resource feed URI for the Organization Unit Provisioning API.

    Using this client's Google Apps domain, create a feed URI for organization
    unit provisioning in that domain. If an org unit path or org user email
    address is provided, return a URI for that specific resource.
    If params are provided, append them as GET params.

    Args:
      feed_type: string The type of feed (orgunit/orguser)
      customer_id: string The customerId of the user.
      org_unit_path_or_user_email: string (optional) The org unit path or
          org user email address for which to make a feed URI.
      params: dict (optional) key -> value params to append as GET vars to the
          URI. Example: params={'start': 'my-resource-id'}

    Returns:
      A string giving the URI for organization unit provisioning for this
          client's Google Apps domain.
    """
    uri = ORGANIZATION_UNIT_URI_TEMPLATE % (feed_type, self.api_version,
                                            customer_id)
    if org_unit_path_or_user_email:
      uri += '/' + org_unit_path_or_user_email
    if params:
      uri += '?' + urllib.urlencode(params)
    return uri

  MakeOrganizationUnitProvisioningUri = make_organization_unit_provisioning_uri

  def make_organization_unit_orgunit_provisioning_uri(self, customer_id,
                                                      org_unit_path=None,
                                                      params=None):
    """Creates a resource feed URI for the orgunit's Provisioning API calls.

    Using this client's Google Apps domain, create a feed URI for organization
    unit orgunit's provisioning in that domain. If an org_unit_path is
    provided, return a URI for that specific resource.
    If params are provided, append them as GET params.

    Args:
      customer_id: string The customerId of the user.
      org_unit_path: string (optional) The organization unit's path for which
          to make a feed URI.
      params: dict (optional) key -> value params to append as GET vars to the
          URI. Example: params={'start': 'my-resource-id'}

    Returns:
      A string giving the URI for organization unit provisioning for
          given org_unit_path
    """
    return self.make_organization_unit_provisioning_uri(
        ORGANIZATION_UNIT_FEED, customer_id, org_unit_path, params)

  MakeOrganizationUnitOrgunitProvisioningUri = make_organization_unit_orgunit_provisioning_uri

  def make_organization_unit_orguser_provisioning_uri(self, customer_id,
                                                      org_user_email=None,
                                                      params=None):
    """Creates a resource feed URI for the orguser's Provisioning API calls.

    Using this client's Google Apps domain, create a feed URI for organization
    unit orguser's provisioning in that domain. If an org_user_email is
    provided, return a URI for that specific resource.
    If params are provided, append them as GET params.

    Args:
      customer_id: string The customerId of the user.
      org_user_email: string (optional) The organization unit's path for which
          to make a feed URI.
      params: dict (optional) key -> value params to append as GET vars to the
          URI. Example: params={'start': 'my-resource-id'}

    Returns:
      A string giving the URI for organization user provisioning for
          given org_user_email
    """
    return self.make_organization_unit_provisioning_uri(
        ORGANIZATION_USER_FEED, customer_id, org_user_email, params)

  MakeOrganizationUnitOrguserProvisioningUri = make_organization_unit_orguser_provisioning_uri

  def make_customer_id_feed_uri(self):
    """Creates a feed uri for retrieving customerId of the user.

    Returns:
      A string giving the URI for retrieving customerId of the user.
    """
    uri = CUSTOMER_ID_URI_TEMPLATE % (self.api_version)
    return uri

  MakeCustomerIdFeedUri = make_customer_id_feed_uri

  def retrieve_customer_id(self, **kwargs):
    """Retrieve the Customer ID for the customer domain.

    Returns:
      A gdata.apps.organization.data.CustomerIdEntry.
    """
    uri = self.MakeCustomerIdFeedUri()
    return self.GetEntry(
        uri,
        desired_class=gdata.apps.organization.data.CustomerIdEntry,
        **kwargs)

  RetrieveCustomerId = retrieve_customer_id

  def create_org_unit(self, customer_id, name, parent_org_unit_path='/',
                      description='', block_inheritance=False, **kwargs):
    """Create a Organization Unit.

    Args:
      customer_id: string The ID of the Google Apps customer.
      name: string The simple organization unit text name, not the full path
            name.
      parent_org_unit_path: string The full path of the parental tree to this
                            organization unit (default: '/').
                            [Note: Each element of the path MUST be URL encoded
                            (example: finance%2Forganization/suborganization)]
      description: string The human readable text description of the
                   organization unit (optional).
      block_inheritance: boolean This parameter blocks policy setting
                         inheritance from organization units higher in
                         the organization tree (default: False).

    Returns:
      A gdata.apps.organization.data.OrgUnitEntry representing an organization
      unit.
    """
    new_org_unit = gdata.apps.organization.data.OrgUnitEntry(
        org_unit_name=name, parent_org_unit_path=parent_org_unit_path,
        org_unit_description=description,
        org_unit_block_inheritance=block_inheritance)
    return self.post(
        new_org_unit,
        self.MakeOrganizationUnitOrgunitProvisioningUri(customer_id), **kwargs)

  CreateOrgUnit = create_org_unit

  def update_org_unit(self, customer_id, org_unit_path, org_unit_entry,
                      **kwargs):
    """Update a Organization Unit.

    Args:
      customer_id: string The ID of the Google Apps customer.
      org_unit_path: string The organization's full path name.
                     [Note: Each element of the path MUST be URL encoded
                     (example: finance%2Forganization/suborganization)]
      org_unit_entry: gdata.apps.organization.data.OrgUnitEntry
                      The updated organization unit entry.

    Returns:
      A gdata.apps.organization.data.OrgUnitEntry representing an organization
          unit.
    """
    if not org_unit_entry.GetParentOrgUnitPath():
      org_unit_entry.SetParentOrgUnitPath('/')
    return self.update(org_unit_entry,
                       uri=self.MakeOrganizationUnitOrgunitProvisioningUri(
                           customer_id, org_unit_path=org_unit_path), **kwargs)

  UpdateOrgUnit = update_org_unit

  def move_users_to_org_unit(self, customer_id, org_unit_path, users_to_move,
                             **kwargs):
    """Move a user to an Organization Unit.

    Args:
      customer_id: string The ID of the Google Apps customer.
      org_unit_path: string The organization's full path name.
                     [Note: Each element of the path MUST be URL encoded
                     (example: finance%2Forganization/suborganization)]
      users_to_move: list Email addresses of users to move in list format.
                     [Note: You can move a maximum of 25 users at one time.]

    Returns:
      A gdata.apps.organization.data.OrgUnitEntry representing
      an organization unit.
    """
    org_unit_entry = self.retrieve_org_unit(customer_id, org_unit_path)
    org_unit_entry.SetUsersToMove(', '.join(users_to_move))
    if not org_unit_entry.GetParentOrgUnitPath():
      org_unit_entry.SetParentOrgUnitPath('/')
    return self.update(org_unit_entry,
                       uri=self.MakeOrganizationUnitOrgunitProvisioningUri(
                           customer_id, org_unit_path=org_unit_path), **kwargs)

  MoveUserToOrgUnit = move_users_to_org_unit

  def retrieve_org_unit(self, customer_id, org_unit_path, **kwargs):
    """Retrieve a Orgunit based on its path.

    Args:
      customer_id: string The ID of the Google Apps customer.
      org_unit_path: string The organization's full path name.
                     [Note: Each element of the path MUST be URL encoded
                     (example: finance%2Forganization/suborganization)]

    Returns:
      A gdata.apps.organization.data.OrgUnitEntry representing
          an organization unit.
    """
    uri = self.MakeOrganizationUnitOrgunitProvisioningUri(
        customer_id, org_unit_path=org_unit_path)
    return self.GetEntry(
        uri, desired_class=gdata.apps.organization.data.OrgUnitEntry, **kwargs)

  RetrieveOrgUnit = retrieve_org_unit

  def retrieve_feed_from_uri(self, uri, desired_class, **kwargs):
    """Retrieve feed from given uri.

    Args:
      uri: string The uri from where to get the feed.
      desired_class: Feed The type of feed that if to be retrieved.

    Returns:
      Feed of type desired class.
    """
    return self.GetFeed(uri, desired_class=desired_class, **kwargs)

  RetrieveFeedFromUri = retrieve_feed_from_uri

  def retrieve_all_org_units_from_uri(self, uri, **kwargs):
    """Retrieve all OrgUnits from given uri.

    Args:
      uri: string The uri from where to get the orgunits.

    Returns:
      gdata.apps.organisation.data.OrgUnitFeed object
    """
    orgunit_feed = gdata.apps.organization.data.OrgUnitFeed()
    temp_feed = self.RetrieveFeedFromUri(
        uri, gdata.apps.organization.data.OrgUnitFeed)
    orgunit_feed.entry = temp_feed.entry
    next_link = temp_feed.GetNextLink()
    while next_link is not None:
      uri = next_link.GetAttributes()[0].value
      temp_feed = self.GetFeed(
          uri, desired_class=gdata.apps.organization.data.OrgUnitFeed, **kwargs)
      orgunit_feed.entry[0:0] = temp_feed.entry
      next_link = temp_feed.GetNextLink()
    return orgunit_feed

  RetrieveAllOrgUnitsFromUri = retrieve_all_org_units_from_uri

  def retrieve_all_org_units(self, customer_id, **kwargs):
    """Retrieve all OrgUnits in the customer's domain.

    Args:
      customer_id: string The ID of the Google Apps customer.

    Returns:
      gdata.apps.organisation.data.OrgUnitFeed object
    """
    uri = self.MakeOrganizationUnitOrgunitProvisioningUri(
        customer_id, params={'get': 'all'}, **kwargs)
    return self.RetrieveAllOrgUnitsFromUri(uri)

  RetrieveAllOrgUnits = retrieve_all_org_units

  def retrieve_page_of_org_units(self, customer_id, startKey=None, **kwargs):
    """Retrieve one page of OrgUnits in the customer's domain.

    Args:
      customer_id: string The ID of the Google Apps customer.
      startKey: string The key to continue for pagination through all OrgUnits.

    Returns:
      gdata.apps.organisation.data.OrgUnitFeed object
    """
    uri = ''
    if startKey is not None:
      uri = self.MakeOrganizationUnitOrgunitProvisioningUri(
          customer_id, params={'get': 'all', 'startKey': startKey}, **kwargs)
    else:
      uri = self.MakeOrganizationUnitOrgunitProvisioningUri(
          customer_id, params={'get': 'all'}, **kwargs)
    return self.GetFeed(
        uri, desired_class=gdata.apps.organization.data.OrgUnitFeed, **kwargs)

  RetrievePageOfOrgUnits = retrieve_page_of_org_units

  def retrieve_sub_org_units(self, customer_id, org_unit_path, **kwargs):
    """Retrieve all Sub-OrgUnits of the provided OrgUnit.

    Args:
      customer_id: string The ID of the Google Apps customer.
      org_unit_path: string The organization's full path name.
                     [Note: Each element of the path MUST be URL encoded
                     (example: finance%2Forganization/suborganization)]

    Returns:
      gdata.apps.organisation.data.OrgUnitFeed object
    """
    uri = self.MakeOrganizationUnitOrgunitProvisioningUri(
        customer_id,
        params={'get': 'children', 'orgUnitPath': org_unit_path}, **kwargs)
    return self.RetrieveAllOrgUnitsFromUri(uri)

  RetrieveSubOrgUnits = retrieve_sub_org_units

  def delete_org_unit(self, customer_id, org_unit_path, **kwargs):
    """Delete a Orgunit based on its path.

    Args:
      customer_id: string The ID of the Google Apps customer.
      org_unit_path: string The organization's full path name.
                     [Note: Each element of the path MUST be URL encoded
                     (example: finance%2Forganization/suborganization)]

    Returns:
      An HTTP response object.  See gdata.client.request().
    """
    return self.delete(self.MakeOrganizationUnitOrgunitProvisioningUri(
        customer_id, org_unit_path=org_unit_path), **kwargs)

  DeleteOrgUnit = delete_org_unit

  def update_org_user(self, customer_id, user_email, org_unit_path, **kwargs):
    """Update the OrgUnit of a OrgUser.

    Args:
      customer_id: string The ID of the Google Apps customer.
      user_email: string The email address of the user.
      org_unit_path: string The new organization's full path name.
                     [Note: Each element of the path MUST be URL encoded
                     (example: finance%2Forganization/suborganization)]

    Returns:
      A gdata.apps.organization.data.OrgUserEntry representing
          an organization user.
    """
    old_user_entry = self.RetrieveOrgUser(customer_id, user_email)
    old_org_unit_path = old_user_entry.GetOrgUnitPath()
    if not old_org_unit_path:
      old_org_unit_path = '/'
    old_user_entry.SetOldOrgUnitPath(old_org_unit_path)
    old_user_entry.SetOrgUnitPath(org_unit_path)
    return self.update(old_user_entry,
                       uri=self.MakeOrganizationUnitOrguserProvisioningUri(
                           customer_id, user_email), **kwargs)

  UpdateOrgUser = update_org_user

  def retrieve_org_user(self, customer_id, user_email, **kwargs):
    """Retrieve an organization user.

    Args:
      customer_id: string The ID of the Google Apps customer.
      user_email: string The email address of the user.

    Returns:
      A gdata.apps.organization.data.OrgUserEntry representing
          an organization user.
    """
    uri = self.MakeOrganizationUnitOrguserProvisioningUri(customer_id,
                                                          user_email)
    return self.GetEntry(
        uri, desired_class=gdata.apps.organization.data.OrgUserEntry, **kwargs)

  RetrieveOrgUser = retrieve_org_user

  def retrieve_all_org_users_from_uri(self, uri, **kwargs):
    """Retrieve all OrgUsers from given uri.

    Args:
      uri: string The uri from where to get the orgusers.

    Returns:
      gdata.apps.organisation.data.OrgUserFeed object
    """
    orguser_feed = gdata.apps.organization.data.OrgUserFeed()
    temp_feed = self.RetrieveFeedFromUri(
        uri, gdata.apps.organization.data.OrgUserFeed)
    orguser_feed.entry = temp_feed.entry
    next_link = temp_feed.GetNextLink()
    while next_link is not None:
      uri = next_link.GetAttributes()[0].value
      temp_feed = self.GetFeed(
          uri, desired_class=gdata.apps.organization.data.OrgUserFeed, **kwargs)
      orguser_feed.entry[0:0] = temp_feed.entry
      next_link = temp_feed.GetNextLink()
    return orguser_feed

  RetrieveAllOrgUsersFromUri = retrieve_all_org_users_from_uri

  def retrieve_all_org_users(self, customer_id, **kwargs):
    """Retrieve all OrgUsers in the customer's domain.

    Args:
      customer_id: string The ID of the Google Apps customer.

    Returns:
      gdata.apps.organisation.data.OrgUserFeed object
    """
    uri = self.MakeOrganizationUnitOrguserProvisioningUri(
        customer_id, params={'get': 'all'}, **kwargs)
    return self.RetrieveAllOrgUsersFromUri(uri)

  RetrieveAllOrgUsers = retrieve_all_org_users

  def retrieve_page_of_org_users(self, customer_id, startKey=None, **kwargs):
    """Retrieve one page of OrgUsers in the customer's domain.

    Args:
      customer_id: string The ID of the Google Apps customer.
      startKey: The string key to continue for pagination through all OrgUnits.

    Returns:
      gdata.apps.organisation.data.OrgUserFeed object
    """
    uri = ''
    if startKey is not None:
      uri = self.MakeOrganizationUnitOrguserProvisioningUri(
          customer_id, params={'get': 'all', 'startKey': startKey}, **kwargs)
    else:
      uri = self.MakeOrganizationUnitOrguserProvisioningUri(
          customer_id, params={'get': 'all'})
    return self.GetFeed(
        uri, desired_class=gdata.apps.organization.data.OrgUserFeed, **kwargs)

  RetrievePageOfOrgUsers = retrieve_page_of_org_users

  def retrieve_org_unit_users(self, customer_id, org_unit_path, **kwargs):
    """Retrieve all OrgUsers of the provided OrgUnit.

    Args:
      customer_id: string The ID of the Google Apps customer.
      org_unit_path: string The organization's full path name.
                     [Note: Each element of the path MUST be URL encoded
                     (example: finance%2Forganization/suborganization)]

    Returns:
      gdata.apps.organisation.data.OrgUserFeed object
    """
    uri = self.MakeOrganizationUnitOrguserProvisioningUri(
        customer_id,
        params={'get': 'children', 'orgUnitPath': org_unit_path})
    return self.RetrieveAllOrgUsersFromUri(uri, **kwargs)

  RetrieveOrgUnitUsers = retrieve_org_unit_users
