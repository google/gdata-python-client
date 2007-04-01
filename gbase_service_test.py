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
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gbase_service
import gdata_service
import app_service
import gbase
import atom
import test_data


username = ''
password = ''


class GBaseServiceUnitTest(unittest.TestCase):
  
  def setUp(self):
    self.gd_client = gbase_service.GBaseService()
    self.gd_client.email = username 
    self.gd_client.password = password 
    self.gd_client.source = 'BaseClient "Unit" Tests'
    self.gd_client.api_key = 'ABQIAAAAoLioN3buSs9KqIIq9VmkFxT2yXp_ZAY8_ufC' +\
                             '3CFXhHIE1NvwkxRK8C1Q8OWhsWA2AIKv-cVKlVrNhQ'

  def tearDown(self):
    # No teardown needed
    pass  

  def testProperties(self):
    email_string = 'Test Email'
    password_string = 'Passwd'
    api_key_string = 'my API key'

    self.gd_client.email = email_string
    self.assertEquals(self.gd_client.email, email_string)
    self.gd_client.password = password_string
    self.assertEquals(self.gd_client.password, password_string)
    self.gd_client.api_key = api_key_string
    self.assertEquals(self.gd_client.api_key, api_key_string)
    self.gd_client.api_key = None
    self.assert_(self.gd_client.api_key is None)

  def testQuery(self):
    my_query = gbase_service.BaseQuery(feed='/base/feeds/snippets')
    my_query['max-results'] = '25'
    my_query.bq = 'digital camera [item type: products]'
    result = self.gd_client.Query(my_query.ToUri())
    self.assert_(isinstance(result, atom.Feed))

    service = gbase_service.GBaseService(username, password)
    query = gbase_service.BaseQuery()
    query.feed = '/base/feeds/snippets'
    query.bq = 'digital camera'
    feed = service.Query(query.ToUri())
    
  def testCorrectReturnTypes(self):
    q = gbase_service.BaseQuery()
    q.feed = '/base/feeds/snippets'
    q.bq = 'digital camera'
    result = self.gd_client.QuerySnippetsFeed(q.ToUri())
    self.assert_(isinstance(result, gbase.GBaseSnippetFeed))

    q.feed = '/base/feeds/attributes'
    result = self.gd_client.QueryAttributesFeed(q.ToUri())
    self.assert_(isinstance(result, gbase.GBaseAttributesFeed))

    q = gbase_service.BaseQuery()
    q.feed = '/base/feeds/itemtypes/en_US'
    result = self.gd_client.QueryItemTypesFeed(q.ToUri())
    self.assert_(isinstance(result, gbase.GBaseItemTypesFeed))

    q = gbase_service.BaseQuery()
    q.feed = '/base/feeds/locales'
    result = self.gd_client.QueryLocalesFeed(q.ToUri())
    self.assert_(isinstance(result, gbase.GBaseLocalesFeed))

  def testInsertItemUpdateItemAndDeleteItem(self):
    try:
      self.gd_client.ProgrammaticLogin()
      self.assert_(self.gd_client.auth_token is not None)
      self.assert_(self.gd_client.captcha_token is None)
      self.assert_(self.gd_client.captcha_url is None)
    except gdata_service.CaptchaRequired:
      self.fail('Required Captcha')

    
    proposed_item = gbase.GBaseItemFromString(test_data.TEST_BASE_ENTRY)
    result = self.gd_client.InsertItem(proposed_item)

    item_id = result.id.text

    updated_item = gbase.GBaseItemFromString(test_data.TEST_BASE_ENTRY)
    updated_item.label[0].text = 'Test Item'
    result = self.gd_client.UpdateItem(item_id, updated_item)

    # Try to update an incorrect item_id.
    try:
      result = self.gd_client.UpdateItem(item_id + '2', updated_item)
      self.fail()
    except gdata_service.RequestError:
      pass

    result = self.gd_client.DeleteItem(item_id)
    self.assert_(result)

    # Delete and already deleted item.
    try:
      result = self.gd_client.DeleteItem(item_id)
      self.fail()
    except gdata_service.RequestError:
      pass

        
if __name__ == '__main__':
  print ('NOTE: Please run these tests only with a test account. ' +
      'The tests may delete or update your data.')
  username = raw_input('Please enter your username: ')
  password = getpass.getpass()
  unittest.main()
