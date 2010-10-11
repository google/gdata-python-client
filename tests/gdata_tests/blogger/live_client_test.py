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
import gdata.blogger.client
import gdata.blogger.data
import gdata.gauth
import gdata.client
import atom.http_core
import atom.mock_http_core
import atom.core
import gdata.data
import gdata.test_config as conf


conf.options.register_option(conf.BLOG_ID_OPTION)


class BloggerClientTest(unittest.TestCase):

  def setUp(self):
    self.client = None
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.blogger.client.BloggerClient()
      conf.configure_client(self.client, 'BloggerTest', 'blogger')

  def tearDown(self):
    conf.close_client(self.client)

  def test_create_update_delete(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_create_update_delete')

    # Add a blog post.
    created = self.client.add_post(conf.options.get_value('blogid'),
                                   'test post from BloggerClientTest',
                                   'Hey look, another test!',
                                   labels=['test', 'python'])

    self.assertEqual(created.title.text, 'test post from BloggerClientTest')
    self.assertEqual(created.content.text, 'Hey look, another test!')
    self.assertEqual(len(created.category), 2)
    self.assert_(created.control is None)

    # Change the title of the blog post we just added.
    created.title.text = 'Edited'
    updated = self.client.update(created)

    self.assertEqual(updated.title.text, 'Edited')
    self.assert_(isinstance(updated, gdata.blogger.data.BlogPost))
    self.assertEqual(updated.content.text, created.content.text)

    # Delete the test entry from the blog.
    self.client.delete(updated)

  def test_create_draft_post(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    conf.configure_cache(self.client, 'test_create_draft_post')

    # Add a draft blog post.
    created = self.client.add_post(conf.options.get_value('blogid'),
                                   'draft test post from BloggerClientTest',
                                   'This should only be a draft.',
                                   labels=['test2', 'python'], draft=True)

    self.assertEqual(created.title.text,
                     'draft test post from BloggerClientTest')
    self.assertEqual(created.content.text, 'This should only be a draft.')
    self.assertEqual(len(created.category), 2)
    self.assert_(created.control is not None)
    self.assert_(created.control.draft is not None)
    self.assertEqual(created.control.draft.text, 'yes')
    
    # Publish the blog post. 
    created.control.draft.text = 'no'
    updated = self.client.update(created)

    if updated.control is not None and updated.control.draft is not None:
      self.assertNotEqual(updated.control.draft.text, 'yes')
      
    # Delete the test entry from the blog using the URL instead of the entry.
    self.client.delete(updated.find_edit_link())


  def test_create_draft_page(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    conf.configure_cache(self.client, 'test_create_draft_page')

    # List all pages on the blog.
    pages_before = self.client.get_pages(conf.options.get_value('blogid'))

    # Add a draft page to blog.
    created = self.client.add_page(conf.options.get_value('blogid'),
                                   'draft page from BloggerClientTest',
                                   'draft content',
                                   draft=True)

    self.assertEqual(created.title.text, 'draft page from BloggerClientTest')
    self.assertEqual(created.content.text, 'draft content')
    self.assert_(created.control is not None)
    self.assert_(created.control.draft is not None)
    self.assertEqual(created.control.draft.text, 'yes')
    self.assertEqual(str(int(created.get_page_id())), created.get_page_id())

    # List all pages after adding one.
    pages_after = self.client.get_pages(conf.options.get_value('blogid'))
    self.assertEqual(len(pages_before.entry) + 1, len(pages_after.entry))

    # Publish page.
    created.control.draft.text = 'no'
    updated = self.client.update(created)

    if updated.control is not None and updated.control.draft is not None:
      self.assertNotEqual(updated.control.draft.text, 'yes')

    # Delete test page.
    self.client.delete(updated.find_edit_link())
    pages_after = self.client.get_pages(conf.options.get_value('blogid'))

    self.assertEqual(len(pages_before.entry), len(pages_after.entry))


  def test_retrieve_post_with_categories(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    conf.configure_cache(self.client, 'test_retrieve_post_with_categories')
    query = gdata.blogger.client.Query(categories=["news"], strict=True)
    posts = self.client.get_posts(conf.options.get_value('blogid'), query=query)

def suite():
  return conf.build_suite([BloggerClientTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
