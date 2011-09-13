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
import gdata.docs.data
import gdata.test_config as conf


class DocsEntryTest(unittest.TestCase):

  def setUp(self):
    self.entry = atom.core.parse(test_data.DOCUMENT_LIST_ENTRY_V3,
                                 gdata.docs.data.Resource)

  def testToAndFromStringDocsEntry(self):
    self.assert_(isinstance(self.entry, gdata.docs.data.Resource))
    self.assertEqual(self.entry.GetResourceType(), 'spreadsheet')
    self.assert_(isinstance(self.entry.last_viewed, gdata.docs.data.LastViewed))
    self.assertEqual(self.entry.last_viewed.text, '2009-03-05T07:48:21.493Z')
    self.assert_(
        isinstance(self.entry.last_modified_by, gdata.docs.data.LastModifiedBy))
    self.assertEqual(
        self.entry.last_modified_by.email.text, 'test.user@gmail.com')
    self.assertEqual(self.entry.last_modified_by.name.text, 'test.user')
    self.assert_(isinstance(self.entry.resource_id, gdata.docs.data.ResourceId))
    self.assertEqual(self.entry.resource_id.text,
                     'spreadsheet:supercalifragilisticexpealidocious')
    self.assert_(isinstance(self.entry.writers_can_invite,
                            gdata.docs.data.WritersCanInvite))
    self.assertEqual(self.entry.writers_can_invite.value, 'true')
    self.assert_(isinstance(self.entry.quota_bytes_used,
                            gdata.docs.data.QuotaBytesUsed))
    self.assertEqual(self.entry.quota_bytes_used.text, '1000')
    self.assertEqual(len(self.entry.feed_link), 2)
    self.assert_(isinstance(self.entry.feed_link[0], gdata.data.FeedLink))

    self.assertEqual(
        self.entry.GetAclFeedLink().href,
        ('https://docs.google.com/feeds/default/private/full/'
         'spreadsheet%3Asupercalifragilisticexpealidocious/acl'))
    self.assertEqual(
        self.entry.GetRevisionsFeedLink().href,
        ('https://docs.google.com/feeds/default/private/full/'
         'spreadsheet%3Asupercalifragilisticexpealidocious/revisions'))

    self.assertEqual(len(self.entry.InCollections()), 1)
    self.assertEqual(self.entry.InCollections()[0].title, 'AFolderName')


