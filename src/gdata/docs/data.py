#!/usr/bin/python
#
# Copyright 2009 Google Inc. All Rights Reserved.
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

"""Data model classes for parsing and generating XML for the DocList Data API"""

__author__ = 'vicfryzel@google.com (Vic Fryzel)'

import re
import atom.core
import atom.data
import gdata.acl.data
import gdata.data


DOCUMENTS_NS = 'http://schemas.google.com/docs/2007'
DOCUMENTS_TEMPLATE = '{http://schemas.google.com/docs/2007}%s'
ACL_FEEDLINK_REL = 'http://schemas.google.com/acl/2007#accessControlList'
REVISION_FEEDLINK_REL = DOCUMENTS_NS + '/revisions'
PARENT_LINK_REL = DOCUMENTS_NS + '#parent'
PUBLISH_LINK_REL = DOCUMENTS_NS + '#publish'
DATA_KIND_SCHEME = 'http://schemas.google.com/g/2005#kind'
DOCUMENT_LABEL = 'document'
SPREADSHEET_LABEL = 'spreadsheet'
DRAWING_LABEL = 'drawing'
PRESENTATION_LABEL = 'presentation'
FILE_LABEL = 'file'
PDF_LABEL = 'pdf'
FORM_LABEL = 'form'
COLLECTION_LABEL = 'folder'


def make_kind_category(label):
  """Builds the appropriate atom.data.Category for the label passed in.

  Args:
    label: str The value for the category entry.

  Returns:
    An atom.data.Category or None if label is None.
  """
  if label is None:
    return None

  return atom.data.Category(
    scheme=DATA_KIND_SCHEME, term='%s#%s' % (DOCUMENTS_NS, label), label=label)

MakeKindCategory = make_kind_category


class ResourceId(atom.core.XmlElement):
  """The DocList gd:resourceId element."""
  _qname = gdata.data.GDATA_TEMPLATE  % 'resourceId'


class LastModifiedBy(atom.data.Person):
  """The DocList gd:lastModifiedBy element."""
  _qname = gdata.data.GDATA_TEMPLATE  % 'lastModifiedBy'


class LastViewed(atom.data.Person):
  """The DocList gd:lastViewed element."""
  _qname = gdata.data.GDATA_TEMPLATE  % 'lastViewed'


class WritersCanInvite(atom.core.XmlElement):
  """The DocList docs:writersCanInvite element."""
  _qname = DOCUMENTS_TEMPLATE  % 'writersCanInvite'
  value = 'value'


class Deleted(atom.core.XmlElement):
  """The DocList gd:deleted element."""
  _qname = gdata.data.GDATA_TEMPLATE  % 'deleted'


class QuotaBytesUsed(atom.core.XmlElement):
  """The DocList gd:quotaBytesUsed element."""
  _qname = gdata.data.GDATA_TEMPLATE  % 'quotaBytesUsed'


class Publish(atom.core.XmlElement):
  """The DocList docs:publish element."""
  _qname = DOCUMENTS_TEMPLATE  % 'publish'
  value = 'value'


class PublishAuto(atom.core.XmlElement):
  """The DocList docs:publishAuto element."""
  _qname = DOCUMENTS_TEMPLATE  % 'publishAuto'
  value = 'value'


class PublishOutsideDomain(atom.core.XmlElement):
  """The DocList docs:publishOutsideDomain element."""
  _qname = DOCUMENTS_TEMPLATE  % 'publishOutsideDomain'
  value = 'value'


