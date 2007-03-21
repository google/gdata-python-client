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


"""Contains classes representing Atom elements.

  Module objective: provide data classes for Atom constructs. These classes hide
  the XML-ness of Atom and provide a set of native Python classes to interact 
  with.

  Conversions to and from XML should only be necessary when the Atom classes
  "touch the wire" and are sent over HTTP. For this reason this module 
  provides  methods and functions to convert Atom classes to and from strings.

  For more information on the Atom data model, see RFC 4287 
  (http://www.ietf.org/rfc/rfc4287.txt)

  AtomBase: A foundation class on which Atom classes are built. It 
      handles the parsing of attributes and children which are common to all
      Atom classes. By default, the AtomBase class translates all XML child 
      nodes into ExtensionElements.

  ExtensionElement: Atom allows Atom objects to contain XML which is not part 
      of the Atom specification, these are called extension elements. If a 
      classes parser encounters an unexpected XML construct, it is translated
      into an ExtensionElement instance. ExtensionElement is designed to fully
      capture the information in the XML. Child nodes in an XML extension are
      turned into ExtensionElements as well.


"""


__author__ = 'api.jscudder (Jeffrey Scudder)'


from elementtree import ElementTree


# XML namespaces which are often used in GData entities.
ATOM_NAMESPACE = 'http://www.w3.org/2005/Atom'
ELEMENT_TEMPLATE = '{http://www.w3.org/2005/Atom}%s'


def _AtomInstanceFromElementTree(class_constructor, class_tag_name, 
    class_namespace):
  """Instantiates an instance of an Atom class.

  This is a template function which is used to generate factory functions like 
  AuthorFromElementTree, EntryFromElementTree, etc. The internal closure is 
  used to precompute the desired tag and improve performace. 

  Args:
    class_constructor: function The constructor which will be called if the
        element tree passed in later has a tag with the desired tag name and
        namespace.
    class_tag_name: str The tag name for the desired Atom instance. If the tag
        name and namespace do not match, a new object will not be created.
        Examples: 'entry', 'feed', 'email', etc.
    class_namespace: str The namespace for the desired Atom instance. In this
        module it is always ATOM_NAMESPACE, but other modules may specify a
        different namespace.

  Returns: 
    A function which takes an ElementTree._Element and creates an instance
    of the desired class if the tag and namespace are correct.
  """
  def TemplateFunction(element_tree):
    new_object = None
    if element_tree.tag == '{%s}%s' % (class_namespace, class_tag_name):
      new_object = class_constructor()
      new_object._TransferFromElementTree(element_tree)
    return new_object
  return TemplateFunction


