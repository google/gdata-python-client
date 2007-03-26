#!/usr/bin/python
#
# Copyright (C) 2006 Google Inc.
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

__author__ = 'jscudder@google.com (Jeff Scudder)'

import unittest
import getpass
from elementtree import ElementTree
import gdata_service
import gdata
import atom
import gbase
import test_data


username = ''
password = ''


class GDataServiceUnitTest(unittest.TestCase):
  
  def setUp(self):
    self.gd_client = gdata_service.GDataService()
    self.gd_client.email = username
    self.gd_client.password = password
    self.gd_client.service = 'gbase'
    self.gd_client.source = 'GDataClient "Unit" Tests'
    pass

  def tearDown(self):
    # No teardown needed
    pass  

  def testProperties(self):
    email_string = 'Test Email'
    password_string = 'Passwd'

    self.gd_client.email = email_string
    self.assertEquals(self.gd_client.email, email_string)
    self.gd_client.password = password_string
    self.assertEquals(self.gd_client.password, password_string)

  def testCorrectLogin(self):
    try:
      self.gd_client.ProgrammaticLogin()
      self.assert_(self.gd_client.auth_token is not None)
      self.assert_(self.gd_client.captcha_token is None)
      self.assert_(self.gd_client.captcha_url is None)
    except gdata_service.CaptchaRequired:
    
      self.fail('Required Captcha')

  def testGet(self):
    try:
      self.gd_client.ProgrammaticLogin()
    except gdata_service.CaptchaRequired:
      self.fail('Required Captcha')
    except gdata_service.BadAuthentication:
      self.fail('Bad Authentication')
    except gdata_service.Error:
      self.fail('Login Error')
    self.gd_client.additional_headers = {'X-Google-Key': 
                                               'ABQIAAAAoLioN3buSs9KqIIq9V' +
                                               'mkFxT2yXp_ZAY8_ufC3CFXhHIE' +
                                               '1NvwkxRK8C1Q8OWhsWA2AIKv-c' +
                                               'VKlVrNhQ'}
    self.gd_client.server = 'base.google.com'
    result = self.gd_client.Get('/base/feeds/snippets?bq=digital+camera')
    self.assert_(result is not None)
    self.assert_(isinstance(result, atom.Feed))

  def testGetWithAuthentication(self):
    try:
      self.gd_client.ProgrammaticLogin()
    except gdata_service.CaptchaRequired:
      self.fail('Required Captcha')
    except gdata_service.BadAuthentication:
      self.fail('Bad Authentication')
    except gdata_service.Error:
      self.fail('Login Error')
    self.gd_client.additional_headers = {'X-Google-Key':
                                               'ABQIAAAAoLioN3buSs9KqIIq9V' +
                                               'mkFxT2yXp_ZAY8_ufC3CFXhHIE' +
                                               '1NvwkxRK8C1Q8OWhsWA2AIKv-c' +
                                               'VKlVrNhQ'}
    self.gd_client.server = 'base.google.com'
    result = self.gd_client.Get('/base/feeds/items?bq=digital+camera')
    self.assert_(result is not None)
    self.assert_(isinstance(result, atom.Feed))

  def testGetEntry(self):
    try:
      self.gd_client.ProgrammaticLogin()
    except gdata_service.CaptchaRequired:
      self.fail('Required Captcha')
    except gdata_service.BadAuthentication:
      self.fail('Bad Authentication')
    except gdata_service.Error:
      self.fail('Login Error')
    self.gd_client.server = 'base.google.com'
    try:
      result = self.gd_client.GetEntry('/base/feeds/items?bq=digital+camera')
      self.fail(
          'Result from server in GetEntry should have raised an exception')
    except gdata_service.UnexpectedReturnType:
      pass

  def testGetFeed(self):
    try:
      self.gd_client.ProgrammaticLogin()
    except gdata_service.CaptchaRequired:
      self.fail('Required Captcha')
    except gdata_service.BadAuthentication:
      self.fail('Bad Authentication')
    except gdata_service.Error:
      self.fail('Login Error')
    self.gd_client.server = 'base.google.com'
    result = self.gd_client.GetFeed('/base/feeds/items?bq=digital+camera')
    self.assert_(result is not None)
    self.assert_(isinstance(result, atom.Feed))

  def testPostPutAndDelete(self):
    try:
      self.gd_client.ProgrammaticLogin()
    except gdata_service.CaptchaRequired:
      self.fail('Required Captcha')
    except gdata_service.BadAuthentication:
      self.fail('Bad Authentication')
    except gdata_client.Error:
      self.fail('Login Error')
    self.gd_client.additional_headers = {'X-Google-Key':
                                               'ABQIAAAAoLioN3buSs9KqIIq9V' +
                                               'mkFxT2yXp_ZAY8_ufC3CFXhHIE' +
                                               '1NvwkxRK8C1Q8OWhsWA2AIKv-c' +
                                               'VKlVrNhQ'}
    self.gd_client.server = 'base.google.com'

    # Insert a new item
    response = self.gd_client.Post(test_data.TEST_BASE_ENTRY, 
        '/base/feeds/items')
    self.assert_(response is not None)
    self.assert_(isinstance(response, atom.Entry))
    self.assert_(response.category[0].term == 'products')

    # Find the item id of the created item
    item_id = response.id.text.lstrip(
        'http://www.google.com/base/feeds/items/')
    self.assert_(item_id is not None)
    
    updated_xml = gbase.GBaseItemFromString(test_data.TEST_BASE_ENTRY)
    # Change one of the labels in the item
    updated_xml.label[2].text = 'beach ball'
    # Update the item
    response = self.gd_client.Put(updated_xml, 
        '/base/feeds/items/%s' % item_id)
    self.assert_(response is not None)
    new_base_item = gbase.GBaseItemFromString(str(response))
    self.assert_(isinstance(new_base_item, atom.Entry))
    
    # Delete the item the test just created.
    response = self.gd_client.Delete('/base/feeds/items/%s' % item_id)
    self.assert_(response)


