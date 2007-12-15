#!/usr/bin/python
#
# Copyright (C) 2007 Google Inc.
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

__author__ = 'api.jscudder (Jeffrey Scudder)'

import getpass
import time
import unittest
import StringIO
import gdata.photos.service


username = ''
password = ''
test_image_location = '../../testimage.jpg'
test_image_name = 'testimage.jpg'


class PhotosServiceTest(unittest.TestCase):

  def setUp(self):
    # Initialize the client and create a new album for testing.
    self.client = gdata.photos.service.PhotosService()
    self.client.email = username
    self.client.password = password
    self.client.source = 'Photos Client Unit Tests'
    self.client.ProgrammaticLogin()

    # Give the album a unique title by appending the current time.
    self.test_album = self.client.InsertAlbum(
        'Python library test' + str(time.time()), 
        'A temporary test album.')

  def testUploadGetAndDeletePhoto(self):
    image_entry = self.client.InsertPhotoSimple(self.test_album,
        'test', 'a pretty testing picture', test_image_location)
    self.assert_(image_entry.title.text == 'test')
    results_feed = self.client.SearchUserPhotos('test')
    self.assert_(len(results_feed.entry) > 0)
    self.client.Delete(image_entry)

  def tearDown(self):
    # Delete the test album.
    test_album = self.client.GetEntry(self.test_album.GetSelfLink().href)
    self.client.Delete(test_album)
  

if __name__ == '__main__':
  print ('NOTE: Please run these tests only with a test account. ' +
      'The tests may delete or update your data.')
  username = raw_input('Please enter your username: ')
  password = getpass.getpass()
  unittest.main()
