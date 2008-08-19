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


__author__ = 'api.jscudder (Jeff Scudder)'


import urlparse
import urllib


def parse_url(url_string):
  parts = urlparse.urlparse(url_string)
  url = Url()
  if parts[0]:
    url.protocol = parts[0]
  if parts[1]:
    host_parts = parts[1].split(':')
    if host_parts[0]:
      url.host = host_parts[0]
    if len(host_parts) > 1:
      url.port = host_parts[1]
  if parts[2]:
    url.path = parts[2]
  if parts[4]:
    param_pairs = parts[4].split('&')
    for pair in param_pairs:
      pair_parts = pair.split('=')
      if len(pair_parts) > 1:
        url.params[urllib.unquote_plus(pair_parts[0])] = (
            urllib.unquote_plus(pair_parts[1]))
      elif len(pair_parts) == 1:
        url.params[urllib.unquote_plus(pair_parts[0])] = None
  return url   
   
class Url(object):
  def __init__(self, protocol=None, host=None, port=None, path=None, params=None):
    self.protocol = protocol
    self.host = host
    self.port = port
    self.path = path
    self.params = params or {}

  def to_string(self):
    url_parts = ['', '', '', '', '', '']
    if self.protocol:
      url_parts[0] = self.protocol
    if self.host:
      if self.port:
        url_parts[1] = ':'.join((self.host, str(self.port)))
      else:
        url_parts[1] = self.host
    if self.path:
      url_parts[2] = self.path
    if self.params:
      url_parts[4] = self.get_param_string()
    return urlparse.urlunparse(url_parts)

  def get_param_string(self):
    param_pairs = []
    for key, value in self.params.iteritems():
      param_pairs.append('='.join((urllib.quote_plus(key), 
          urllib.quote_plus(value))))
    return '&'.join(param_pairs)

  def get_request_uri(self):
    """Returns the path with the parameters escaped and appended."""
    return '?'.join([self.path, self.get_param_string()])

  def __str__(self):
    return self.to_string()
    
