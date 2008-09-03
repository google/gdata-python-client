#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
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


__author__ = 'api.jscudder (Jeff Scudder)'


import unittest
import atom.token_store
import atom.http_interface
import atom.service

class TokenStoreTest(unittest.TestCase):

  def setUp(self):
    self.token = atom.service.BasicAuthToken('aaa1', scopes=[
        'http://example.com/', 'http://example.org'])
    self.tokens = atom.token_store.TokenStore()
    self.tokens.add_token(self.token)

  def testAddAndFindTokens(self):
    self.assert_(self.tokens.find_token('http://example.com/') == self.token)
    self.assert_(self.tokens.find_token('http://example.org/') == self.token)
    self.assert_(self.tokens.find_token('http://example.org/foo?ok=1') == (
        self.token))
    self.assert_(isinstance(self.tokens.find_token('http://example.net/'),
        atom.http_interface.GenericToken))
    self.assert_(isinstance(self.tokens.find_token('example.com/'), 
        atom.http_interface.GenericToken))

  def testFindTokenUsingMultipleUrls(self):
    self.assert_(self.tokens.find_token(
        'http://example.com/') == self.token)
    self.assert_(self.tokens.find_token(
        'http://example.org/bar') == self.token)
    self.assert_(isinstance(self.tokens.find_token(''), 
        atom.http_interface.GenericToken))
    self.assert_(isinstance(self.tokens.find_token(
            'http://example.net/'), 
        atom.http_interface.GenericToken))

  def testRemoveTokens(self):
    self.assert_(self.tokens.remove_token(self.token) == True)
    self.assert_(self.tokens.find_token('http://example.org/') != self.token)
    self.assert_(isinstance(self.tokens.find_token('http://example.com/'),
        atom.http_interface.GenericToken))
    self.assert_(self.tokens.remove_token(self.token) == False)
    self.assert_(isinstance(self.tokens.find_token('http://example.org/'),
        atom.http_interface.GenericToken))


if __name__ == '__main__':
  unittest.main()
