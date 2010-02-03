#!/usr/bin/env python
#
# Copyright (C) 2008, 2009 Google Inc.
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


__author__ = 'e.bidelman@google.com (Eric Bidelman)'


import os
import unittest
import atom.data
import gdata.client
import gdata.data
import gdata.gauth
import gdata.docs.client
import gdata.docs.data
import gdata.test_config as conf


TEST_FILE_LOCATION_OPTION = conf.Option(
    'file',
    'Please enter the full path to a test file to upload',
    description=('This test file will be uploaded to DocList which. An example '
                 'file can be found in tests/gdata_tests/docs/test.doc'))

CONTENT_TYPE_OPTION = conf.Option(
    'contenttype',
    'Please enter the mimetype of the file',
    description='The content type should match that of the upload file.')

conf.options.register_option(TEST_FILE_LOCATION_OPTION)
conf.options.register_option(CONTENT_TYPE_OPTION)


class ResumableUploadTestCase(unittest.TestCase):

  def setUp(self):
    self.client = None
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.docs.client.DocsClient(source='ResumableUploadTest')
      if conf.options.get_value('ssl') == 'true':
        self.client.ssl = True
      self.f = open(conf.options.get_value('file'))
      self.content_type = conf.options.get_value('contenttype')
      conf.configure_client(
          self.client, 'ResumableUploadTest', self.client.auth_service)

  def tearDown(self):
    conf.close_client(self.client)
    self.f.close()

  def testUploadEntireDocumentAndUpdate(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUploadDocument')

    uploader = gdata.client.ResumableUploader(
        self.client, self.f, self.content_type, os.path.getsize(self.f.name),
        chunk_size=20000,  # 20000 bytes.
        desired_class=gdata.docs.data.DocsEntry)

    e = gdata.docs.data.DocsEntry(
        title=atom.data.Title(text='MyResumableTitleEntireFile'))
    e.category.append(gdata.docs.data.make_kind_category('document'))
    e.writers_can_invite = gdata.docs.data.WritersCanInvite(value='false')

    entry = uploader.UploadFile(
        '/feeds/upload/create-session/default/private/full', entry=e)

    # Verify upload has really completed.
    self.assertEqual(uploader.QueryUploadStatus(), True)

    self.assert_(isinstance(entry, gdata.docs.data.DocsEntry))
    self.assertEqual(entry.title.text, 'MyResumableTitleEntireFile')
    self.assertEqual(entry.GetDocumentType(), 'document')
    self.assertEqual(entry.writers_can_invite.value, 'false')
    self.assertEqual(int(entry.quota_bytes_used.text), 0)
    self.client.Delete(entry, force=True)

  def testUploadDocumentInChunks(self):
    if not conf.options.get_value('runlive') == 'true':
      return

    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'testUploadDocumentInChunks')

    uploader = gdata.client.ResumableUploader(
        self.client, self.f, self.content_type, os.path.getsize(self.f.name),
        desired_class=gdata.docs.data.DocsEntry)

    uploader._InitSession(
        '/feeds/upload/create-session/default/private/full',
        headers={'Slug': 'MyManualChunksNoAtomTitle'})

    start_byte = 0
    entry = None

    while not entry:
      entry = uploader.UploadChunk(
          start_byte, uploader.file_handle.read(uploader.chunk_size))
      start_byte += uploader.chunk_size

    # Verify upload has really completed.
    self.assertEqual(uploader.QueryUploadStatus(), True)

    self.assert_(isinstance(entry, gdata.docs.data.DocsEntry))
    self.assertEqual(entry.title.text, 'MyManualChunksNoAtomTitle')
    self.assertEqual(entry.GetDocumentType(), 'document')
    self.client.Delete(entry, force=True)


def suite():
  return conf.build_suite([ResumableUploadTestCase])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
  

