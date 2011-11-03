#!/usr/bin/python
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

# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.

"""Live integration tests of the Google Documents List API.

  RESOURCES: Dict of test resource data, keyed on resource type.
"""

__author__ = 'vicfryzel@google.com (Vic Fryzel)'

import os
import os.path
import tempfile
import time
import unittest
import gdata.client
import gdata.data
import gdata.gauth
import gdata.docs.client
import gdata.docs.data
import gdata.test_config as conf


RESOURCES = {
    'document': (gdata.docs.data.DOCUMENT_LABEL,
                 'Text Document',
                 'data/test.0.doc',
                 'data/test.1.doc',
                 'application/msword',
                 'doc'),
    'empty_document': (gdata.docs.data.DOCUMENT_LABEL,
                       'Empty Text Document',
                       None,
                       'data/test.1.doc',
                       'application/msword',
                       'txt'),
    'spreadsheet': (gdata.docs.data.SPREADSHEET_LABEL,
                    'Spreadsheet',
                    'data/test.0.csv',
                    'data/test.1.csv',
                    'text/csv',
                    'csv'),
    'presentation': (gdata.docs.data.PRESENTATION_LABEL,
                     'Presentation',
                     'data/test.0.ppt',
                     'data/test.1.ppt',
                     'application/vnd.ms-powerpoint',
                     'ppt'),
    'drawing': (gdata.docs.data.DRAWING_LABEL,
                'Drawing',
                'data/test.0.wmf',
                'data/test.1.wmf',
                'application/x-msmetafile',
                'png'),
    'pdf': (gdata.docs.data.PDF_LABEL,
            'PDF',
            'data/test.0.pdf',
            'data/test.1.pdf',
            'application/pdf',
            None),
    'file': (gdata.docs.data.FILE_LABEL,
             'File',
             'data/test.0.bin',
             'data/test.1.bin',
             'application/octet-stream',
             None),
    'collection': (gdata.docs.data.COLLECTION_LABEL,
                   'Collection A',
                   None,
                   None,
                   None,
                   None)
}


class DocsTestCase(unittest.TestCase):
  def shortDescription(self):
    if hasattr(self, 'resource_type'):
      return '%s for %s' % (self.__class__.__name__, self.resource_type)
    else:
      return self.__class__.__name__

  def _delete(self, resource):
    try:
      self.client.DeleteResource(resource, permanent=True, force=True)
    except:
      pass

  def _delete_all(self):
    resources = self.client.GetAllResources(
        '/feeds/default/private/full?showfolders=true&showdeleted=true')
    for resource in resources:
      self._delete(resource)

  def _create(self):
    ms = None
    if self.resource_path is not None and self.resource_mime is not None:
      ms = gdata.data.MediaSource(
          file_path=os.path.join(os.path.dirname(__file__), self.resource_path),
          content_type=self.resource_mime)
    entry = gdata.docs.data.Resource(type=self.resource_label,
                                     title=self.resource_title)
    self.resource = self.client.CreateResource(entry, media=ms)

  def _update(self):
    ms = None
    if self.resource_alt_path is not None and self.resource_mime is not None:
      ms = gdata.data.MediaSource(
          file_path=os.path.join(os.path.dirname(__file__),
                                 self.resource_alt_path),
          content_type=self.resource_mime)
    self.resource.title.text = '%s Updated' % self.resource_title
    return self.client.UpdateResource(self.resource, media=ms, force=True,
                                      new_revision=True)

  def setUp(self):
    if conf.options.get_value('runlive') != 'true':
      raise RuntimeError('Live tests require --runlive true')

    self.client = gdata.docs.client.DocsClient()
    if conf.options.get_value('ssl') == 'false':
      self.client.ssl = False
    conf.configure_client(self.client, 'DocsTest', self.client.auth_service)
    conf.configure_cache(self.client, str(self.__class__))
    if conf.options.get_value('clean') == 'true':
      self._delete_all()

    tries = 0
    while tries < 3:
      try:
        tries += 1
        self._create()
        break
      except gdata.client.RequestError:
        if tries >= 2:
          self.tearDown()
          raise

  def tearDown(self):
    if conf.options.get_value('runlive') == 'true':
      if conf.options.get_value('clean') == 'true':
        self._delete_all()
      else:
        try:
          self._delete(self.resource)
        except:
          pass
    conf.close_client(self.client)