class QueryTest(unittest.TestCase):

  def setUp(self):
    self.query = gdata_service.Query()

  def testQueryShouldBehaveLikeDict(self):
    try:
      self.query['zap']
      self.fail()
    except KeyError:
      pass
    self.query['zap'] = 'x'
    self.assert_(self.query['zap'] == 'x')

  def testContructorShouldRejectBadInputs(self):
    test_q = gdata_service.Query(params=[1,2,3,4])
    self.assert_(len(test_q.keys()) == 0)

  def testTextQueryProperty(self):
    self.assert_(self.query.text_query is None)
    self.query['q'] = 'test1'
    self.assert_(self.query.text_query == 'test1')
    self.query.text_query = 'test2'
    self.assert_(self.query.text_query == 'test2')

  def testQueryShouldProduceExampleUris(self):
    self.query.feed = '/base/feeds/snippets'
    self.query.text_query = 'This is a test'
    self.assert_(self.query.ToUri() == '/base/feeds/snippets?q=This+is+a+test')

  def testCategoriesFormattedCorrectly(self):
    self.query.feed = '/x'
    self.query.categories.append('Fritz')
    self.query.categories.append('Laurie')
    self.assert_(self.query.ToUri() == '/x/-/Fritz/Laurie')
    # The query's feed should not have been changed
    self.assert_(self.query.feed == '/x')
    self.assert_(self.query.ToUri() == '/x/-/Fritz/Laurie')

  def testCategoryQueriesShouldEscapeOrSymbols(self):
    self.query.feed = '/x'
    self.query.categories.append('Fritz|Laurie')
    self.assert_(self.query.ToUri() == '/x/-/Fritz%7CLaurie')


if __name__ == '__main__':
  username = raw_input('Please enter your username: ')
  password = getpass.getpass()
  unittest.main()
