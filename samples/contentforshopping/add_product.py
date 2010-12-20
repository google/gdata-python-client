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


from gdata.contentforshopping.data import build_entry
from gdata.contentforshopping.client import ContentForShoppingClient


# Gather merchant information
account_id = raw_input('Merchant Account ID? ').strip()
email = raw_input('Google Email Address? ').strip()

# Create a client
client = ContentForShoppingClient(account_id)

# Perform programmatic login
client.client_login(email, getpass.getpass('Google Password? '),
    'Shopping API for Content sample', 'structuredcontent')

# Generate a product entry
product_entry = build_entry(
  id='ipod2',
  title='iPod Nano 8GB',
  content='A nice small mp3 player',
  price='149',
  price_unit='USD',
  shipping_price = '5',
  shipping_price_unit = 'USD',
  tax_rate='17.5',
  target_country = 'US',
  content_language = 'EN',
  condition = 'new',
  link = 'http://pseudoscience.co.uk/google4e823e35f032f011.html',
  brand = u'Apple',
  sizes = [u'Standard'],
  features = [u'Mp3', u'Multitouch', u'Color screen', '8GB Storage'],
  color = 'Green',
  featured_product = 'true',
  product_type = u'Electronics > Audio > Audio Players & Recorders > MP3 Players',
)

# Post it to the service
client.insert_product(product_entry)
