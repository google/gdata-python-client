#!/usr/bin/python
#
# Copyright 2009 Google Inc. All Rights Reserved.
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


__author__ = 'e.bidelman (Eric Bidelman)'

import unittest
import atom
from gdata import test_data
import gdata.acl.data
import gdata.data
import gdata.sites.data
import gdata.test_config as conf


def parse(xml_string, target_class):
  """Convenience wrapper for converting an XML string to an XmlElement."""
  return atom.core.xml_element_from_string(xml_string, target_class)


class CommentEntryTest(unittest.TestCase):

  def setUp(self):
    self.entry = parse(test_data.SITES_COMMENT_ENTRY,
                       gdata.sites.data.ContentEntry)

  def testToAndFromStringCommentEntry(self):
    self.assertEqual(self.entry.Kind(), 'comment')
    self.assert_(isinstance(self.entry.in_reply_to, gdata.sites.data.InReplyTo))
    self.assertEqual(self.entry.in_reply_to.type, 'text/html')
    self.assertEqual(
        self.entry.FindParentLink(),
        'http://sites.google.com/feeds/content/site/gdatatestsite/abc123parent')
    self.assertEqual(
        self.entry.in_reply_to.href,
        'http://sites.google.com/site/gdatatestsite/annoucment/testpost')
    self.assertEqual(
        self.entry.in_reply_to.ref,
        'http://sites.google.com/feeds/content/site/gdatatestsite/abc123')
    self.assertEqual(
        self.entry.in_reply_to.source,
        'http://sites.google.com/feeds/content/site/gdatatestsite')


class ListPageEntryTest(unittest.TestCase):

  def setUp(self):
    self.entry = parse(test_data.SITES_LISTPAGE_ENTRY,
                       gdata.sites.data.ContentEntry)

  def testToAndFromStringWithData(self):
    self.assert_(isinstance(self.entry, gdata.sites.data.ContentEntry))
    self.assertEqual(self.entry.title.text, 'ListPagesTitle')
    self.assertEqual(len(self.entry.author), 1)
    self.assertEqual(self.entry.author[0].name.text, 'Test User')
    self.assertEqual(self.entry.author[0].email.text, 'test@gmail.com')
    self.assertEqual(self.entry.worksheet.name, 'listpage')
    self.assertEqual(self.entry.header.row, '1')
    self.assertEqual(self.entry.data.startRow, '2')
    self.assertEqual(len(self.entry.data.column), 5)
    self.assert_(isinstance(self.entry.data.column[0], gdata.sites.data.Column))
    self.assertEqual(self.entry.data.column[0].index, 'A')
    self.assertEqual(self.entry.data.column[0].name, 'Owner')
    self.assert_(isinstance(self.entry.feed_link, gdata.data.FeedLink))
    self.assertEqual(
        self.entry.feed_link.href,
        'http:///sites.google.com/feeds/content/site/gdatatestsite?parent=abc')
    self.assert_(isinstance(self.entry.content, gdata.sites.data.Content))
    self.assert_(isinstance(self.entry.content.html, atom.core.XmlElement))
    self.assertEqual(self.entry.content.type, 'xhtml')


class ListItemEntryTest(unittest.TestCase):

  def setUp(self):
    self.entry = parse(test_data.SITES_LISTITEM_ENTRY,
                       gdata.sites.data.ContentEntry)

  def testToAndFromStringWithData(self):
    self.assert_(isinstance(self.entry, gdata.sites.data.ContentEntry))
    self.assertEqual(len(self.entry.field), 5)
    self.assert_(isinstance(self.entry.field[0], gdata.sites.data.Field))
    self.assertEqual(self.entry.field[0].index, 'A')
    self.assertEqual(self.entry.field[0].name, 'Owner')
    self.assertEqual(self.entry.field[0].text, 'test value')
    self.assertEqual(
        self.entry.FindParentLink(),
        'http://sites.google.com/feeds/content/site/gdatatestsite/abc123def')