class ResourcesTest(DocsTestCase):
  def testGetAllResources(self):
    results = self.client.GetAllResources(
        '/feeds/default/private/full?showfolders=true')
    self.assert_(all(isinstance(item, gdata.docs.data.Resource) \
        for item in results))
    self.assertEqual(len(results), 1)

  def testGetResources(self):
    feed = self.client.GetResources(
        '/feeds/default/private/full?showfolders=true', limit=1)
    self.assert_(isinstance(feed, gdata.docs.data.ResourceFeed))
    self.assertEqual(len(feed.entry), 1)

  def testGetResource(self):
    entry = self.client.GetResource(self.resource)
    self.assert_(isinstance(entry, gdata.docs.data.Resource))
    self.assert_(entry.id.text is not None)
    self.assert_(entry.title.text is not None)
    self.assert_(entry.resource_id.text is not None)
    self.assert_(entry.title.text is not None)
    entry = self.client.GetResourceById(self.resource.resource_id.text)
    self.assert_(isinstance(entry, gdata.docs.data.Resource))
    self.assert_(entry.id.text is not None)
    self.assert_(entry.title.text is not None)
    self.assert_(entry.resource_id.text is not None)
    self.assert_(entry.title.text is not None)
    entry = self.client.GetResourceById(
        self.resource.resource_id.text.split(':')[1])
    self.assert_(isinstance(entry, gdata.docs.data.Resource))
    self.assert_(entry.id.text is not None)
    self.assert_(entry.title.text is not None)
    self.assert_(entry.resource_id.text is not None)
    self.assert_(entry.title.text is not None)
    entry = self.client.GetResourceBySelfLink(
        self.resource.GetSelfLink().href)
    self.assert_(isinstance(entry, gdata.docs.data.Resource))
    self.assert_(entry.id.text is not None)
    self.assert_(entry.title.text is not None)
    self.assert_(entry.resource_id.text is not None)
    self.assert_(entry.title.text is not None)

  def testMoveResource(self):
    entry = gdata.docs.data.Resource(
        type=gdata.docs.data.COLLECTION_LABEL,
        title='Collection B')
    collection = self.client.CreateResource(entry)

    # Start off in 0 collections
    self.assertEqual(len(self.resource.InCollections()), 0)

    # Move resource into collection
    entry = self.client.MoveResource(self.resource, collection)
    self.assertEqual(len(entry.InCollections()), 1)
    self.assertEqual(entry.InCollections()[0].title, collection.title.text)
    self.client.DeleteResource(collection, permanent=True, force=True)

  def testCopyResource(self):
    copy_title = '%s Copy' % self.resource_title
    # Copy only supported for document, spreadsheet, presentation types
    if self.resource_type in ['document', 'empty_document', 'spreadsheet',
                              'presentation']:
      copy = self.client.CopyResource(self.resource, copy_title)
      self.assertEqual(copy.title.text, copy_title)
      self.client.DeleteResource(copy, permanent=True, force=True)

    # TODO(vicfryzel): Expect appropriate error for drawings.
    elif self.resource_type != 'drawing':
      self.assertRaises(gdata.client.NotImplemented, self.client.CopyResource,
                        self.resource, copy_title)

  def testDownloadResource(self):
    tmp = tempfile.mkstemp()
    if self.resource_type != 'collection':
      if self.resource_export is not None:
        extra_params = {'exportFormat': self.resource_export,
                        'format': self.resource_export}
        self.client.DownloadResource(self.resource, tmp[1],
                                     extra_params=extra_params)
      else:
        self.client.DownloadResource(self.resource, tmp[1])
    else:
      # Cannot download collections
      self.assertRaises(ValueError, self.client.DownloadResource,
                        self.resource, tmp[1])

    # Should get a 404
    entry = gdata.docs.data.Resource(type=gdata.docs.data.DOCUMENT_LABEL,
                                     title='Does Not Exist')
    self.assertRaises(AttributeError, self.client.DownloadResource, entry,
                      tmp[1])
    os.close(tmp[0])
    os.remove(tmp[1])

  def testDownloadResourceToMemory(self):
    if self.resource_type != 'collection':
      data = None
      if self.resource_export is not None:
        extra_params = {'exportFormat': self.resource_export,
                        'format': self.resource_export}
        data = self.client.DownloadResourceToMemory(
            self.resource, extra_params=extra_params)
      else:
        data = self.client.DownloadResourceToMemory(self.resource)
      if self.resource_type == 'empty_document':
        self.assertEqual(len(data), 3)
      else:
        self.assertNotEqual(len(data), 0)
    else:
      # Cannot download collections
      self.assertRaises(ValueError, self.client.DownloadResourceToMemory,
                        self.resource)

  def testDelete(self):
    self.assertEqual(self.resource.deleted, None)
    self.client.DeleteResource(self.resource, force=True)
    self.resource = self.client.GetResource(self.resource)
    self.assertNotEqual(self.resource.deleted, None)
    self.client.DeleteResource(self.resource, permanent=True, force=True)
    self.assertRaises(gdata.client.RequestError, self.client.GetResource,
                      self.resource)


