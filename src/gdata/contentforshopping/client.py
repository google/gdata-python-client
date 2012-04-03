#!/usr/bin/python
#
# Copyright (C) 2010-2011 Google Inc.
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


"""Extend the gdata client for the Content API for Shopping.

TODO:

1. Proper MCA Support.
2. Add classes for datafeed functions instead of asking for raw XML.
"""


__author__ = 'afshar (Ali Afshar), dhermes (Daniel Hermes)'


import atom.data
import gdata.client
from gdata.contentforshopping.data import ClientAccount
from gdata.contentforshopping.data import ClientAccountFeed
from gdata.contentforshopping.data import DatafeedEntry
from gdata.contentforshopping.data import DatafeedFeed
from gdata.contentforshopping.data import ProductEntry
from gdata.contentforshopping.data import ProductFeed


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

  api_version = '1.0'

  def __init__(self, account_id=None, api_version=CFS_VERSION, **kwargs):
    self.cfs_account_id = account_id
    self.cfs_api_version = api_version
    gdata.client.GDClient.__init__(self, **kwargs)

  def _create_uri(self, account_id, resource, path=(), use_projection=True,
                  dry_run=False, warnings=False, max_results=None,
                  start_token=None, start_index=None,
                  performance_start=None, performance_end=None):
    """Create a request uri from the given arguments.

    If arguments are None, use the default client attributes.
    """
    account_id = account_id or self.cfs_account_id
    if account_id is None:
        raise ValueError('No Account ID set. '
                         'Either set for the client, or per request')
    segments = [CFS_URI, self.cfs_api_version, account_id, resource]
    if use_projection:
      segments.append(CFS_PROJECTION)
    segments.extend(path)
    result = '/'.join(segments)

    request_params = []
    if dry_run:
      request_params.append('dry-run')
    if warnings:
      request_params.append('warnings')
    if max_results is not None:
      request_params.append('max-results=%s' % max_results)
    if start_token is not None:
      request_params.append('start-token=%s' % start_token)
    if start_index is not None:
      request_params.append('start-index=%s' % start_index)
    if performance_start is not None:
      request_params.append('performance.start=%s' % performance_start)
    if performance_end is not None:
      request_params.append('performance.end=%s' % performance_end)
    request_params = '&'.join(request_params)

    if request_params:
      result = '%s?%s' % (result, request_params)

    return result

  def _create_product_id(self, id, country, language):
    return 'online:%s:%s:%s' % (language, country, id)

  def _create_batch_feed(self, entries, operation, feed=None):
    if feed is None:
      feed = ProductFeed()
    for entry in entries:
      entry.batch_operation = gdata.data.BatchOperation(type=operation)
      feed.entry.append(entry)
    return feed

  # Operations on a single product

  def get_product(self, id, country, language, account_id=None,
                  auth_token=None):
    """Get a product by id, country and language.

    :param id: The product ID
    :param country: The country (target_country)
    :param language: The language (content_language)
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    """
    pid = self._create_product_id(id, country, language)
    uri = self._create_uri(account_id, 'items/products', path=[pid])
    return self.get_entry(uri, desired_class=ProductEntry,
                          auth_token=auth_token)

  GetProduct = get_product

  def insert_product(self, product, account_id=None, auth_token=None,
                     dry_run=False, warnings=False):
    """Create a new product, by posting the product entry feed.

    :param product: A :class:`gdata.contentforshopping.data.ProductEntry` with
                    the required product data.
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
    :param warnings: Flag to include warnings in response. False by default.
    """
    uri = self._create_uri(account_id, 'items/products',
                           dry_run=dry_run, warnings=warnings)
    return self.post(product, uri=uri, auth_token=auth_token)

  InsertProduct = insert_product

  def update_product(self, product, account_id=None, auth_token=None,
                     dry_run=False, warnings=False):
    """Update a product, by putting the product entry feed.

    :param product: A :class:`gdata.contentforshopping.data.ProductEntry` with
                    the required product data.
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
                    :param warnings: Flag to include warnings in response. False
                    by default.
    """
    pid = self._create_product_id(product.product_id.text,
                                  product.target_country.text,
                                  product.content_language.text)
    uri = self._create_uri(account_id, 'items/products', path=[pid],
                           dry_run=dry_run, warnings=warnings)
    return self.update(product, uri=uri, auth_token=auth_token)

  UpdateProduct = update_product

  def delete_product(self, product, account_id=None, auth_token=None,
                     dry_run=False, warnings=False):
    """Delete a product

    :param product: A :class:`gdata.contentforshopping.data.ProductEntry` with
                    the required product data.
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
    :param warnings: Flag to include warnings in response. False by default.
    """
    pid = self._create_product_id(product.product_id.text,
                                  product.target_country.text,
                                  product.content_language.text)
    uri = self._create_uri(account_id, 'items/products', path=[pid],
                           dry_run=dry_run, warnings=warnings)
    return self.delete(uri, auth_token=auth_token)

  DeleteProduct = delete_product

  # Operations on multiple products

  def get_products(self, max_results=None, start_token=None, start_index=None,
                   performance_start=None, performance_end=None,
                   account_id=None, auth_token=None):
    """Get a feed of products for the account.

    :param max_results: The maximum number of results to return (default 25,
                        maximum 250).
    :param start_token: The start token of the feed provided by the API.
    :param start_index: The starting index of the feed to return (default 1,
                        maximum 10000)
    :param performance_start: The start date (inclusive) of click data returned.
                              Should be represented as YYYY-MM-DD; not appended
                              if left as None.
    :param performance_end: The end date (inclusive) of click data returned.
                            Should be represented as YYYY-MM-DD; not appended
                            if left as None.
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    """
    uri = self._create_uri(account_id, 'items/products',
                           max_results=max_results,
                           start_token=start_token,
                           start_index=start_index,
                           performance_start=performance_start,
                           performance_end=performance_end)
    return self.get_feed(uri, auth_token=auth_token,
        desired_class=gdata.contentforshopping.data.ProductFeed)

  GetProducts = get_products

  def batch(self, feed, account_id=None, auth_token=None,
            dry_run=False, warnings=False):
    """Send a batch request.

    :param feed: The feed of batch entries to send.
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
    :param warnings: Flag to include warnings in response. False by default.
    """
    uri = self._create_uri(account_id, 'items/products', path=['batch'],
                           dry_run=dry_run, warnings=warnings)
    return self.post(feed, uri=uri, auth_token=auth_token,
                     desired_class=ProductFeed)

  Batch = batch

  def insert_products(self, products, account_id=None, auth_token=None,
                      dry_run=False, warnings=False):
    """Insert the products using a batch request

    :param products: A list of product entries
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
    :param warnings: Flag to include warnings in response. False by default.
    """
    feed = self._create_batch_feed(products, 'insert')
    return self.batch(feed, account_id=account_id, auth_token=auth_token,
                      dry_run=dry_run, warnings=warnings)

  InsertProducts = insert_products

  def update_products(self, products, account_id=None, auth_token=None,
                      dry_run=False, warnings=False):
    """Update the products using a batch request

    :param products: A list of product entries
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
    :param warnings: Flag to include warnings in response. False by default.

    .. note:: Entries must have the atom:id element set.
    """
    feed = self._create_batch_feed(products, 'update')
    return self.batch(feed, account_id=account_id, auth_token=auth_token,
                      dry_run=dry_run, warnings=warnings)

  UpdateProducts = update_products

  def delete_products(self, products, account_id=None, auth_token=None,
                      dry_run=False, warnings=False):
    """Delete the products using a batch request.

    :param products: A list of product entries
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
    :param warnings: Flag to include warnings in response. False by default.

    .. note:: Entries must have the atom:id element set.
    """
    feed = self._create_batch_feed(products, 'delete')
    return self.batch(feed, account_id=account_id, auth_token=auth_token,
                      dry_run=dry_run, warnings=warnings)

  DeleteProducts = delete_products

  # Operations on datafeeds

  def get_datafeeds(self, account_id=None):
    """Get the feed of datafeeds.

    :param account_id: The Sub-Account ID. If ommitted the default
                       Account ID will be used for this client.
    """
    uri = self._create_uri(account_id, 'datafeeds/products',
                           use_projection=False)
    return self.get_feed(uri, desired_class=DatafeedFeed)

  GetDatafeeds = get_datafeeds

  # Operations on a single datafeed

  def get_datafeed(self, feed_id, account_id=None, auth_token=None):
    """Get the feed of a single datafeed.

    :param feed_id: The ID of the desired datafeed.
    :param account_id: The Sub-Account ID. If ommitted the default
                       Account ID will be used for this client.
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    """
    uri = self._create_uri(account_id, 'datafeeds/products', path=[feed_id],
                           use_projection=False)
    return self.get_feed(uri, auth_token=auth_token,
                         desired_class=DatafeedEntry)

  GetDatafeed = get_datafeed

  def insert_datafeed(self, entry, account_id=None, auth_token=None,
                      dry_run=False, warnings=False):
    """Insert a datafeed.

    :param entry: XML Content of post request required for registering a
                  datafeed.
    :param account_id: The Sub-Account ID. If ommitted the default
                       Account ID will be used for this client.
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
    :param warnings: Flag to include warnings in response. False by default.
    """
    uri = self._create_uri(account_id, 'datafeeds/products',
                           use_projection=False, dry_run=dry_run,
                           warnings=warnings)
    return self.post(entry, uri=uri, auth_token=auth_token)

  InsertDatafeed = insert_datafeed

  def update_datafeed(self, entry, feed_id, account_id=None, auth_token=None,
                      dry_run=False, warnings=False):
    """Update the feed of a single datafeed.

    :param entry: XML Content of put request required for updating a
                  datafeed.
    :param feed_id: The ID of the desired datafeed.
    :param account_id: The Sub-Account ID. If ommitted the default
                       Account ID will be used for this client.
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
    :param warnings: Flag to include warnings in response. False by default.
    """
    uri = self._create_uri(account_id, 'datafeeds/products', path=[feed_id],
                           use_projection=False, dry_run=dry_run,
                           warnings=warnings)
    return self.update(entry, auth_token=auth_token, uri=uri)

  UpdateDatafeed = update_datafeed

  def delete_datafeed(self, feed_id, account_id=None, auth_token=None):
    """Delete a single datafeed.

    :param feed_id: The ID of the desired datafeed.
    :param account_id: The Sub-Account ID. If ommitted the default
                       Account ID will be used for this client.
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    """
    uri = self._create_uri(account_id, 'datafeeds/products', path=[feed_id],
                           use_projection=False)
    return self.delete(uri, auth_token=auth_token)

  DeleteDatafeed = delete_datafeed

  # Operations on client accounts

  def get_client_accounts(self, account_id=None, auth_token=None):
    """Get the feed of managed accounts

    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    """
    uri = self._create_uri(account_id, 'managedaccounts/products',
                           use_projection=False)
    return self.get_feed(uri, desired_class=ClientAccountFeed,
                         auth_token=auth_token)

  GetClientAccounts = get_client_accounts

  def insert_client_account(self, entry, account_id=None, auth_token=None,
                            dry_run=False, warnings=False):
    """Insert a client account entry

    :param entry: An entry of type ClientAccount
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
    :param warnings: Flag to include warnings in response. False by default.
    """
    uri = self._create_uri(account_id, 'managedaccounts/products',
                           use_projection=False, dry_run=dry_run,
                           warnings=warnings)
    return self.post(entry, uri=uri, auth_token=auth_token)

  InsertClientAccount = insert_client_account

  def update_client_account(self, entry, client_account_id, account_id=None,
                            auth_token=None, dry_run=False, warnings=False):
    """Update a client account

    :param entry: An entry of type ClientAccount to update to
    :param client_account_id: The client account ID
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
    :param warnings: Flag to include warnings in response. False by default.
    """
    uri = self._create_uri(account_id, 'managedaccounts/products',
                           path=[client_account_id], use_projection=False,
                           dry_run=dry_run, warnings=warnings)
    return self.update(entry, uri=uri, auth_token=auth_token)

  UpdateClientAccount = update_client_account

  def delete_client_account(self, client_account_id, account_id=None,
                            auth_token=None, dry_run=False, warnings=False):
    """Delete a client account

    :param client_account_id: The client account ID
    :param account_id: The Merchant Center Account ID. If ommitted the default
                       Account ID will be used for this client
    :param auth_token: An object which sets the Authorization HTTP header in its
                       modify_request method.
    :param dry_run: Flag to run all requests that modify persistent data in
                    dry-run mode. False by default.
    :param warnings: Flag to include warnings in response. False by default.
    """

    uri = self._create_uri(account_id, 'managedaccounts/products',
                           path=[client_account_id], use_projection=False,
                           dry_run=dry_run, warnings=warnings)
    return self.delete(uri, auth_token=auth_token)

  DeleteClientAccount = delete_client_account
