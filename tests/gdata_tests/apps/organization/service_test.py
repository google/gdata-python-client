#!/usr/bin/python
#
# Copyright (C) 2008 Google
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

"""Test for Organization service."""


__author__ = 'Alexandre Vivien (alex@simplecode.fr)'


import urllib
import unittest
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import atom
import gdata.apps
import gdata.apps.service
import gdata.apps.organization.service
import getpass
import time


domain = ''
admin_email = ''
admin_password = ''
username = ''


class OrganizationTest(unittest.TestCase):
  """Test for the OrganizationService."""

  def setUp(self):
    self.postfix = time.strftime("%Y%m%d%H%M%S")
    self.apps_client = gdata.apps.service.AppsService(
        email=admin_email, domain=domain, password=admin_password,
        source='OrganizationClient "Unit" Tests')
    self.apps_client.ProgrammaticLogin()
    self.organization_client = gdata.apps.organization.service.OrganizationService(
        email=admin_email, domain=domain, password=admin_password,
        source='GroupsClient "Unit" Tests')
    self.organization_client.ProgrammaticLogin()
    self.created_users = []
    self.created_org_units = []
    self.cutomer_id = None
    self.createUsers();

  def createUsers(self):
    user_name = 'yujimatsuo-' + self.postfix
    family_name = 'Matsuo'
    given_name = 'Yuji'
    password = '123$$abc'
    suspended = 'false'

    try:
      self.user_yuji = self.apps_client.CreateUser(user_name=user_name,
                                                   family_name=family_name,
                                                   given_name=given_name,
                                                   password=password,
                                                   suspended=suspended)
      print 'User ' + user_name + ' created'
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.created_users.append(self.user_yuji)

    user_name = 'taromatsuo-' + self.postfix
    family_name = 'Matsuo'
    given_name = 'Taro'
    password = '123$$abc'
    suspended = 'false'

    try:
      self.user_taro = self.apps_client.CreateUser(user_name=user_name,
                                                   family_name=family_name,
                                                   given_name=given_name,
                                                   password=password,
                                                   suspended=suspended)
      print 'User ' + user_name + ' created'
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.created_users.append(self.user_taro)
    
    user_name = 'alexandrevivien-' + self.postfix
    family_name = 'Vivien'
    given_name = 'Alexandre'
    password = '123$$abc'
    suspended = 'false'

    try:
      self.user_alex = self.apps_client.CreateUser(user_name=user_name,
                                                   family_name=family_name,
                                                   given_name=given_name,
                                                   password=password,
                                                   suspended=suspended)
      print 'User ' + user_name + ' created'
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.created_users.append(self.user_alex)

  def tearDown(self):
    print '\n'
    for user in self.created_users:
      try:
        self.apps_client.DeleteUser(user.login.user_name)
        print 'User ' + user.login.user_name + ' deleted'
      except Exception, e:
        print e
    # We reverse to delete sub OrgUnit first
    self.created_org_units.reverse()
    for org_unit_path in self.created_org_units:
      try:
        self.organization_client.DeleteOrgUnit(self.customer_id, org_unit_path)
        print 'OrgUnit ' + org_unit_path + ' deleted'
      except Exception, e:
        print e

  def testOrganizationService(self):

    # tests RetrieveCustomerId method
    try:
      customer = self.organization_client.RetrieveCustomerId()
      self.customer_id = customer['customerId']
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)
    print 'tests RetrieveCustomerId successful'
    
    # tests CreateOrgUnit method
    orgUnit01_name = 'OrgUnit01-' + self.postfix
    orgUnit02_name = 'OrgUnit02-' + self.postfix
    sub0rgUnit01_name = 'SubOrgUnit01-' + self.postfix
    orgUnit03_name = 'OrgUnit03-' + self.postfix
    try:
      orgUnit01 = self.organization_client.CreateOrgUnit(self.customer_id, 
                                                         name=orgUnit01_name, 
                                                         parent_org_unit_path='/',
                                                         description='OrgUnit Test 01',
                                                         block_inheritance=False)
      orgUnit02 = self.organization_client.CreateOrgUnit(self.customer_id,
                                                         name=orgUnit02_name,
                                                         parent_org_unit_path='/',
                                                         description='OrgUnit Test 02',
                                                         block_inheritance=False)
      sub0rgUnit01 = self.organization_client.CreateOrgUnit(self.customer_id,
                                                            name=sub0rgUnit01_name,
                                                            parent_org_unit_path=orgUnit02['orgUnitPath'],
                                                            description='SubOrgUnit Test 01',
                                                            block_inheritance=False)
      orgUnit03 = self.organization_client.CreateOrgUnit(self.customer_id,
                                                         name=orgUnit03_name,
                                                         parent_org_unit_path='/',
                                                         description='OrgUnit Test 03',
                                                         block_inheritance=False)
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)
    
    self.assertEquals(orgUnit01['orgUnitPath'], urllib.quote_plus(orgUnit01_name))
    self.assertEquals(orgUnit02['orgUnitPath'], urllib.quote_plus(orgUnit02_name))
    self.assertEquals(sub0rgUnit01['orgUnitPath'], urllib.quote_plus(orgUnit02_name) + '/' + urllib.quote_plus(sub0rgUnit01_name))
    self.assertEquals(orgUnit03['orgUnitPath'], urllib.quote_plus(orgUnit03_name))
    self.created_org_units.append(orgUnit01['orgUnitPath'])
    self.created_org_units.append(orgUnit02['orgUnitPath'])
    self.created_org_units.append(sub0rgUnit01['orgUnitPath'])
    self.created_org_units.append(orgUnit03['orgUnitPath'])
    print 'tests CreateOrgUnit successful'
    
    # tests UpdateOrgUnit method
    try:
      updated_orgunit = self.organization_client.UpdateOrgUnit(self.customer_id,
                                                               org_unit_path=self.created_org_units[3],
                                                               description='OrgUnit Test 03 Updated description')
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.assertEquals(updated_orgunit['orgUnitPath'], self.created_org_units[3])
    print 'tests UpdateOrgUnit successful'

    # tests RetrieveOrgUnit method
    try:
      retrieved_orgunit = self.organization_client.RetrieveOrgUnit(self.customer_id,
                                                                   org_unit_path=self.created_org_units[1])
      retrieved_suborgunit = self.organization_client.RetrieveOrgUnit(self.customer_id,
                                                                      org_unit_path=self.created_org_units[2])
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.assertEquals(retrieved_orgunit['orgUnitPath'], self.created_org_units[1])
    self.assertEquals(retrieved_suborgunit['orgUnitPath'], self.created_org_units[2])
    print 'tests RetrieveOrgUnit successful'
   
    # tests RetrieveAllOrgUnits method
    try:
      retrieved_orgunits = self.organization_client.RetrieveAllOrgUnits(self.customer_id)
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.assertTrue(len(retrieved_orgunits) >= len(self.created_org_units))
    print 'tests RetrieveAllOrgUnits successful'
   
    # tests MoveUserToOrgUnit method
    try:
      updated_orgunit01 = self.organization_client.MoveUserToOrgUnit(self.customer_id,
                                                                   org_unit_path=self.created_org_units[0],
                                                                   users_to_move=[self.user_yuji.login.user_name + '@' + domain])
      updated_orgunit02 = self.organization_client.MoveUserToOrgUnit(self.customer_id,
                                                                     org_unit_path=self.created_org_units[1],
                                                                     users_to_move=[self.user_taro.login.user_name + '@' + domain,
                                                                                    self.user_alex.login.user_name + '@' + domain])
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.assertEquals(updated_orgunit01['usersMoved'], self.user_yuji.login.user_name + '@' + domain)
    self.assertEquals(updated_orgunit02['usersMoved'], self.user_taro.login.user_name + '@' + domain + ',' + \
                                                       self.user_alex.login.user_name + '@' + domain)
    print 'tests MoveUserToOrgUnit successful'
    
    # tests RetrieveSubOrgUnits method
    try:
      retrieved_suborgunits = self.organization_client.RetrieveSubOrgUnits(self.customer_id,
                                                                           org_unit_path=self.created_org_units[1])
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.assertEquals(len(retrieved_suborgunits), 1)
    self.assertEquals(retrieved_suborgunits[0]['orgUnitPath'], self.created_org_units[2])
    print 'tests RetrieveSubOrgUnits successful'
    
    # tests RetrieveOrgUser method
    try:
      retrieved_orguser = self.organization_client.RetrieveOrgUser(self.customer_id,
                                                                   user_email=self.user_yuji.login.user_name + '@' + domain)
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.assertEquals(retrieved_orguser['orgUserEmail'], self.user_yuji.login.user_name + '@' + domain)
    self.assertEquals(retrieved_orguser['orgUnitPath'], self.created_org_units[0])
    print 'tests RetrieveOrgUser successful'
    
    # tests UpdateOrgUser method
    try:
      updated_orguser = self.organization_client.UpdateOrgUser(self.customer_id,
                                                               org_unit_path=self.created_org_units[0],
                                                               user_email=self.user_alex.login.user_name + '@' + domain)
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.assertEquals(updated_orguser['orgUserEmail'], self.user_alex.login.user_name + '@' + domain)
    self.assertEquals(updated_orguser['orgUnitPath'], self.created_org_units[0])
    print 'tests UpdateOrgUser successful'
  
    # tests RetrieveAllOrgUsers method
    try:
      retrieved_orgusers = self.organization_client.RetrieveAllOrgUsers(self.customer_id)
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.assertTrue(len(retrieved_orgusers) >= len(self.created_users))
    print 'tests RetrieveAllOrgUsers successful'
    
    """ This test needs to create more than 100 test users
    # tests RetrievePageOfOrgUsers method
    try:
      retrieved_orgusers01_feed = self.organization_client.RetrievePageOfOrgUsers(self.customer_id)
      next = retrieved_orgusers01_feed.GetNextLink()
      self.assertNotEquals(next, None)
      startKey = next.href.split("startKey=")[1]
      retrieved_orgusers02_feed = self.organization_client.RetrievePageOfOrgUsers(self.customer_id, startKey=startKey)
      retrieved_orgusers01_entry = self.organization_client._PropertyEntry2Dict(retrieved_orgusers01_feed.entry[0])
      retrieved_orgusers02_entry = self.organization_client._PropertyEntry2Dict(retrieved_orgusers02_feed.entry[0])
      self.assertNotEquals(retrieved_orgusers01_entry['orgUserEmail'], retrieved_orgusers02_entry['orgUserEmail'])
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    print 'tests RetrievePageOfOrgUsers successful'
    """
    
    # tests RetrieveOrgUnitUsers method
    try:
      retrieved_orgusers = self.organization_client.RetrieveOrgUnitUsers(self.customer_id,
                                                                         org_unit_path=self.created_org_units[0])
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    self.assertEquals(len(retrieved_orgusers), 2)
    print 'tests RetrieveOrgUnitUsers successful'
    
    """ This test needs to create more than 100 test users
    # tests RetrieveOrgUnitPageOfUsers method
    try:
      retrieved_orgusers01_feed = self.organization_client.RetrieveOrgUnitPageOfUsers(self.customer_id,
                                                                                      org_unit_path='/')
      next = retrieved_orgusers01_feed.GetNextLink()
      self.assertNotEquals(next, None)
      startKey = next.href.split("startKey=")[1]
      retrieved_orgusers02_feed = self.organization_client.RetrieveOrgUnitPageOfUsers(self.customer_id,
                                                                                      org_unit_path='/',
                                                                                      startKey=startKey)
      retrieved_orgusers01_entry = self.organization_client._PropertyEntry2Dict(retrieved_orgusers01_feed.entry[0])
      retrieved_orgusers02_entry = self.organization_client._PropertyEntry2Dict(retrieved_orgusers02_feed.entry[0])
      self.assertNotEquals(retrieved_orgusers01_entry['orgUserEmail'], retrieved_orgusers02_entry['orgUserEmail'])
    except Exception, e:
      self.fail('Unexpected exception occurred: %s' % e)

    print 'tests RetrieveOrgUnitPageOfUsers successful'
    """

if __name__ == '__main__':
  print("""Google Apps Groups Service Tests

NOTE: Please run these tests only with a test user account.
""")
  domain = raw_input('Google Apps domain: ')
  admin_email = '%s@%s' % (raw_input('Administrator username: '), domain)
  admin_password = getpass.getpass('Administrator password: ')
  unittest.main()