class AclTest(DocsTestCase):
  def testGetAcl(self):
    acl_feed = self.client.GetResourceAcl(self.resource)
    self.assert_(isinstance(acl_feed, gdata.docs.data.AclFeed))
    self.assertEqual(len(acl_feed.entry), 1)
    self.assert_(isinstance(acl_feed.entry[0], gdata.docs.data.AclEntry))
    self.assert_(acl_feed.entry[0].scope is not None)
    self.assert_(acl_feed.entry[0].role is not None)

  def testGetAclEntry(self):
    acl_feed = self.client.GetResourceAcl(self.resource)
    acl_entry = acl_feed.entry[0]
    same_acl_entry = self.client.GetAclEntry(acl_entry)
    self.assert_(isinstance(same_acl_entry, gdata.docs.data.AclEntry))
    self.assertEqual(acl_entry.GetSelfLink().href,
                     same_acl_entry.GetSelfLink().href)
    self.assertEqual(acl_entry.title.text, same_acl_entry.title.text)

  def testAddAclEntry(self):
    acl_entry_to_add = gdata.docs.data.AclEntry.GetInstance(
        role='writer', scope_type='default', key=True)

    new_acl_entry = self.client.AddAclEntry(self.resource, acl_entry_to_add)
    self.assertEqual(acl_entry_to_add.scope.type, new_acl_entry.scope.type)
    self.assertEqual(new_acl_entry.scope.value, None)
    # Key will always be overridden on add
    self.assertEqual(acl_entry_to_add.with_key.role.value,
                     new_acl_entry.with_key.role.value)
    acl_feed = self.client.GetResourceAcl(self.resource)
    self.assert_(isinstance(acl_feed, gdata.docs.data.AclFeed))
    self.assert_(isinstance(acl_feed.entry[0], gdata.docs.data.AclEntry))
    self.assert_(isinstance(acl_feed.entry[1], gdata.docs.data.AclEntry))

  def testUpdateAclEntry(self):
    acl_entry_to_add = gdata.docs.data.AclEntry.GetInstance(
        role='reader', scope_type='user', scope_value='jeff@example.com',
        key=True)
    other_acl_entry = gdata.docs.data.AclEntry.GetInstance(
        role='writer', scope_type='user', scope_value='jeff@example.com')

    new_acl_entry = self.client.AddAclEntry(self.resource, acl_entry_to_add)
    new_acl_entry.with_key = None
    new_acl_entry.scope = other_acl_entry.scope
    new_acl_entry.role = other_acl_entry.role
    updated_acl_entry = self.client.UpdateAclEntry(new_acl_entry)

    self.assertEqual(updated_acl_entry.GetSelfLink().href,
                     new_acl_entry.GetSelfLink().href)
    self.assertEqual(updated_acl_entry.title.text, new_acl_entry.title.text)
    self.assertEqual(updated_acl_entry.scope.type, other_acl_entry.scope.type)
    self.assertEqual(updated_acl_entry.scope.value, other_acl_entry.scope.value)
    self.assertEqual(updated_acl_entry.role.value, other_acl_entry.role.value)
    self.assertEqual(updated_acl_entry.with_key, None)

  def testDeleteAclEntry(self):
    acl_entry_to_add = gdata.docs.data.AclEntry.GetInstance(
        role='writer', scope_type='user', scope_value='joe@example.com',
        key=True)
    acl_feed = self.client.GetResourceAcl(self.resource)
    new_acl_entry = self.client.AddAclEntry(self.resource, acl_entry_to_add)
    acl_feed = self.client.GetResourceAcl(self.resource)

    self.assert_(isinstance(acl_feed, gdata.docs.data.AclFeed))
    self.assertEqual(len(acl_feed.entry), 2)
    self.assert_(isinstance(acl_feed.entry[0], gdata.docs.data.AclEntry))
    self.assert_(isinstance(acl_feed.entry[1], gdata.docs.data.AclEntry))

    self.client.DeleteAclEntry(new_acl_entry)

    acl_feed = self.client.GetResourceAcl(self.resource)
    self.assert_(isinstance(acl_feed, gdata.docs.data.AclFeed))
    self.assertEqual(len(acl_feed.entry), 1)
    self.assert_(isinstance(acl_feed.entry[0], gdata.docs.data.AclEntry))