class AtomBase(object):
  """A foundation class for all Atom entities to derive from.

  It provides data handling methods which are reused by the Atom classes.
  This class should never be instantiated directly, it provides method 
  implementations which are used by most of the classes in this module.
  """
  
  def __init__(self, extension_elements=None, extension_attributes=None, 
      text=None):
    """Constructor for the Atom base class.

    The constructor is provided for illustrative purposes, you should not
    need to instantiate an AtomBase.
    
    Args:
      extension_elements: list A list of ExtensionElement instances which are
          children of this element.
      extension_attributes: dict A dictionary of strings which are the values
          for additional XML attributes of this element.
      text: String The text contents of the element. This is the contents
          of the Entry's XML text node. (Example: <foo>This is the text</foo>)
    """
    self.extension_elements = []
    self.extension_attributes = {}
    self.text = None
    
  def _TransferToElementTree(self, element_tree):
    """Transfer this object's data to an element tree.

    Sets the text of the element_tree to the text of this object and converts
    all extension elements into child nodes in the element tree.
    
    Args:
      element_tree: ElementTree._Element The element tree to which all of this
          object's data will be transfered.
    
    Returns:
      The element_tree which was passed in. The original element_tree is returned
      in order to allow function chaining (ex: 
      DoSomethingWithElementTree(x._TransferToElementTree(element_tree))  ).
    """
    
    if self.extension_elements:
      for extension in self.extension_elements:
        # Create a new element tree which will hold the extensions's data. 
        # Note that the extension's _TransferToElementTree method will 
        # overwrite the element tree's tag.
        new_element_tree = ElementTree.Element('none')
        extension._TransferToElementTree(new_element_tree)
        element_tree.append(new_element_tree)
    if self.extension_attributes:
      for attribute, value in self.extension_attributes.iteritems():
        element_tree.attrib[attribute] = value
    element_tree.text = self.text
    return element_tree
    
  def ToString(self):
    """Converts the Atom object to a string containing XML."""
  
    return ElementTree.tostring(self._ToElementTree())

  def __str__(self):
    return self.ToString()
    
  def _ToElementTree(self):
    """Converts the Atom object to an ElementTree._Element."""
  
    return self._TransferToElementTree(ElementTree.Element(''))
    
  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    """Translates the XML attribute into a class attribute.

    In AtomBase, all XML attributes become extension attributes, but
    other Atom elements use selected XML attributes. In such cases, the
    extending Atom class overloads this method to transfer selected 
    attributes to class members.

    The attribute is removed from the element_tree so that it will not be
    processed by future method calls.
    
    Args:
      attribute: str The name of the attribute which should be processed.
      element_tree: ElementTree._Element The node which contains the 
          attribute. The element_tree is modified by this method.
    """
    
    self.extension_attributes[attribute] = element_tree.attrib[attribute]
    # Consume the attribute
    del element_tree.attrib[attribute]

  def _TakeChildFromElementTree(self, child, element_tree):
    """Translates an XML child node into a class attribute and add as a member.

    In AtomBase, all XML child nodes become extension elements, but
    other Atom elements translate selected XML elements into class members. 
    In such cases, the extending Atom class overloads this method to transfer 
    selected child nodes to class members.

    The child node is removed from the element_tree so that it will not be
    processed by future method calls.

    Args:
      child: ElementTree._Element The XML node in the element_tree which
          should be processed.
      element_tree: ElementTree._Element The node which contains the
          attribute. The element_tree is modified by this method.
    """    
    
    self.extension_elements.append(_ExtensionElementFromElementTree(child))
    # Consume the child element
    element_tree.remove(child)
    

  def _TransferFromElementTree(self, element_tree):
    """Creates extension elements and attributes from children in element_tree
    
    It also moves the text from the element_tree to the Base instance.
    Note that all element_tree children will become extension elements, so any
    children which should not become extension elements must be removed before
    calling this method. Also, all element attributes will become extension
    attributes so any attributes which should not become extensions must be
    removed prior to calling this method.

    Args:
      element_tree: ElementTree._Element The element tree whose data is moved to
          the Base instance. This function removes children from element_tree.
    """

    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    current_key = None
    while len(element_tree.attrib.keys()) > 0:
      current_key = element_tree.attrib.keys()[0]
      self._TakeAttributeFromElementTree(current_key, element_tree)
    self.text = element_tree.text 
    
  
class Person(AtomBase):
  """A foundation class from which atom:author and atom:contributor extend.
  
  This class should never be instantiated.
  """

  def __init__(self, name=None, email=None, uri=None, 
      extension_elements=None, extension_attributes=None, text=None):
    """Foundation from which author and contributor are derived.

    The constructor is provided for illustrative purposes, you should not
    need to instantiate a Person.
    
    Args:
      name: Name The person's name
      email: Email The person's email address
      uri: Uri The URI of the person's webpage
      extension_elements: list A list of ExtensionElement instances which are
          children of this element.
      extension_attributes: dict A dictionary of strings which are the values
          for additional XML attributes of this element.
      text: String The text contents of the element. This is the contents
          of the Entry's XML text node. (Example: <foo>This is the text</foo>)
    """

    self.name = name
    self.email = email
    self.uri = uri
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    self.text = text
    
  def _TransferToElementTree(self, element_tree):
    """Translates members into XML child nodes.
    
    Args:
      element_tree: ElementTree._Element The element tree to which child
          nodes will be added. The contents of this person will be converted
          to element trees and appended to the element_tree provided.
    """
    
    if self.name:
      element_tree.append(self.name._ToElementTree())
    if self.email:
      element_tree.append(self.email._ToElementTree())
    if self.uri:
      element_tree.append(self.uri._ToElementTree())
    # Call the parent's tranfer to method to convert all other class members
    # into XML nodes. By parent I mean superclass.
    AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    """Translates XML child nodes into Person members.
    
    Args:
      child: ElementTree._Element The child node in element_tree which is
          to be processed. If the child node is part of a person object, this
          method converts it to the appropriate object and adds it to the
          person. If the child node is not part of the person or an atom 
          object, it is turned into an extension element. In all cases the
          child node is removed from element_tree.
      element_tree: ElementTree._Element The parent of the child node. This
          method removes the child from element_tree after converting it to
          an Atom object.
    """
    
    if child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'name'):
      self.name = _NameFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'email'):
      self.email = _EmailFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'uri'):
      self.uri = _UriFromElementTree(child)
      element_tree.remove(child)
    else:
      # Call the parent's transfer method to process all other nodes. 
      # AtomBase turns all remaining child nodes into ExtensionElements.
      AtomBase._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    """Processes all XML child nodes and adds them to this Person instance.
    
    Args:
      element_tree: ElementTree._Element The element tree whose children are
          converted into Atom objects and stored as children of self.
    """

    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    AtomBase._TransferFromElementTree(self, element_tree)


