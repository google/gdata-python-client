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

# Note:
# This sample demonstrates 2 Legged OAuth using v2 of the Google Data APIs.
# See 2_legged_oauth.py for an example of using 2LO with v1.0 of the APIs.

__author__ = 'e.bidelman (Eric Bidelman)'

import gdata.gauth
import gdata.contacts.client
import gdata.docs.client

SOURCE_APP_NAME = 'google-PyClient2LOSample-v2.0'

CONSUMER_KEY = 'yourdomain.com'
CONSUMER_SECRET = 'YOUR_CONSUMER_KEY'

def PrintContacts(client):
  print '\nListing contacts for %s...' % client.auth_token.requestor_id
  feed = client.GetContacts()
  for entry in feed.entry:
    print entry.title.text


# Contacts Data API Example ====================================================
requestor_id = 'any.user@' + CONSUMER_KEY
two_legged_oauth_token = gdata.gauth.TwoLeggedOAuthHmacToken(
    CONSUMER_KEY, CONSUMER_SECRET, requestor_id)

contacts_client = gdata.contacts.client.ContactsClient(source=SOURCE_APP_NAME)
contacts_client.auth_token = two_legged_oauth_token

# GET - fetch user's contact list
PrintContacts(contacts_client)

# GET - fetch another user's contact list
contacts_client.auth_token.requestor_id = 'different.user' + CONSUMER_KEY
PrintContacts(contacts_client)


# Documents List Data API Example ==============================================
docs_client = gdata.docs.client.DocsClient(source=SOURCE_APP_NAME)
docs_client.auth_token = two_legged_oauth_token
docs_client.ssl = True

# POST - upload a document
print "\nUploading doc to %s's account..." % docs_client.auth_token.requestor_id
entry = docs_client.Upload('test.txt', 'MyDocTitle', content_type='text/plain')
print 'Document now accessible online at:', entry.GetAlternateLink().href

# GET - fetch the user's document list
print '\nListing Google Docs for %s...' % docs_client.auth_token.requestor_id
feed = docs_client.GetDocList()
for entry in feed.entry:
  print entry.title.text