class AclTest(unittest.TestCase):

  def setUp(self):
    self.acl_entry = atom.core.parse(test_data.DOCUMENT_LIST_ACL_ENTRY,
                                     gdata.docs.data.AclEntry)
    self.acl_entry_withkey = atom.core.parse(
      test_data.DOCUMENT_LIST_ACL_WITHKEY_ENTRY, gdata.docs.data.AclEntry)
    self.acl_entry_additional_role = atom.core.parse(
      test_data.DOCUMENT_LIST_ACL_ADDITIONAL_ROLE_ENTRY,
      gdata.docs.data.AclEntry)

  def testToAndFromString(self):
    self.assert_(isinstance(self.acl_entry, gdata.docs.data.AclEntry))
    self.assert_(isinstance(self.acl_entry.role, gdata.acl.data.AclRole))
    self.assert_(isinstance(self.acl_entry.scope, gdata.acl.data.AclScope))
    self.assertEqual(self.acl_entry.scope.value, 'user@gmail.com')
    self.assertEqual(self.acl_entry.scope.type, 'user')
    self.assertEqual(self.acl_entry.role.value, 'writer')

    acl_entry_str = str(self.acl_entry)
    new_acl_entry = atom.core.parse(acl_entry_str, gdata.docs.data.AclEntry)
    self.assert_(isinstance(new_acl_entry, gdata.docs.data.AclEntry))
    self.assert_(isinstance(new_acl_entry.role, gdata.acl.data.AclRole))
    self.assert_(isinstance(new_acl_entry.scope, gdata.acl.data.AclScope))
    self.assertEqual(new_acl_entry.scope.value, self.acl_entry.scope.value)
    self.assertEqual(new_acl_entry.scope.type, self.acl_entry.scope.type)
    self.assertEqual(new_acl_entry.role.value, self.acl_entry.role.value)

  def testToAndFromStringWithKey(self):
    self.assert_(isinstance(self.acl_entry_withkey, gdata.docs.data.AclEntry))
    self.assert_(self.acl_entry_withkey.role is None)
    self.assert_(isinstance(self.acl_entry_withkey.with_key,
                            gdata.acl.data.AclWithKey))
    self.assert_(isinstance(self.acl_entry_withkey.with_key.role,
                            gdata.acl.data.AclRole))
    self.assert_(isinstance(self.acl_entry_withkey.scope,
                            gdata.acl.data.AclScope))
    self.assertEqual(self.acl_entry_withkey.with_key.key, 'somekey')
    self.assertEqual(self.acl_entry_withkey.with_key.role.value, 'writer')
    self.assertEqual(self.acl_entry_withkey.scope.value, 'example.com')
    self.assertEqual(self.acl_entry_withkey.scope.type, 'domain')

    acl_entry_withkey_str = str(self.acl_entry_withkey)
    new_acl_entry_withkey = atom.core.parse(acl_entry_withkey_str,
                                            gdata.docs.data.AclEntry)
    self.assert_(isinstance(new_acl_entry_withkey, gdata.docs.data.AclEntry))
    self.assert_(new_acl_entry_withkey.role is None)
    self.assert_(isinstance(new_acl_entry_withkey.with_key,
                            gdata.acl.data.AclWithKey))
    self.assert_(isinstance(new_acl_entry_withkey.with_key.role,
                            gdata.acl.data.AclRole))
    self.assert_(isinstance(new_acl_entry_withkey.scope,
                            gdata.acl.data.AclScope))
    self.assertEqual(new_acl_entry_withkey.with_key.key,
                     self.acl_entry_withkey.with_key.key)
    self.assertEqual(new_acl_entry_withkey.with_key.role.value,
                     self.acl_entry_withkey.with_key.role.value)
    self.assertEqual(new_acl_entry_withkey.scope.value,
                     self.acl_entry_withkey.scope.value)
    self.assertEqual(new_acl_entry_withkey.scope.type,
                     self.acl_entry_withkey.scope.type)

  def testCreateNewAclEntry(self):
    cat = gdata.atom.Category(
        term='http://schemas.google.com/acl/2007#accessRule',
        scheme='http://schemas.google.com/g/2005#kind')
    acl_entry = gdata.docs.DocumentListAclEntry(category=[cat])
    acl_entry.scope = gdata.docs.Scope(value='user@gmail.com', type='user')
    acl_entry.role = gdata.docs.Role(value='writer')
    self.assert_(isinstance(acl_entry, gdata.docs.DocumentListAclEntry))
    self.assert_(isinstance(acl_entry.role, gdata.docs.Role))
    self.assert_(isinstance(acl_entry.scope, gdata.docs.Scope))
    self.assertEqual(acl_entry.scope.value, 'user@gmail.com')
    self.assertEqual(acl_entry.scope.type, 'user')
    self.assertEqual(acl_entry.role.value, 'writer')

  def testAdditionalRole(self):
    self.assertEqual(
        self.acl_entry_additional_role.additional_role.value,
        'commenter')
    self.assertEqual(
        self.acl_entry_additional_role.with_key.additional_role.value,
        'commenter')


class AclFeedTest(unittest.TestCase):

  def setUp(self):
    self.feed = atom.core.parse(test_data.DOCUMENT_LIST_ACL_FEED,
                                gdata.docs.data.AclFeed)

  def testToAndFromString(self):
    for entry in self.feed.entry:
      self.assert_(isinstance(entry, gdata.docs.data.AclEntry))

    feed = atom.core.parse(str(self.feed), gdata.docs.data.AclFeed)
    for entry in feed.entry:
      self.assert_(isinstance(entry, gdata.docs.data.AclEntry))

  def testConvertActualData(self):
    entries = self.feed.entry
    self.assert_(len(entries) == 2)
    self.assertEqual(entries[0].title.text,
                     'Document Permission - user@gmail.com')
    self.assertEqual(entries[0].role.value, 'owner')
    self.assertEqual(entries[0].scope.type, 'user')
    self.assertEqual(entries[0].scope.value, 'user@gmail.com')
    self.assert_(entries[0].GetSelfLink() is not None)
    self.assert_(entries[0].GetEditLink() is not None)
    self.assertEqual(entries[1].title.text,
                     'Document Permission - user2@google.com')
    self.assertEqual(entries[1].role.value, 'writer')
    self.assertEqual(entries[1].scope.type, 'domain')
    self.assertEqual(entries[1].scope.value, 'google.com')
    self.assert_(entries[1].GetSelfLink() is not None)
    self.assert_(entries[1].GetEditLink() is not None)


