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

__author__ = 'e.bidelman@google.com (Eric Bidelman)'

import getopt
import mimetypes
import os.path
import sys
import atom.data
import gdata.client
import gdata.data
import gdata.gauth
import gdata.docs.client
import gdata.docs.data
import gdata.sample_util


APP_NAME = 'GDataResumableUploadPySample-v1.0'


def get_mimetype(filename):
  file_ext = filename[filename.rfind('.'):]
  if file_ext in mimetypes.types_map:
    content_type = mimetypes.types_map[file_ext]
  else:
    content_type = raw_input(
        "Unrecognized file extension. Please enter the file's content type: ")
  return content_type


class ResumableUploadDemo(object):
  """Helper class to setup a resumable upload, and upload a file."""

  CREATE_SESSION_URI = '/feeds/upload/create-session/default/private/full'

  client = None  # A gdata.client.GDClient object.
  uploader = None  # A gdata.client.ResumableUploader object.

  def __init__(self, filepath, chunk_size=None, convert=None,
               host=None, ssl=False, debug=False):
    self.client = gdata.docs.client.DocsClient(source=APP_NAME)
    self.client.ssl = ssl
    self.client.http_client.debug = debug
    self.convert = convert

    if host:
      self.client.host = host

    if chunk_size:
      self.chunk_size = chunk_size

    # Authenticate the user with CLientLogin, OAuth, or AuthSub.
    try:
      gdata.sample_util.authorize_client(
          self.client, service=self.client.auth_service, source=APP_NAME,
          scopes=self.client.auth_scopes)
    except gdata.client.BadAuthentication:
      exit('Invalid user credentials given.')
    except gdata.client.Error:
      exit('Login Error')

    mimetypes.init()  # Register common mimetypes on system.

    self.f = open(filepath)
    content_type = get_mimetype(self.f.name)
    file_size = os.path.getsize(self.f.name)

    self.uploader = gdata.client.ResumableUploader(
        self.client, self.f, content_type, file_size,
        chunk_size=self.chunk_size, desired_class=gdata.docs.data.DocsEntry)

  def __del__(self):
    if self.uploader is not None:
      self.uploader.file_handle.close()

  def UploadAutomaticChunks(self, new_entry):
    """Uploads an entire file, handing the chunking for you.

    Args:
      new_entry: gdata.data.docs.DocsEntry An object holding metadata to create
          the document with.

    Returns:
      A gdata.docs.data.DocsEntry of the created document on the server.
    """
    uri = self.CREATE_SESSION_URI

    # If convert=false is used on the initial request to start a resumable
    # upload, the document will be treated as arbitrary file upload.
    if self.convert is not None:
      uri += '?convert=' + self.convert

    return self.uploader.UploadFile(uri, entry=new_entry)

  def UploadInManualChunks(self, new_entry):
    """Uploads a file, demonstrating manually chunking the file.

    Args:
      new_entry: gdata.data.docs.DocsEntry An object holding metadata to create
          the document with.

    Returns:
      A gdata.docs.data.DocsEntry of the created document on the server.
    """
    uri = self.CREATE_SESSION_URI

    # If convert=false is used on the initial request to start a resumable
    # upload, the document will be treated as arbitrary file upload.
    if self.convert is not None:
      uri += '?convert=' + self.convert

    # Need to create the initial session manually.
    self.uploader._InitSession(uri, entry=new_entry)

    start_byte = 0
    entry = None

    while not entry:
      print 'Uploading bytes: %s-%s/%s' % (start_byte,
                                           self.uploader.chunk_size - 1,
                                           self.uploader.total_file_size)
      entry = self.uploader.UploadChunk(
          start_byte, self.uploader.file_handle.read(self.uploader.chunk_size))
      start_byte += self.uploader.chunk_size

    return entry

  def UploadUsingNormalPath(self):
    """Uploads a file using the standard DocList API upload path.

    This method is included to show the difference between the standard upload
    path and the resumable upload path. Also note, file uploads using this
    normal upload method max out ~10MB.

    Returns:
      A gdata.docs.data.DocsEntry of the created document on the server.
    """
    ms = gdata.data.MediaSource(
        file_handle=self.f, content_type=self.uploader.content_type,
        content_length=self.uploader.total_file_size)

    uri = self.client.DOCLIST_FEED_URI

    # If convert=false is used on the initial request to start a resumable
    # upload, the document will be treated as arbitrary file upload.
    if self.convert is not None:
      uri += '?convert=' + self.convert

    return self.client.Upload(ms, self.f.name, folder_or_uri=uri)


def main():
  try:
    opts, args = getopt.getopt(
        sys.argv[1:], '', ['filepath=', 'convert=', 'chunk_size=',
                           'ssl', 'debug'])
  except getopt.error, msg:
    print '''python resumable_upload_sample.py
        --filepath= [file to upload]
        --convert= [document uploads will be converted to native Google Docs.
                    Possible values are 'true' and 'false'.]
        --ssl [enables HTTPS if set]
        --debug [prints debug info if set]'''
    print ('Example usage: python resumable_upload_sample.py '
           '--filepath=/path/to/test.doc --convert=true --ssl')
    sys.exit(2)

  filepath = None
  convert = 'true'  # Convert to Google Docs format by default
  chunk_size = gdata.client.ResumableUploader.DEFAULT_CHUNK_SIZE
  debug = False
  ssl = False

  for option, arg in opts:
    if option == '--filepath':
      filepath = arg
    elif option == '--convert':
      convert = arg.lower()
    elif option == '--chunk_size':
      chunk_size = int(arg)
    elif option == '--ssl':
      ssl = True
    elif option == '--debug':
      debug = True

  if filepath is None:
    filepath = raw_input('Enter path to a file: ')

  demo = ResumableUploadDemo(filepath, chunk_size=chunk_size,
                             convert=convert, ssl=ssl, debug=debug)

  title = raw_input('Enter title for the document: ')

  print 'Uploading %s ( %s ) @ %s bytes...' % (demo.uploader.file_handle.name,
                                               demo.uploader.content_type,
                                               demo.uploader.total_file_size)

  entry = demo.UploadInManualChunks(
      gdata.docs.data.DocsEntry(title=atom.data.Title(text=title)))
  print 'Done: %s' % demo.uploader.QueryUploadStatus()
  print 'Document uploaded: ' + entry.title.text
  print 'Quota used: %s' % entry.quota_bytes_used.text

  print 'file closed: %s' % demo.uploader.file_handle.closed

if __name__ == '__main__':
  main()
