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


"""Content API for Shopping tests"""


__author__ = 'afshar (Ali Afshar)'


import unittest


from gdata.contentforshopping import client, data


class CFSClientTest(unittest.TestCase):

  def test_uri_missing_account_id(self):
    c = client.ContentForShoppingClient()
    self.assertRaises(ValueError, c._create_uri,
                      account_id=None, projection=None, resource='a/b')

  def test_uri_bad_projection(self):
    c = client.ContentForShoppingClient()
    self.assertRaises(ValueError, c._create_uri,
                      account_id='123', projection='banana', resource='a/b')

  def test_good_default_account_id(self):
    c = client.ContentForShoppingClient(account_id='123')
    uri = c._create_uri(account_id=None, projection=None, resource='a/b')
    self.assertEqual(uri,
        'https://content.googleapis.com/content/v1/123/a/b/generic')

  def test_override_request_account_id(self):
    c = client.ContentForShoppingClient(account_id='123')
    uri = c._create_uri(account_id='321', projection=None, resource='a/b')
    self.assertEqual(uri,
        'https://content.googleapis.com/content/v1/321/a/b/generic')

  def test_default_projection(self):
    c = client.ContentForShoppingClient(account_id='123')
    uri = c._create_uri(account_id=None, projection=None, resource='a/b')
    self.assertEqual(c.cfs_projection, 'generic')
    self.assertEqual(uri,
        'https://content.googleapis.com/content/v1/123/a/b/generic')

  def test_default_projection_change(self):
    c = client.ContentForShoppingClient(account_id='123', projection='schema')
    uri = c._create_uri(account_id=None, projection=None, resource='a/b')
    self.assertEqual(c.cfs_projection, 'schema')
    self.assertEqual(uri,
        'https://content.googleapis.com/content/v1/123/a/b/schema')

  def test_request_projection(self):
    c = client.ContentForShoppingClient(account_id='123')
    uri = c._create_uri(account_id=None, projection='schema', resource='a/b')
    self.assertEqual(c.cfs_projection, 'generic')
    self.assertEqual(uri,
        'https://content.googleapis.com/content/v1/123/a/b/schema')

  def test_request_resource(self):
    c = client.ContentForShoppingClient(account_id='123')
    uri = c._create_uri(account_id=None, projection=None, resource='x/y/z')
    self.assertEqual(uri,
        'https://content.googleapis.com/content/v1/123/x/y/z/generic')

  def test_path_single(self):
    c = client.ContentForShoppingClient(account_id='123')
    uri = c._create_uri(account_id=None, projection=None, resource='r',
                        path=['1'])
    self.assertEqual(uri,
        'https://content.googleapis.com/content/v1/123/r/generic/1')

  def test_path_multiple(self):
    c = client.ContentForShoppingClient(account_id='123')
    uri = c._create_uri(account_id=None, projection=None, resource='r',
                        path=['1', '2'])
    self.assertEqual(uri,
        'https://content.googleapis.com/content/v1/123/r/generic/1/2')


if __name__ == '__main__':
    unittest.main()