class RevisionFeedTest(unittest.TestCase):

  def setUp(self):
    self.feed = atom.core.parse(test_data.DOCUMENT_LIST_REVISION_FEED,
                                gdata.docs.data.RevisionFeed)

  def testToAndFromString(self):
    for entry in self.feed.entry:
      self.assert_(isinstance(entry, gdata.docs.data.Revision))

    feed = atom.core.parse(str(self.feed), gdata.docs.data.RevisionFeed)
    for entry in feed.entry:
      self.assert_(isinstance(entry, gdata.docs.data.Revision))

  def testConvertActualData(self):
    entries = self.feed.entry
    self.assert_(len(entries) == 1)
    self.assertEqual(entries[0].title.text, 'Revision 2')
    self.assertEqual(entries[0].publish.value, 'true')
    self.assertEqual(entries[0].publish_auto.value, 'true')
    self.assertEqual(entries[0].publish_outside_domain.value, 'false')
    self.assertEqual(
         entries[0].GetPublishLink().href,
         'https://docs.google.com/View?docid=dfr4&pageview=1&hgd=1')
    self.assertEqual(
         entries[0].FindPublishLink(),
         'https://docs.google.com/View?docid=dfr4&pageview=1&hgd=1')


class DataClassSanityTest(unittest.TestCase):

  def test_basic_element_structure(self):
    conf.check_data_classes(self, [
        gdata.docs.data.ResourceId, gdata.docs.data.LastModifiedBy,
        gdata.docs.data.LastViewed, gdata.docs.data.WritersCanInvite,
        gdata.docs.data.QuotaBytesUsed, gdata.docs.data.Publish,
        gdata.docs.data.PublishAuto, gdata.docs.data.PublishOutsideDomain,
        gdata.docs.data.Resource, gdata.docs.data.AclEntry, gdata.docs.data.AclFeed,
        gdata.docs.data.ResourceFeed, gdata.docs.data.Revision,
        gdata.docs.data.RevisionFeed])


