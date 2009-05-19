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


__author__ = 'j.s@google.com (Jeff Scudder)'


import unittest
import gdata.data


SIMPLE_V2_FEED_TEST_DATA = """<feed xmlns='http://www.w3.org/2005/Atom'
    xmlns:gd='http://schemas.google.com/g/2005'
    gd:etag='W/"CUMBRHo_fip7ImA9WxRbGU0."'>
  <title>Elizabeth Bennet's Contacts</title>
  <link rel='next' type='application/atom+xml'
        href='http://www.google.com/m8/feeds/contacts/.../more' />
  <entry gd:etag='"Qn04eTVSLyp7ImA9WxRbGEUORAQ."'>
    <id>http://www.google.com/m8/feeds/contacts/liz%40gmail.com/base/c9e</id>
    <title>Fitzwilliam</title>
    <link rel='http://schemas.google.com/contacts/2008/rel#photo' 
     type='image/*'
     href='http://www.google.com/m8/feeds/photos/media/liz%40gmail.com/c9e'
     gd:etag='"KTlcZWs1bCp7ImBBPV43VUV4LXEZCXERZAc."' />
    <link rel='self' type='application/atom+xml'
     href='Changed to ensure we are really getting the edit URL.'/>
    <link rel='edit' type='application/atom+xml'
     href='http://www.google.com/m8/feeds/contacts/liz%40gmail.com/full/c9e'/>
  </entry>
  <entry gd:etag='&quot;123456&quot;'>
    <link rel='edit' href='http://example.com/1' />
  </entry>
</feed>
"""


class SimpleV2FeedTest(unittest.TestCase):

  def test_parsing_etags_and_edit_url(self):
    feed = gdata.data.feed_from_string(SIMPLE_V2_FEED_TEST_DATA)

    # General parsing assertions.
    self.assertEqual(feed.get_elements('title')[0].text, 
                     'Elizabeth Bennet\'s Contacts')
    self.assertEqual(len(feed.entry), 2)
    for entry in feed.entry:
      self.assertTrue(isinstance(entry, gdata.data.GEntry))
    self.assertEqual(feed.entry[0].GetElements('title')[0].text,
                     'Fitzwilliam')
    self.assertEqual(feed.entry[0].get_elements('id')[0].text,
        'http://www.google.com/m8/feeds/contacts/liz%40gmail.com/base/c9e')

    # ETags checks.
    self.assertEqual(feed.etag, 'W/"CUMBRHo_fip7ImA9WxRbGU0."')
    self.assertEqual(feed.entry[0].etag, '"Qn04eTVSLyp7ImA9WxRbGEUORAQ."')
    self.assertEqual(feed.entry[1].etag, '"123456"')

    # Look for Edit URLs.
    self.assertEqual(feed.entry[0].get_edit_url(), 
        'http://www.google.com/m8/feeds/contacts/liz%40gmail.com/full/c9e')
    self.assertEqual(feed.entry[1].GetEditUrl(), 'http://example.com/1')

    # Look for Next URLs.
    self.assertEqual(feed.get_next_url(),
        'http://www.google.com/m8/feeds/contacts/.../more')

  def test_constructor_defauls(self):
    feed = gdata.data.GFeed()
    self.assertTrue(feed.etag is None)
    self.assertEqual(feed.link, [])
    self.assertEqual(feed.entry, [])
    entry = gdata.data.GEntry()
    self.assertTrue(entry.etag is None)
    self.assertEqual(entry.link, [])
    link = gdata.data.Link()
    self.assertTrue(link.href is None)
    self.assertTrue(link.rel is None)
    link1 = gdata.data.Link(href='http://example.com', rel='test')
    self.assertEqual(link1.href, 'http://example.com')
    self.assertEqual(link1.rel, 'test')
    link2 = gdata.data.Link(href='http://example.org/', rel='alternate')
    entry = gdata.data.GEntry(etag='foo', link=[link1, link2])
    feed = gdata.data.GFeed(etag='12345', entry=[entry])
    self.assertEqual(feed.etag, '12345')
    self.assertEqual(len(feed.entry), 1)
    self.assertEqual(feed.entry[0].etag, 'foo')
    self.assertEqual(len(feed.entry[0].link), 2)


def suite():
  return unittest.TestSuite((unittest.makeSuite(SimpleV2FeedTest, 'test'),))


if __name__ == '__main__':
  unittest.main()


