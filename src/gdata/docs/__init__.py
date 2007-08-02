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

"""Contains extensions to Atom objects used with Google Documents."""

__author__ = 'api.jfisher (Jeff Fisher)'

try:
  from xml.etree import cElementTree as ElementTree
except ImportError:
  try:
    import cElementTree as ElementTree
  except ImportError:
    from elementtree import ElementTree
import atom
import gdata


class DocumentListFeed(gdata.GDataFeed):
  """A feed containing a list of Google Documents Items"""

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_DocumentListEntryFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataFeed._TransferFromElementTree(self, element_tree)


def DocumentListFeedFromString(xml_string):
  """Converts an XML string into a DocumentListFeed object.

  Args:
    xml_string: string The XML describing a DocumentList feed.

  Returns:
    A DocumentListFeed object corresponding to the given XML.
  """
  element_tree = ElementTree.fromstring(xml_string)
  return _DocumentListFeedFromElementTree(element_tree)


# Generate function to handle feed parsing using ElementTree.
_DocumentListFeedFromElementTree = atom._AtomInstanceFromElementTree(
    DocumentListFeed, 'feed', atom.ATOM_NAMESPACE)


class DocumentListEntry(gdata.GDataEntry):
  """The Google Documents version of an Atom Entry"""
  pass


def DocumentListEntryFromString(xml_string):
  """Converts an XML string into a DocumentListEntry object.

  Args:
    xml_string: string The XML describing a Document List feed entry.

  Returns:
    A DocumentListEntry object corresponding to the given XML.
  """
  element_tree = ElementTree.fromstring(xml_string)
  return _DocumentListEntryFromElementTree(element_tree)


# Generate function to handle feed entry parsing using ElementTree.
_DocumentListEntryFromElementTree = atom._AtomInstanceFromElementTree(
    DocumentListEntry, 'entry', atom.ATOM_NAMESPACE)
