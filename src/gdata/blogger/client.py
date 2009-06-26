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


"""Contains a client to communicate with the Blogger servers."""


__author__ = 'j.s@google.com (Jeff Scudder)'


import gdata.client
import gdata.data.blogger


# List user's blogs, takes a user ID, or 'default'.
BLOGS_URL = 'http://www.blogger.com/feeds/%s/blogs'
# Takes a blog ID.
BLOG_POST_URL = 'http://www.blogger.com/feeds/%s/posts/default'
# Takes a blog ID and post ID.
BLOG_POST_COMMENTS_URL = 'http://www.blogger.com/feeds/%s/%s/comments/default'
# Takes a blog ID.
BLOG_COMMENTS_URL = 'http://www.blogger.com/feeds/%s/comments/default'
# Takes a blog ID.
BLOG_ARCHIVE_URL = 'http://www.blogger.com/feeds/%s/archive/full'

class BloggerClient(gdata.client.GDClient):
  api_version = '2'
  auth_serice = 'blogger'
  auth_scopes = ['http://www.blogger.com/feeds/']

  def get_blogs(self, user_id='default', auth_token=None, 
                desired_class=gdata.blogger.data.BlogFeed, **kwargs):
    return self.get_feed(BLOGS_URL % user_id, auth_token=auth_token,
                         desired_class=desired_class, **kwargs)

