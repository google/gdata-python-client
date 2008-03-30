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


"""MockService provides CRUD ops. for mocking calls to AtomPub services.

  MockService: Exposes the publicly used methods of AtomService to provide
      a mock interface which can be used in unit tests.
"""

import atom.service
import pickle

__author__ = 'api.jscudder (Jeffrey Scudder)'


class MockHttpResponse(object):
  """Returned from MockService crud methods as the server's response."""

  def __init__(self, body=None, status=None, reason=None, headers=None):
    """Construct a mock HTTPResponse and set members.

    Args:
      body: str (optional) The HTTP body of the server's response. 
      status: int (optional) 
      reason: str (optional)
      headers: dict (optional)
    """
    self.body = body
    self.status = status
    self.reason = reason
    self.headers = headers or {}

  def read(self):
    return self.body

  def getheader(self, header_name):
    return self.headers[header_name]


class MockRequest(object):
  """Represents a thumbprint of an HTTP request also mocks HTTPConnection.
  
  These objects are used to determine if a request matches a recorded HTTP 
  request to determine what the mock server's response will be. It only looks
  at the request's URL and HTTP headers.

  Args:
    verb: str Should be an HTTP verb, one of GET, POST, PUT, or DELETE.
    url: str
    headers: dict (optional)
    body: str (optional)
    response: MockHttpResponse (optional) The response to give when the 
        simulated request is made. Returned in getresponse.
  """

  def __init__(self, verb, url, headers=None, body=None, response=None):
    self.url = url
    self.verb = verb
    self.headers = headers or {}
    self.body = body
    self.response = response


  def IsMatch(self, other_request):
    if other_request.url == self.url and other_request.verb == self.verb:
      # Make sure that all headers defined are present in the request.
      # (Additional headers are allowed)
      for key, value in self.headers.iteritems():
        if (not other_request.headers.has_key(key) 
            or other_request.headers[key] != value):
          return False
      return True
    else:
      return False

  def ToString(self):
    return pickle.dumps(self)

  # The following methods make the mock request act like a HTTPConnection
  def putrequest(self, verb, url):
    self.verb = verb
    self.url = url

  def putheader(self, key, value):
    self.headers[key] = value

  def endheaders(self):
    pass

  def getresponse(self):
    return self.response

  def send(self, data):
    if not self.body:
      self.body = data
    else:
      self.body = ''.join([self.body, data])


def MockRequestFromString(thumbprint_string):
  return pickle.loads(thumbprint_string)


class MockService(atom.service.AtomService):
  """Simulates Atom Publishing Protocol CRUD operations.
  
  The MockService can be configured with expectations and responses.
  """

  def __init__(self, server=None, additional_headers=None, 
      real_service=None):
    """Creates a new MockService client.
    
    Args:
      server: string (optional) The start of a URL for the server
          to which all operations should be directed. Example: 
          'www.google.com'
      additional_headers: dict (optional) Any additional HTTP headers which
          should be included with CRUD operations.
      real_service: atom.service.AtomService A service object which will be
          used to make requests. When the real_service is set, all requests
          will actually be sent using this object and responses will be added
          to the list of recordings. Setting this member puts the mock service
          in record mode, unsetting (None) puts the mock service into replay
          mode and it will answer requests out of it's recordings. This could
          be an instance of AtomService or a subclass.
    """
    self.server = server
    self.additional_headers = additional_headers or {}
    self.recordings = []
    self.real_service = real_service

  def DumpRecording(self):
    return pickle.dumps(self.recordings)

  def LoadRecording(self, pickle_string):
    self.recordings =  pickle.loads(pickle_string)

  def FindMatchingResponse(self, verb, url):
    """Returns the first recorded response with the desired verb and URL.

    If multiple recorded responses match the given verb-url combination, the
    first will always be returned. You can remove a response which has already
    been used by calling RemoveMatchingResponse.
    """
    for recording in self.recordings:
      # We might need to modify the url comparison to ignore URL params.
      if recording.verb == verb and url == url:
        return recording.response

  def RemoveMatchingResponse(self, verb, url):
    """Used when you want to "use up" a response when muliple matches exist.

    Args:
      verb: str One of 'GET', 'POST', 'PUT', or 'DELETE'. The HTTP verb used
          in the request.
      url: str
    """
    # Logic should exactly match that in FindMatchingResponse.
    i = 0
    for recording in self.recordings:
      if recording.verb == verb and url == url:
        del self.recordings[i]
        return
      i += 1  

  def PrepareConnection(self, full_uri):
    if self.real_service:
      response = self.real_service.PrepareConnection(full_uri)
      # Store the response in the recordings.
      # Return the response.
      return response
    # TODO: complete
    return (MockRequest(None, full_uri), full_uri)
    
  def CreateConnection(self, uri, http_operation, extra_headers=None,
      url_params=None, escape_params=True):
    if self.real_service:
      response = self.real_service.CreateConnection(uri, http_operation, 
          extra_headers=extra_headers, url_params=url_params,
          escape_params=escape_params)
      return response
    # TODO: complete
    mock_request = None
    pass

  def Get(self, uri, extra_headers=None, url_params=None, escape_params=True):
    if not self.real_service:
      return self.FindMatchingResponse('GET', uri)
    else:
      live_response = self.real_service.Get(uri, extra_headers=extra_headers, 
          url_params=url_params, escape_params=escape_params)
      # Store the response as a recording.
      stored_response = MockHttpResponse(body=live_response.read(), 
          status=live_response.status, reason=live_response.reason)
      stored_request = MockRequest(verb='GET', url=uri, response=stored_response)
      self.recordings.append(stored_request)
      return stored_response


  def Post(self, data, uri, extra_headers=None, url_params=None, 
           escape_params=True, content_type='application/atom+xml'):
    if not self.real_service:
      return self.FindMatchingResponse('POST', uri)
    else:
      live_response = self.real_service.Post(data, uri, 
          extra_headers=extra_headers, url_params=url_params,
          escape_params=escape_params)
      # Store the response as a recording.
      stored_response = MockHttpResponse(body=live_response.read(), 
          status=live_response.status, reason=live_response.reason)
      stored_request = MockRequest(verb='POST', url=uri, response=stored_response)
      self.recordings.append(stored_request)
      return stored_response
      

  def Put(self, data, uri, extra_headers=None, url_params=None, 
          escape_params=True, content_type='application/atom+xml'):
    if not self.real_service:
      return self.FindMatchingResponse('PUT', uri)
    else:
      live_response = self.real_service.Put(data, uri,
          extra_headers=extra_headers, url_params=url_params,
          escape_params=escape_params)
      # Store the response as a recording.
      stored_response = MockHttpResponse(body=live_response.read(), 
          status=live_response.status, reason=live_response.reason)
      stored_request = MockRequest(verb='GET', url=uri, response=stored_response)
      self.recordings.append(stored_request)
      return stored_response

  def Delete(self, uri, extra_headers=None, url_params=None, 
             escape_params=True):
    if not self.should_record:
      return self.FindMatchingResponse('DELETE', uri)
    else:
      live_response = self.real_service.Delete(uri, 
          extra_headers=extra_headers, url_params=url_params,
          escape_params=escape_params)
      # Store the response as a recording.
      stored_response = MockHttpResponse(body=live_response.read(), 
          status=live_response.status, reason=live_response.reason)
      stored_request = MockRequest(verb='GET', url=uri, response=stored_response)
      self.recordings.append(stored_request)
      return stored_response