class Resource(gdata.data.GDEntry):
  """DocList version of an Atom Entry."""

  last_viewed = LastViewed
  last_modified_by = LastModifiedBy
  resource_id = ResourceId
  deleted = Deleted
  writers_can_invite = WritersCanInvite
  quota_bytes_used = QuotaBytesUsed
  feed_link = [gdata.data.FeedLink]

  def __init__(self, type=None, title=None, **kwargs):
    super(Resource, self).__init__(**kwargs)
    if isinstance(type, str):
      self.category.append(gdata.docs.data.make_kind_category(type))

    if title is not None:
      if isinstance(title, str):
        self.title = atom.data.Title(text=title)
      else:
        self.title = title

  def get_document_type(self):
    """Extracts the type of document this Resource is.

    This method returns the type of document the Resource represents. Possible
    values are document, presentation, drawing, spreadsheet, file, folder,
    form, or pdf.

    'folder' is a possible return value of this method because, for legacy
    support, we have not yet renamed the folder keyword to collection in
    the API itself.

    Returns:
      String representing the type of document.
    """
    if self.category:
      for category in self.category:
        if category.scheme == DATA_KIND_SCHEME:
          return category.label
    else:
      return None

  GetDocumentType = get_document_type

  def get_acl_feed_link(self):
    """Extracts the Resource's ACL feed <gd:feedLink>.

    Returns:
      A gdata.data.FeedLink object.
    """
    for feed_link in self.feed_link:
      if feed_link.rel == ACL_FEEDLINK_REL:
        return feed_link
    return None

  GetAclFeedLink = get_acl_feed_link

  def get_revisions_feed_link(self):
    """Extracts the Resource's revisions feed <gd:feedLink>.

    Returns:
      A gdata.data.FeedLink object.
    """
    for feed_link in self.feed_link:
      if feed_link.rel == REVISION_FEEDLINK_REL:
        return feed_link
    return None

  GetRevisionsFeedLink = get_revisions_feed_link

  def get_resumable_edit_media_link(self):
    """Extracts the Resource's resumable update link.

    Returns:
      A gdata.data.FeedLink object.
    """
    for feed_link in self.feed_link:
      if feed_link.rel == RESUMABLE_EDIT_MEDIA_LINK_REL:
        return feed_link
    return None

  GetRevisionsFeedLink = get_revisions_feed_link

  def in_collections(self):
    """Returns the parents link(s) (collections) of this entry."""
    links = []
    for link in self.link:
      if link.rel == PARENT_LINK_REL and link.href:
        links.append(link)
    return links

  InCollections = in_collections


class ResourceFeed(gdata.data.GDFeed):
  """Main feed containing a list of resources."""
  entry = [Resource]


class AclEntry(gdata.acl.data.AclEntry, gdata.data.BatchEntry):
  """Resource ACL entry."""
  @staticmethod
  def get_instance(role=None, scope_type=None, scope_value=None, key=False):
    entry = AclEntry()

    if role is not None:
      if key:
        new_role = role
        if isinstance(role, str):
          new_role = gdata.acl.data.AclRole(value=role)
        entry.with_key = gdata.acl.data.AclWithKey(key='1234', role=new_role)
      else:
        entry.role = role
        if isinstance(role, str):
          entry.role = gdata.acl.data.AclRole(value=role)

    if scope_type is not None and scope_value is not None:
      entry.scope = gdata.acl.data.AclScope(type=scope_type, value=scope_value)
    return entry

  GetInstance = get_instance


class AclFeed(gdata.acl.data.AclFeed):
  """Resource ACL feed."""
  entry = [AclEntry]


class Revision(gdata.data.GDEntry):
  """Resource Revision entry."""
  publish = Publish
  publish_auto = PublishAuto
  publish_outside_domain = PublishOutsideDomain

  def find_publish_link(self):
    """Get the link that points to the published resource on the web.

    Returns:
      A str for the URL in the link with a rel ending in #publish.
    """
    return self.find_url(PUBLISH_LINK_REL)

  FindPublishLink = find_publish_link

  def get_publish_link(self):
    """Get the link that points to the published resource on the web.

    Returns:
      A gdata.data.Link for the link with a rel ending in #publish.
    """
    return self.get_link(PUBLISH_LINK_REL)

  GetPublishLink = get_publish_link


class RevisionFeed(gdata.data.GDFeed):
  """A DocList Revision feed."""
  entry = [Revision]


class ArchiveResourceId(atom.core.XmlElement):
  """The DocList docs:removed element."""
  _qname = DOCUMENTS_TEMPLATE  % 'archiveResourceId'


class ArchiveFailure(atom.core.XmlElement):
  """The DocList docs:archiveFailure element."""
  _qname = DOCUMENTS_TEMPLATE  % 'archiveFailure'


class ArchiveComplete(atom.core.XmlElement):
  """The DocList docs:archiveComplete element."""
  _qname = DOCUMENTS_TEMPLATE  % 'archiveComplete'


class ArchiveTotal(atom.core.XmlElement):
  """The DocList docs:archiveTotal element."""
  _qname = DOCUMENTS_TEMPLATE  % 'archiveTotal'


