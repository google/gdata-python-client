#!/usr/bin/python
#
# Copyright (C) 2008 Yu-Jie Lin
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

"""GWebmasterToolsService extends the GDataService to streamline
Google Webmaster Tools operations.

  GWebmasterToolsService: Provides methods to query feeds and manipulate items.
                          Extends GDataService.
"""

__author__ = 'livibetter (Yu-Jie Lin)'

import urllib
import gdata
import atom.service
import gdata.service
import gdata.webmastertools as webmastertools
import atom


FEED_BASE = '/webmasters/tools/feeds/'
SITES_FEED = FEED_BASE + 'sites/'
SITE_TEMPLATE = SITES_FEED + '%s'
SITEMAPS_FEED_TEMPLATE = FEED_BASE + '%(site_id)s/sitemaps/'
SITEMAP_TEMPLATE = SITEMAPS_FEED_TEMPLATE + '%(sitemap_id)s'


class Error(Exception):
  pass


class RequestError(Error):
  pass


class GWebmasterToolsService(gdata.service.GDataService):
  """Client for the Google Webmaster Tools service."""

  def __init__(self, email=None, password=None, source=None, 
               server='www.google.com', api_key=None, 
               additional_headers=None, handler=None):
    gdata.service.GDataService.__init__(self, email=email, password=password,
                                        service='sitemaps', source=source, 
                                        server=server, 
                                        additional_headers=additional_headers,
                                        handler=handler)

  def GetSitesFeed(self, uri=SITES_FEED,
      converter=webmastertools.SitesFeedFromString):
    """Gets sites feed.

    Args:
      uri: str (optional) URI to retrieve sites feed.
      converter: func (optional) Function which is executed on the server's
          response before it is returned. Usually this is a function like
          SitesFeedFromString which will parse the response and turn it into
          an object.

    Returns:
      If converter is defined, the results of running converter on the server's
      response. Otherwise, it will be a SitesFeed object.
    """
    return self.Get(uri, converter=converter)

  def AddSite(self, site_uri, uri=SITES_FEED,
      url_params=None, escape_params=True, converter=None):
    """Adds a site to Google Webmaster Tools.

    Args: 
      site_uri: str URI of which site to add.
      uri: str (optional) URI to add a site.
      url_params: dict (optional) Additional URL parameters to be included
                  in the insertion request. 
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.
      converter: func (optional) Function which is executed on the server's
          response before it is returned. Usually this is a function like
          SitesEntryFromString which will parse the response and turn it into
          an object.

    Returns:
      If converter is defined, the results of running converter on the server's
      response. Otherwise, it will be a SitesEntry object.
    """

    site_entry = webmastertools.SitesEntry()
    site_entry.content = atom.Content(src=site_uri)
    response = self.Post(site_entry, uri,
        url_params=url_params, 
        escape_params=escape_params, converter=converter)
    if not converter and isinstance(response, atom.Entry):
      return webmastertools.SitesEntryFromString(response.ToString())
    return response

  def DeleteSite(self, site_uri, uri=SITE_TEMPLATE,
      url_params=None, escape_params=True):
    """Removes a site from Google Webmaster Tools.

    Args: 
      site_uri: str URI of which site to remove.
      uri: str (optional) A URI template to send DELETE request.
           Default SITE_TEMPLATE.
      url_params: dict (optional) Additional URL parameters to be included
                  in the insertion request. 
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.

    Returns:
      True if the delete succeeded.
    """

    return self.Delete(
        uri % urllib.quote_plus(site_uri),
        url_params=url_params, escape_params=escape_params)

  def GetSitemapsFeed(self, site_uri, uri=SITEMAPS_FEED_TEMPLATE,
      converter=webmastertools.SitemapsFeedFromString):
    """Gets sitemaps feed of a site.
    
    Args:
      site_uri: str (optional) URI of which site to retrieve its sitemaps feed.
      uri: str (optional) URI to retrieve sites feed.
      converter: func (optional) Function which is executed on the server's
          response before it is returned. Usually this is a function like
          SitemapsFeedFromString which will parse the response and turn it into
          an object.

    Returns:
      If converter is defined, the results of running converter on the server's
      response. Otherwise, it will be a SitemapsFeed object.
    """
    return self.Get(uri % {'site_id': urllib.quote_plus(site_uri)},
        converter=converter)

  def AddSitemap(self, site_uri, sitemap_uri, sitemap_type='WEB',
      uri=SITEMAPS_FEED_TEMPLATE,
      url_params=None, escape_params=True, converter=None):
    """Adds a regular sitemap to a site.

    Args: 
      site_uri: str URI of which site to add sitemap for.
      sitemap_uri: str URI of sitemap to add to a site.
      sitemap_type: str Type of added sitemap. Valid types: WEB, VIDEO, or CODE.
      uri: str (optional) URI template to add a sitemap.
           Default SITEMAP_TEMPLATE.
      url_params: dict (optional) Additional URL parameters to be included
                  in the insertion request. 
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.
      converter: func (optional) Function which is executed on the server's
          response before it is returned. Usually this is a function like
          SitemapsEntryFromString which will parse the response and turn it into
          an object.

    Returns:
      If converter is defined, the results of running converter on the server's
      response. Otherwise, it will be a SitemapsEntry object.
    """

    sitemap_entry = webmastertools.SitemapsEntry(
        atom_id=atom.Id(text=sitemap_uri),
        category=atom.Category(
            scheme='http://schemas.google.com/g/2005#kind',
            term='http://schemas.google.com/webmasters/tools/2007#sitemap-regular'),
        sitemap_type=webmastertools.SitemapType(text=sitemap_type))
    response = self.Post(
        sitemap_entry,
        uri % {'site_id': urllib.quote_plus(site_uri)},
        url_params=url_params,
        escape_params=escape_params, converter=converter)
    if not converter and isinstance(response, atom.Entry):
      return webmastertools.SitemapsEntryFromString(response.ToString())
    return response

  def AddMobileSitemap(self):
    # TODO
    pass

  def AddNewsSitemap(self):
    # TODO
    pass

  def DeleteSitemap(self, site_uri, sitemap_uri, uri=SITEMAP_TEMPLATE,
      url_params=None, escape_params=True):
    """Removes a sitemap from a site.

    Args: 
      site_uri: str URI of which site to remove a sitemap from.
      sitemap_uri: str URI of sitemap to remove from a site.
      uri: str (optional) A URI template to send DELETE request.
           Default SITEMAP_TEMPLATE.
      url_params: dict (optional) Additional URL parameters to be included
                  in the insertion request. 
      escape_params: boolean (optional) If true, the url_parameters will be
                     escaped before they are included in the request.

    Returns:
      True if the delete succeeded.
    """

    return self.Delete(
        uri % {'site_id': urllib.quote_plus(site_uri),
            'sitemap_id': urllib.quote_plus(sitemap_uri)},
        url_params=url_params, escape_params=escape_params)
