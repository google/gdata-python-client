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


__author__ = 'j.s@google.com (Jeff Scudder)'


import atom.core


# TODO: once atom Link exists, inherit from that.
class Link(atom.core.XmlElement):
  _qname = '{http://www.w3.org/2005/Atom}link'
  rel = 'rel'
  href = 'href'


# TODO: remove this once atom Entry and Feed exist.
class FeedEntryParent(atom.core.XmlElement):
  etag = '{http://schemas.google.com/g/2005}etag'
  link = [Link]

  def find_url(self, rel):
    for link in self.link:
      if link.rel == rel and link.href:
        return link.href
    return None


# TODO: once atom Entry exists, inherit from that.
class GEntry(FeedEntryParent):
  _qname = '{http://www.w3.org/2005/Atom}entry'

  def get_edit_url(self):
    return self.find_url('edit')

  GetEditUrl = get_edit_url


def entry_from_string(xml_string, version=1, encoding='UTF-8'):
  return atom.core.xml_element_from_string(xml_string, GEntry, version, 
                                           encoding)


EntryFromString = entry_from_string


# TODO: once atom Feed exists, inherit from that.
class GFeed(FeedEntryParent):
  _qname = '{http://www.w3.org/2005/Atom}feed'
  entry = [GEntry]

  def get_next_url(self):
    return self.find_url('next')

  GetNextUrl = get_next_url


def feed_from_string(xml_string, version=1, encoding='UTF-8'):
  return atom.core.xml_element_from_string(xml_string, GFeed, version, 
                                           encoding)


FeedFromString = feed_from_string


# Used as a placeholder until the GDEntry is fully specified.
# GDEntry is used in 
# http://code.google.com/p/gdata-python-client/wiki/WritingDataModelClasses
GDEntry = GEntry
GDFeed = GFeed
