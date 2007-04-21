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
from gdata import test_data


class StartIndexTest(unittest.TestCase):
  
  def setUp(self):
    self.start_index = gdata.StartIndex()
    
  def testToAndFromString(self):
    self.start_index.text = '1'
    self.assert_(self.start_index.text == '1')
    new_start_index = gdata.StartIndexFromString(self.start_index.ToString())
    self.assert_(self.start_index.text == new_start_index.text)
    
    
class ItemsPerPageTest(unittest.TestCase):
  
  def setUp(self):
    self.items_per_page = gdata.ItemsPerPage()
    
  def testToAndFromString(self):
    self.items_per_page.text = '10'
    self.assert_(self.items_per_page.text == '10')
    new_items_per_page = gdata.ItemsPerPageFromString(
         self.items_per_page.ToString())
    self.assert_(self.items_per_page.text == new_items_per_page.text)


class GDataEntryTest(unittest.TestCase):

  def setUp(self):
    #self.entry = gdata.GDataEntry()
    pass

  def testIdShouldBeCleaned(self):
    entry = gdata.GDataEntryFromString(test_data.XML_ENTRY_1)
    element_tree = ElementTree.fromstring(test_data.XML_ENTRY_1)
    self.assert_(element_tree.findall(
        '{http://www.w3.org/2005/Atom}id')[0].text != entry.id.text)
    self.assert_(entry.id.text == 'http://www.google.com/test/id/url')
    
  def testGeneratorShouldBeCleaned(self):
    feed = gdata.GDataFeedFromString(test_data.GBASE_FEED)
    element_tree = ElementTree.fromstring(test_data.GBASE_FEED)
    self.assert_(element_tree.findall('{http://www.w3.org/2005/Atom}generator'
        )[0].text != feed.generator.text)
    self.assert_(feed.generator.text == 'GoogleBase')
    
    
if __name__ == '__main__':
  unittest.main()
