#!/usr/bin/env python
#
# Copyright 2011 Google Inc. All Rights Reserved.
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

"""Unshare domain users contact information when contact sharing is enabled."""

__author__ = 'alainv@google.com (Alain Vongsouvanh)'


import sys

import gdata.contacts.client
import gdata.contacts.data
import gdata.gauth


class BatchResult(object):
  """Hold batch processing results.

  Attributes:
    success_count: Number of successful operations.
    error_count: Number of failed operations.
    error_entries: List of failed entries.
  """
  success_count = 0
  error_count = 0
  error_entries = []


class ProfilesManager(object):
  """ProfilesManager object used to unshare domain users contact information.

  Basic usage is:
    >>> manager = ProfilesManager(CONSUMER_KEY, CONSUMER_SECRET, ADMIN_EMAIL)
    >>> result = manager.UnshareProfiles()
    >>> print 'Success: %s - Error: %s' % (result.success, result.error_count)

  Attributes:
    profiles: List of ProfilesEntry.
    batch_size: Number of operations per batch request (default to 100).
  """

  def __init__(self, consumer_key, consumer_secret, admin_email):
    domain = admin_email[admin_email.index('@') + 1:]
    self._gd_client = gdata.contacts.client.ContactsClient(
        source='GoogleInc-UnshareProfiles-1', domain=domain)
    self._gd_client.auth_token = gdata.gauth.TwoLeggedOAuthHmacToken(
        consumer_key, consumer_secret, admin_email)
    self._profiles = None
    self.batch_size = 100

  @property
  def profiles(self):
    """Get the list of profiles for the domain.

    Returns:
      List of ProfilesEntry.
    """
    if not self._profiles:
      self.GetAllProfiles()
    return self._profiles

  def GetAllProfiles(self):
    """Retrieve the list of user profiles for the domain."""
    profiles = []
    feed_uri = self._gd_client.GetFeedUri('profiles')
    while feed_uri:
      feed = self._gd_client.GetProfilesFeed(uri=feed_uri)
      profiles.extend(feed.entry)
      feed_uri = feed.FindNextLink()
    self._profiles = profiles

  def UnshareProfiles(self):
    """Unshare users' contact information.

    Uses batch request to optimize the resources.

    Returns:
      BatchResult object.
    """
    if not self._profiles:
      self.GetAllProfiles()
    batch_size = max(self.batch_size, 100)
    index = 0
    result = BatchResult()
    while index < len(self._profiles):
      request_feed = gdata.contacts.data.ProfilesFeed()
      for entry in self._profiles[index:index + batch_size]:
        entry.status = gdata.contacts.data.Status(indexed='false')
        request_feed.AddUpdate(entry=entry)
      result_feed = self._gd_client.ExecuteBatchProfiles(request_feed)
      for entry in result_feed.entry:
        if entry.batch_status.code == '200':
          self._profiles[index] = entry
          result.success_count += 1
        else:
          result.error_entries.append(entry)
          result.error_count += 1
        index += 1
    return result


def main():
  """Demonstrates the use of the Profiles API to unshare profiles."""
  if len(sys.argv) > 3:
    consumer_key = sys.argv[1]
    consumer_secret = sys.argv[2]
    admin_email = sys.argv[3]
  else:
    print ('python unshare_profiles.py [consumer_key] [consumer_secret]'
           ' [admin_email]')
    sys.exit(2)

  manager = ProfilesManager(consumer_key, consumer_secret, admin_email)
  result = manager.UnshareProfiles()
  print 'Success: %s - Error: %s' % (result.success_count, result.error_count)
  for entry in result.error_entries:
    print ' > Failed to update %s: (%s) %s' % (
        entry.id.text, entry.batch_status.code, entry.batch_status.reason)
  sys.exit(result.error_count)


if __name__ == '__main__':
  main()
