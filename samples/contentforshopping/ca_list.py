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

import getpass

from gdata.contentforshopping.client import ContentForShoppingClient

# Gather merchant information
account_id = raw_input('Merchant Account ID? ').strip()
email = raw_input('Google Email Address? ').strip()

# Create a client
client = ContentForShoppingClient(account_id)

# Perform programmatic login
client.client_login(email, getpass.getpass('Google Password? '),
    'Shopping API for Content sample', 'structuredcontent')

# Get the feed of client accounts
client_account_feed = client.get_client_accounts()

# Display the title and self link for each client account
for client_account in client_account_feed.entry:
  print client_account.title.text, client_account.GetSelfLink().href
