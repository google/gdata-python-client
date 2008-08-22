#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
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

"""This module provides a common interface for all HTTP requests.

  HttpResponse: Represents the server's response to an HTTP request. Provides
      an interface identical to httplib.HTTPResponse which is the response
      expected from higher level classes which use HttpClient.request.
"""


__author__ = 'api.jscudder (Jeff Scudder)'


import StringIO


class Error(Exception):
  pass


class UnparsableUrlObject(Error):
  pass


class ContentLengthRequired(Error):
  pass
  

class HttpResponse(object):
  def __init__(self, body=None, status=None, reason=None, headers=None):
    """Constructor for an HttpResponse object. 

    HttpResponse represents the server's response to an HTTP request from
    the client. The HttpClient.request method returns a httplib.HTTPResponse
    object and this HttpResponse class is designed to mirror the interface
    exposed by httplib.HTTPResponse.

    Args:
      body: A file like object, with a read() method. The body could also
          be a string, and the constructor will wrap it so that 
          HttpResponse.read(self) will return the full string.
      status: The HTTP status code as an int. Example: 200, 201, 404.
      reason: The HTTP status message which follows the code. Example: 
          OK, Created, Not Found
      headers: A dictionary containing the HTTP headers in the server's 
          response. A common header in the response is Content-Length.
    """
    if body:
      if hasattr(body, 'read'):
        self._body = body
      else:
        self._body = StringIO.StringIO(body)
    else:
      self._body = None
    if status is not None:
      self.status = int(status)
    else:
      self.status = None
    self.reason = reason
    self._headers = headers or {}

  def getheader(self, name, default=None):
    if name in self._headers:
      return self._headers[name]
    else:
      return default
    
  def read(self, amt=None):
    if not amt:
      return self._body.read()
    else:
      return self._body.read(amt)
