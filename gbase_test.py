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
try:
  from xml.etree import ElementTree
except ImportError:
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
    self.item.item_attributes.append(gbase.ItemAttribute('extra', text='foo'))
    self.assert_(self.item.item_attributes[0].text == 'foo')
    self.assert_(self.item.item_attributes[0].name == 'extra')
    new_item = gbase.GBaseItemFromString(self.item.ToString())
    self.assert_(self.item.label[0].text == new_item.label[0].text)
    self.assert_(self.item.item_type.text == new_item.item_type.text)
    self.assert_(self.item.item_attributes[0].text == 
        new_item.item_attributes[0].text)

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
        for attrib in an_entry.item_attributes:
          if attrib.name == 'payment_notes':
            self.assert_(attrib.text == 
                'PayPal & Bill Me Later credit available online only.')
          if attrib.name == 'condition':
            self.assert_(attrib.text == 'new')
#        self.assert_(an_entry.item_attributes['condition'].text == 'new')


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


class AttributeTest(unittest.TestCase):

  def testAttributeToAndFromString(self):
    attrib = gbase.Attribute()
    attrib.type = 'float'
    attrib.count = '44000'
    attrib.name = 'test attribute'
    attrib.value.append(gbase.Value(count='500', text='a value'))
    self.assert_(attrib.type == 'float')
    self.assert_(attrib.count == '44000')
    self.assert_(attrib.name == 'test attribute')
    self.assert_(attrib.value[0].count == '500')
    self.assert_(attrib.value[0].text == 'a value')
    new_attrib = gbase.AttributeFromString(str(attrib))
    self.assert_(attrib.type == new_attrib.type)
    self.assert_(attrib.count == new_attrib.count)
    self.assert_(attrib.value[0].count == new_attrib.value[0].count)
    self.assert_(attrib.value[0].text == new_attrib.value[0].text)
    self.assert_(attrib.name == new_attrib.name)


class ValueTest(unittest.TestCase):

  def testValueToAndFromString(self):
    value = gbase.Value()
    value.count = '5123'
    value.text = 'super great'
    self.assert_(value.count == '5123')
    self.assert_(value.text == 'super great')
    new_value = gbase.ValueFromString(str(value))
    self.assert_(new_value.count == value.count)
    self.assert_(new_value.text == value.text)
    

class AttributeEntryTest(unittest.TestCase):

  def testAttributeEntryToAndFromString(self):
    value = gbase.Value(count='500', text='happy')
    attribute = gbase.Attribute(count='600', value=[value])
    a_entry = gbase.GBaseAttributeEntry(attribute=[attribute])
    self.assert_(a_entry.attribute[0].count == '600')
    self.assert_(a_entry.attribute[0].value[0].count == '500')
    self.assert_(a_entry.attribute[0].value[0].text == 'happy')
    new_entry = gbase.GBaseAttributeEntryFromString(str(a_entry))
    self.assert_(new_entry.attribute[0].count == '600')
    self.assert_(new_entry.attribute[0].value[0].count == '500')
    self.assert_(new_entry.attribute[0].value[0].text == 'happy')
    

class GBaseAttributeEntryTest(unittest.TestCase):

  def testAttribteEntryFromExampleData(self):
    entry = gbase.GBaseAttributeEntryFromString(
        test_data.GBASE_ATTRIBUTE_ENTRY)
    self.assert_(len(entry.attribute) == 1)
    self.assert_(len(entry.attribute[0].value) == 10)
    self.assert_(entry.attribute[0].name == 'job industry')
    for val in entry.attribute[0].value:
      if val.text == 'it internet':
        self.assert_(val.count == '380772')
      elif val.text == 'healthcare':
        self.assert_(val.count == '261565')
      


class GBaseAttributesFeedTest(unittest.TestCase):

  def testAttributesFeedExampleData(self):
    #feed = gbase.GBaseAttributesFeedFromString(test_data.GBASE_ATTRIBUTE_FEED)
    #self.assert_(len(feed.entry) == 1)
    #self.assert_(isinstance(feed.entry[0], gbase.GBaseAttributeEntry))
    #TODO: find the malformed XML in test_data.GBASE_ATTRIBUTE_FEED
    pass

  def testAttributesFeedToAndFromString(self):
    value = gbase.Value(count='500', text='happy')
    attribute = gbase.Attribute(count='600', value=[value])
    a_entry = gbase.GBaseAttributeEntry(attribute=[attribute])
    feed = gbase.GBaseAttributesFeed(entry=[a_entry])
    self.assert_(feed.entry[0].attribute[0].count == '600')
    self.assert_(feed.entry[0].attribute[0].value[0].count == '500')
    self.assert_(feed.entry[0].attribute[0].value[0].text == 'happy')
    new_feed = gbase.GBaseAttributesFeedFromString(str(feed))
    self.assert_(new_feed.entry[0].attribute[0].count == '600')
    self.assert_(new_feed.entry[0].attribute[0].value[0].count == '500')
    self.assert_(new_feed.entry[0].attribute[0].value[0].text == 'happy')
            

class GBaseLocalesFeedTest(unittest.TestCase):
  
  def testLocatesFeedWithExampleData(self):
    feed = gbase.GBaseLocalesFeedFromString(test_data.GBASE_LOCALES_FEED)
    self.assert_(len(feed.entry) == 3)
    self.assert_(feed.GetSelfLink().href == 
        'http://www.google.com/base/feeds/locales/') 
    for an_entry in feed.entry:
      if an_entry.title.text == 'en_US':
        self.assert_(an_entry.category[0].term == 'en_US')
      self.assert_(an_entry.title.text == an_entry.category[0].term)

  
class GBaseItemTypesFeedAndEntryTest(unittest.TestCase):

  def testItemTypesFeedToAndFromString(self):
    feed = gbase.GBaseItemTypesFeed()
    entry = gbase.GBaseItemTypeEntry()
    entry.attributes.append(gbase.Attribute(name='location', 
        attribute_type='location'))
    entry.item_type = gbase.ItemType(text='jobs')
    feed.entry.append(entry)
    self.assert_(len(feed.entry) == 1)
    self.assert_(feed.entry[0].item_type.text == 'jobs')
    self.assert_(feed.entry[0].attributes[0].name == 'location')
    new_feed = gbase.GBaseItemTypesFeedFromString(str(feed))
    self.assert_(len(new_feed.entry) == 1)
    self.assert_(new_feed.entry[0].item_type.text == 'jobs')
    self.assert_(new_feed.entry[0].attributes[0].name == 'location')
    
if __name__ == '__main__':
  unittest.main()
