#!/usr/bin/env python
#
# Copyright (C) 2009 Google Inc.
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


# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.


__author__ = 'j.s@google.com (Jeff Scudder)'


import unittest
import gdata.test_config as conf
import gdata.contacts.client
import atom.core
import atom.data
import gdata.data


class ContactsTest(unittest.TestCase):

  def setUp(self):
    self.client = None
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.contacts.client.ContactsClient()
      conf.configure_client(self.client, 'ContactsTest', 'cp')

  def tearDown(self):
    conf.close_client(self.client)

  def test_create_update_delete_contact(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_create_update_delete_contact')

    new_contact = gdata.contacts.data.ContactEntry(
        nickname=gdata.contacts.data.NickName(text='Joe'),
        name=gdata.data.Name(
            given_name=gdata.data.GivenName(text='Joseph'),
            family_name=gdata.data.FamilyName(text='Testerson')))
    new_contact.birthday = gdata.contacts.data.Birthday(when='2009-11-11')
    new_contact.language.append(gdata.contacts.data.Language(
        label='German'))
    created = self.client.create_contact(new_contact)

    # Add another language.
    created.language.append(gdata.contacts.data.Language(
        label='French'))

    # Create a new membership group for our test contact.
    new_group = gdata.contacts.data.GroupEntry(
        title=atom.data.Title(text='a test group'))
    created_group = self.client.create_group(new_group)

    self.assert_(created_group.id.text)

    # Add the contact to the new group.
    created.group_membership_info.append(
        gdata.contacts.data.GroupMembershipInfo(href=created_group.id.text))

    # Upload the changes to the language and group membership.
    edited = self.client.update(created)

    # Delete the group and the test contact.
    self.client.delete(created_group)
    self.client.delete(edited)

  def test_low_level_create_update_delete(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_low_level_create_update_delete')
    entry = atom.data.Entry()
    entry.title = atom.data.Title(text='Jeff')
    entry._other_elements.append(
        gdata.data.Email(rel=gdata.data.WORK_REL, address='j.s@google.com'))

    http_request = atom.http_core.HttpRequest()
    http_request.add_body_part(entry.to_string(), 'application/atom+xml')
    posted = self.client.request('POST', 
        'http://www.google.com/m8/feeds/contacts/default/full',
        desired_class=atom.data.Entry, http_request=http_request)

    self_link = None
    edit_link = None
    for link in posted.get_elements('link', 'http://www.w3.org/2005/Atom'):
      if link.get_attributes('rel')[0].value == 'self':
        self_link = link.get_attributes('href')[0].value
      elif link.get_attributes('rel')[0].value == 'edit':
        edit_link = link.get_attributes('href')[0].value
    self.assert_(self_link is not None)
    self.assert_(edit_link is not None)

    etag = posted.get_attributes('etag')[0].value
    self.assert_(etag is not None)
    self.assert_(len(etag) > 0)

    # Delete the test contact.
    http_request = atom.http_core.HttpRequest()
    http_request.headers['If-Match'] = etag
    self.client.request('DELETE', edit_link, http_request=http_request)

def suite():
  return conf.build_suite([ContactsTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
