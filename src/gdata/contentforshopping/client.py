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


"""Extend the gdata client for the Content PAI for Shopping.
"""


__author__ = 'afshar (Ali Afshar)'


import gdata.client

from gdata.contentforshopping.data import ProductEntry, ProductFeed


CFS_VERSION = 'v1'
CFS_HOST = 'content.googleapis.com'
CFS_URI = 'https://%s/content' % CFS_HOST
CFS_PROJECTION = 'generic'


class ContentForShoppingClient(gdata.client.GDClient):
  """Client for Content for Shopping API.

  :param account_id: Merchant account ID. This value will be used by default
                     for all requests, but may be overridden on a
                     request-by-request basis.
  :param api_version: The version of the API to target. Default value: 'v1'.
  :param **kwargs: Pass all addtional keywords to the GDClient constructor.
  """

  def __init__(self, account_id=None, api_version=CFS_VERSION, **kwargs):
    self.cfs_account_id = account_id
    self.cfs_api_version = api_version
    gdata.client.GDClient.__init__(self, **kwargs)

  def _create_uri(self, account_id, resource, path=()):
    """Create a request uri from the given arguments.

    If arguments are None, use the default client attributes.
    """
    account_id = account_id or self.cfs_account_id
    if account_id is None:
        raise ValueError('No Account ID set. '
                         'Either set for the client, or per request')
    return '/'.join([CFS_URI, self.cfs_api_version, account_id, resource,
                     CFS_PROJECTION] + list(path))

  def _create_product_id(self, id, country, language):
    return 'online:%s:%s:%s' % (language, country, id)

  def get_products(self, start_index=None, max_results=None, account_id=None,
                   auth_token=None):
    """Get a feed of products for the account.

    :param max_results: The maximum number of results to return (default 25,
                        maximum 250).
    :param start_index: The starting index of the feed to return (default 1,
                        maximum 10000)
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    """
    uri = self._create_uri(account_id, 'items/products')
    return self.get_feed(uri, auth_token=auth_token,
        desired_class=gdata.contentforshopping.data.ProductFeed)

  def get_product(self, id, country, language, account_id=None,
                  auth_token=None):
    """Get a product by id, country and language.
    """
    pid = self._create_product_id(id, country, language)
    uri = self._create_uri(account_id, 'items/products', [pid])
    return self.get_entry(uri, desired_class=ProductEntry,
                          auth_token=auth_token)

  def insert_product(self, product, account_id=None, auth_token=None):
    """Create a new product, by posting the product entry feed.

    :param product: A :class:`gdata.contentforshopping.data.ProductEntry` with
                    the required product data.
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    """
    uri = self._create_uri(account_id, 'items/products')
    return self.post(product, uri=uri, auth_token=auth_token)

  def update_product(self, product, account_id=None,
                     auth_token=None):
    """Update a product, by putting the product entry feed.

    :param product: A :class:`gdata.contentforshopping.data.ProductEntry` with
                    the required product data.
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    """
    pid = self._create_product_id(product.id.text, product.target_country.text,
                                  product.content_language.text)
    uri = self._create_uri(account_id, 'items/products', [pid])
    return self.update(product, uri=uri, auth_token=auth_token)