class BaseSiteEntryTest(unittest.TestCase):

  def testCreateBaseSiteEntry(self):
    entry = gdata.sites.data.BaseSiteEntry()
    parent_link = atom.data.Link(
        rel=gdata.sites.data.SITES_PARENT_LINK_REL, href='abc')
    entry.link.append(parent_link)
    entry.category.append(
        atom.data.Category(
            scheme=gdata.sites.data.SITES_KIND_SCHEME,
            term='%s#%s' % (gdata.sites.data.SITES_NAMESPACE, 'webpage'),
            label='webpage'))
    self.assertEqual(entry.Kind(), 'webpage')
    self.assertEqual(entry.category[0].label, 'webpage')
    self.assertEqual(
        entry.category[0].term,
        '%s#%s' % ('http://schemas.google.com/sites/2008', 'webpage'))
    self.assertEqual(entry.link[0].href, 'abc')
    self.assertEqual(entry.link[0].rel,
                     'http://schemas.google.com/sites/2008#parent')

    entry2 = gdata.sites.data.BaseSiteEntry(kind='webpage')
    self.assertEqual(
        entry2.category[0].term,
        '%s#%s' % ('http://schemas.google.com/sites/2008', 'webpage'))


class ContentFeedTest(unittest.TestCase):

  def setUp(self):
    self.feed = parse(test_data.SITES_CONTENT_FEED,
                      gdata.sites.data.ContentFeed)

  def testToAndFromStringContentFeed(self):
    self.assert_(isinstance(self.feed, gdata.sites.data.ContentFeed))
    self.assertEqual(len(self.feed.entry), 8)
    self.assert_(isinstance(self.feed.entry[0].revision,
                            gdata.sites.data.Revision))
    self.assertEqual(int(self.feed.entry[0].revision.text), 2)
    self.assertEqual(self.feed.entry[0].GetNodeId(), '1712987567114738703')
    self.assert_(isinstance(self.feed.entry[0].page_name,
                            gdata.sites.data.PageName))
    self.assertEqual(self.feed.entry[0].page_name.text, 'home')
    self.assertEqual(self.feed.entry[0].FindRevisionLink(),
        'http:///sites.google.com/feeds/content/site/gdatatestsite/12345')
    for entry in self.feed.entry:
      self.assert_(isinstance(entry, gdata.sites.data.ContentEntry))
      if entry.deleted is not None:
        self.assert_(isinstance(entry.deleted, gdata.sites.data.Deleted))
        self.assertEqual(entry.IsDeleted(), True)
      else:
        self.assertEqual(entry.IsDeleted(), False)

  def testCreateContentEntry(self):
    new_entry = gdata.sites.data.ContentEntry()
    new_entry.content = gdata.sites.data.Content()
    new_entry.content.html = '<div><p>here is html</p></div>'
    self.assert_(isinstance(new_entry, gdata.sites.data.ContentEntry))
    self.assert_(isinstance(new_entry.content, gdata.sites.data.Content))
    self.assert_(isinstance(new_entry.content.html, atom.core.XmlElement))

    new_entry2 = gdata.sites.data.ContentEntry()
    new_entry2.content = gdata.sites.data.Content(
        html='<div><p>here is html</p></div>')
    self.assert_(isinstance(new_entry2, gdata.sites.data.ContentEntry))
    self.assert_(isinstance(new_entry2.content, gdata.sites.data.Content))
    self.assert_(isinstance(new_entry2.content.html, atom.core.XmlElement))

  def testGetHelpers(self):
    kinds = {'announcement': self.feed.GetAnnouncements,
             'announcementspage': self.feed.GetAnnouncementPages,
             'attachment': self.feed.GetAttachments,
             'comment': self.feed.GetComments,
             'filecabinet': self.feed.GetFileCabinets,
             'listitem': self.feed.GetListItems,
             'listpage': self.feed.GetListPages,
             'webpage': self.feed.GetWebpages}

    for k, v in kinds.iteritems():
      entries = v()
      self.assertEqual(len(entries), 1)
      for entry in entries:
        self.assertEqual(entry.Kind(), k)
        if k == 'attachment':
          self.assertEqual(entry.GetAlternateLink().href,
                           'http://sites.google.com/feeds/SOMELONGURL')


class ActivityFeedTest(unittest.TestCase):

  def setUp(self):
    self.feed = parse(test_data.SITES_ACTIVITY_FEED,
                      gdata.sites.data.ActivityFeed)

  def testToAndFromStringActivityFeed(self):
    self.assert_(isinstance(self.feed, gdata.sites.data.ActivityFeed))
    self.assertEqual(len(self.feed.entry), 2)
    for entry in self.feed.entry:
      self.assert_(isinstance(entry.summary, gdata.sites.data.Summary))
      self.assertEqual(entry.summary.type, 'xhtml')
      self.assert_(isinstance(entry.summary.html, atom.core.XmlElement))