class RevisionsTest(DocsTestCase):
  def testGetRevisions(self):
    # There are no revisions of collections
    if self.resource_type != 'collection':
      revisions = self.client.GetRevisions(self.resource)
      self.assert_(isinstance(revisions, gdata.docs.data.RevisionFeed))
      self.assert_(isinstance(revisions.entry[0], gdata.docs.data.Revision))
      # Currently, there is a bug where new presentations have 2 revisions.
      if self.resource_type != 'presentation':
        self.assertEqual(len(revisions.entry), 1)

  def testGetRevision(self):
    # There are no revisions of collections
    if self.resource_type != 'collection':
      revisions = self.client.GetRevisions(self.resource)
      entry = revisions.entry[0]
      new_entry = self.client.GetRevision(entry)
      self.assertEqual(entry.GetSelfLink().href, new_entry.GetSelfLink().href)
      self.assertEqual(entry.title.text, new_entry.title.text)

  def testGetRevisionBySelfLink(self):
    # There are no revisions of collections
    if self.resource_type != 'collection':
      revisions = self.client.GetRevisions(self.resource)
      entry = revisions.entry[0]
      new_entry = self.client.GetRevisionBySelfLink(entry.GetSelfLink().href)
      self.assertEqual(entry.GetSelfLink().href, new_entry.GetSelfLink().href)
      self.assertEqual(entry.title.text, new_entry.title.text)

  def testMultipleRevisionsAndUpdateResource(self):
    if self.resource_type not in ['collection', 'presentation']:
      revisions = self.client.GetRevisions(self.resource)
      self.assertEqual(len(revisions.entry), 1)
    # Currently, there is a bug where uploaded presentations have 2 revisions.
    elif self.resource_type == 'presentation':
      revisions = self.client.GetRevisions(self.resource)
      self.assertEqual(len(revisions.entry), 2)

    # Drawings do not currently support update, thus the rest of these 
    # tests do not yet work as expected.
    if self.resource_type == 'drawing':
      return

    entry = self._update()
    self.assertEqual(entry.title.text, '%s Updated' % self.resource_title)

    if self.resource_type != 'collection':
      revisions = self.client.GetRevisions(entry)
      self.assert_(isinstance(revisions, gdata.docs.data.RevisionFeed))
      if self.resource_type == 'presentation':
        self.assertEqual(len(revisions.entry), 3)
        self.assert_(isinstance(revisions.entry[2], gdata.docs.data.Revision))
      else:
        self.assertEqual(len(revisions.entry), 2)
      self.assert_(isinstance(revisions.entry[0], gdata.docs.data.Revision))
      self.assert_(isinstance(revisions.entry[1], gdata.docs.data.Revision))

  def testPublishRevision(self):
    if self.resource_type in ['file', 'pdf', 'collection']:
      return

    # Drawings do not currently support update, thus this test would fail.
    if self.resource_type == 'drawing':
      return

    entry = self._update()
    revisions = self.client.GetRevisions(entry)
    revision = self.client.PublishRevision(revisions.entry[1])
    # Currently, there is a bug where uploaded presentations have 2 revisions.
    if self.resource_type == 'presentation':
      revisions = self.client.GetRevisions(entry)
      revision = revisions.entry[2]
    self.assert_(isinstance(revision, gdata.docs.data.Revision))
    self.assertEqual(revision.publish.value, 'true')
    self.assertEqual(revision.publish_auto.value, 'false')

    # The rest of the tests require an Apps domain
    if 'gmail' in conf.options.get_value('username'):
      return

    self.assertEqual(revision.publish_outside_domain.value, 'false')

    # Empty documents won't have further revisions b/c content didn't change
    if self.resource_type == 'empty_document':
      return

    revisions = self.client.GetRevisions(entry)
    if self.resource_type == 'presentation':
      revision = self.client.PublishRevision(
          revisions.entry[2], publish_auto=True, publish_outside_domain=True)
    else:
      revision = self.client.PublishRevision(
          revisions.entry[1], publish_auto=True, publish_outside_domain=True)
      if self.resource_type == 'spreadsheet':
        revision = client.GetRevisions(entry).entry[1]
    self.assert_(isinstance(revision, gdata.docs.data.Revision))
    self.assertEqual(revision.publish.value, 'true')
    self.assertEqual(revision.publish_auto.value, 'true')
    self.assertEqual(revision.publish_outside_domain.value, 'true')

    revision = self.client.GetRevision(revisions.entry[0])
    self.assertEqual(revision.publish, None)
    self.assertEqual(revision.publish_auto, None)
    self.assertEqual(revision.publish_outside_domain, None)

  def testDownloadRevision(self):
    if self.resource_type == 'collection':
      return

    revisions = self.client.GetRevisions(self.resource)
    tmp = tempfile.mkstemp()
    self.client.DownloadRevision(revisions.entry[0], tmp[1])
    os.close(tmp[0])
    os.remove(tmp[1])

  def testDeleteRevision(self):
    # API can only delete file revisions
    if self.resource_type != 'file':
      return

    entry = self._update()
    revisions = self.client.GetRevisions(entry)
    self.assertEqual(len(revisions.entry), 2)
    self.client.DeleteRevision(revisions.entry[1])
    self.assert_(isinstance(revisions, gdata.docs.data.RevisionFeed))
    self.assert_(isinstance(revisions.entry[0], gdata.docs.data.Revision))
    revisions = self.client.GetRevisions(entry)
    self.assertEqual(len(revisions.entry), 1)


