#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
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


__author__ = 'api.jscudder (Jeff Scudder)'


import unittest
from gdata import test_data
import gdata.blogger


class BlogEntryTest(unittest.TestCase):

  def testBlogEntryFromString(self):
    entry = gdata.blogger.BlogEntryFromString(test_data.BLOG_ENTRY)
    self.assertEquals(entry.GetBlogName(), 'blogName')
    self.assertEquals(entry.GetBlogId(), 'blogID')
    self.assertEquals(entry.title.text, 'Lizzy\'s Diary')

  def testBlogPostFeedFromString(self):
    feed = gdata.blogger.BlogPostFeedFromString(test_data.BLOG_POSTS_FEED)
    self.assertEquals(len(feed.entry), 1)
    self.assert_(isinstance(feed, gdata.blogger.BlogPostFeed))
    self.assert_(isinstance(feed.entry[0], gdata.blogger.BlogPostEntry))
    self.assertEquals(feed.entry[0].GetPostId(), 'postID')
    self.assertEquals(feed.entry[0].GetBlogId(), 'blogID')
    self.assertEquals(feed.entry[0].title.text, 'Quite disagreeable')

  def testCommentFeedFromString(self):
    feed = gdata.blogger.CommentFeedFromString(test_data.BLOG_COMMENTS_FEED)
    self.assertEquals(len(feed.entry), 1)
    self.assert_(isinstance(feed, gdata.blogger.CommentFeed))
    self.assert_(isinstance(feed.entry[0], gdata.blogger.CommentEntry))
    self.assertEquals(feed.entry[0].GetBlogId(), 'blogID')
    self.assertEquals(feed.entry[0].GetCommentId(), 'commentID')
    self.assertEquals(feed.entry[0].title.text, 'This is my first comment')


if __name__ == '__main__':
  unittest.main()
#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
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


__author__ = 'api.jscudder (Jeff Scudder)'


import unittest
from gdata import test_data
import gdata.blogger


class BlogEntryTest(unittest.TestCase):

  def testBlogEntryFromString(self):
    entry = gdata.blogger.BlogEntryFromString(test_data.BLOG_ENTRY)
    self.assertEquals(entry.GetBlogName(), 'blogName')
    self.assertEquals(entry.GetBlogId(), 'blogID')
    self.assertEquals(entry.title.text, 'Lizzy\'s Diary')

  def testBlogPostFeedFromString(self):
    feed = gdata.blogger.BlogPostFeedFromString(test_data.BLOG_POSTS_FEED)
    self.assertEquals(len(feed.entry), 1)
    self.assert_(isinstance(feed, gdata.blogger.BlogPostFeed))
    self.assert_(isinstance(feed.entry[0], gdata.blogger.BlogPostEntry))
    self.assertEquals(feed.entry[0].GetPostId(), 'postID')
    self.assertEquals(feed.entry[0].GetBlogId(), 'blogID')
    self.assertEquals(feed.entry[0].title.text, 'Quite disagreeable')

  def testCommentFeedFromString(self):
    feed = gdata.blogger.CommentFeedFromString(test_data.BLOG_COMMENTS_FEED)
    self.assertEquals(len(feed.entry), 1)
    self.assert_(isinstance(feed, gdata.blogger.CommentFeed))
    self.assert_(isinstance(feed.entry[0], gdata.blogger.CommentEntry))
    self.assertEquals(feed.entry[0].GetBlogId(), 'blogID')
    self.assertEquals(feed.entry[0].GetCommentId(), 'commentID')
    self.assertEquals(feed.entry[0].title.text, 'This is my first comment')


if __name__ == '__main__':
  unittest.main()
