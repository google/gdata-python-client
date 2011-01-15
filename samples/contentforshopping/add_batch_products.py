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

products = []

for color in ['red', 'green', 'white', 'black', 'purple', 'brown', 'yellow',
              'orange', 'magenta']:
  # Generate a product entry
  product_entry = build_entry(
    product_id='ipod%s' % color,
    target_country = 'US',
    content_language = 'EN',
    title='iPod Nano 8GB, %s' % color,
    content='A nice small mp3 player, in %s' % color,
    price='149',
    price_unit='USD',
    shipping_price = '5',
    shipping_price_unit = 'USD',
    tax_rate='17.5',
    condition = 'new',
    link = 'http://pseudoscience.co.uk/google4e823e35f032f011.html',
    color = color,
  )
  products.append(product_entry)

# Post it to the service
client.insert_products(products)
