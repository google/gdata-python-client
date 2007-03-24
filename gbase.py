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

"""Contains extensions to Atom objects used with Google Base."""

__author__ = 'api.jscudder (Jeffrey Scudder)'


#TODO: create the following GBaseAttribute, GBaseAttributesFeed, GBaseItemType, GBaseItemTypeFeed, Attribute, Value, ...

from elementtree import ElementTree
import atom
import gdata


# XML namespaces which are often used in Google Base entities.
GBASE_NAMESPACE = 'http://base.google.com/ns/1.0'
GBASE_TEMPLATE = '{http://base.google.com/ns/1.0}%s'
GMETA_NAMESPACE = 'http://base.google.com/ns-metadata/1.0'
GMETA_TEMPLATE = '{http://base.google.com/ns-metadata/1.0}%s'

class GBaseItemFeed(gdata.GDataFeed):
  """A feed containing Google Base Items"""

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_GBaseItemFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataFeed._TransferFromElementTree(self, element_tree)

def GBaseItemFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _GBaseItemFeedFromElementTree(element_tree)

def _GBaseItemFeedFromElementTree(element_tree):
  return atom._XFromElementTree(GBaseItemFeed, 'feed', atom.ATOM_NAMESPACE,
      element_tree)


class GBaseSnippetFeed(GBaseItemFeed):
  """A feed containing Google Base Snippets"""

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_GBaseSnippetFromElementTree(child))
      element_tree.remove(child)
    else:
      GBaseItemFeed._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    GBaseItemFeed._TransferFromElementTree(self, element_tree)

def GBaseSnippetFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _GBaseSnippetFeedFromElementTree(element_tree)

_GBaseSnippetFeedFromElementTree = atom._AtomInstanceFromElementTree(
    GBaseSnippetFeed, 'feed', atom.ATOM_NAMESPACE)


class GBaseAttributesFeed(gdata.GDataFeed):
  """A feed containing Google Base Attributes
 
  A query sent to the attributes feed will return a feed of
  attributes which are present in the items that match the
  query. 
  """

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_GBaseAttributeEntryFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataFeed._TransferFromElementTree(self, element_tree)

def GBaseAttributesFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _GBaseAttributesFeedFromElementTree(element_tree)

_GBaseAttributesFeedFromElementTree = atom._AtomInstanceFromElementTree(
    GBaseAttributesFeed, 'feed', atom.ATOM_NAMESPACE)


class GBaseLocalesFeed(gdata.GDataFeed):
  """The locales feed from Google Base.

  This read-only feed defines the permitted locales for Google Base. The 
  locale value identifies the language, currency, and date formats used in a
  feed.
  """
  pass

def GBaseLocalesFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _GBaseLocalesFeedFromElementTree(element_tree)

_GBaseLocalesFeedFromElementTree = atom._AtomInstanceFromElementTree(
    GBaseLocalesFeed, 'feed', atom.ATOM_NAMESPACE)


class ItemAttributeContainer(object):
  """Provides methods for finding Google Base Item attributes.
  
  Google Base item attributes are child nodes in the gbase namespace. Google
  Base allows you to define your own item attributes and this class provides
  methods to interact with the custom attributes.   
  """

  def FindItemAttribute(self, name):
    """Get the contents of the first Base item attribute which matches name.
    
    Args: 
      name: str The tag of the desired base attribute. For example, calling
          this method with name = 'rating' would search for a tag rating
          in the GBase namespace in the item attributes. 

    Returns:
      The text contents of the item attribute, or none if the attribute was
      not found.
    """
  
    for attrib in self.item_attributes:
      if attrib.name == name:
        return attrib.text
    return None

  def AddItemAttribute(self, name, value, value_type=None):
    """Adds a new item attribute tag containing the value.
    
    Creates a new extension element in the GBase namespace to represent a
    Google Base item attribute.
    
    Args:
      name: str The tag name for the new attribute. This must be a valid xml
        tag name. The tag will be placed in the GBase namespace.
      value: str Contents for the item attribute
      value_type: str (optional) The type of data in the vlaue, Examples: text
          float
    """

    new_attribute =  ItemAttribute(name, text=value, 
        text_type=value_type)
    self.item_attributes.append(new_attribute)
    
  def SetItemAttribute(self, name, value):
    """Changes an existing item attribute's value."""

    for attrib in self.item_attributes:
      if attrib.name == name:
        attrib.text = value
        return

  def RemoveItemAttribute(self, name):
    """Deletes the first extension element which matches name.
    
    Deletes the first extension element which matches name. 
    """

    for i in xrange(len(self.item_attributes)):
      if self.item_attributes[i].name == name:
        del self.item_attributes[i]
        return


