#!/usr/bin/python2.4
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

"""Live client tests for the Organization Unit Provisioning API."""

# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.


__author__ = 'Gunjan Sharma <gunjansharma@google.com>'


import random
import unittest
import gdata.apps.organization.client
import gdata.apps.organization.data
import gdata.client
import gdata.data
import gdata.gauth
import gdata.test_config as conf

conf.options.register_option(conf.APPS_DOMAIN_OPTION)


class OrganizationUnitProvisioningClientTest(unittest.TestCase):

  def setUp(self):
    self.client = gdata.apps.organization.client.OrganizationUnitProvisioningClient(
        domain='example.com')
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.apps.organization.client.OrganizationUnitProvisioningClient(
          domain=conf.options.get_value('appsdomain'))
      if conf.options.get_value('ssl') == 'true':
        self.client.ssl = True
      conf.configure_client(self.client,
                            'OrganizationUnitProvisioningClientTest',
                            self.client.auth_service, True)

  def tearDown(self):
    conf.close_client(self.client)

  def testClientConfiguration(self):
    self.assertEqual('apps-apis.google.com', self.client.host)
    self.assertEqual('2.0', self.client.api_version)
    self.assertEqual('apps', self.client.auth_service)
    self.assertEqual(
        ('https://apps-apis.google.com/a/feeds/user/',
         'https://apps-apis.google.com/a/feeds/policies/',
         'https://apps-apis.google.com/a/feeds/alias/',
         'https://apps-apis.google.com/a/feeds/groups/'),
        self.client.auth_scopes)
    if conf.options.get_value('runlive') == 'true':
      self.assertEqual(self.client.domain,
                       conf.options.get_value('appsdomain'))
    else:
      self.assertEqual(self.client.domain, 'example.com')

  def testMakeCustomerIdFeedUri(self):
    self.assertEqual('/a/feeds/customer/2.0/customerId',
                     self.client.MakeCustomerIdFeedUri())

  def testMakeOrganizationUnitOrgunitProvisioningUri(self):
    self.customer_id = 'tempo'
    self.assertEqual('/a/feeds/orgunit/2.0/%s' % self.customer_id,
                     self.client.MakeOrganizationUnitOrgunitProvisioningUri(
                         self.customer_id))
    self.assertEqual(
        '/a/feeds/orgunit/2.0/%s/testing/Test+Test' % self.customer_id,
        self.client.MakeOrganizationUnitOrgunitProvisioningUri(
            self.customer_id, org_unit_path='testing/Test+Test'))
    self.assertEqual(
        '/a/feeds/orgunit/2.0/%s?get=all' % (self.customer_id),
        self.client.MakeOrganizationUnitOrgunitProvisioningUri(
            self.customer_id, params={'get': 'all'}))

  def testMakeOrganizationUnitOrguserProvisioningUri(self):
    self.customer_id = 'tempo'
    self.assertEqual('/a/feeds/orguser/2.0/%s' % self.customer_id,
                     self.client.MakeOrganizationUnitOrguserProvisioningUri(
                         self.customer_id))
    self.assertEqual(
        '/a/feeds/orguser/2.0/%s/admin@example.com' % self.customer_id,
        self.client.MakeOrganizationUnitOrguserProvisioningUri(
            self.customer_id, org_user_email='admin@example.com'))
    self.assertEqual(
        '/a/feeds/orguser/2.0/%s?get=all' % (self.customer_id),
        self.client.MakeOrganizationUnitOrguserProvisioningUri(
            self.customer_id, params={'get': 'all'}))

  def testCreateRetrieveUpdateDelete(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testCreateRetrieveUpdateDelete')

    customer_id = self.client.RetrieveCustomerId().GetCustomerId()
    rnd_number = random.randrange(0, 100001)
    org_unit_name = 'test_org_unit_name%s' % (rnd_number)
    org_unit_description = 'test_org_unit_description%s' % (rnd_number)
    org_unit_path = org_unit_name

    new_entry = self.client.CreateOrgUnit(customer_id, org_unit_name,
                                          parent_org_unit_path='/',
                                          description=org_unit_description,
                                          block_inheritance=False)
    self.assert_(isinstance(new_entry,
                            gdata.apps.organization.data.OrgUnitEntry))
    self.assertEquals(new_entry.org_unit_path, org_unit_path)

    entry = self.client.RetrieveOrgUnit(customer_id, org_unit_path)
    self.assert_(isinstance(entry,
                            gdata.apps.organization.data.OrgUnitEntry))
    self.assertEquals(entry.org_unit_name, org_unit_name)
    self.assertEquals(entry.org_unit_description, org_unit_description)
    self.assertEquals(entry.parent_org_unit_path, '')
    self.assertEquals(entry.org_unit_path, org_unit_path)
    self.assertEquals(entry.org_unit_block_inheritance, 'false')

    self.client.DeleteOrgUnit(customer_id, org_unit_name)


def suite():
  return conf.build_suite([OrganizationUnitProvisioningClientTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