class RevisionFeedTest(unittest.TestCase):

  def setUp(self):
    self.feed = parse(test_data.SITES_REVISION_FEED,
                      gdata.sites.data.RevisionFeed)

  def testToAndFromStringRevisionFeed(self):
    self.assert_(isinstance(self.feed, gdata.sites.data.RevisionFeed))
    self.assertEqual(len(self.feed.entry), 1)
    entry = self.feed.entry[0]
    self.assert_(isinstance(entry.content, gdata.sites.data.Content))
    self.assert_(isinstance(entry.content.html, atom.core.XmlElement))
    self.assertEqual(entry.content.type, 'xhtml')
    self.assertEqual(
        entry.FindParentLink(),
        'http://sites.google.com/feeds/content/site/siteName/54395424125706119')


class SiteFeedTest(unittest.TestCase):

  def setUp(self):
    self.feed = parse(test_data.SITES_SITE_FEED,
                      gdata.sites.data.SiteFeed)

  def testToAndFromStringSiteFeed(self):
    self.assert_(isinstance(self.feed, gdata.sites.data.SiteFeed))
    self.assertEqual(len(self.feed.entry), 2)
    entry = self.feed.entry[0]
    self.assert_(isinstance(entry.site_name, gdata.sites.data.SiteName))
    self.assertEqual(entry.title.text, 'New Test Site')
    self.assertEqual(entry.site_name.text, 'new-test-site')
    self.assertEqual(
        entry.FindAclLink(),
        'http://sites.google.com/feeds/acl/site/example.com/new-test-site')
    self.assertEqual(
        entry.FindSourceLink(),
        'http://sites.google.com/feeds/site/example.com/source-site')
    self.assertEqual(entry.theme.text, 'iceberg')


class AclFeedTest(unittest.TestCase):

  def setUp(self):
    self.feed = parse(test_data.SITES_ACL_FEED,
                      gdata.sites.data.AclFeed)

  def testToAndFromStringAclFeed(self):
    self.assert_(isinstance(self.feed, gdata.sites.data.AclFeed))
    self.assertEqual(len(self.feed.entry), 1)
    entry = self.feed.entry[0]
    self.assert_(isinstance(entry, gdata.sites.data.AclEntry))
    self.assert_(isinstance(entry.scope, gdata.acl.data.AclScope))
    self.assertEqual(entry.scope.type, 'user')
    self.assertEqual(entry.scope.value, 'user@example.com')
    self.assert_(isinstance(entry.role, gdata.acl.data.AclRole))
    self.assertEqual(entry.role.value, 'owner')
    self.assertEqual(
        entry.GetSelfLink().href,
        ('https://sites.google.com/feeds/acl/site/example.com/'
         'new-test-site/user%3Auser%40example.com'))


class DataClassSanityTest(unittest.TestCase):

  def test_basic_element_structure(self):
    conf.check_data_classes(self, [
        gdata.sites.data.Revision, gdata.sites.data.PageName,
        gdata.sites.data.Deleted, gdata.sites.data.Publisher,
        gdata.sites.data.Worksheet, gdata.sites.data.Header,
        gdata.sites.data.Column, gdata.sites.data.Data,
        gdata.sites.data.Field, gdata.sites.data.InReplyTo,
        gdata.sites.data.BaseSiteEntry, gdata.sites.data.ContentEntry,
        gdata.sites.data.ContentFeed, gdata.sites.data.ActivityEntry,
        gdata.sites.data.ActivityFeed, gdata.sites.data.RevisionEntry,
        gdata.sites.data.RevisionFeed, gdata.sites.data.Content,
        gdata.sites.data.Summary, gdata.sites.data.SiteName,
        gdata.sites.data.SiteEntry, gdata.sites.data.SiteFeed,
        gdata.sites.data.AclEntry, gdata.sites.data.AclFeed,
        gdata.sites.data.Theme])


def suite():
  return conf.build_suite([
      CommentEntryTest, ListPageEntryTest, ListItemEntryTest, BaseSiteEntryTest,
      ContentFeedTest, ActivityFeedTest, RevisionFeedTest, SiteFeedTest,
      AclFeedTest, DataClassSanityTest])


if __name__ == '__main__':
  unittest.main()