class ItemAttribute(atom.Text):
  """An optional or user defined attribute for a GBase item.
  
  Google Base allows items to have custom attribute child nodes. These nodes
  have contents and a type attribute which tells Google Base whether the
  contents are text, a float value with units, etc. The Atom text class has 
  the same structure, so this class inherits from Text.
  """

  def __init__(self, name, text_type=None, text=None, 
      extension_elements=None, extension_attributes=None):
    """Constructor for a GBase item attribute

    Args:
      name: str The name of the attribute. Examples include
          price, color, make, model, pages, salary, etc.
      text_type: str (optional) The type associated with the text contents
      text: str (optional) The text data in the this element
      extension_elements: list (optional) A  list of ExtensionElement 
          instances
      extension_attributes: dict (optional) A dictionary of attribute 
          value string pairs
    """

    self.name = name
    self.type = text_type
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.name:
      element_tree.tag = GBASE_TEMPLATE % self.name
    atom.Text._TransferToElementTree(self, element_tree)
    return element_tree

  def _TransferFromElementTree(self, element_tree):
    full_tag = element_tree.tag
    if full_tag.find(GBASE_TEMPLATE % '') == 0:
      self.name = full_tag[full_tag.index('}')+1:]
    # Transfer all xml attributes and children
    atom.Text._TransferFromElementTree(self, element_tree)

def ItemAttributeFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _ItemAttributeFromElementTree(element_tree)

def _ItemAttributeFromElementTree(element_tree):
  if element_tree.tag.find(GBASE_TEMPLATE % '') == 0:
    to_return = ItemAttribute('')
    to_return._TransferFromElementTree(element_tree)
    if to_return.name and to_return.name != '':
      return to_return
  return None
  

class GBaseItem(gdata.GDataEntry, ItemAttributeContainer):
  """An Google Base flavor of an Atom Entry.
  
  Google Base items have required attributes, recommended attributes, and user
  defined attributes. The required attributes are stored in this class as 
  members, and other attributes are stored as extension elements. You can 
  access the recommended and user defined attributes by using 
  AddItemAttribute, SetItemAttribute, FindItemAttribute, and 
  RemoveItemAttribute.
  
  The Base Item
  """
  
  def __init__(self, author=None, category=None, content=None,
      contributor=None, atom_id=None, link=None, published=None, rights=None,
      source=None, summary=None, title=None, updated=None, label=None, 
      item_type=None, item_attributes=None,
      text=None, extension_elements=None, extension_attributes=None):
    self.author = author or []
    self.category = category or []
    self.content = content
    self.contributor = contributor or []
    self.id = atom_id
    self.link = link or []
    self.published = published
    self.rights = rights
    self.source = source
    self.summary = summary
    self.title = title
    self.updated = updated
    self.label = label or []
    self.item_type = item_type
    self.item_attributes = item_attributes or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    for a_label in self.label:
      element_tree.append(a_label._ToElementTree())
    # Added: converting the item type to XML
    if self.item_type:
      element_tree.append(self.item_type._ToElementTree())
    for attribute in self.item_attributes:
      element_tree.append(attribute._ToElementTree())
    atom.Entry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (GBASE_NAMESPACE, 'label'):
      self.label.append(_LabelFromElementTree(child))
      element_tree.remove(child)
    # Added: finding the the item type
    elif child.tag == '{%s}%s' % (GBASE_NAMESPACE, 'item_type'):
      self.item_type = _ItemTypeFromElementTree(child)
      element_tree.remove(child)
    elif child.tag.find('{%s}' % GBASE_NAMESPACE) == 0:
      # If the tag is in the GBase namespace, make it into an extension 
      # attribute.
      item_attribute = _ItemAttributeFromElementTree(child)
      if item_attribute:
        self.item_attributes.append(item_attribute)
        element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    atom.Entry._TransferFromElementTree(self, element_tree)

def GBaseItemFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _GBaseItemFromElementTree(element_tree)

