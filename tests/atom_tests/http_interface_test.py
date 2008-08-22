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
import atom.http_interface
import StringIO


class HttpResponseTest(unittest.TestCase):

  def testConstructorWithStrings(self):
    resp = atom.http_interface.HttpResponse(body='Hi there!', status=200, 
        reason='OK', headers={'Content-Length':'9'})
    self.assertTrue(resp.read(amt=1) == 'H')
    self.assertTrue(resp.read(amt=2) == 'i ')
    self.assertTrue(resp.read() == 'there!')
    self.assertTrue(resp.read() == '')
    self.assertTrue(resp.reason == 'OK')
    self.assertTrue(resp.status == 200)
    self.assertTrue(resp.getheader('Content-Length') == '9')
    self.assertTrue(resp.getheader('Missing') is None)
    self.assertTrue(resp.getheader('Missing', default='yes') == 'yes')


if __name__ == '__main__':
  unittest.main()
