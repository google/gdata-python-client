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

# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.


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


class DocsTestCase(unittest.TestCase):
  resources = [
      (gdata.docs.data.DOCUMENT_LABEL, 'Text Document', 'document',
       'data/test.doc', 'application/msword', 'doc'),
      (gdata.docs.data.DOCUMENT_LABEL, 'Empty Text Document', 'empty_document',
       None, None, 'txt'),
      (gdata.docs.data.SPREADSHEET_LABEL, 'Spreadsheet', 'spreadsheet',
       'data/test.csv', 'text/csv', 'csv'),
      (gdata.docs.data.PRESENTATION_LABEL, 'Presentation', 'presentation',
       'data/test.ppt', 'application/vnd.ms-powerpoint', 'ppt'),
      (gdata.docs.data.DRAWING_LABEL, 'Drawing', 'drawing',
       'data/test.wmf', 'application/x-msmetafile', 'png'),
      (gdata.docs.data.PDF_LABEL, 'PDF', 'pdf',
       'data/test.pdf', 'application/pdf', None),
      (gdata.docs.data.FILE_LABEL, 'File', 'file',
       'data/test.bin', 'application/octet-stream', None),
      (gdata.docs.data.COLLECTION_LABEL, 'Collection 1', 'collection1',
       None, None, None),
      (gdata.docs.data.COLLECTION_LABEL, 'Collection 2', 'collection2',
       None, None, None)
  ]

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

  def _create(self, resource):
    ms = None
    if resource[3] is not None and resource[4] is not None:
      ms = gdata.data.MediaSource(
          file_path=os.path.join(os.path.dirname(__file__), resource[3]),
          content_type=resource[4])
    entry = gdata.docs.data.DocsEntry(
        type=resource[0],
        title=resource[1])
    setattr(self, resource[2], self.client.CreateResource(entry, media=ms))

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
      for resource in self.resources:
        tries = 0
        while tries < 3:
          try:
            self._create(resource)
            tries += 1
            break
          except gdata.client.RequestError:
            if tries == 2:
              self.tearDown()
              raise

  def tearDown(self):
    if conf.options.get_value('runlive') == 'true':
      for resource in self.resources:
        try:
          self._delete(getattr(self, resource[2]))
        except:
          pass
    if conf.options.get_value('clean') == 'true':
      self._delete_all()
    conf.close_client(self.client)