class ChangesTest(DocsTestCase):
  def testGetChanges(self):
    # This test assumes that by the time this test is run, the account
    # being used already has a number of changes

    changes = self.client.GetChanges(max_results=5)
    self.assert_(isinstance(changes, gdata.docs.data.ChangeFeed))
    self.assert_(len(changes.entry) <= 5)
    self.assert_(isinstance(changes.entry[0], gdata.docs.data.Change))
    self._update()
    changes = self.client.GetChanges(changes.entry[0].changestamp.value, 5)
    self.assert_(isinstance(changes, gdata.docs.data.ChangeFeed))
    self.assert_(len(changes.entry) <= 5)
    self.assert_(isinstance(changes.entry[0], gdata.docs.data.Change))

  def testDeleteResourceCreatesNewChange(self):
    """Ensure that deleting a resource causes a new change entry."""
    self._update()
    changes = self.client.GetChanges(max_results=1)
    latest = changes.entry[0].changestamp.value
    self._delete(self.resource)
    time.sleep(10)
    changes = self.client.GetChanges(max_results=1)
    self.assert_(latest < changes.entry[0].changestamp.value)


class MetadataTest(DocsTestCase):
  def setUp(self):
    if conf.options.get_value('runlive') != 'true':
      raise RuntimeError('Live tests require --runlive true')
    else:
      self.client = gdata.docs.client.DocsClient()
      if conf.options.get_value('ssl') == 'true':
        self.client.ssl = True
      conf.configure_client(self.client, 'DocsTest', self.client.auth_service)
      conf.configure_cache(self.client, str(self.__class__))
      if conf.options.get_value('clean') == 'true':
        self._delete_all()

  def tearDown(self):
    conf.close_client(self.client)

  def testMetadata(self):
    metadata = self.client.GetMetadata()
    self.assert_(isinstance(metadata, gdata.docs.data.Metadata))
    self.assertNotEqual(int(metadata.quota_bytes_total.text), 0)
    self.assertEqual(int(metadata.quota_bytes_used.text), 0)
    self.assertEqual(int(metadata.quota_bytes_used_in_trash.text), 0)
    self.assertNotEqual(len(metadata.import_formats), 0)
    self.assertNotEqual(len(metadata.export_formats), 0)
    self.assertNotEqual(len(metadata.features), 0)
    self.assertNotEqual(len(metadata.max_upload_sizes), 0)


def suite():
  suite = unittest.TestSuite()
  for key, value in RESOURCES.iteritems():
    for case in [ResourcesTest, AclTest, RevisionsTest, ChangesTest]:
      tests = unittest.TestLoader().loadTestsFromTestCase(case)
      for test in tests:
        test.resource_type = key
        test.resource_label = value[0]
        test.resource_title = value[1]
        test.resource_path = value[2]
        test.resource_alt_path = value[3]
        test.resource_mime = value[4]
        test.resource_export = value[5]
        suite.addTest(test)
  suite.addTests(unittest.TestLoader().loadTestsFromTestCase(MetadataTest))
  return suite


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
