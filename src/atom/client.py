#!/usr/bin/env python
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


"""AtomPubClient provides CRUD ops. in line with the Atom Publishing Protocol.

"""

__author__ = 'j.s@google.com (Jeff Scudder)'


import atom.http_core


class AtomPubClient(object):
  host = None
  auth_token = None

  def __init__(self, http_client=None, host=None, auth_token=None, **kwargs):
    self.http_client = http_client or atom.http_core.HttpClient()
    if host is not None:
      self.host = host
    if auth_token is not None:
      self.auth_token = auth_token

  def request(self, method=None, uri=None, auth_token=None,
              http_request=None, **kwargs):
    """Performs an HTTP request to the server indicated.

    Uses the http_client instance to make the request.

    Args:
      method: The HTTP method as a string, usually one of 'GET', 'POST',
              'PUT', or 'DELETE'
      uri: The URI desired as a string or atom.http_core.Uri. 
      http_request: 
      auth_token: An authorization token object whose modify_request method
                  sets the HTTP Authorization header.
    """
    if http_request is None:
      http_request = atom.http_core.HttpRequest()
    # If the http_request didn't specify the target host, use the client's
    # default host (if set).
    if self.host is not None and http_request.host is None:
      http_request.host = self.host
    # Modify the request based on the AtomPubClient settings and parameters
    # passed in to the request.
    if isinstance(uri, (str, unicode)):
      uri = atom.http_core.parse_uri(uri)
    if uri is not None:
      uri.modify_request(http_request)
    if isinstance(method, (str, unicode)):
      http_request.method = method
    # Any unrecognized arguments are assumed to be capable of modifying the
    # HTTP request.
    for name, value in kwargs.iteritems():
      if value is not None:
        value.modify_request(http_request)
    # Default to an http request if the protocol scheme is not set.
    if http_request.scheme is None:
      http_request.scheme = 'http'
    # Add the Authorization header at the very end. The Authorization header
    # value may need to be calculated using information in the request.
    if auth_token:
      auth_token.modify_request(http_request)
    elif self.auth_token:
      self.auth_token.modify_request(http_request)
    # Perform the fully specified request using the http_client instance. 
    # Sends the request to the server and returns the server's response.
    return self.http_client.request(http_request)

  Request = request

  def get(self, uri=None, auth_token=None, http_request=None, **kwargs):
    return self.request(method='GET', uri=uri, auth_token=auth_token, 
                        http_request=http_request, **kwargs)

  Get = get

  def post(self, uri=None, data=None, auth_token=None, http_request=None, 
           **kwargs):
    return self.request(method='POST', uri=uri, auth_token=auth_token, 
                        http_request=http_request, data=data, **kwargs)

  Post = post

  def put(self, uri=None, data=None, auth_token=None, http_request=None, 
          **kwargs):
    return self.request(method='PUT', uri=uri, auth_token=auth_token, 
                        http_request=http_request, data=data, **kwargs)

  Put = put

  def delete(self, uri=None, auth_token=None, http_request=None, **kwargs):
    return self.request(method='DELETE', uri=uri, auth_token=auth_token, 
                        http_request=http_request, **kwargs)

  Delete = delete