class ResourcesTest(DocsTestCase):
  def testGetAllResources(self):
    results = self.client.GetAllResources()
    self.assert_(all(isinstance(item, gdata.docs.data.DocsEntry) \
        for item in results))
    self.assertEqual(len(results), 7)

    results = self.client.GetAllResources(
        '/feeds/default/private/full?showfolders=true')
    self.assert_(all(isinstance(item, gdata.docs.data.DocsEntry) \
        for item in results))
    self.assertEqual(len(results), 9)

  def testGetResources(self):
    feed = self.client.GetResources(limit=1)
    self.assert_(isinstance(feed, gdata.docs.data.DocList))
    self.assertEqual(len(feed.entry), 1)

  def testGetResource(self):
    entry = None
    for resource in self.resources:
      entry = self.client.GetResource(getattr(self, resource[2]))
      self.assert_(isinstance(entry, gdata.docs.data.DocsEntry))
      self.assert_(entry.id.text is not None)
      self.assert_(entry.title.text is not None)
      self.assert_(entry.resource_id.text is not None)
      self.assert_(entry.title.text is not None)
      entry = self.client.GetResourceBySelfLink(
          getattr(self, resource[2]).GetSelfLink().href)
      self.assert_(isinstance(entry, gdata.docs.data.DocsEntry))
      self.assert_(entry.id.text is not None)
      self.assert_(entry.title.text is not None)
      self.assert_(entry.resource_id.text is not None)
      self.assert_(entry.title.text is not None)

  def testMove(self):
    entry = None
    for resource in self.resources:
      entry = getattr(self, resource[2])
      # Start off in 0 collections
      self.assertEqual(len(entry.InCollections()), 0)
      
      # Move resource into collection
      if resource[2] != 'collection2':
        entry = self.client.MoveResource(entry, self.collection2)
        self.assertEqual(len(entry.InCollections()), 1)
        self.assertEqual(entry.InCollections()[0].title,
                         self.collection2.title.text)
      else:
        # Can't move a collection into itself
        self.assertRaises(
            gdata.client.RequestError,
            lambda: self.client.MoveResource(self.collection2, self.collection2))

  def testCopy(self):
    entry = None
    for resource in self.resources:
      entry = getattr(self, resource[2])

      if resource[2] not in \
          ['file', 'pdf', 'collection1', 'collection2', 'drawing']:
        copy = self.client.CopyResource(entry, '%s Copy' % resource[1])
        self.assertEqual(copy.title.text, '%s Copy' % resource[1])
        self.client.DeleteResource(copy, force=True)
      elif resource[2] != 'drawing':
        self.assertRaises(gdata.client.NotImplemented, self.client.CopyResource,
                          entry, '%s Copy' % resource[1])

  def testDownloadResource(self):
    entry = None
    for resource in self.resources:
      entry = getattr(self, resource[2])
      tmp = tempfile.mkstemp()
      if resource[2] != 'collection1' and resource[2] != 'collection2':
        if resource[5] is not None:
          extra_params = {'exportFormat': resource[5], 'format': resource[5]}
          self.client.DownloadResource(entry, tmp[1], extra_params=extra_params)
        else:
          self.client.DownloadResource(entry, tmp[1])
      else:
        # Cannot download collections
        self.assertRaises(ValueError, self.client.DownloadResource, entry,
                          tmp[1])
      os.close(tmp[0])
      os.remove(tmp[1])

    # Should get a 404
    entry = gdata.docs.data.DocsEntry(type=gdata.docs.data.DOCUMENT_LABEL,
                                      title='Does Not Exist')
    tmp = tempfile.mkstemp()
    self.assertRaises(AttributeError, self.client.DownloadResource, entry,
                      tmp[1])
    os.close(tmp[0])
    os.remove(tmp[1])

  def testDownloadResourceToMemory(self):
    entry = None
    for resource in self.resources:
      entry = getattr(self, resource[2])
      if resource[2] != 'collection1' and resource[2] != 'collection2':
        data = None
        if resource[5] is not None:
          extra_params = {'exportFormat': resource[5], 'format': resource[5]}
          data = self.client.DownloadResourceToMemory(
              entry, extra_params=extra_params)
        else:
          data = self.client.DownloadResourceToMemory(entry)
        self.assertNotEqual(len(data), 0)
      else:
        # Cannot download collections
        self.assertRaises(ValueError, self.client.DownloadResourceToMemory,
                          entry)

  def testDelete(self):
    entry = None
    for resource in self.resources:
      entry = getattr(self, resource[2])
      self.assertEqual(entry.deleted, None)
      self.client.DeleteResource(entry, force=True)
      entry = self.client.GetResource(entry)
      self.assertNotEqual(entry.deleted, None)
      self.client.DeleteResource(entry, permanent=True, force=True)
      self.assertRaises(gdata.client.RequestError, self.client.GetResource,
                        entry)


