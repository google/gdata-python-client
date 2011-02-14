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
from atom.data import Title
from gdata.contentforshopping.client import ContentForShoppingClient
from gdata.contentforshopping.data import ClientAccount, AdultContent

# Gather merchant information
account_id = raw_input('Merchant Account ID? ').strip()
email = raw_input('Google Email Address? ').strip()

# Create a client
client = ContentForShoppingClient(account_id)

# Perform programmatic login
client.client_login(email, getpass.getpass('Google Password? '),
    'Shopping API for Content sample', 'structuredcontent')

# Create 10 accounts
for i in range(10):
  client_account = ClientAccount()
  client_account.title = Title('Test Account %s' % (i + 1))
  client_account.adult_content = AdultContent('no')
  # Insert the client account
  client.insert_client_account(client_account)
  # Display something to the user
  print i + 1, '/', 10
