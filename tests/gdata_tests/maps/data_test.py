#!/usr/bin/env python
#
# Copyright (C) 2009 Google Inc.
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


__author__ = 'api.roman.public@gmail.com (Roman Nurik)'


import unittest
from gdata import test_data
import gdata.maps.data
import atom.core
import gdata.test_config as conf


class MapsDataTest(unittest.TestCase):

  def testMapEntryFromString(self):
    entry = atom.core.parse(test_data.MAP_ENTRY, gdata.maps.data.Map)
    self.assertEquals(entry.GetUserId(), '208825816854482607313')
    self.assertEquals(entry.GetMapId(), '00046fb45f88fa910bcea')
    self.assertEquals(entry.title.text, 'Untitled')

  def testMapFeedFromString(self):
    feed = atom.core.parse(test_data.MAP_FEED, gdata.maps.data.MapFeed)
    self.assertEquals(len(feed.entry), 1)
    self.assert_(isinstance(feed, gdata.maps.data.MapFeed))
    self.assert_(isinstance(feed.entry[0], gdata.maps.data.Map))
    self.assertEquals(feed.entry[0].GetUserId(), '208825816854482607313')
    self.assertEquals(feed.entry[0].GetMapId(), '00046fb45f88fa910bcea')
    self.assertEquals(feed.entry[0].title.text, 'Untitled')

  def testFeatureEntryFromString(self):
    entry = atom.core.parse(test_data.MAP_FEATURE_ENTRY,
                            gdata.maps.data.Feature)
    self.assertEquals(entry.GetUserId(), '208825816854482607313')
    self.assertEquals(entry.GetMapId(), '00046fb45f88fa910bcea')
    self.assertEquals(entry.GetFeatureId(), '00046fb4632573b19e0b7')
    self.assertEquals(entry.title.text, 'Some feature title')
    self.assertEquals(entry.content.type,
                      'application/vnd.google-earth.kml+xml')
  
  def testFeatureFeedFromString(self):
    feed = atom.core.parse(test_data.MAP_FEATURE_FEED,
                           gdata.maps.data.FeatureFeed)
    self.assertEquals(len(feed.entry), 3)
    self.assert_(isinstance(feed, gdata.maps.data.FeatureFeed))
    self.assert_(isinstance(feed.entry[0], gdata.maps.data.Feature))
    self.assertEquals(feed.entry[0].GetUserId(), '208825816854482607313')
    self.assertEquals(feed.entry[0].GetMapId(), '00046fb45f88fa910bcea')
    self.assertEquals(feed.entry[0].GetFeatureId(), '00046fb4632573b19e0b7')
    self.assertEquals(feed.entry[0].title.text, 'Some feature title')
    self.assertEquals(feed.entry[0].content.type,
                      'application/vnd.google-earth.kml+xml')
    self.assertEquals(type(feed.entry[0].content), gdata.maps.data.KmlContent)


class KmlContentTest(unittest.TestCase):

  def testKmlContentFromString(self):
    content = gdata.maps.data.KmlContent(kml=test_data.MAP_FEATURE_KML)
    self.assertEquals(len(content.children), 1)
    self.assertEquals(content.children[0].tag, 'Placemark')


def suite():
  return conf.build_suite([MapsDataTest, KmlContentTest])


if __name__ == '__main__':
  unittest.main()