class Author(Person):
  """The atom:author element"""

  def __init__(self, name=None, email=None, uri=None, 
      extension_elements=None, extension_attributes=None, text=None):
    """Constructor for Author
    
    Args:
      name: Name
      email: Email
      uri: Uri
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
      text: str The text data in the this element
    """
    
    self.name = name
    self.email = email
    self.uri = uri
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    self.text = text

  def _TransferToElementTree(self, element_tree):
    # Call the parent's tranfer to method to convert all other class members
    # into XML nodes. By parent I mean superclass.
    Person._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'author'
    return element_tree
    
def AuthorFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _AuthorFromElementTree(element_tree)
  
_AuthorFromElementTree = _AtomInstanceFromElementTree(Author, 'author', 
    ATOM_NAMESPACE)


def _XFromElementTree(class_x, x_tag, x_namespace, element_tree):
  """Creates instance of class X if the element_tree's tag and namespace are 
     correct.

  DEPRECATED
  
  Args:
    class_x: function The constructor method for the desired class.
    x_tag: str The expected tag for the desired class.
    x_namespace: str The expected namespace for the desired class.
    element_tree: ElementTree._Element The element_tree from which class data 
        is extracted. 
  
  Returns:
    An instance of class_x with the data from the element_tree, or None if the
    element_tree's tag and namespace were not the desired values.
  """

  new_object = None
  if element_tree.tag == '{%s}%s' % (x_namespace, x_tag):
    new_object = class_x()
    new_object._TransferFromElementTree(element_tree)
  return new_object


class Contributor(Person):
  """The atom:contributor element"""

  def __init__(self, name=None, email=None, uri=None,
      extension_elements=None, extension_attributes=None, text=None):
    """Constructor for Contributor
    
    Args:
      name: Name
      email: Email
      uri: Uri
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
      text: str The text data in the this element
    """

    self.name = name
    self.email = email
    self.uri = uri
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    self.text = text

  def _TransferToElementTree(self, element_tree):
    # Call the parent's tranfer to method to convert all other class members
    # into XML nodes.
    Person._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'contributor'
    return element_tree

def ContributorFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _ContributorFromElementTree(element_tree)

_ContributorFromElementTree = _AtomInstanceFromElementTree(Contributor, 
    'contributor', ATOM_NAMESPACE)
  
  
class Name(AtomBase):
  """The atom:name element"""

  def __init__(self, text=None, extension_elements=None, 
      extension_attributes=None):
    """Constructor for Name
    
    Args:
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    
  def _TransferToElementTree(self, element_tree):
    AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'name'
    return element_tree
  
def NameFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _NameFromElementTree(element_tree)
  
_NameFromElementTree = _AtomInstanceFromElementTree(Name, 'name', 
    ATOM_NAMESPACE)
  
  
class Email(AtomBase):
  """The atom:email element"""
  
  def __init__(self, text=None, extension_elements=None, 
      extension_attributes=None):
    """Constructor for Email
    
    Args:
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
      text: str The text data in the this element
    """

    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
  
  def _TransferToElementTree(self, element_tree):
    AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'email'
    return element_tree

def EmailFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _EmailFromElementTree(element_tree)
  
_EmailFromElementTree = _AtomInstanceFromElementTree(Email, 'email', 
    ATOM_NAMESPACE)


class Uri(AtomBase):
  """The atom:uri element"""

  def __init__(self, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Uri
    
    Args:
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
      text: str The text data in the this element
    """

    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'uri'
    return element_tree

def UriFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _UriFromElementTree(element_tree)

_UriFromElementTree = _AtomInstanceFromElementTree(Uri, 'uri', ATOM_NAMESPACE)
  
  
class Link(AtomBase):
  """The atom:link element"""
  
  def __init__(self, href=None, rel=None, type=None, hreflang=None, 
      title=None, length=None, text=None, extension_elements=None, 
      extension_attributes=None):
    """Constructor for Link
    
    Args:
      href: string The href attribute of the link
      rel: string
      type: string
      hreflang: string The language for the href
      title: string
      length: string The length of the href's destination
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
      text: str The text data in the this element
    """

    self.href = href
    self.rel = rel
    self.type = type
    self.hreflang = hreflang
    self.title = title
    self.length = length
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.href:
      element_tree.attrib['href'] = self.href
    if self.rel:
      element_tree.attrib['rel'] = self.rel
    if self.type:
      element_tree.attrib['type'] = self.type
    if self.hreflang:
      element_tree.attrib['hreflang'] = self.hreflang
    if self.title:
      element_tree.attrib['title'] = self.title
    if self.length:
      element_tree.attrib['length'] = self.length    
    AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'link'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'href':
      self.href = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'rel':
      self.rel = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'type':
      self.type = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'hreflang':
      self.hreflang = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'title':
      self.title = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'length':
      self.length = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)

  def _TransferFromElementTree(self, element_tree):
    # find all attributes
    while len(element_tree.attrib.keys()) > 0:
      current_key = element_tree.attrib.keys()[0]
      self._TakeAttributeFromElementTree(current_key, element_tree)
    AtomBase._TransferFromElementTree(self, element_tree)
    
def LinkFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _LinkFromElementTree(element_tree)
  
_LinkFromElementTree = _AtomInstanceFromElementTree(Link, 'link', 
    ATOM_NAMESPACE)


