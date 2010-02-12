#!/usr/bin/env python
#
# Copyright (C) 2010 Google Inc.
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


# This module is used for version 2 of the Google Data APIs.


__author__ = 'j.s@google.com (Jeff Scudder)'


import unittest
import gdata.core
import gdata.test_config as conf 



PLAYLIST_EXAMPLE = (
    '{"apiVersion": "2.0","data": {"totalResults": 347,"startIndex": 1,"it'
    'emsPerPage": 2,"items": [{"id": "4DAEFAF23BB3CDD0","created": "2008-1'
    '2-09T20:23:06.000Z","updated": "2010-01-04T02:56:19.000Z","author": "'
    'GoogleDevelopers","title": "Google Web Toolkit Developers","descripti'
    'on": "Developers talk about using Google Web Toolkit ...","tags": ["g'
    'oogle","web","toolkit","developers","gwt"],"size": 12},{"id": "586D32'
    '2B5E2764CF","created": "2007-11-13T19:41:21.000Z","updated": "2010-01'
    '-04T17:41:16.000Z","author": "GoogleDevelopers","title": "Android","d'
    'escription": "Demos and tutorials about the new Android platform.","t'
    'ags": ["android","google","developers","mobile"],"size": 32}]}}')


VIDEO_EXAMPLE = (
    '{"apiVersion": "2.0","data": {"updated": "2010-01-07T19:58:42.949Z","'
    'totalItems": 800,"startIndex": 1,"itemsPerPage": 1, "items": [{"id": '
    '"hYB0mn5zh2c","uploaded": "2007-06-05T22:07:03.000Z","updated": "2010'
    '-01-07T13:26:50.000Z","uploader": "GoogleDeveloperDay","category": "N'
    'ews","title": "Google Developers Day US - Maps API Introduction","des'
    'cription": "Google Maps API Introduction ...","tags": ["GDD07","GDD07'
    'US","Maps"],"thumbnail": {"default": "http://i.ytimg.com/vi/hYB0mn5zh'
    '2c/default.jpg","hqDefault": "http://i.ytimg.com/vi/hYB0mn5zh2c/hqdef'
    'ault.jpg"},"player": {"default": "http://www.youtube.com/watch?v'
    '\u003dhYB0mn5zh2c"},"content": {"1": "rtsp://v5.cache3.c.youtube.com/'
    'CiILENy.../0/0/0/video.3gp","5": "http://www.youtube.com/v/hYB0mn5zh2'
    'c?f...","6": "rtsp://v1.cache1.c.youtube.com/CiILENy.../0/0/0/video.3'
    'gp"},"duration": 2840,"rating": 4.63,"ratingCount": 68,"viewCount": 2'
    '20101,"favoriteCount": 201,"commentCount": 22}]}}')


class JsoncConversionTest(unittest.TestCase):
  
  # See http://code.google.com/apis/youtube/2.0/developers_guide_jsonc.html 
  def test_from_and_to_old_json(self):
    json = ('{"media$group":{"media$credit":[{"$t":"GoogleDevelopers", '
            '"role":"uploader", "scheme":"urn:youtube"}]}}')
    jsonc_obj = gdata.core.parse_json(json)
    self.assert_(isinstance(jsonc_obj, gdata.core.Jsonc))
    raw = gdata.core._convert_to_object(jsonc_obj)
    self.assertEqual(raw['media$group']['media$credit'][0]['$t'],
                     'GoogleDevelopers')

  def test_to_and_from_jsonc(self):
    x = {'a': 1}
    jsonc_obj = gdata.core._convert_to_jsonc(x)
    self.assertEqual(jsonc_obj.a, 1)
    # Convert the json_obj back to a dict and compare.
    self.assertEqual(x, gdata.core._convert_to_object(jsonc_obj))

  def test_from_and_to_new_json(self):
    x = gdata.core.parse_json(PLAYLIST_EXAMPLE)
    self.assertEqual(x._dict['apiVersion'], '2.0')
    self.assertEqual(x._dict['data']._dict['items'][0]._dict['id'],
                     '4DAEFAF23BB3CDD0')
    self.assertEqual(x._dict['data']._dict['items'][1]._dict['id'],
                     '586D322B5E2764CF')
    x = gdata.core.parse_json(VIDEO_EXAMPLE)
    self.assertEqual(x._dict['apiVersion'], '2.0')
    self.assertEqual(x.data._dict['totalItems'], 800)
    self.assertEqual(x.data.items[0]._dict['viewCount'], 220101)

  def test_pretty_print(self):
    x = gdata.core.Jsonc(x=1, y=2, z=3)
    pretty = gdata.core.prettify_jsonc(x)
    self.assert_(isinstance(pretty, (str, unicode)))
    
    pretty = gdata.core.prettify_jsonc(x, 4)
    self.assert_(isinstance(pretty, (str, unicode)))