class CategoryTest(unittest.TestCase):

  def setUp(self):
    self.entry = atom.core.parse(test_data.DOCUMENT_LIST_ENTRY_V3,
                                 gdata.docs.data.Resource)

  def testAddCategory(self):
    entry = gdata.docs.data.Resource()
    entry.AddCategory('test_scheme', 'test_term', 'test_label')
    self.assertEqual(entry.GetFirstCategory('test_scheme').scheme,
                     'test_scheme')
    self.assertEqual(entry.GetFirstCategory('test_scheme').term, 'test_term')
    self.assertEqual(entry.GetFirstCategory('test_scheme').label, 'test_label')

  def testGetFirstCategory(self):
    entry = gdata.docs.data.Resource()
    cat1 = entry.AddCategory('test_scheme', 'test_term1', 'test_label1')
    cat2 = entry.AddCategory('test_scheme', 'test_term2', 'test_label2')
    self.assertEqual(entry.GetFirstCategory('test_scheme'), cat1)

  def testGetCategories(self):
    cat1 = self.entry.AddCategory('test_scheme', 'test_term1', 'test_label1')
    cat2 = self.entry.AddCategory('test_scheme', 'test_term2', 'test_label2')
    cats = list(self.entry.GetCategories('test_scheme'))
    self.assertTrue(cat1 in cats)
    self.assertTrue(cat2 in cats)

  def testRemoveCategories(self):
    self.entry.RemoveCategories(gdata.docs.data.LABELS_SCHEME)
    self.assertEqual(self.entry.GetLabels(), set())

  def testResourceType(self):
    entry = gdata.docs.data.Resource('spreadsheet')
    self.assertEqual(self.entry.GetResourceType(), 'spreadsheet')

  def testGetResourceType(self):
    self.assertEqual(self.entry.GetResourceType(), 'spreadsheet')

  def testSetResourceType(self):
    self.assertEqual(self.entry.GetResourceType(), 'spreadsheet')
    self.entry.SetResourceType('drawing')
    self.assertEqual(self.entry.GetResourceType(), 'drawing')

  def testGetLabels(self):
    self.assertEqual(self.entry.GetLabels(),
                     set(['mine', 'private', 'restricted-download',
                          'shared-with-domain', 'viewed', 'starred', 'hidden',
                          'trashed']))

  def testAddLabel(self):
    entry = gdata.docs.data.Resource()
    entry.AddLabel('banana')
    self.assertTrue('banana' in entry.GetLabels())

  def testRemoveLabel(self):
    entry = gdata.docs.data.Resource()
    entry.AddLabel('banana')
    entry.AddLabel('orange')
    self.assertTrue('banana' in entry.GetLabels())
    self.assertTrue('orange' in entry.GetLabels())
    entry.RemoveLabel('orange')
    self.assertFalse('orange' in entry.GetLabels())

  def testIsHidden(self):
    self.assertTrue(self.entry.IsHidden())

  def testIsNotHidden(self):
    self.entry.remove_categories(gdata.docs.data.LABELS_SCHEME)
    self.assertFalse(self.entry.IsHidden())

  def testIsViewed(self):
    self.assertTrue(self.entry.IsViewed())

  def testIsNotViewed(self):
    self.entry.remove_categories(gdata.docs.data.LABELS_SCHEME)
    self.assertFalse(self.entry.IsViewed())

  def testIsStarred(self):
    self.assertTrue(self.entry.IsStarred())

  def testIsNotStarred(self):
    self.entry.remove_categories(gdata.docs.data.LABELS_SCHEME)
    self.assertFalse(self.entry.IsStarred())

  def testIsTrashed(self):
    self.assertTrue(self.entry.IsTrashed())

  def testIsNotTrashed(self):
    self.entry.remove_categories(gdata.docs.data.LABELS_SCHEME)
    self.assertFalse(self.entry.IsTrashed())

  def testIsPrivate(self):
    self.assertTrue(self.entry.IsPrivate())

  def testIsNotPrivate(self):
    self.entry.remove_categories(gdata.docs.data.LABELS_SCHEME)
    self.assertFalse(self.entry.IsPrivate())

  def testIsMine(self):
    self.assertTrue(self.entry.IsMine())

  def testIsNotMine(self):
    self.entry.remove_categories(gdata.docs.data.LABELS_SCHEME)
    self.assertFalse(self.entry.IsMine())

  def testIsSharedWithDomain(self):
    self.assertTrue(self.entry.IsSharedWithDomain())

  def testIsNotSharedWithDomain(self):
    self.entry.remove_categories(gdata.docs.data.LABELS_SCHEME)
    self.assertFalse(self.entry.IsSharedWithDomain())

  def testIsRestrictedDownload(self):
    self.assertTrue(self.entry.IsRestrictedDownload())

  def testIsNotRestrictedDownload(self):
    self.entry.remove_categories(gdata.docs.data.LABELS_SCHEME)
    self.assertFalse(self.entry.IsRestrictedDownload())


class MetadataTest(unittest.TestCase):

  def setUp(self):
    self.entry = atom.core.parse(test_data.DOCUMENT_LIST_METADATA,
                                 gdata.docs.data.Metadata)

  def testAdditionalRoleInfo(self):
    self.assertEqual(self.entry.additional_role_info[0].kind, 'document')

  def testAdditionalRoleSet(self):
    self.assertEqual(
        self.entry.additional_role_info[0].additional_role_set[0].primaryRole,
        'reader')

  def testAdditionalRole(self):
    self.assertEqual(
        self.entry.additional_role_info[0].additional_role_set[0].\
            additional_role[0].value, 'commenter')


def suite():
  return conf.build_suite(
      [DataClassSanityTest, CategoryTest, DocsHelperTest, DocsEntryTest,
       AclTest, AclFeed, MetadataTest])


if __name__ == '__main__':
  unittest.main()