def _GBaseItemFromElementTree(element_tree):
  return atom._XFromElementTree(GBaseSnippet, 'entry', atom.ATOM_NAMESPACE, 
      element_tree)


class GBaseSnippet(GBaseItem):
  pass

def GBaseSnippetFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _GBaseSnippetFromElementTree(element_tree)

def _GBaseSnippetFromElementTree(element_tree):
  return atom._XFromElementTree(GBaseSnippet, 'entry', atom.ATOM_NAMESPACE,
      element_tree)

class Label(atom.AtomBase):
  """The Google Base label element"""

  def __init__(self, text=None, extension_elements=None,
      extension_attributes=None):
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    element_tree.tag = GBASE_TEMPLATE % 'label'
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

def LabelFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _LabelFromElementTree(element_tree)

def _LabelFromElementTree(element_tree):
  return atom._XFromElementTree(Label, 'label', GBASE_NAMESPACE, 
      element_tree)


class ItemType(atom.Text):
  """The Google Base item_type element"""

  def __init__(self, text=None, extension_elements=None,
      text_type=None, extension_attributes=None):
    self.text = text
    self.type = text_type
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    element_tree.tag = GBASE_TEMPLATE % 'item_type'
    atom.Text._TransferToElementTree(self, element_tree)
    return element_tree

def ItemTypeFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _ItemTypeFromElementTree(element_tree)

def _ItemTypeFromElementTree(element_tree):
  return atom._XFromElementTree(ItemType, 'item_type', GBASE_NAMESPACE,
      element_tree)


class Value(atom.AtomBase):
  """Metadata about common values for a given attribute
  
  A value is a child of an attribute which comes from the attributes feed.
  The value's text is a commonly used value paired with an attribute name
  and the value's count tells how often this value appears for the given
  attribute in the search results.
  """
 
  def __init__(self, count=None, text=None, extension_elements=None, 
      extension_attributes=None):
    """Constructor for Attribute metadata element

    Args:
      count: str (optional) The number of times the value in text is given
          for the parent attribute.
      text: str (optional) The value which appears in the search results.
      extension_elements: list (optional) A  list of ExtensionElement
          instances
      extension_attributes: dict (optional) A dictionary of attribute value
          string pairs
    """

    self.count = count
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.count:
      element_tree.attrib['count'] = self.count
    atom.AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = GMETA_TEMPLATE % 'value'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'count':
      self.count = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)

def ValueFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _ValueFromElementTree(element_tree)

_ValueFromElementTree = atom._AtomInstanceFromElementTree(Value,
    'value', GMETA_NAMESPACE)
 
  

class Attribute(atom.Text):
  """Metadata about an attribute from the attributes feed
  
  An entry from the attributes feed contains a list of attributes. Each 
  attribute describes the attribute's type and count of the items which
  use the attribute.
  """

  def __init__(self, name=None, attribute_type=None, count=None, value=None, 
      text=None, extension_elements=None, extension_attributes=None):
    """Constructor for Attribute metadata element

    Args:
      name: str (optional) The name of the attribute
      attribute_type: str (optional) The type for the attribute. Examples:
          test, float, etc.
      count: str (optional) The number of times this attribute appears in
          the query results.
      value: list (optional) The values which are often used for this 
          attirbute.
      text: str (optional) The text contents of the XML for this attribute.
      extension_elements: list (optional) A  list of ExtensionElement 
          instances
      extension_attributes: dict (optional) A dictionary of attribute value 
          string pairs
    """

    self.name = name
    self.type = attribute_type
    self.count = count
    self.value = value or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.name:
      element_tree.attrib['name'] = self.name
    if self.count:
      element_tree.attrib['count'] = self.count
    for a_value in self.value:
      element_tree.append(a_value._ToElementTree())
    atom.Text._TransferToElementTree(self, element_tree)
    element_tree.tag = GMETA_TEMPLATE % 'attribute'
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (GMETA_NAMESPACE, 'value'):
      self.value.append(_ValueFromElementTree(child))
      element_tree.remove(child)
    else:
      atom.Text._TakeChildFromElementTree(self, child, element_tree)

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'count':
      self.count = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'name':
      self.name = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.Text._TakeAttributeFromElementTree(self, attribute, element_tree)

def AttributeFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _AttributeFromElementTree(element_tree)

