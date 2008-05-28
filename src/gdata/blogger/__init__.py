#!/usr/bin/python
#
# Copyright (C) 2007, 2008 Google Inc.
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


"""Contains extensions to Atom objects used with Blogger."""


__author__ = 'api.jscudder (Jeffrey Scudder)'


import atom
import gdata
import re


LABEL_SCHEME = 'http://www.blogger.com/atom/ns#'


class BloggerEntry(gdata.GDataEntry):
  """Adds convenience methods inherited by all Blogger entries."""

  blog_name_pattern = re.compile('(http://)(\w*)')
  blog_id_pattern = re.compile('(tag:blogger.com,1999:blog-)(\w*)')

  def GetBlogId(self):
    """Extracts the Blogger id of this blog.
    This method is useful when contructing URLs by hand. The blog id is
    often used in blogger operation URLs. This should not be confused with
    the id member of a BloggerBlog. The id element is the Atom id XML element.
    The blog id which this method returns is a part of the Atom id.

    Returns:
      The blog's unique id as a string.
    """
    if self.id.text:
      return self.blog_id_pattern.match(self.id.text).group(2)
    return None

  def GetBlogName(self):
    """Finds the name of this blog as used in the 'alternate' URL.
    An alternate URL is in the form 'http://blogName.blogspot.com/'. For an
    entry representing the above example, this method would return 'blogName'.

    Returns:
      The blog's URL name component as a string.
    """
    for link in self.link:
      if link.rel == 'alternate':
        return self.blog_name_pattern.match(link.href).group(2)
    return None


class BlogCommentEntry(BloggerEntry):
  """Describes a blog comment entry in the feed of a blog's comments.

  """
  pass


def BlogCommentEntryFromString(xml_string):
  return atom.CreateClassFromXMLString(BlogCommentEntry, xml_string)


class BlogCommentFeed(gdata.GDataFeed):
  """Describes a feed of a blog's comments.

  """
  pass


def BlogCommentFeedFromString(xml_string):
  return atom.CreateClassFromXMLString(BlogCommentFeed, xml_string)


class BlogEntry(BloggerEntry):
  """Describes a blog entry in the feed of a user's blogs.

  """
  pass


def BlogEntryFromString(xml_string):
  return atom.CreateClassFromXMLString(BlogEntry, xml_string)


class BlogFeed(gdata.GDataFeed):
  """Describes a feed of a user's blogs.

  """
  


def BlogFeedFromString(xml_string):
  return atom.CreateClassFromXMLString(BlogFeed, xml_string)


class BlogPostEntry(BloggerEntry):
  """Describes a blog post entry in the feed of a blog's posts.

  """

  def AddLabel(self, label):
    """Adds a label to the blog post. 

    The label is represented by an Atom category element, so this method
    is shorthand for appending a new atom.Category object.

    Args:
      label: str
    """
    self.category.append(atom.Category(scheme=LABEL_SCHEME, term=label))


def BlogPostEntryFromString(xml_string):
  return atom.CreateClassFromXMLString(BlogPostEntry, xml_string)


class BlogPostFeed(gdata.GDataFeed):
  """Describes a feed of a blog's posts.

  """
  pass


def BlogPostFeedFromString(xml_string):
  return atom.CreateClassFromXMLString(BlogPostFeed, xml_string)


class BloggerLink(atom.Link):
  """Extends the base Link class with Blogger extensions.

  """
  pass


def BloggerLinkFromString(xml_string):
  return atom.CreateClassFromXMLString(BloggerLink, xml_string)


class PostCommentEntry(BloggerEntry):
  """Describes a blog post comment entry in the feed of a blog post's comments.

  """
  pass


def PostCommentEntryFromString(xml_string):
  return atom.CreateClassFromXMLString(PostCommentEntry, xml_string)


class PostCommentFeed(gdata.GDataFeed):
  """Describes a feed of a blog post's comments.

  """
  pass


def PostCommentFeedFromString(xml_string):
  return atom.CreateClassFromXMLString(PostCommentFeed, xml_string)


