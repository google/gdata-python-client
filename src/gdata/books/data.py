#!/usr/bin/python
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


"""Contains the data classes of the Google Book Search Data API"""


__author__ = 'j.s@google.com (Jeff Scudder)'


import atom.core
import atom.data
import gdata.data
import gdata.dublincore.data
import gdata.opensearch.data


GBS_TEMPLATE = '{http://schemas.google.com/books/2008/}%s'


class CollectionEntry(gdata.data.BatchEntry):
  """Describes an entry in a feed of collections"""


class CollectionFeed(gdata.data.BatchFeed):
  """Describes a Book Search collection feed"""
  entry = [CollectionEntry]


class Embeddability(atom.core.XmlElement):
  """Describes an embeddability"""
  _qname = GBS_TEMPLATE % 'embeddability'
  value = 'value'


class OpenAccess(atom.core.XmlElement):
  """Describes an open access"""
  _qname = GBS_TEMPLATE % 'openAccess'
  value = 'value'


class Review(atom.core.XmlElement):
  """User-provided review"""
  _qname = GBS_TEMPLATE % 'review'
  type = 'type'
  lang = 'lang'


class Viewability(atom.core.XmlElement):
  """Describes a viewability"""
  _qname = GBS_TEMPLATE % 'viewability'
  value = 'value'


class VolumeEntry(gdata.data.BatchEntry):
  """Describes an entry in a feed of Book Search volumes"""
  subject = [gdata.dublincore.data.Subject]
  rating = gdata.data.Rating
  review = Review
  identifier = [gdata.dublincore.data.Identifier]
  dc_title = [gdata.dublincore.data.Title]
  embeddability = Embeddability
  comments = gdata.data.Comments
  creator = [gdata.dublincore.data.Creator]
  format = [gdata.dublincore.data.Format]
  viewability = Viewability
  date = [gdata.dublincore.data.Date]
  description = [gdata.dublincore.data.Description]
  publisher = [gdata.dublincore.data.Publisher]
  language = [gdata.dublincore.data.Language]
  open_access = OpenAccess


class VolumeFeed(gdata.data.BatchFeed):
  """Describes a Book Search volume feed"""
  entry = [VolumeEntry]


