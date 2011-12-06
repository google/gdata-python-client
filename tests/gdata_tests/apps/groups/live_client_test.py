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

"""Live client tests for the Groups Provisioning API."""

# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.


__author__ = 'Shraddha gupta <shraddhag@google.com>'


import random
import unittest
import gdata.apps.groups.client
import gdata.apps.groups.data
import gdata.client
import gdata.data
import gdata.gauth
import gdata.test_config as conf

conf.options.register_option(conf.APPS_DOMAIN_OPTION)


class GroupsProvisioningClientTest(unittest.TestCase):

  def setUp(self):
    self.client = gdata.apps.groups.client.GroupsProvisioningClient(
        domain='example.com')
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.apps.groups.client.GroupsProvisioningClient(
          domain=conf.options.get_value('appsdomain'))
      if conf.options.get_value('ssl') == 'true':
        self.client.ssl = True
      conf.configure_client(self.client, 'GroupsProvisioningClientTest',
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
      self.assertEqual(self.client.domain, conf.options.get_value('appsdomain'))
    else:
      self.assertEqual(self.client.domain, 'example.com')

  def testMakeGroupProvisioningUri(self):
    self.assertEqual('/a/feeds/group/2.0/%s' % self.client.domain,
        self.client.MakeGroupProvisioningUri())
    self.assertEqual('/a/feeds/group/2.0/%s/firstgroup@example.com'
        % self.client.domain,
        self.client.MakeGroupProvisioningUri(group_id='firstgroup@example.com'))
    self.assertEqual(
        '/a/feeds/group/2.0/%s?member=member1' % self.client.domain,
        self.client.MakeGroupProvisioningUri(params={'member':'member1'}))

  def testMakeGroupMembersUri(self):
    self.assertEqual('/a/feeds/group/2.0/%s/firstgroup@example.com/member'
        % self.client.domain,
        self.client.MakeGroupMembersUri(group_id='firstgroup@example.com'))
    self.assertEqual(
        '/a/feeds/group/2.0/%s/firstgroup@example.com/member/liz@example.com'
        % self.client.domain,
        self.client.MakeGroupMembersUri(
            group_id='firstgroup@example.com', member_id='liz@example.com'))

  def testCreateRetrieveUpdateDelete(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testCreateUpdateDelete')

    rnd_number = random.randrange(0, 100)
    group_id = 'test_groupid%s@%s' % (rnd_number, self.client.domain)
    group_name = 'test_groupname%s' % (rnd_number)
    member_id = 'test_member%s@%s' % (rnd_number, self.client.domain)

    new_group = self.client.CreateGroup(
        group_id=group_id, group_name=group_name, description='Test Group',
        email_permission='Domain')

    self.assert_(isinstance(new_group,
        gdata.apps.groups.data.GroupEntry))
    self.assertEquals(new_group.group_id, group_id)
    self.assertEquals(new_group.group_name, group_name)
    self.assertEquals(new_group.description, 'Test Group')
    self.assertEquals(new_group.email_permission, 'Domain')

    fetched_entry = self.client.RetrieveGroup(group_id=group_id)
    self.assert_(isinstance(fetched_entry,
        gdata.apps.groups.data.GroupEntry))
    self.assertEquals(new_group.group_id, group_id)
    self.assertEquals(new_group.group_name, group_name)
    self.assertEquals(new_group.description, 'Test Group')
    self.assertEquals(new_group.email_permission, 'Domain')

    new_group.group_name = 'updated name'
    updated_group = self.client.UpdateGroup(
        group_id=group_id, group_entry=new_group)
    self.assert_(isinstance(updated_group,
        gdata.apps.groups.data.GroupEntry))
    self.assertEqual(updated_group.group_name, 'updated name')

    new_member = self.client.AddMemberToGroup(group_id=group_id,
        member_id=member_id)
    self.assert_(isinstance(new_member,
        gdata.apps.groups.data.GroupMemberEntry))
    self.assertEquals(new_member.member_id, member_id)

    fetched_member = self.client.RetrieveGroupMember(group_id=group_id,
        member_id=member_id)
    self.assertEquals(fetched_member.member_id, member_id)

    self.client.RemoveMemberFromGroup(group_id=group_id,
        member_id=member_id)
    self.client.DeleteGroup(group_id=group_id)


def suite():
  return conf.build_suite([GroupsProvisioningClientTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
