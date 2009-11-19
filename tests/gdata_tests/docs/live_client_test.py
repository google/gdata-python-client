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


__author__ = 'e.bidelman (Eric Bidelman)'


import os
import unittest
import gdata.client
import gdata.data
import gdata.gauth
import gdata.docs.client
import gdata.docs.data
import gdata.test_config as conf


class DocsTestCase(unittest.TestCase):

  def setUp(self):
    self.client = None
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.docs.client.DocsClient()
      if conf.options.get_value('ssl') == 'true':
        self.client.ssl = True
      conf.configure_client(self.client, 'DocsTest', self.client.auth_service)

  def tearDown(self):
    conf.close_client(self.client)


class DocsFetchingDataTest(DocsTestCase):

  def testGetDocList(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testGetDocList')

    # Query using GetDocList()
    feed = self.client.GetDocList(limit=1)
    self.assert_(isinstance(feed, gdata.docs.data.DocList))
    self.assertEqual(len(feed.entry), 1)

  def testGetDoc(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testGetDoc')

    uri = ('http://docs.google.com/feeds/default/private/full/'
           '-/spreadsheet?max-results=1')
    feed = self.client.GetDocList(uri, limit=1)
    self.assertEqual(len(feed.entry), 1)
    self.assertEqual(feed.entry[0].GetDocumentType(), 'spreadsheet')
    resource_id = feed.entry[0].resource_id.text
    entry = self.client.GetDoc(resource_id)
    self.assert_(isinstance(entry, gdata.docs.data.DocsEntry))
    self.assert_(entry.id.text is not None)
    self.assert_(entry.title.text is not None)
    self.assert_(entry.resource_id.text is not None)
    self.assert_(entry.title.text is not None)

  def testGetAclFeed(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testGetAclFeed')

    uri = ('http://docs.google.com/feeds/default/private/full/'
           '-/mine?max-results=1')
    feed = self.client.GetDocList(uri=uri)
    self.assertEqual(len(feed.entry), 1)
    acl_feed = self.client.GetAclPermissions(feed.entry[0].resource_id.text)
    self.assert_(isinstance(acl_feed, gdata.docs.data.AclFeed))
    self.assert_(isinstance(acl_feed.entry[0], gdata.docs.data.Acl))
    self.assert_(acl_feed.entry[0].scope is not None)
    self.assert_(acl_feed.entry[0].role is not None)

  def testGetRevisionFeed(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testGetRevisionFeed')

    uri = 'http://docs.google.com/feeds/default/private/full/-/document'
    feed = self.client.GetDocList(uri=uri, limit=1)
    self.assertEqual(len(feed.entry), 1)
    acl_feed = self.client.GetRevisions(feed.entry[0].resource_id.text)
    self.assert_(isinstance(acl_feed, gdata.docs.data.RevisionFeed))
    self.assert_(isinstance(acl_feed.entry[0], gdata.docs.data.Revision))


class CreatingAndDeletionTest(DocsTestCase):

  def testCreateAndMoveDoc(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testCreateAndMoveDoc')

    new_folder = self.client.Create(gdata.docs.data.FOLDER_LABEL, 'My Folder')
    self.assertEqual(new_folder.title.text, 'My Folder')
    self.assertEqual(new_folder.GetDocumentType(), 'folder')

    new_doc = self.client.Create(gdata.docs.data.DOCUMENT_LABEL, 'My Doc',
                                 writers_can_invite=False)
    self.assertEqual(new_doc.GetDocumentType(), 'document')
    self.assertEqual(new_doc.title.text, 'My Doc')
    self.assertEqual(new_doc.writers_can_invite.value, 'false')

    # Move doc into folder
    new_entry = self.client.Move(new_doc, new_folder)
    self.assertEqual(len(new_entry.InFolders()), 1)
    self.assertEqual(new_entry.InFolders()[0].title, 'My Folder')

    # Create new spreadsheet inside the folder.
    new_spread = self.client.Create(
        gdata.docs.data.SPREADSHEET_LABEL, 'My Spread', folder_or_id=new_folder)
    self.assertEqual(new_spread.GetDocumentType(), 'spreadsheet')
    self.assertEqual(len(new_spread.InFolders()), 1)
    self.assertEqual(new_spread.InFolders()[0].title, 'My Folder')

    # Create new folder, and move spreadsheet into that folder too.
    new_folder2 = self.client.Create(gdata.docs.data.FOLDER_LABEL, 'My Folder2')
    self.assertEqual(new_folder2.title.text, 'My Folder2')
    self.assertEqual(new_folder2.GetDocumentType(), 'folder')
    moved_entry = self.client.Move(
        new_spread, new_folder2, keep_in_folders=True)
    self.assertEqual(len(moved_entry.InFolders()), 2)

    # Move spreadsheet to root level
    was_moved = self.client.Move(moved_entry)
    self.assert_(was_moved)
    spread_entry = self.client.GetDoc(moved_entry.resource_id.text)
    self.assertEqual(len(spread_entry.InFolders()), 0)
    
    # Clean up our mess.
    self.client.Delete(new_folder.GetEditLink().href, force=True)
    self.client.Delete(new_folder2.GetEditLink().href, force=True)
    self.client.Delete(new_doc.GetEditLink().href, force=True)
    self.client.Delete(spread_entry.GetEditLink().href, force=True)


class DocumentListUploadTest(DocsTestCase):

  def testUploadAndDeleteDocument(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUploadAndDeleteDocument')

    ms = gdata.data.MediaSource(file_path='test.doc',
                                content_type='application/msword')

    entry = self.client.Upload(ms, 'test doc')
    self.assertEqual(entry.title.text, 'test doc')
    self.assertEqual(entry.GetDocumentType(), 'document')
    self.assert_(isinstance(entry, gdata.docs.data.DocsEntry))
    self.client.Delete(entry, force=True)

  def testUploadAndDeletePdf(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUploadAndDeletePdf')

    # Try passing in filename isntead of MediaSource object on this upload.
    entry = self.client.Upload(
        'test.pdf', 'test pdf', content_type='application/pdf')
    self.assertEqual(entry.title.text, 'test pdf')
    self.assertEqual(entry.GetDocumentType(), 'pdf')
    self.assert_(isinstance(entry, gdata.docs.data.DocsEntry))
    self.client.Delete(entry, force=True)


class DocumentListExportTest(DocsTestCase):

  def testExportDocument(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testExportDocument')

    uri = 'http://docs.google.com/feeds/default/private/full/-/document'
    feed = self.client.GetDocList(uri=uri, limit=1)
    file_paths = ['./downloadedTest.doc', './downloadedTest.html',
                  './downloadedTest.odt', './downloadedTest.pdf',
                  './downloadedTest.png', './downloadedTest.rtf',
                  './downloadedTest.txt', './downloadedTest.zip']
    for path in file_paths:
      self.client.Export(feed.entry[0], path)
      self.assert_(os.path.exists(path))
      self.assert_(os.path.getsize(path))
      os.remove(path)

  def testExportNonExistentDocument(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testExportNonExistentDocument')

    path = './ned.txt'
    self.assert_(not os.path.exists(path))

    exception_raised = False
    try:
      self.client.Export('non_existent_doc', path)
    except Exception, e:  # expected
      exception_raised = True

    self.assert_(exception_raised)
    self.assert_(not os.path.exists(path))

  def testDownloadPdf(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testDownloadPdf')

    uri = 'http://docs.google.com/feeds/default/private/full/-/pdf'
    feed = self.client.GetDocList(uri=uri, limit=1)
    path = './downloadedTest.pdf'
    self.client.Download(feed.entry[0], path)
    self.assert_(os.path.exists(path))
    self.assert_(os.path.getsize(path))
    os.remove(path)


def suite():
  return conf.build_suite([DocsFetchingDataTest, CreatingAndDeletionTest,
                           DocumentListUploadTest, DocumentListExportTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
