#!/usr/bin/python
#
# Copyright (C) 2007 Google Inc.
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

"""Classes to interact with the Blogger server."""

__author__ = 'api.jscudder (Jeffrey Scudder)'

import gdata.service
import gdata.blogger


class BloggerService(gdata.service.GDataService):

  def __init__(self, email=None, password=None, source=None,
               server=None, api_key=None,
               additional_headers=None):
    gdata.service.GDataService.__init__(self, email=email, password=password,
                                        service='blogger', source=source,
                                        server=server,
                                        additional_headers=additional_headers)

  def GetBlogFeed(self, uri):
    return self.Get(uri, converter=gdata.blogger.BlogFeedFromString)

  def GetBlogCommentFeed(self, uri):
    return self.Get(uri, converter=gdata.blogger.BlogCommentFeedFromString)

  def GetBlogPostFeed(self, uri):
    return self.Get(uri, converter=gdata.blogger.BlogPostFeedFromString)

  def GetPostCommentFeed(self, uri):
    return self.Get(uri, converter=gdata.blogger.PostCommentFeedFromString)

  def AddPost(self, entry, blog_id=None, uri=None):
    if blog_id:
      uri = 'http://www.blogger.com/feeds/%s/posts/default' % blog_id
    return self.Post(entry, uri, 
                     converter=gdata.blogger.BlogPostEntryFromString)

  def UpdatePost(self, entry, uri=None):
    if not uri:
      uri = entry.GetEditLink().href
    return self.Put(entry, uri, 
                    converter=gdata.blogger.BlogPostEntryFromString)

  def PostComment(self, comment_entry, blog_id=None, post_id=None, uri=None):
    # TODO
    pass