class AclTest(DocsTestCase):
  def testGetAcl(self):
    for resource in self.resources:
      entry = getattr(self, resource[2])
      acl_feed = self.client.GetResourceAcl(entry)
      self.assert_(isinstance(acl_feed, gdata.docs.data.AclFeed))
      self.assertEqual(len(acl_feed.entry), 1)
      self.assert_(isinstance(acl_feed.entry[0], gdata.docs.data.AclEntry))
      self.assert_(acl_feed.entry[0].scope is not None)
      self.assert_(acl_feed.entry[0].role is not None)

  def testGetAclEntry(self):
    for resource in self.resources:
      entry = getattr(self, resource[2])
      acl_feed = self.client.GetResourceAcl(entry)
      acl_entry = acl_feed.entry[0]
      same_acl_entry = self.client.GetAclEntry(acl_entry)
      self.assert_(isinstance(same_acl_entry, gdata.docs.data.AclEntry))
      self.assertEqual(acl_entry.GetSelfLink().href,
                       same_acl_entry.GetSelfLink().href)
      self.assertEqual(acl_entry.title.text, same_acl_entry.title.text)

  def testAddAclEntry(self):
    acl_entry = gdata.docs.data.AclEntry(
        role='writer', scope_type='domain', scope_value='example.com',
        key=True)
    
    for resource in self.resources:
      entry = getattr(self, resource[2])
      new_acl_entry = self.client.AddAclEntry(entry, acl_entry_to_add)
      self.assertEqual(acl_entry.GetSelfLink().href,
                       new_acl_entry.GetSelfLink().href)
      self.assertEqual(acl_entry.title.text, new_acl_entry.title.text)
      self.assertEqual(acl_entry.scope.type, new_acl_entry.scope.type)
      self.assertEqual(acl_entry.scope.value, new_acl_entry.scope.value)
      self.assertEqual(acl_entry.with_key.role.value,
                       new_acl_entry.with_key.role.value)
      acl_feed = self.client.GetResourceAcl(entry)
      self.assert_(isinstance(acl_feed, gdata.docs.data.AclFeed))
      self.assert_(isinstance(acl_feed.entry[0], gdata.docs.data.AclEntry))
      self.assert_(isinstance(acl_feed.entry[1], gdata.docs.data.AclEntry))

  def testUpdateAclEntry(self):
    acl_entry = gdata.docs.data.AclEntry(
        role='writer', scope_type='domain', scope_value='example.com',
        key=True)
    other_acl_entry = gdata.docs.data.AclEntry(
        role='reader', scope_type='user', scope_value='joe@example.com')
    
    for resource in self.resources:
      entry = getattr(self, resource[2])
      new_acl_entry = self.client.AddAclEntry(entry, acl_entry_to_add)
      new_acl_entry.with_key = None
      new_acl_entry.scope = other_acl_entry.scope
      new_acl_entry.role = other_acl_entry.role
      updated_acl_entry = self.client.UpdateAclEntry(new_acl_entry)

      self.assertEqual(new_acle_entry.GetSelfLink().href,
                       updated_acl_entry.GetSelfLink().href)
      self.assertNotEqual(new_acl_entry.title.text,
                          updated_acl_entry.title.text)
      self.assertEqual(other_acl_entry.scope.type, new_acl_entry.scope.type)
      self.assertEqual(other_acl_entry.scope.value, new_acl_entry.scope.value)
      self.assertEqual(other_acl_entry.role.value, new_acl_entry.role.value)
      self.assertEqual(new_acl_entry.with_key, None)

  def testDeleteAclEntry(self):
    acl_entry = gdata.docs.data.AclEntry(
        role='writer', scope_type='domain', scope_value='example.com',
        key=True)
    
    for resource in self.resources:
      entry = getattr(self, resource[2])
      new_acl_entry = self.client.AddAclEntry(entry, acl_entry_to_add)
      acl_feed = self.client.GetResourceAcl(entry)
      self.assert_(isinstance(acl_feed, gdata.docs.data.AclFeed))
      self.assertEqual(len(acl_feed.entry), 2)
      self.assert_(isinstance(acl_feed.entry[0], gdata.docs.data.AclEntry))
      self.assert_(isinstance(acl_feed.entry[1], gdata.docs.data.AclEntry))
      self.client.DeleteAclEntry(new_acl_entry)

      acl_feed = self.client.GetResourceAcl(entry)
      self.assert_(isinstance(acl_feed, gdata.docs.data.AclFeed))
      self.assert_(isinstance(acl_feed.entry[0], gdata.docs.data.AclEntry))
      self.assertEqual(len(acl_feed.entry), 1)