_AttributeFromElementTree = atom._AtomInstanceFromElementTree(Attribute, 
    'attribute', GMETA_NAMESPACE)


class GBaseAttributeEntry(gdata.GDataEntry):
  """An Atom Entry from the attributes feed"""

  def __init__(self, author=None, category=None, content=None,
      contributor=None, atom_id=None, link=None, published=None, rights=None,
      source=None, summary=None, title=None, updated=None, label=None,
      attribute=None,
      text=None, extension_elements=None, extension_attributes=None):
    self.author = author or []
    self.category = category or []
    self.content = content
    self.contributor = contributor or []
    self.id = atom_id
    self.link = link or []
    self.published = published
    self.rights = rights
    self.source = source
    self.summary = summary
    self.title = title
    self.updated = updated
    self.label = label or []
    self.attribute = attribute or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {} 

  def _TransferToElementTree(self, element_tree):
    for an_attribute in self.attribute:
      element_tree.append(an_attribute._ToElementTree())
    gdata.GDataEntry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (GMETA_NAMESPACE, 'attribute'):
      self.attribute.append(_AttributeFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataEntry._TransferFromElementTree(self, element_tree)

def GBaseAttributeEntryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _GBaseAttributeEntryFromElementTree(element_tree)

_GBaseAttributeEntryFromElementTree = atom._AtomInstanceFromElementTree(
    GBaseAttributeEntry, 'entry', atom.ATOM_NAMESPACE)


class GBaseItemTypeEntry(gdata.GDataEntry):
  """An Atom entry from the item types feed
  
  These entries contain a list of attributes which are stored in one
  XML node called attributes. This class simplifies the data structure
  by treating attributes as a list of attribute instances. 
  """

  def __init__(self, author=None, category=None, content=None,
      contributor=None, atom_id=None, link=None, published=None, rights=None,
      source=None, summary=None, title=None, updated=None, label=None,
      item_type=None, attributes=None,
      text=None, extension_elements=None, extension_attributes=None):
    self.author = author or []
    self.category = category or []
    self.content = content
    self.contributor = contributor or []
    self.id = atom_id
    self.link = link or []
    self.published = published
    self.rights = rights
    self.source = source
    self.summary = summary
    self.title = title
    self.updated = updated
    self.label = label or []
    self.item_type = item_type
    self.attributes = attributes or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    attribute_list = ElementTree.Element(GMETA_TEMPLATE % 'attributes')
    for an_attribute in self.attributes:
      attribute_list.append(an_attribute._ToElementTree())
    if len(attribute_list) > 0:
      element_tree.append(attribute_list)
    if self.item_type:
      element_tree.append(self.item_type._ToElementTree())
    gdata.GDataEntry._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (GMETA_NAMESPACE, 'attributes'):
      while len(child) > 0:
        if child[0].tag == '{%s}%s' % (GMETA_NAMESPACE, 'attribute'):
          self.attributes.append(_AttributeFromElementTree(child[0]))
          child.remove(child[0])
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (GMETA_NAMESPACE, 'attribute'):
      self.attributes.append(_AttributeFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (GBASE_NAMESPACE, 'item_type'):
      self.item_type = _ItemTypeFromElementTree(child)
      element_tree.remove(child)
    else:
      gdata.GDataEntry._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataEntry._TransferFromElementTree(self, element_tree)

def GBaseItemTypeEntryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _GBaseItemTypeEntryFromElementTree(element_tree)

_GBaseItemTypeEntryFromElementTree = atom._AtomInstanceFromElementTree(
    GBaseItemTypeEntry, 'entry', atom.ATOM_NAMESPACE)
 

class GBaseItemTypesFeed(gdata.GDataFeed):
  """A feed from the Google Base item types feed"""

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (atom.ATOM_NAMESPACE, 'entry'):
      self.entry.append(_GBaseItemTypeEntryFromElementTree(child))
      element_tree.remove(child)
    else:
      gdata.GDataFeed._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    gdata.GDataFeed._TransferFromElementTree(self, element_tree)

def GBaseItemTypesFeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _GBaseItemTypesFeedFromElementTree(element_tree)

def _GBaseItemTypesFeedFromElementTree(element_tree):
  return atom._XFromElementTree(GBaseItemTypesFeed, 'feed', atom.ATOM_NAMESPACE,
      element_tree)