class Generator(AtomBase):
  """The atom:generator element"""

  def __init__(self, uri=None, version=None, text=None, 
      extension_elements=None, extension_attributes=None):
    """Constructor for Generator
    
    Args:
      uri: string
      version: string
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.uri = uri
    self.version = version
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.uri:
      element_tree.attrib['uri'] = self.uri
    if self.version:
      element_tree.attrib['version'] = self.version
    AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'generator'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'uri':
      self.uri = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'version':
      self.version = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      AtomBase._TakeAttributeFromElementTree(self, attribute, element_tree)

  def _TransferFromElementTree(self, element_tree):
    # find all attributes
    while len(element_tree.attrib.keys()) > 0:
      current_key = element_tree.attrib.keys()[0]
      self._TakeAttributeFromElementTree(current_key, element_tree)
    AtomBase._TransferFromElementTree(self, element_tree)

def GeneratorFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _GeneratorFromElementTree(element_tree)

_GeneratorFromElementTree = _AtomInstanceFromElementTree(Generator, 
    'generator', ATOM_NAMESPACE)


class Text(AtomBase):
  """A parent class for atom:title, summary, etc."""

  def __init__(self, text_type=None, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Text
    
    Args:
      text_type: string
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    
    self.type = text_type
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.type:
      element_tree.attrib['type'] = self.type
    AtomBase._TransferToElementTree(self, element_tree)
    return element_tree
  
  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'type':
      self.type = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      AtomBase._TakeAttributeFromElementTree(self, attribute, element_tree)

  def _TransferFromElementTree(self, element_tree):
    # Transfer all xml attributes
    while len(element_tree.attrib.keys()) > 0:
      current_key = element_tree.attrib.keys()[0]
      self._TakeAttributeFromElementTree(current_key, element_tree)
    AtomBase._TransferFromElementTree(self, element_tree)


class Title(Text):
  """The atom:title element"""

  def __init__(self, title_type=None, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Title
    
    Args:
      title_type: string
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.type = title_type
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    Text._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'title'
    return element_tree
 
  def _TransferFromElementTree(self, element_tree):
    Text._TransferFromElementTree(self, element_tree)

def TitleFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _TitleFromElementTree(element_tree)

_TitleFromElementTree = _AtomInstanceFromElementTree(Title, 'title', 
    ATOM_NAMESPACE)

class Subtitle(Text):
  """The atom:subtitle element"""

  def __init__(self, subtitle_type=None, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Subtitle
    
    Args:
      subtitle_type: string
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.type = subtitle_type
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    Text._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'subtitle'
    return element_tree

  def _TransferFromElementTree(self, element_tree):
    Text._TransferFromElementTree(self, element_tree)

def SubtitleFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _SubtitleFromElementTree(element_tree)

_SubtitleFromElementTree = _AtomInstanceFromElementTree(Subtitle, 'subtitle',
    ATOM_NAMESPACE)


class Rights(Text):
  """The atom:rights element"""

  def __init__(self, rights_type=None, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Rights
    
    Args:
      rights_type: string
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.type = rights_type
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    Text._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'rights'
    return element_tree

  def _TransferFromElementTree(self, element_tree):
    Text._TransferFromElementTree(self, element_tree)

def RightsFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _RightsFromElementTree(element_tree)

_RightsFromElementTree = _AtomInstanceFromElementTree(Rights, 'rights', 
    ATOM_NAMESPACE)


class Summary(Text):
  """The atom:summary element"""

  def __init__(self, summary_type=None, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Summary
    
    Args:
      summary_type: string
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.type = summary_type
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    Text._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'summary'
    return element_tree

  def _TransferFromElementTree(self, element_tree):
    Text._TransferFromElementTree(self, element_tree)

def SummaryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _SummaryFromElementTree(element_tree)

_SummaryFromElementTree = _AtomInstanceFromElementTree(Summary, 'summary', ATOM_NAMESPACE)


class Content(Text):
  """The atom:content element"""

  def __init__(self, content_type=None, src=None, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Content
    
    Args:
      content_type: string
      src: string
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    
    self.type = content_type
    self.src = None
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.src:
      element_tree.attrib['src'] = self.src
    Text._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'content'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'src':
      self.src = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      Text._TakeAttributeFromElementTree(self, attribute, element_tree)

  def _TransferFromElementTree(self, element_tree):
    # Transfer all xml attributes
    while len(element_tree.attrib.keys()) > 0:
      current_key = element_tree.attrib.keys()[0]
      self._TakeAttributeFromElementTree(current_key, element_tree)
    Text._TransferFromElementTree(self, element_tree)

def ContentFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _ContentFromElementTree(element_tree)

_ContentFromElementTree = _AtomInstanceFromElementTree(Content, 'content', ATOM_NAMESPACE)


class Category(AtomBase):
  """The atom:category element"""

  def __init__(self, term=None, scheme=None, label=None, text=None, 
      extension_elements=None, extension_attributes=None):
    """Constructor for Category
    
    Args:
      term: str
      scheme: str
      label: str
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    
    self.term = term
    self.scheme = scheme
    self.label = label
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.term:
      element_tree.attrib['term'] = self.term
    if self.scheme:
      element_tree.attrib['scheme'] = self.scheme
    if self.label:
      element_tree.attrib['label'] = self.label
    AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'category'
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'term':
      self.term = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'scheme':
      self.scheme = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    elif attribute == 'label':
      self.label = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      AtomBase._TakeAttributeFromElementTree(self, attribute, element_tree)

  def _TransferFromElementTree(self, element_tree):
    # find all attributes
    while len(element_tree.attrib.keys()) > 0:
      current_key = element_tree.attrib.keys()[0]
      self._TakeAttributeFromElementTree(current_key, element_tree)
    AtomBase._TransferFromElementTree(self, element_tree)

def CategoryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _CategoryFromElementTree(element_tree)

_CategoryFromElementTree = _AtomInstanceFromElementTree(Category, 'category', ATOM_NAMESPACE)