class RevisionsTest(DocsTestCase):
  def testGetRevisions(self):
    for resource in self.resources:
      if resource[2] not in ['collection1', 'collection2']:
        revisions = self.client.GetRevisions(getattr(self, resource[2]))
        self.assert_(isinstance(revisions, gdata.docs.data.RevisionFeed))
        self.assert_(isinstance(revisions.entry[0], gdata.docs.data.Revision))
        # Currently, there is a bug where new presentations have 2 revisions.
        if resource[2] != 'presentation':
          self.assertEqual(len(revisions.entry), 1)

  def testGetRevision(self):
    for resource in self.resources:
      if resource[2] not in ['collection1', 'collection2']:
        revisions = self.client.GetRevisions(getattr(self, resource[2]))
        entry = revisions.entry[0]
        new_entry = self.client.GetRevision(entry)
        self.assertEqual(entry.GetSelfLink().href, new_entry.GetSelfLink().href)
        self.assertEqual(entry.title.text, new_entry.title.text)

  def testGetRevisionBySelfLink(self):
    for resource in self.resources:
      if resource[2] not in ['collection1', 'collection2']:
        revisions = self.client.GetRevisions(getattr(self, resource[2]))
        entry = revisions.entry[0]
        new_entry = self.client.GetRevision(entry.GetSelfLink().href)
        self.assertEqual(entry.GetSelfLink().href, new_entry.GetSelfLink().href)
        self.assertEqual(entry.title.text, new_entry.title.text)

  def _update_resource(self, resource, entry):
    ms = None
    if resource[3] is not None:
      ms = gdata.data.MediaSource(
          file_path=os.path.join(os.path.dirname(__file__), resource[3]),
          content_type=resource[4])
    entry.title.text = '%s Updated' % resource[1]
    return self.client.UpdateResource(entry, media=ms, force=True)

  def testMultipleRevisionsAndUpdateResource(self):
    entry = None
    for resource in self.resources:
      print resource[2]
      entry = getattr(self, resource[2])

      if resource[2] not in ['collection1', 'collection2', 'presentation']:
        revisions = self.client.GetRevisions(entry)
        self.assertEqual(len(revisions.entry), 1)
      # Currently, there is a bug where new presentations have 2 revisions.
      elif resource[2] == 'presentation':
        self.assertEqual(len(revisions.entry), 2)

      # Drawings do not currently support update, thus the rest of these 
      # tests do not yet work as expected.
      if resource[2] == 'drawing':
        continue

      entry = self._update_resource(resource, entry)
      self.assertEqual(entry.title.text, '%s Updated' % resource[1])

      if resource[2] in ['collection1', 'collection2']:
        self.assertRaises(gdata.client.RequestError, self.client.GetRevisions,
                          entry)
      else:
        revisions = self.client.GetRevisions(entry)
        self.assert_(isinstance(revisions, gdata.docs.data.RevisionFeed))
        # If you don't update document content, no new revision is created
        # Thus, empty_document will only have 1 revision
        if resource[2] != 'empty_document':
          self.assertEqual(len(revisions.entry), 2)
          self.assert_(isinstance(revisions.entry[0], gdata.docs.data.Revision))
          self.assert_(isinstance(revisions.entry[1], gdata.docs.data.Revision))
        else:
          self.assertEqual(len(revisions.entry), 1)
          self.assert_(isinstance(revisions.entry[0], gdata.docs.data.Revision))

  def testPublishRevision(self):
    entry = None
    for resource in self.resources:
      if resource[2] in ['collection1', 'collection2']:
        continue

      # Drawings do not currently support update, thus this test would fail.
      if resource[2] == 'drawing':
        continue

      entry = getattr(self, resource[2])
      entry = self._update_resource(resource, entry)
      revisions = self.client.GetRevisions(entry)
      revision = self.client.PublishRevision(revisions.entry[0])
      self.assert_(isinstance(revision, gdata.docs.data.Revision))
      self.assertEqual(revision.publish.value, 'true')
      self.assertEqual(revision.publish_auto.value, 'false')
      self.assertEqual(revision.publish_to_domain.value, 'false')

      revision = self.client.PublishRevision(
          revisions.entry[1], auto_publish=True, publish_to_domain=True)
      self.assert_(isinstance(revision, gdata.docs.data.Revision))
      self.assertEqual(revision.publish.value, 'true')
      self.assertEqual(revision.publish_auto.value, 'true')
      self.assertEqual(revision.publish_to_domain.value, 'true')

      revision = self.client.GetRevision(revisions.entry[0])
      self.assertEqual(revision.publish.value, 'false')
      self.assertEqual(revision.publish_auto.value, 'false')

  def testDownloadRevision(self):
    entry = None
    for resource in self.resources:
      if resource[2] in ['collection1', 'collection2']:
        continue

      entry = getattr(self, resource[2])
      revisions = self.client.GetRevisions(entry)
      tmp = tempfile.mkstemp()
      self.client.DownloadRevision(revisions.entry[0], tmp[1])
      os.close(tmp[0])
      os.remove(tmp[1])

  def testDeleteRevision(self):
    entry = None
    for resource in self.resources:
      if resource[2] in ['collection1', 'collection2']:
        continue

      # Drawings do not currently support update, thus this test would fail.
      if resource[2] == 'drawing':
        continue

      entry = getattr(self, resource[2])
      entry = self._update_resource(resource, entry)
      # Only files and pdfs support deleting revisions
      if resource[2] in ['file', 'pdf']:
        self.client.DeleteRevision(revisions.entry[1], force=True)
        revisions = self.client.GetRevisions(entry)
        self.assert_(isinstance(revisions, gdata.docs.data.RevisionFeed))
        self.assert_(isinstance(revisions.entry[0], gdata.docs.data.Revision))
        self.assertEqual(len(revisions.entry), 1)
      elif len(revisions.entry) > 1:
        self.assertRaises(gdata.client.NotImplemented, 
                          self.client.DeleteResource,
                          revisions.entry[1],
                          force=True)