class MemberNameConversionTest(unittest.TestCase):

  def test_member_to_jsonc(self):
    self.assertEqual(gdata.core._to_jsonc_name(''), '')
    self.assertEqual(gdata.core._to_jsonc_name('foo'), 'foo')
    self.assertEqual(gdata.core._to_jsonc_name('Foo'), 'Foo')
    self.assertEqual(gdata.core._to_jsonc_name('test_x'), 'testX')
    self.assertEqual(gdata.core._to_jsonc_name('test_x_y_zabc'), 'testXYZabc')


def build_test_object():
    return gdata.core.Jsonc(
        api_version='2.0',
        data=gdata.core.Jsonc(
            total_items=800,
            items=[
                gdata.core.Jsonc(
                    view_count=220101,
                    comment_count=22,
                    favorite_count=201,
                    content={
                        '1': ('rtsp://v5.cache3.c.youtube.com'
                              '/CiILENy.../0/0/0/video.3gp')})]))


class JsoncObjectTest(unittest.TestCase):

  def check_video_json(self, x):
    """Validates a JsoncObject similar to VIDEO_EXAMPLE."""
    self.assert_(isinstance(x._dict, dict))
    self.assert_(isinstance(x.data, gdata.core.Jsonc))
    self.assert_(isinstance(x._dict['data'], gdata.core.Jsonc))
    self.assert_(isinstance(x.data._dict, dict))
    self.assert_(isinstance(x._dict['data']._dict, dict))
    self.assert_(isinstance(x._dict['apiVersion'], (str, unicode)))
    self.assert_(isinstance(x.api_version, (str, unicode)))
    self.assert_(isinstance(x.data._dict['items'], list))
    self.assert_(isinstance(x.data.items[0]._dict['commentCount'],
                            (int, long)))
    self.assert_(isinstance(x.data.items[0].favorite_count, (int, long)))
    self.assertEqual(x.data.total_items, 800)
    self.assertEqual(x._dict['data']._dict['totalItems'], 800)
    self.assertEqual(x.data.items[0].view_count, 220101)
    self.assertEqual(x._dict['data']._dict['items'][0]._dict['viewCount'],
                     220101)
    self.assertEqual(x.data.items[0].comment_count, 22)
    self.assertEqual(x.data.items[0]._dict['commentCount'], 22)
    self.assertEqual(x.data.items[0].favorite_count, 201)
    self.assertEqual(x.data.items[0]._dict['favoriteCount'], 201)
    self.assertEqual(
        x.data.items[0].content._dict['1'],
        'rtsp://v5.cache3.c.youtube.com/CiILENy.../0/0/0/video.3gp')
    self.assertEqual(x.api_version, '2.0')
    self.assertEqual(x.api_version, x._dict['apiVersion'])

  def test_convert_to_jsonc(self):
    x = gdata.core._convert_to_jsonc(1)
    self.assert_(isinstance(x, (int, long)))
    self.assertEqual(x, 1)

    x = gdata.core._convert_to_jsonc([1, 'a'])
    self.assert_(isinstance(x, list))
    self.assertEqual(len(x), 2)
    self.assert_(isinstance(x[0], (int, long)))
    self.assertEqual(x[0], 1)
    self.assert_(isinstance(x[1], (str, unicode)))
    self.assertEqual(x[1], 'a')

    x = gdata.core._convert_to_jsonc([{'b': 1}, 'a'])
    self.assert_(isinstance(x, list))
    self.assertEqual(len(x), 2)
    self.assert_(isinstance(x[0], gdata.core.Jsonc))
    self.assertEqual(x[0].b, 1)

  def test_non_json_members(self):
    x = gdata.core.Jsonc(alpha=1, _beta=2, deep={'_bbb': 3, 'aaa': 2})
    x.test = 'a'
    x._bar = 'bacon'
    # Should be able to access the _beta member.
    self.assertEqual(x._beta, 2)
    self.assertEqual(getattr(x, '_beta'), 2)
    try:
      self.assertEqual(getattr(x.deep, '_bbb'), 3)
    except AttributeError:
      pass
    # There should not be a letter 'B' anywhere in the generated JSON.
    self.assertEqual(gdata.core.jsonc_to_string(x).find('B'), -1)
    # We should find a 'b' becuse we don't consider names of dict keys in
    # the constructor as aliases to camelCase names.
    self.assert_(not gdata.core.jsonc_to_string(x).find('b') == -1)

  def test_constructor(self):
    x = gdata.core.Jsonc(a=[{'x': 'y'}, 2])
    self.assert_(isinstance(x, gdata.core.Jsonc))
    self.assert_(isinstance(x.a, list))
    self.assert_(isinstance(x.a[0], gdata.core.Jsonc))
    self.assertEqual(x.a[0].x, 'y')
    self.assertEqual(x.a[1], 2)

  def test_read_json(self):
    x = gdata.core.parse_json(PLAYLIST_EXAMPLE)
    self.assert_(isinstance(x._dict, dict))
    self.assertEqual(x._dict['apiVersion'], '2.0')
    self.assertEqual(x.api_version, '2.0')

    x = gdata.core.parse_json(VIDEO_EXAMPLE)
    self.assert_(isinstance(x._dict, dict))
    self.assertEqual(x._dict['apiVersion'], '2.0')
    self.assertEqual(x.api_version, '2.0')

    x = gdata.core.parse_json(VIDEO_EXAMPLE)
    self.check_video_json(x)

  def test_write_json(self):
    x = gdata.core.Jsonc()
    x._dict['apiVersion'] = '2.0'
    x.data = {'totalItems': 800}
    x.data.items = []
    x.data.items.append(gdata.core.Jsonc(view_count=220101))
    x.data.items[0]._dict['favoriteCount'] = 201
    x.data.items[0].comment_count = 22
    x.data.items[0].content = {
        '1': 'rtsp://v5.cache3.c.youtube.com/CiILENy.../0/0/0/video.3gp'}
    self.check_video_json(x)

  def test_build_using_contructor(self):
    x = build_test_object()
    self.check_video_json(x)

  def test_to_dict(self):
    x = build_test_object()
    self.assertEqual(
        gdata.core._convert_to_object(x),
        {'data': {'totalItems': 800, 'items': [
          {'content': {
            '1': 'rtsp://v5.cache3.c.youtube.com/CiILENy.../0/0/0/video.3gp'},
           'viewCount': 220101, 'commentCount': 22, 'favoriteCount': 201}]},
         'apiVersion': '2.0'})

  def test_try_json_syntax(self):
    x = build_test_object()
    self.assertEqual(x.data.items[0].commentCount, 22)

    x.data.items[0].commentCount = 33
    self.assertEqual(x.data.items[0].commentCount, 33)
    self.assertEqual(x.data.items[0].comment_count, 33)
    self.assertEqual(x.data.items[0]._dict['commentCount'], 33)

  def test_to_string(self):
    self.check_video_json(
        gdata.core.parse_json(
            gdata.core.jsonc_to_string(
                gdata.core._convert_to_object(
                    build_test_object()))))

  def test_del_attr(self):
    x = build_test_object()
    self.assertEqual(x.data.items[0].commentCount, 22)
    del x.data.items[0].comment_count
    try:
      x.data.items[0].commentCount
      self.fail('Should not be able to access commentCount after deletion')
    except AttributeError:
      pass

    self.assertEqual(x.data.items[0].favorite_count, 201)
    del x.data.items[0].favorite_count
    try:
      x.data.items[0].favorite_count
      self.fail('Should not be able to access favorite_count after deletion')
    except AttributeError:
      pass
    try:
      x.data.items[0]._dict['favoriteCount']
      self.fail('Should not see [\'favoriteCount\'] after deletion')
    except KeyError:
      pass

    self.assertEqual(x.data.items[0].view_count, 220101)
    del x.data.items[0]._dict['viewCount']
    try:
      x.data.items[0].view_count
      self.fail('Should not be able to access view_count after deletion')
    except AttributeError:
      pass

    try:
      del x.data.missing
      self.fail('Should not delete a missing attribute')
    except AttributeError:
      pass

  def test_del_protected_attribute(self):
    x = gdata.core.Jsonc(public='x', _private='y')
    self.assertEqual(x.public, 'x')
    self.assertEqual(x._private, 'y')
    self.assertEqual(x['public'], 'x')
    try:
      x['_private']
      self.fail('Should not be able to getitem with _name')
    except KeyError:
      pass

    del x._private
    try:
      x._private
      self.fail('Should not be able to access deleted member')
    except AttributeError:
      pass

  def test_get_set_del_item(self):
    x = build_test_object()

    # Check for expected members using different access patterns.
    self.assert_(isinstance(x._dict, dict))
    self.assert_(isinstance(x['data'], gdata.core.Jsonc))
    self.assert_(isinstance(x._dict['data'], gdata.core.Jsonc))
    self.assert_(isinstance(x['data']._dict, dict))
    self.assert_(isinstance(x._dict['data']._dict, dict))
    self.assert_(isinstance(x['apiVersion'], (str, unicode)))
    try:
      x['api_version']
      self.fail('Should not find using Python style name')
    except KeyError:
      pass
    self.assert_(isinstance(x.data['items'], list))
    self.assert_(isinstance(x.data['items'][0]._dict['commentCount'],
                            (int, long)))
    self.assert_(isinstance(x['data'].items[0]['favoriteCount'], (int, long)))
    self.assertEqual(x['data'].total_items, 800)
    self.assertEqual(x['data']['totalItems'], 800)
    self.assertEqual(x.data['items'][0]['viewCount'], 220101)
    self.assertEqual(x._dict['data'].items[0]._dict['viewCount'],
                     220101)
    self.assertEqual(x['data'].items[0].comment_count, 22)
    self.assertEqual(x.data.items[0]['commentCount'], 22)
    self.assertEqual(x.data.items[0]['favoriteCount'], 201)
    self.assertEqual(x.data.items[0]._dict['favoriteCount'], 201)
    self.assertEqual(
        x.data.items[0].content['1'],
        'rtsp://v5.cache3.c.youtube.com/CiILENy.../0/0/0/video.3gp')
    self.assertEqual(
        x.data.items[0]['content']['1'],
        'rtsp://v5.cache3.c.youtube.com/CiILENy.../0/0/0/video.3gp')
    self.assertEqual(x.api_version, '2.0')
    self.assertEqual(x['apiVersion'], x._dict['apiVersion'])

    # Set properties using setitem
    x['apiVersion'] = '3.2'
    self.assertEqual(x.api_version, '3.2')
    x.data['totalItems'] = 500
    self.assertEqual(x['data'].total_items, 500)
    self.assertEqual(x['data'].items[0].favoriteCount, 201)
    try:
      del x['data']['favoriteCount']
      self.fail('Should not be able to delete missing item')
    except KeyError:
      pass
    del x.data['items'][0]['favoriteCount']
    try:
      x['data'].items[0].favoriteCount
      self.fail('Should not find favoriteCount removed using del item')
    except AttributeError:
      pass


def suite():
  return conf.build_suite([JsoncConversionTest, MemberNameConversionTest,
                           JsoncObjectTest])


if __name__ == '__main__':
  unittest.main()