class Id(AtomBase):
  """The atom:id element."""

  def __init__(self, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Id
    
    Args:
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'id'
    return element_tree

def IdFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _IdFromElementTree(element_tree)

_IdFromElementTree = _AtomInstanceFromElementTree(Id, 'id', ATOM_NAMESPACE)


class Icon(AtomBase):
  """The atom:icon element."""

  def __init__(self, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Icon
    
    Args:
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'icon'
    return element_tree

def IconFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _IconFromElementTree(element_tree)

_IconFromElementTree = _AtomInstanceFromElementTree(Icon, 'icon', 
    ATOM_NAMESPACE)


class Logo(AtomBase):
  """The atom:logo element."""

  def __init__(self, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Logo
    
    Args:
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """
    
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    AtomBase._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'logo'
    return element_tree

def LogoFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _LogoFromElementTree(element_tree)

_LogoFromElementTree = _AtomInstanceFromElementTree(Logo, 'logo', 
    ATOM_NAMESPACE)


class Date(AtomBase):
  """A parent class for atom:updated, published, etc."""

  #TODO Add text to and from time conversion methods to allow users to set
  # the contents of a Date to a python DateTime object.

  def __init__(self, text=None, extension_elements=None,
      extension_attributes=None):
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


class Updated(Date):
  """The atom:updated element."""

  def __init__(self, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Updated
    
    Args:
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    Date._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'updated'
    return element_tree

  def _TransferFromElementTree(self, element_tree):
    Date._TransferFromElementTree(self, element_tree)

def UpdatedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _UpdatedFromElementTree(element_tree)

_UpdatedFromElementTree = _AtomInstanceFromElementTree(Updated, 'updated', 
    ATOM_NAMESPACE)


class Published(Date):
  """The atom:published element."""

  def __init__(self, text=None, extension_elements=None,
      extension_attributes=None):
    """Constructor for Published
    
    Args:
      text: str The text data in the this element
      extension_elements: list A  list of ExtensionElement instances
      extension_attributes: dict A dictionary of attribute value string pairs
    """

    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    Date._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'published'
    return element_tree

  def _TransferFromElementTree(self, element_tree):
    Date._TransferFromElementTree(self, element_tree)

def PublishedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _PublishedFromElementTree(element_tree)

_PublishedFromElementTree = _AtomInstanceFromElementTree(Published, 
    'published', ATOM_NAMESPACE)

 
class FeedEntryParent(AtomBase):
  """A super class for atom:feed and entry, contains shared attributes"""

  def __init__(self, author=None, category=None, contributor=None, 
      atom_id=None, link=None, rights=None, title=None, updated=None, text=None, 
      extension_elements=None, extension_attributes=None):
    self.author = author or []
    self.category = category or []
    self.contributor = contributor or []
    self.id = atom_id
    self.link = link or []
    self.rights = rights
    self.title = title
    self.updated = updated
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    for an_author in self.author:
      element_tree.append(an_author._ToElementTree())
    for a_category in self.category:
      element_tree.append(a_category._ToElementTree())
    for a_contributor in self.contributor:
      element_tree.append(a_contributor._ToElementTree())
    if self.id:
      element_tree.append(self.id._ToElementTree())
    for a_link in self.link:
      element_tree.append(a_link._ToElementTree())
    if self.rights:
      element_tree.append(self.rights._ToElementTree())
    if self.title:
      element_tree.append(self.title._ToElementTree())
    if self.updated:
      element_tree.append(self.updated._ToElementTree())
    AtomBase._TransferToElementTree(self, element_tree)
    return element_tree
 
  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'author'):
      self.author.append(_AuthorFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'category'):
      self.category.append(_CategoryFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'contributor'):
      self.contributor.append(_ContributorFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'id'):
      self.id = _IdFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'link'):
      self.link.append(_LinkFromElementTree(child))
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'rights'):
      self.rights = _RightsFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'title'):
      self.title = _TitleFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'updated'):
      self.updated = _UpdatedFromElementTree(child)
      element_tree.remove(child)
    else:
      AtomBase._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    AtomBase._TransferFromElementTree(self, element_tree)
  

class Entry(FeedEntryParent):
  """The atom:entry element"""

  def __init__(self, author=None, category=None, content=None, 
      contributor=None, atom_id=None, link=None, published=None, rights=None,
      source=None, summary=None, title=None, updated=None, text=None,
      extension_elements=None, extension_attributes=None):
    """Constructor for atom:entry
    
    Args:
      author: list A list of Author instances which belong to this class.
      category: list A list of Category instances
      content: Content The entry's Content
      contributor: list A list on Contributor instances
      id: Id The entry's Id element
      link: list A list of Link instances
      published: Published The entry's Published element
      rights: Rights The entry's Rights element
      source: Source the entry's source element
      summary: Summary the entry's summary element
      title: Title the entry's title element
      updated: Updated the entry's updated element
      text: String The text contents of the element. This is the contents
          of the Entry's XML text node. (Example: <foo>This is the text</foo>)
      extension_elements: list A list of ExtensionElement instances which are
          children of this element.
      extension_attributes: dict A dictionary of strings which are the values
          for additional XML attributes of this element.
    """

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
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.content:
      element_tree.append(self.content._ToElementTree())
    if self.published:
      element_tree.append(self.published._ToElementTree())
    if self.source:
      element_tree.append(self.source._ToElementTree())
    if self.summary:
      element_tree.append(self.summary._ToElementTree())
    FeedEntryParent._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'entry'
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'content'):
      self.content = _ContentFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'published'):
      self.published = _PublishedFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'source'):
      self.source = _SourceFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'summary'):
      self.summary = _SummaryFromElementTree(child)
      element_tree.remove(child)
    else:
      FeedEntryParent._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    FeedEntryParent._TransferFromElementTree(self, element_tree)

def EntryFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _EntryFromElementTree(element_tree)

_EntryFromElementTree = _AtomInstanceFromElementTree(Entry, 'entry', 
    ATOM_NAMESPACE)


class Source(FeedEntryParent):
  """The atom:source element"""

  def __init__(self, author=None, category=None, contributor=None,
      generator=None, icon=None, atom_id=None, link=None, logo=None, rights=None, subtitle=None, title=None, updated=None, text=None,
      extension_elements=None, extension_attributes=None):
    """Constructor for Source
    
    Args:
      author: list (optional) A list of Author instances which belong to this 
          class.
      category: list (optional) A list of Category instances
      contributor: list (optional) A list on Contributor instances
      generator: Generator (optional) 
      icon: Icon (optional) 
      id: Id (optional) The entry's Id element
      link: list (optional) A list of Link instances
      logo: Logo (optional) 
      rights: Rights (optional) The entry's Rights element
      subtitle: Subtitle (optional) The entry's subtitle element
      title: Title (optional) the entry's title element
      updated: Updated (optional) the entry's updated element
      text: String (optional) The text contents of the element. This is the 
          contents of the Entry's XML text node. 
          (Example: <foo>This is the text</foo>)
      extension_elements: list (optional) A list of ExtensionElement instances
          which are children of this element.
      extension_attributes: dict (optional) A dictionary of strings which are 
          the values for additional XML attributes of this element.
    """

    self.author = author or []
    self.category = category or []
    self.contributor = contributor or []
    self.generator = generator
    self.icon = icon
    self.id = atom_id
    self.link = link or []
    self.logo = logo
    self.rights = rights
    self.subtitle = subtitle
    self.title = title
    self.updated = updated
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.generator:
      element_tree.append(self.generator._ToElementTree())
    if self.icon:
      element_tree.append(self.icon._ToElementTree())
    if self.logo:
      element_tree.append(self.logo._ToElementTree())
    if self.subtitle:
      element_tree.append(self.subtitle._ToElementTree())
    FeedEntryParent._TransferToElementTree(self, element_tree)
    element_tree.tag = ELEMENT_TEMPLATE % 'source'
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'generator'):
      self.generator = _GeneratorFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'icon'):
      self.icon = _IconFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'logo'):
      self.logo = _LogoFromElementTree(child)
      element_tree.remove(child)
    elif child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'subtitle'):
      self.subtitle = _SubtitleFromElementTree(child)
      element_tree.remove(child)
    else:
      FeedEntryParent._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    FeedEntryParent._TransferFromElementTree(self, element_tree)

def SourceFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _SourceFromElementTree(element_tree)

_SourceFromElementTree = _AtomInstanceFromElementTree(Source, 'source', 
    ATOM_NAMESPACE)


class Feed(Source):
  """The atom:feed element"""

  def __init__(self, author=None, category=None, contributor=None,
      generator=None, icon=None, atom_id=None, link=None, logo=None, rights=None, subtitle=None, title=None, updated=None, entry=None, text=None,
      extension_elements=None, extension_attributes=None):
    """Constructor for Source
    
    Args:
      author: list (optional) A list of Author instances which belong to this
          class.
      category: list (optional) A list of Category instances
      contributor: list (optional) A list on Contributor instances
      generator: Generator (optional) 
      icon: Icon (optional) 
      id: Id (optional) The entry's Id element
      link: list (optional) A list of Link instances
      logo: Logo (optional) 
      rights: Rights (optional) The entry's Rights element
      subtitle: Subtitle (optional) The entry's subtitle element
      title: Title (optional) the entry's title element
      updated: Updated (optional) the entry's updated element
      entry: list (optional) A list of the Entry instances contained in the 
          feed.
      text: String (optional) The text contents of the element. This is the 
          contents of the Entry's XML text node. 
          (Example: <foo>This is the text</foo>)
      extension_elements: list (optional) A list of ExtensionElement instances
          which are children of this element.
      extension_attributes: dict (optional) A dictionary of strings which are 
          the values for additional XML attributes of this element.
    """

    self.author = author or []
    self.category = category or []
    self.contributor = contributor or []
    self.generator = generator
    self.icon = icon
    self.id = atom_id
    self.link = link or []
    self.logo = logo
    self.rights = rights
    self.subtitle = subtitle
    self.title = title
    self.updated = updated
    self.entry = entry or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    for an_entry in self.entry:
      element_tree.append(an_entry._ToElementTree())
    Source._TransferToElementTree(self, element_tree)
    # set the element_tree tag at the end of this method
    # because Source.TransferToElementTree sets the tag
    # to atom:source
    element_tree.tag = ELEMENT_TEMPLATE % 'feed'
    return element_tree

  def _TakeChildFromElementTree(self, child, element_tree):
    if child.tag == '{%s}%s' % (ATOM_NAMESPACE, 'entry'):
      self.entry.append(_EntryFromElementTree(child))
      element_tree.remove(child)
    else:
      Source._TakeChildFromElementTree(self, child, element_tree)

  def _TransferFromElementTree(self, element_tree):
    while len(element_tree) > 0:
      self._TakeChildFromElementTree(element_tree[0], element_tree)
    Source._TransferFromElementTree(self, element_tree)

def FeedFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _FeedFromElementTree(element_tree)

_FeedFromElementTree = _AtomInstanceFromElementTree(Feed, 'feed', ATOM_NAMESPACE)
  
  
class ExtensionElement(object):
  """Represents extra XML elements contained in Atom classes."""
  
  def __init__(self, tag, namespace=None, attributes=None, 
      children=None, text=None):
    """Constructor for EtensionElement

    Args:
      namespace: string (optional) The XML namespace for this element.
      tag: string (optional) The tag (without the namespace qualifier) for
          this element. To reconstruct the full qualified name of the element,
          combine this tag with the namespace.
      attributes: dict (optinal) The attribute value string pairs for the XML 
          attributes of this element.
      children: list (optional) A list of ExtensionElements which represent 
          the XML child nodes of this element.
    """

    self.namespace = namespace
    self.tag = tag
    self.attributes = attributes or {}
    self.children = children or []
    self.text = text
    
  def ToString(self):
    element_tree = self._TransferToElementTree(ElementTree.Element(''))
    return ElementTree.tostring(element_tree)
    
  def _TransferToElementTree(self, element_tree):
    if self.tag is None:
      return None
      
    if self.namespace is not None:
      element_tree.tag = '{%s}%s' % (self.namespace, self.tag)
    else:
      element_tree.tag = self.tag
      
    for key, value in self.attributes.iteritems():
      element_tree.attrib[key] = value
      
    for child in self.children:
      element_tree.append(child._TransferToElementTree(
          ElementTree.Element('')))
      
    element_tree.text = self.text
      
    return element_tree
    
def ExtensionElementFromString(xml_string):
  element_tree = ElementTree.fromstring(xml_string)
  return _ExtensionElementFromElementTree(element_tree)

def _ExtensionElementFromElementTree(element_tree):
  element_tag = element_tree.tag
  if '}' in element_tag:
    namespace = element_tag[1:element_tag.index('}')]
    tag = element_tag[element_tag.index('}')+1:]
  else: 
    namespace = None
    tag = element_tag
  extension = ExtensionElement(namespace=namespace, tag=tag)
  for key, value in element_tree.attrib.iteritems():
    extension.attributes[key] = value
  for child in element_tree:
    extension.children.append(_ExtensionElementFromElementTree(child))
  extension.text = element_tree.text
  return extension