class ChangesTest(DocsTestCase):
  def testGetChanges(self):
    changes = self.client.GetChanges()
    self.assert_(isinstance(changes, gdata.docs.data.ChangeFeed))
    self.assertEqual(len(changes.entry), len(resources))
    self.assert_(isinstance(changes.entry[0], gdata.docs.data.Change))
    self._update_resource(self.resources[0], getattr(self, resources[0][2]))
    changes = self.client.GetChanges()
    self.assert_(isinstance(changes, gdata.docs.data.ChangeFeed))
    self.assertEqual(len(changes.entry), len(resources) + 1)
    self.assert_(isinstance(changes.entry[0], gdata.docs.data.Change))


class MetadataTest(unittest.TestCase):
  def setUp(self):
    if conf.options.get_value('runlive') != 'true':
      raise RuntimeError('Live tests require --runlive true')
    else:
      self.client = gdata.docs.client.DocsClient()
      if conf.options.get_value('ssl') == 'true':
        self.client.ssl = True
      conf.configure_client(self.client, 'DocsTest', self.client.auth_service)
      conf.configure_cache(self.client, str(self.__class__))

  def tearDown(self):
    conf.close_client(self.client)

  def testMetadata(self):
    metadata = self.client.GetMetadata()
    self.assert_(isinstance(metadata, gdata.docs.data.Metadata))
    self.assertNotEqual(metadata.quota_bytes_total, 0)
    self.assertEqual(metadata.quota_bytes_used, 0)
    self.assertEqual(metadata.quota_bytes_used_in_trash, 0)
    self.assertNotEqual(len(metadata.import_formats), 0)
    self.assertNotEqual(len(metadata.export_formats), 0)
    self.assertNotEqual(len(metadata.features), 0)
    self.assertNotEqual(len(metadata.max_upload_sizes), 0)


def suite():
  return conf.build_suite([ResourcesTest, AclTest, RevisionsTest, ChangesTest,
                           MetadataTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
