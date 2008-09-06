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


"""Provides HTTP functions for gdata.service to use on Google App Engine

AppEngineHttpClient: Provides an HTTP request method which uses App Engine's
   urlfetch API. Set the http_client member of a GDataService object to an
   instance of an AppEngineHttpClient to allow the gdata library to run on
   Google App Engine.

run_on_appengine: Function which will modify an existing GDataService object
   to allow it to run on App Engine. It works by creating a new instance of
   the AppEngineHttpClient and replacing the GDataService object's
   http_client.
"""


__author__ = 'api.jscudder (Jeff Scudder)'


import StringIO
import atom.service
import atom.http_interface
from google.appengine.api import urlfetch


def run_on_appengine(gdata_service):
  """Modifies a GDataService object to allow it to run on App Engine.

  Args:
    gdata_service: An instance of AtomService, GDataService, or any
        of their subclasses which has an http_client member.
  """
  gdata_service.http_client = AppEngineHttpClient()


class AppEngineHttpClient(atom.http_interface.GenericHttpClient):
  def __init__(self, headers=None):
    self.debug = False
    self.headers = headers or {}

  def request(self, operation, url, data=None, headers=None):
    """Performs an HTTP call to the server, supports GET, POST, PUT, and
    DELETE.

    Usage example, perform and HTTP GET on http://www.google.com/:
      import atom.http
      client = atom.http.HttpClient()
      http_response = client.request('GET', 'http://www.google.com/')

    Args:
      operation: str The HTTP operation to be performed. This is usually one
          of 'GET', 'POST', 'PUT', or 'DELETE'
      data: filestream, list of parts, or other object which can be converted
          to a string. Should be set to None when performing a GET or DELETE.
          If data is a file-like object which can be read, this method will
          read a chunk of 100K bytes at a time and send them.
          If the data is a list of parts to be sent, each part will be
          evaluated and sent.
      url: The full URL to which the request should be sent. Can be a string
          or atom.url.Url.
      headers: dict of strings. HTTP headers which should be sent
          in the request.
    """
    all_headers = self.headers.copy()
    if headers:
      all_headers.update(headers)

    # Construct the full payload.
    # Assume that data is None or a string.
    data_str = data
    if data:
      if isinstance(data, list):
        # If data is a list of different objects, convert them all to strings
        # and join them together.
        converted_parts = [__ConvertDataPart(x) for x in data]
        data_str = ''.join(converted_parts)
      else:
        data_str = __ConvertDataPart(data)

    # If the list of headers does not include a Content-Length, attempt to
    # calculate it based on the data object.
    if data and 'Content-Length' not in all_headers:
      all_headers['Content-Length'] = len(data_str)

    # Set the content type to the default value if none was set.
    if 'Content-Type' not in all_headers:
      all_headers['Content-Type'] = 'application/atom+xml'

    # Lookup the urlfetch operation which corresponds to the desired HTTP verb.
    if operation == 'GET':
      method = urlfetch.GET
    elif operation == 'POST':
      method = urlfetch.POST
    elif operation == 'PUT':
      method = urlfetch.PUT
    elif operation == 'DELETE':
      method = urlfetch.DELETE
    else:
      method = None
    return HttpResponse(urlfetch.Fetch(url=str(url), payload=data_str,
        method=method, headers=all_headers))


def __ConvertDataPart(data):
  if not data or isinstance(data, str):
    return data
  elif hasattr(data, 'read'):
    # data is a file like object, so read it completely.
    return data.read()
  # The data object was not a file.
  # Try to convert to a string and send the data.
  return str(data)


class HttpResponse(object):
  """Translates a urlfetch resoinse to look like an hhtplib resoinse.

  Used to allow the resoinse from HttpRequest to be usable by gdata.service
  methods.
  """

  def __init__(self, urlfetch_response):
    self.body = StringIO.StringIO(urlfetch_response.content)
    self.headers = urlfetch_response.headers
    self.status = urlfetch_response.status_code
    self.reason = ''

  def read(self, length=None):
    if not length:
      return self.body.read()
    else:
      return self.body.read(length)

  def getheader(self, name):
    if not self.headers.has_key(name):
      return self.headers[name.lower()]
    return self.headers[name]