class ArchiveTotalComplete(atom.core.XmlElement):
  """The DocList docs:archiveTotalComplete element."""
  _qname = DOCUMENTS_TEMPLATE  % 'archiveTotalComplete'


class ArchiveTotalFailure(atom.core.XmlElement):
  """The DocList docs:archiveTotalFailure element."""
  _qname = DOCUMENTS_TEMPLATE  % 'archiveTotalFailure'


class ArchiveConversion(atom.core.XmlElement):
  """The DocList docs:removed element."""
  _qname = DOCUMENTS_TEMPLATE  % 'archiveConversion'
  source = 'source'
  target = 'target'


class ArchiveNotify(atom.core.XmlElement):
  """The DocList docs:archiveNotify element."""
  _qname = DOCUMENTS_TEMPLATE  % 'archiveNotify'


class ArchiveStatus(atom.core.XmlElement):
  """The DocList docs:archiveStatus element."""
  _qname = DOCUMENTS_TEMPLATE  % 'archiveStatus'


class ArchiveNotifyStatus(atom.core.XmlElement):
  """The DocList docs:archiveNotifyStatus element."""
  _qname = DOCUMENTS_TEMPLATE  % 'archiveNotifyStatus'


class Archive(gdata.data.GDEntry):
  """Archive entry."""
  archive_resource_ids = [ArchiveResourceId]
  status = ArchiveStatus
  date_completed = ArchiveComplete
  num_resources = ArchiveTotal
  num_complete_resources = ArchiveTotalComplete
  num_failed_resources = ArchiveTotalFailure
  failed_resource_ids = [ArchiveFailure]
  notify_status = ArchiveNotifyStatus
  conversions = [ArchiveConversion]
  notification_email = ArchiveNotify
  size = QuotaBytesUsed


class Removed(atom.core.XmlElement):
  """The DocList docs:removed element."""
  _qname = DOCUMENTS_TEMPLATE  % 'removed'


class Changestamp(atom.core.XmlElement):
  """The DocList docs:changestamp element."""
  _qname = DOCUMENTS_TEMPLATE  % 'changestamp'
  value = 'value'


class Change(gdata.data.GDEntry):
  """Change feed entry."""
  resource_id = ResourceId
  changestamp = Changestamp
  removed = Removed

  
class ChangeFeed(gdata.data.GDFeed):
  """DocList Changes feed."""
  entry = [Change] 


class QuotaBytesTotal(atom.core.XmlElement):
  """The DocList gd:quotaBytesTotal element."""
  _qname = gdata.data.GDATA_TEMPLATE  % 'quotaBytesTotal'


class QuotaBytesUsedInTrash(atom.core.XmlElement):
  """The DocList docs:quotaBytesUsedInTrash element."""
  _qname = DOCUMENTS_TEMPLATE  % 'quotaBytesUsedInTrash'


class ImportFormat(atom.core.XmlElement):
  """The DocList docs:importFormat element."""
  _qname = DOCUMENTS_TEMPLATE  % 'importFormat'
  source = 'source'
  target = 'target'


class ExportFormat(atom.core.XmlElement):
  """The DocList docs:exportFormat element."""
  _qname = DOCUMENTS_TEMPLATE  % 'exportFormat'
  source = 'source'
  target = 'target'


class FeatureName(atom.core.XmlElement):
  """The DocList docs:featureName element."""
  _qname = DOCUMENTS_TEMPLATE  % 'featureName'


class FeatureRate(atom.core.XmlElement):
  """The DocList docs:featureRate element."""
  _qname = DOCUMENTS_TEMPLATE  % 'featureRate'


class Feature(atom.core.XmlElement):
  """The DocList docs:feature element."""
  _qname = DOCUMENTS_TEMPLATE  % 'feature'
  name = FeatureName
  rate = FeatureRate


class MaxUploadSize(atom.core.XmlElement):
  """The DocList docs:maxUploadSize element."""
  _qname = gdata.data.GDATA_TEMPLATE  % 'maxUploadSize'
  kind = 'kind'


class Metadata(gdata.data.GDEntry):
  """Metadata entry for a user."""
  quota_bytes_total = QuotaBytesTotal
  quota_bytes_used = QuotaBytesUsed
  quota_bytes_used_in_trash = QuotaBytesUsedInTrash
  import_formats = [ImportFormat]
  export_formats = [ExportFormat]
  features = [Feature]
  max_upload_sizes = [MaxUploadSize]
