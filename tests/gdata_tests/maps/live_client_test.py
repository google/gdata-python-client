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


__author__ = 'api.roman.public@gmail.com (Roman Nurik)'


import unittest
import gdata.maps.client
import gdata.maps.data
import gdata.gauth
import gdata.client
import atom.http_core
import atom.mock_http_core
import atom.core
import gdata.data
import gdata.test_config as conf


class MapsClientTest(unittest.TestCase):

  def setUp(self):
    self.client = None
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.maps.client.MapsClient()
      conf.configure_client(self.client, 'MapsTest', 'local')
      #self.client.http_client.debug = True

  def tearDown(self):
    conf.close_client(self.client)

  def test_create_update_delete_map(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_create_update_delete_map')

    # Create a map.
    created = self.client.create_map('A test map',
                                     'This map is just a little test.')

    self.assertEqual(created.title.text, 'A test map')
    self.assertEqual(created.summary.text, 'This map is just a little test.')
    self.assert_(created.control is None)

    # Change the title of the map we just added.
    created.title.text = 'Edited'
    updated = self.client.update(created)

    self.assertEqual(updated.title.text, 'Edited')
    self.assert_(isinstance(updated, gdata.maps.data.Map))
    self.assertEqual(updated.content.text, created.content.text)

    # Delete the test map.
    self.client.delete(updated)

  def test_create_unlisted_map(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    conf.configure_cache(self.client, 'test_create_unlisted_map')

    # Add an unlisted map.
    created = self.client.create_map('An unlisted test map',
                                     'This should be unlisted.',
                                     unlisted=True)

    self.assertEqual(created.title.text, 'An unlisted test map')
    self.assertEqual(created.summary.text, 'This should be unlisted.')
    self.assert_(created.control is not None)
    self.assert_(created.control.draft is not None)
    self.assertEqual(created.control.draft.text, 'yes')
    
    # Make the map public. 
    created.control.draft.text = 'no'
    updated = self.client.update(created)

    if updated.control is not None and updated.control.draft is not None:
      self.assertNotEqual(updated.control.draft.text, 'yes')
      
    # Delete the test map using the URL instead of the entry.
    self.client.delete(updated.find_edit_link())


def suite():
  return conf.build_suite([MapsClientTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
