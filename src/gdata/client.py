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


import urllib
import urlparse
import gdata.auth
import gdata.service
import atom.service


SCOPE_URL_PARAM_NAME = gdata.service.SCOPE_URL_PARAM_NAME 
# Maps the service names used in ClientLogin to scope URLs. 
CLIENT_LOGIN_SCOPES = gdata.service.CLIENT_LOGIN_SCOPES


class AuthorizationRequired(gdata.service.Error):
  pass


class GDataClient(gdata.service.GDataService):
  """This class is deprecated. 
  
  All functionality has been migrated to gdata.service.GDataService.
  """
  def __init__(self, application_name=None, tokens=None):
    gdata.service.GDataService.__init__(self, source=application_name, 
        tokens=tokens)

  def ClientLogin(self, username, password, service_name, source=None, 
      account_type=None, auth_url=None, login_token=None, login_captcha=None):
    gdata.service.GDataService.ClientLogin(self, username=username, 
        password=password, account_type=account_type, service=service_name,
        auth_service_url=auth_url, source=source, captcha_token=login_token,
        captcha_response=login_captcha)

  def Get(self, url, parser):
    """Simplified interface for Get.

    Requires a parser function which takes the server response's body as
    the only argument.

    Args:
      url: A string or something that can be converted to a string using str.
          The URL of the requested resource.
      parser: A function which takes the HTTP body from the server as it's
          only result. Common values would include str, 
          gdata.GDataEntryFromString, and gdata.GDataFeedFromString.

    Returns: The result of calling parser(http_response_body).
    """
    return gdata.service.GDataService.Get(self, uri=url, converter=parser)

  def Post(self, data, url, parser, media_source=None):
    """Streamlined version of Post.

    Requires a parser function which takes the server response's body as
    the only argument.
    """
    return gdata.service.GDataService.Post(self, data=data, uri=url,
        media_source=media_source, converter=parser)

  def Put(self, data, url, parser, media_source=None):
    """Streamlined version of Put.

    Requires a parser function which takes the server response's body as
    the only argument.
    """
    return gdata.service.GDataService.Put(self, data=data, uri=url,
        media_source=media_source, converter=parser)

  def Delete(self, url):
    return gdata.service.GDataService.Delete(self, uri=url)


ExtractToken = gdata.service.ExtractToken
GenerateAuthSubRequestUrl = gdata.service.GenerateAuthSubRequestUrl    
