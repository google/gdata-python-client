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


__author__ = 'api.jscudder@gmail.com (Jeff Scudder)'


import unittest
from elementtree import ElementTree
import gdata
import test_data
import gbase


class LabelTest(unittest.TestCase):
  
  def setUp(self):
    self.label = gbase.Label()
    
  def testToAndFromString(self):
    self.label.text = 'test label'
    self.assert_(self.label.text == 'test label')
    new_label = gbase.LabelFromString(self.label.ToString())
    self.assert_(self.label.text == new_label.text)

    
class ItemTypeTest(unittest.TestCase):
  
  def setUp(self):
    self.item_type = gbase.ItemType()
    
  def testToAndFromString(self):
    self.item_type.text = 'product'
    self.item_type.type = 'text'
    self.assert_(self.item_type.text == 'product')
    self.assert_(self.item_type.type == 'text')
    new_item_type = gbase.ItemTypeFromString(self.item_type.ToString())
    self.assert_(self.item_type.text == new_item_type.text)
    self.assert_(self.item_type.type == new_item_type.type)


class GBaseItemTest(unittest.TestCase):

  def setUp(self):
    self.item = gbase.GBaseItem()
    
  def testToAndFromString(self):
    self.item.label.append(gbase.Label(text='my label'))
    self.assert_(self.item.label[0].text == 'my label')
    self.item.item_type = gbase.ItemType(text='products')
    self.assert_(self.item.item_type.text == 'products')
    self.item.item_attributes['extra'] = gbase.ItemAttribute('extra', 
        text='foo')
    self.assert_(self.item.item_attributes['extra'].text == 'foo')
    self.assert_(self.item.item_attributes['extra'].name == 'extra')
    new_item = gbase.GBaseItemFromString(self.item.ToString())
    self.assert_(self.item.label[0].text == new_item.label[0].text)
    self.assert_(self.item.item_type.text == new_item.item_type.text)
    self.assert_(self.item.item_attributes['extra'].text == 
        new_item.item_attributes['extra'].text)

  def testCustomItemAttributes(self):
    self.item.AddItemAttribute('test_attrib', 'foo')
    self.assert_(self.item.FindItemAttribute('test_attrib') == 'foo')
    self.item.SetItemAttribute('test_attrib', 'bar')
    self.assert_(self.item.FindItemAttribute('test_attrib') == 'bar')
    self.item.RemoveItemAttribute('test_attrib')
    self.assert_(self.item.FindItemAttribute('test_attrib') is None)

  def testConvertActualData(self):
    feed = gbase.GBaseSnippetFeedFromString(test_data.GBASE_FEED)
    for an_entry in feed.entry:
      if an_entry.author[0].email.text == 'anon-szot0wdsq0at@base.google.com':
        self.assert_(an_entry.item_attributes['payment_notes'].text == 
            'PayPal & Bill Me Later credit available online only.')
        self.assert_(an_entry.item_attributes['condition'].text == 'new')


class GBaseItemFeedTest(unittest.TestCase):

  def setUp(self):
    #self.item_feed = gbase.GBaseItemFeed()
    self.item_feed = gbase.GBaseItemFeedFromString(test_data.GBASE_FEED)

  def testToAndFromString(self):
    self.assert_(len(self.item_feed.entry) == 3)
    for an_entry in self.item_feed.entry:
      self.assert_(isinstance(an_entry, gbase.GBaseItem))
    new_item_feed = gbase.GBaseItemFeedFromString(str(self.item_feed))
    for an_entry in new_item_feed.entry:
      self.assert_(isinstance(an_entry, gbase.GBaseItem))
    
#    self.item_feed.label.append(gbase.Label(text='my label'))
#    self.assert_(self.item.label[0].text == 'my label')
#    self.item.item_type = gbase.ItemType(text='products')
#    self.assert_(self.item.item_type.text == 'products')
#    new_item = gbase.GBaseItemFromString(self.item.ToString())
#    self.assert_(self.item.label[0].text == new_item.label[0].text)
#    self.assert_(self.item.item_type.text == new_item.item_type.text)

  def testLinkFinderFindsHtmlLink(self):
    for entry in self.item_feed.entry:
      # All Base entries should have a self link
      self.assert_(entry.GetSelfLink() is not None)
      # All Base items should have an HTML link
      self.assert_(entry.GetHtmlLink() is not None)
      # None of the Base items should have an edit link
      self.assert_(entry.GetEditLink() is None)


class GBaseSnippetFeedTest(unittest.TestCase):

  def setUp(self):
    #self.item_feed = gbase.GBaseItemFeed()
    self.snippet_feed = gbase.GBaseSnippetFeedFromString(test_data.GBASE_FEED)

  def testToAndFromString(self):
    self.assert_(len(self.snippet_feed.entry) == 3)
    for an_entry in self.snippet_feed.entry:
      self.assert_(isinstance(an_entry, gbase.GBaseSnippet))
    new_snippet_feed = gbase.GBaseItemFeedFromString(str(self.snippet_feed))
    for an_entry in new_snippet_feed.entry:
      self.assert_(isinstance(an_entry, gbase.GBaseSnippet))


class ItemAttributeTest(unittest.TestCase):

  def testToAndFromStirng(self):
    attrib = gbase.ItemAttribute('price')
    attrib.type = 'float'
    self.assert_(attrib.name == 'price')
    self.assert_(attrib.type == 'float')
    new_attrib = gbase.ItemAttributeFromString(str(attrib))
    self.assert_(new_attrib.name == attrib.name)
    self.assert_(new_attrib.type == attrib.type)

  def testClassConvertsActualData(self):
    attrib = gbase.ItemAttributeFromString(test_data.TEST_GBASE_ATTRIBUTE)
    self.assert_(attrib.name == 'brand')
    self.assert_(attrib.type == 'text')
    self.assert_(len(attrib.extension_elements) == 0)

    # Test conversion to en ElementTree
    element = attrib._ToElementTree()
    self.assert_(element.tag == gbase.GBASE_TEMPLATE % 'brand')
    
    
if __name__ == '__main__':
  unittest.main()
