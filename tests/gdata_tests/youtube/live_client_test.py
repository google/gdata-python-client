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

# This module is used for version 2 of the Google Data APIs.
# These tests attempt to connect to Google servers.


__author__ = 's@google.com (John Skidgel)'

# Python imports.
import unittest
import urllib
import urllib2

# Google Data APIs imports.
import gdata.youtube.client
import gdata.youtube.data
import gdata.gauth
import gdata.client
import atom.http_core
import atom.mock_http_core
import atom.core
import gdata.data
import gdata.test_config as conf


# Constants
#DEVELOPER_KEY = 'AI39si4DTx4tY1ZCnIiZJrxtaxzfYuomY20SKDSfIAYrehKForeoHVgAgJZdNcYhmugD103wciae6TRI6M96nSymS8TV1kNP7g'
#CLIENT_ID = 'ytapi-Google-CaptionTube-2rj5q0oh-0'

conf.options.register_option(conf.YT_DEVELOPER_KEY_OPTION)
conf.options.register_option(conf.YT_CLIENT_ID_OPTION)
conf.options.register_option(conf.YT_VIDEO_ID_OPTION)

TRACK_BODY_SRT = """1

00:00:04,0  --> 00:00:05,75
My other computer is a data center
"""

class YouTubeClientTest(unittest.TestCase):
  def setUp(self):
    self.client = None
    if conf.options.get_value('runlive') == 'true':
      self.client = gdata.youtube.client.YouTubeClient()
      
      conf.configure_client(self.client,
          'YouTubeTest',
          'youtube')

  def tearDown(self):
    conf.close_client(self.client)

  def test_retrieve_video_entry(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_retrieve_video_entry')
    entry = self.client.get_video_entry(video_id=conf.options.get_value('videoid'))
    self.assertTrue(entry.etag)
  
  def test_retrieve_video_feed(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_retrieve_video_has_entries')

    entries = self.client.get_videos()
    self.assertTrue(len(entries.entry) > 0)
  
  def test_retrieve_user_feed(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_retrieve_video_has_entries')

    entries = self.client.get_user_feed(username='joegregoriotest')
    self.assertTrue(len(entries.entry) > 0)

  def test_create_update_delete_captions(self):
    if not conf.options.get_value('runlive') == 'true':
      return
    # Either load the recording or prepare to make a live request.
    conf.configure_cache(self.client, 'test_create_update_delete_captions')

    # Add a track.
    created = self.client.create_track(conf.options.get_value('videoid'), 'Test', 'en',
        TRACK_BODY_SRT, conf.options.get_value('clientid'),
        conf.options.get_value('developerkey'))
    
    self.assertEqual(created.__class__, gdata.youtube.data.TrackEntry)
    
    # Update the contents of a track. Language and title cannot be
    # updated due to limitations. A workaround is to delete the original
    # track and replace it with captions that have the desired contents,
    # title, and name. 
    # @see 'Updating a caption track' in the protocol guide for captions:
    # http://code.google.com/intl/en/apis/youtube/2.0/
    # developers_guide_protocol_captions.html
    updated = self.client.update_track(conf.options.get_value('videoid'), created,
        TRACK_BODY_SRT, conf.options.get_value('clientid'),
        conf.options.get_value('developerkey'))
    
    self.assertEqual(updated.__class__, gdata.youtube.data.TrackEntry)
    
    # Retrieve the captions for the track for comparision testing.
    track_url = updated.content.src
    track = self.client.get_caption_track(
        track_url, conf.options.get_value('clientid'),
        conf.options.get_value('developerkey'))
    track_contents = track.read()
    
    self.assertEqual(track_contents, TRACK_BODY_SRT)
    
    # Delete a track.
    resp = self.client.delete_track(conf.options.get_value('videoid'), 
        created,
        conf.options.get_value('clientid'),
        conf.options.get_value('developerkey'))
    self.assertEqual(200, resp.status)


def suite():
  return conf.build_suite([YouTubeClientTest])


if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())
