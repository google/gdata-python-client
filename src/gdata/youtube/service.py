#!/usr/bin/python
#
# Copyright (C) 2006 Google Inc.
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

"""YouTubeService extends GDataService to streamline YouTube operations.

  YouTubeService: Provides methods to perform CRUD operations on YouTube feeds. 
  Extends GDataService.

"""

__author__ = ('api.stephaniel@gmail.com (Stephanie Liu), '
              'api.jhartmann@gmail.com (Jochen Hartmann)')

try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import urllib
import os
import gdata
import atom
import gdata.service
import gdata.youtube
# TODO (jhartmann) - rewrite query class structure + allow passing in projections

YOUTUBE_SERVER = 'gdata.youtube.com'
YOUTUBE_SERVICE = 'youtube'
YOUTUBE_SUPPORTED_UPLOAD_TYPES = ('mov', 'avi', 'wmv', 'mpg', 'quicktime')
YOUTUBE_QUERY_VALID_TIME_PARAMETERS = ('today', 'this_week', 'this_month',
                                        'all_time')
YOUTUBE_QUERY_VALID_ORDERBY_PARAMETERS = ('updated', 'viewCount', 'rating',
                                           'relevance')
YOUTUBE_QUERY_VALID_RACY_PARAMETERS = ('include', 'exclude')
YOUTUBE_QUERY_VALID_FORMAT_PARAMETERS = ('1', '5', '6')
YOUTUBE_STANDARDFEEDS = ('most_recent', 'recently_featured',
                          'top_rated', 'most_viewed','watch_on_mobile')

YOUTUBE_UPLOAD_TOKEN_URI = 'http://gdata.youtube.com/action/GetUploadToken'
YOUTUBE_VIDEO_URI = 'http://gdata.youtube.com/feeds/api/videos'
YOUTUBE_USER_FEED_URI = 'http://gdata.youtube.com/feeds/api/users/'

YOUTUBE_STANDARD_FEEDS = 'http://gdata.youtube.com/feeds/api/standardfeeds'
YOUTUBE_STANDARD_TOP_RATED_URI = YOUTUBE_STANDARD_FEEDS + '/top_rated'
YOUTUBE_STANDARD_MOST_VIEWED_URI = YOUTUBE_STANDARD_FEEDS + '/most_viewed'
YOUTUBE_STANDARD_RECENTLY_FEATURED_URI = YOUTUBE_STANDARD_FEEDS + (
    '/recently_featured')
YOUTUBE_STANDARD_WATCH_ON_MOBILE_URI = YOUTUBE_STANDARD_FEEDS + (
    '/watch_on_mobile')
YOUTUBE_STANDARD_TOP_FAVORITES_URI = YOUTUBE_STANDARD_FEEDS + '/top_favorites'
YOUTUBE_STANDARD_MOST_RECENT_URI = YOUTUBE_STANDARD_FEEDS + '/most_recent'
YOUTUBE_STANDARD_MOST_DISCUSSED_URI = YOUTUBE_STANDARD_FEEDS + '/most_discussed'
YOUTUBE_STANDARD_MOST_LINKED_URI = YOUTUBE_STANDARD_FEEDS + '/most_linked'
YOUTUBE_STANDARD_MOST_RESPONDED_URI = YOUTUBE_STANDARD_FEEDS + '/most_responded'

YOUTUBE_RATING_LINK_REL = 'http://gdata.youtube.com/schemas/2007#video.ratings'
YOUTUBE_COMPLAINT_CATEGORY_SCHEME = 'http://gdata.youtube.com/schemas/2007/complaint-reasons.cat'
YOUTUBE_COMPLAINT_CATEGORY_TERMS = ('PORN', 'VIOLENCE', 'HATE', 'DANGEROUS', 
                                   'RIGHTS', 'SPAM')
YOUTUBE_CONTACT_STATUS = ('accepted', 'rejected')
YOUTUBE_CONTACT_CATEGORY = ('Friends', 'Family')

UNKOWN_ERROR=1000
YOUTUBE_BAD_REQUEST=400
YOUTUBE_CONFLICT=409
YOUTUBE_INTERNAL_SERVER_ERROR=500
YOUTUBE_INVALID_ARGUMENT=601
YOUTUBE_INVALID_CONTENT_TYPE=602
YOUTUBE_NOT_A_VIDEO=603
YOUTUBE_INVALID_KIND=604

class Error(Exception):
  pass

class RequestError(Error):
  pass

class YouTubeError(Error):
  pass

class YouTubeService(gdata.service.GDataService):
  """Client for the YouTube service."""

  def __init__(self, email=None, password=None, source=None,
               server=YOUTUBE_SERVER, additional_headers=None, client_id=None,
               developer_key=None):
    if client_id and developer_key:
      self.client_id = client_id
      self.developer_key = developer_key
      self.additional_headers = {'X-Gdata-Client': self.client_id,
                                 'X-GData-Key': 'key=' + self.developer_key}
      gdata.service.GDataService.__init__(
          self, email=email, password=password,
          service=YOUTUBE_SERVICE, source=source, server=server,
          additional_headers=self.additional_headers)
    elif developer_key and not client_id:
      raise YouTubeError('You must also specify the clientId')
    else:
      gdata.service.GDataService.__init__(
          self, email=email, password=password,
          service=YOUTUBE_SERVICE, source=source, server=server,
          additional_headers=additional_headers)

  def GetYouTubeVideoFeed(self, uri):
    return self.Get(uri, converter=gdata.youtube.YouTubeVideoFeedFromString)

  def GetYouTubeVideoEntry(self, uri=None, video_id=None):
    if not uri and not video_id:
      raise YouTubeError('You must provide at least a uri or a video_id '
                         'to the GetYouTubeVideoEntry() method')
    elif video_id and not uri:
      uri = YOUTUBE_VIDEO_URI + '/' + video_id

    return self.Get(uri, converter=gdata.youtube.YouTubeVideoEntryFromString)

  def GetYouTubeContactFeed(self, uri=None, username=None):
    if not uri and not username:
      raise YouTubeError('You must provide at least a uri or a username '
                         'to the GetYouTubeContactFeed() method')
    elif username and not uri:
      uri = YOUTUBE_USER_FEED_URI + username + '/contacts'

    return self.Get(uri, converter=gdata.youtube.YouTubeContactFeedFromString)

  def GetYouTubeContactEntry(self, uri=None):
    return self.Get(uri, converter=gdata.youtube.YouTubeContactEntryFromString)

  def GetYouTubeVideoCommentFeed(self, uri=None, video_id=None):
    if not uri and not video_id:
      raise YouTubeError('You must provide at least a uri or a video_id '
                         'to the GetYouTubeVideoCommentFeed() method')
    elif video_id and not uri:
      uri = YOUTUBE_VIDEO_URI + '/' + video_id + '/comments'

    return self.Get(
        uri,
        converter=gdata.youtube.YouTubeVideoCommentFeedFromString)

  def GetYouTubeVideoCommentEntry(self, uri):
    return self.Get(
        uri,
        converter=gdata.youtube.YouTubeVideoCommentEntryFromString)

  def GetYouTubeUserFeed(self, uri=None, username=None):
    if not uri and not username:
      raise YouTubeError('You must provide at least a uri or a username '
                         'to the GetYouTubeUserFeed() method')
    elif username and not uri:
      uri = YOUTUBE_USER_FEED_URI + username + '/uploads'

    return self.Get(uri, converter=gdata.youtube.YouTubeUserFeedFromString)

  def GetYouTubeUserEntry(self, uri=None, username=None):
    if not uri and not username:
      raise YouTubeError('You must provide at least a uri or a username '
                         'to the GetYouTubeUserEntry() method')
    elif username and not uri:
      uri = YOUTUBE_USER_FEED_URI + username

    return self.Get(uri, converter=gdata.youtube.YouTubeUserEntryFromString)

  def GetYouTubePlaylistFeed(self, uri=None, username=None):
    if not uri and not username:
      raise YouTubeError('You must provide at least a uri or a username '
                         'to the GetYouTubePlaylistFeed() method')
    elif username and not uri:
      uri = YOUTUBE_USER_FEED_URI + username + '/playlists'

    return self.Get(uri, converter=gdata.youtube.YouTubePlaylistFeedFromString)

  def GetYouTubePlaylistEntry(self, uri):
    return self.Get(uri, converter=gdata.youtube.YouTubePlaylistEntryFromString)

  def GetYouTubePlaylistVideoFeed(self, uri=None, playlist_id=None):
    if not uri and not playlist_id:
      raise YouTubeError('You must provide at least a uri or a playlist_id '
                         'to the GetYouTubePlaylistVideoFeed() method')
    elif playlist_id and not uri:
      uri = 'http://gdata.youtube.com/feeds/api/playlists/' + playlist_id

    return self.Get(
        uri,
        converter=gdata.youtube.YouTubePlaylistVideoFeedFromString)

  def GetYouTubeVideoResponseFeed(self, uri=None, video_id=None):
    if not uri and not video_id:
      raise YouTubeError('You must provide at least a uri or a video_id '
                         'to the GetYouTubeVideoResponseFeed() method')
    elif video_id and not uri:
      uri = YOUTUBE_VIDEO_URI + '/' + video_id + '/responses'

    return self.Get(uri,
                    converter=gdata.youtube.YouTubeVideoResponseFeedFromString)

  def GetYouTubeVideoResponseEntry(self, uri):
    return self.Get(uri,
                    converter=gdata.youtube.YouTubeVideoResponseEntryFromString)

  def GetYouTubeSubscriptionFeed(self, uri=None, username=None):
    if not uri and not username:
      raise YouTubeError('You must provide at least a uri or a username '
                         'to the GetYouTubeSubscriptionFeed() method')
    elif username and not uri:
      uri = ('http://gdata.youtube.com'
             '/feeds/users/') + username + '/subscriptions'

    return self.Get(
        uri,
        converter=gdata.youtube.YouTubeSubscriptionFeedFromString)

  def GetYouTubeSubscriptionEntry(self, uri):
    return self.Get(uri,
                    converter=gdata.youtube.YouTubeSubscriptionEntryFromString)

  def GetYouTubeRelatedVideoFeed(self, uri=None, video_id=None):
    if not uri and not video_id:
      raise YouTubeError('You must provide at least a uri or a video_id '
                         'to the GetYouTubeRelatedVideoFeed() method')
    elif video_id and not uri:
      uri = YOUTUBE_VIDEO_URI + '/' + video_id + '/related'

    return self.Get(uri,
                    converter=gdata.youtube.YouTubeVideoFeedFromString)

  def GetTopRatedVideoFeed(self):
    return self.GetYouTubeVideoFeed(YOUTUBE_STANDARD_TOP_RATED_URI)

  def GetMostViewedVideoFeed(self):
    return self.GetYouTubeVideoFeed(YOUTUBE_STANDARD_MOST_VIEWED_URI)

  def GetRecentlyFeaturedVideoFeed(self):
    return self.GetYouTubeVideoFeed(YOUTUBE_STANDARD_RECENTLY_FEATURED_URI)

  def GetWatchOnMobileVideoFeed(self):
    return self.GetYouTubeVideoFeed(YOUTUBE_STANDARD_WATCH_ON_MOBILE_URI)

  def GetTopFavoritesVideoFeed(self):
    return self.GetYouTubeVideoFeed(YOUTUBE_STANDARD_TOP_FAVORITES_URI)

  def GetMostRecentVideoFeed(self):
    return self.GetYouTubeVideoFeed(YOUTUBE_STANDARD_MOST_RECENT_URI)

  def GetMostDiscussedVideoFeed(self):
    return self.GetYouTubeVideoFeed(YOUTUBE_STANDARD_MOST_DISCUSSED_URI)

  def GetMostLinkedVideoFeed(self):
    return self.GetYouTubeVideoFeed(YOUTUBE_STANDARD_MOST_LINKED_URI)

  def GetMostRespondedVideoFeed(self):
    return self.GetYouTubeVideoFeed(YOUTUBE_STANDARD_MOST_RESPONDED_URI)

  def GetUserFavoritesFeed(self, username='default'):
    return self.GetYouTubeVideoFeed('http://gdata.youtube.com/feeds/api/users/'
                                    + username + '/favorites')

  def InsertVideoEntry(self, video_entry, filename_or_handle,
                       youtube_username='default',
                       content_type='video/quicktime'):
    """Upload a new video to YouTube using the direct upload mechanism

    Needs authentication.

    Arguments:
      video_entry: The YouTubeVideoEntry to upload
      filename_or_handle: A file-like object or file name where the video
          will be read from
      youtube_username: (optional) Username into whose account this video is
          to be uploaded to. Defaults to the currently authenticated user.
      content_type (optional): Internet media type (a.k.a. mime type) of
          media object. Currently the YouTube API supports these types:
            o video/mpeg
            o video/quicktime
            o video/x-msvideo
            o video/mp4

    Returns:
      The newly created YouTubeVideoEntry or a YouTubeError

    """

    # check to make sure we have a valid video entry
    try:
      assert(isinstance(video_entry, gdata.youtube.YouTubeVideoEntry))
    except AssertionError:
      raise YouTubeError({'status':YOUTUBE_INVALID_ARGUMENT,
          'body':'`video_entry` must be a gdata.youtube.VideoEntry instance',
          'reason':'Found %s, not VideoEntry' % type(video_entry)
          })

    # check to make sure the MIME type is supported
    try:
      majtype, mintype = content_type.split('/')
      assert(mintype in YOUTUBE_SUPPORTED_UPLOAD_TYPES)
    except (ValueError, AssertionError):
      raise YouTubeError({'status':YOUTUBE_INVALID_CONTENT_TYPE,
          'body':'This is not a valid content type: %s' % content_type,
          'reason':'Accepted content types: %s' %
              ['video/' + t for t in YOUTUBE_SUPPORTED_UPLOAD_TYPES]
          })
    # check that the video file is valid and readable
    if (isinstance(filename_or_handle, (str, unicode)) 
        and os.path.exists(filename_or_handle)):
      mediasource = gdata.MediaSource()
      mediasource.setFile(filename_or_handle, content_type)
    elif hasattr(filename_or_handle, 'read'):
      if hasattr(filename_or_handle, 'seek'):
        filename_or_handle.seek(0)
      file_handle = StringIO.StringIO(filename_or_handle.read())
      name = 'video'
      if hasattr(filename_or_handle, 'name'):
        name = filename_or_handle.name
      mediasource = gdata.MediaSource(file_handle, content_type,
          content_length=file_handle.len, file_name=name)
    else:
      raise YouTubeError({'status':YOUTUBE_INVALID_ARGUMENT, 'body':
          '`filename_or_handle` must be a path name or a file-like object',
          'reason': ('Found %s, not path name or object '
                     'with a .read() method' % type(filename_or_handle))})

    upload_uri = ('http://uploads.gdata.youtube.com/feeds/api/users/' + 
                  youtube_username + '/uploads')

    self.additional_headers['Slug'] = mediasource.file_name

    # post the video file
    try:
      try:
        return self.Post(video_entry, uri=upload_uri, media_source=mediasource,
                         converter=gdata.youtube.YouTubeVideoEntryFromString)
      except gdata.service.RequestError, e:
        raise YouTubeError(e.args[0])
    finally:
      del(self.additional_headers['Slug'])

  def CheckUploadStatus(self, video_entry=None, video_id=None):
    """Check upload status on a recently uploaded video entry

    Needs authentication.

    Arguments:
      video_entry: (optional) The YouTubeVideoEntry to upload
      video_id: (optional) The videoId of a recently uploaded entry. One of
          these two arguments will need to be present.

    Returns:
      A tuple containing (video_upload_state, detailed_message) or None if
          no status information is found.
    """
    if not video_entry and not video_id:
      raise YouTubeError('You must provide at least a uri or a video_id '
                         'to the CheckUploadStatus() method')
    elif video_id and not video_entry:
       video_entry = self.GetYouTubeVideoEntry(video_id=video_id)

    control = video_entry.control
    if control is not None:
      draft = control.draft
      if draft is not None:
        if draft.text == 'yes':
          yt_state = control.extension_elements[0]
          if yt_state is not None:
            state_value = yt_state.attributes['name']
            message = ''
            if yt_state.text is not None:
              message = yt_state.text

            return (state_value, message)

  def GetFormUploadToken(self, video_entry, uri=YOUTUBE_UPLOAD_TOKEN_URI):
    """Receives a YouTube Token and a YouTube PostUrl with which to construct
    the HTML Upload form for browser-based video uploads

    Needs authentication.

    Arguments:
        video_entry: The YouTubeVideoEntry to upload (meta-data only)
        uri: (optional) A url from where to fetch the token information

    Returns:
        A tuple containing (post_url, youtube_token)
    """
    response = self.Post(video_entry, uri)
    tree = ElementTree.fromstring(response)

    for child in tree:
      if child.tag == 'url':
        post_url = child.text
      elif child.tag == 'token':
        youtube_token = child.text

    return (post_url, youtube_token)

  def UpdateVideoEntry(self, video_entry):
    """Updates a video entry's meta-data

    Needs authentication.

    Arguments:
        video_entry: The YouTubeVideoEntry to update, containing updated 
            meta-data

    Returns:
        An updated YouTubeVideoEntry on success or None
    """
    for link in video_entry.link:
      if link.rel == 'edit':
        edit_uri = link.href

    return self.Put(video_entry, uri=edit_uri,
                    converter=gdata.youtube.YouTubeVideoEntryFromString)

  def DeleteVideoEntry(self, video_entry):
    """Deletes a video entry

    Needs authentication.

    Arguments:
        video_entry: The YouTubeVideoEntry to be deleted

    Returns:
        True if entry was deleted successfully
    """
    for link in video_entry.link:
      if link.rel == 'edit':
        edit_uri = link.href

    return self.Delete(edit_uri)

  def AddRating(self, rating_value, video_entry):
    """Add a rating to a video entry

    Needs authentication.

    Arguments:
        rating_value: The value for the rating (between 1 and 5)
        video_entry: The YouTubeVideoEntry to be rated

    Returns:
      True if the rating was added successfully
    """

    if rating_value < 1 or rating_value > 5:
      raise YouTubeError('AddRating: rating_value must be between 1 and 5')

    entry = gdata.GDataEntry()
    rating = gdata.youtube.Rating(min='1', max='5')
    rating.extension_attributes['name'] = 'value'
    rating.extension_attributes['value'] = str(rating_value)
    entry.extension_elements.append(rating)

    for link in video_entry.link:
      if link.rel == YOUTUBE_RATING_LINK_REL:
        rating_uri = link.href

    return self.Post(entry, uri=rating_uri)

  def AddComment(self, comment_text, video_entry):
    """Add a comment to a video entry

    Needs authentication.

    Arguments:
        comment_text: The text of the comment
        video_entry: The YouTubeVideoEntry to be commented on

    Returns:
      True if the comment was added successfully
    """
    content = atom.Content(text=comment_text)
    comment_entry = gdata.youtube.YouTubeVideoCommentEntry(content=content)
    comment_post_uri = video_entry.comments.feed_link[0].href

    return self.Post(comment_entry, uri=comment_post_uri)

  def AddVideoResponse(self, video_id_to_respond_to, video_response):
    """Add a video response

    Needs authentication.

    Arguments:
        video_id_to_respond_to: Id of the YouTubeVideoEntry to be responded to
        video_response: YouTubeVideoEntry to be posted as a response

    Returns:
        True if video response was posted successfully
    """
    post_uri = YOUTUBE_VIDEO_URI + '/' + video_id_to_respond_to + '/responses'
    return self.Post(video_response, uri=post_uri)

  def DeleteVideoResponse(self, video_id, response_video_id):
    """Delete a video response

    Needs authentication.

    Arguments:
        video_id: Id of YouTubeVideoEntry that contains the response
        response_video_id: Id of the YouTubeVideoEntry posted as response

    Returns:
        True if video response was deleted succcessfully
    """
    delete_uri = (YOUTUBE_VIDEO_URI + '/' + video_id + 
                  '/responses/' + response_video_id)

    return self.Delete(delete_uri)

  def AddComplaint(self, complaint_text, complaint_term, video_id):
    """Add a complaint for a particular video entry

    Needs authentication.

    Arguments:
        complaint_text: Text explaining the complaint
        complaint_term: Complaint category term
        video_id: Id of YouTubeVideoEntry to complain about

    Returns:
        True if posted successfully
    """
    if complaint_term not in YOUTUBE_COMPLAINT_CATEGORY_TERMS:
      raise YouTubeError('Your complaint must be a valid term')

    content = atom.Content(text=complaint_text)
    category = atom.Category(term=complaint_term,
                             scheme=YOUTUBE_COMPLAINT_CATEGORY_SCHEME)

    complaint_entry = gdata.GDataEntry(content=content, category=[category])
    post_uri = YOUTUBE_VIDEO_URI + '/' + video_id + '/complaints'

    return self.Post(complaint_entry, post_uri)

  def AddVideoEntryToFavorites(self, video_entry, username='default'):
    """Add a video entry to a users favorite feed

    Needs authentication.

    Arguments:
        video_entry: The YouTubeVideoEntry to add
        username: (optional) The username to whose favorite feed you wish to
            add the entry. Your client must be authenticated to the username's
            account.
    Returns:
        A GDataEntry if posted successfully
    """
    post_uri = ('http://gdata.youtube.com/feeds/api/users/' + 
                username + '/favorites')

    return self.Post(video_entry, post_uri)

  def DeleteVideoEntryFromFavorites(self, video_id, username='default'):
    """Delete a video entry from the users favorite feed

    Needs authentication.

    Arguments:
        video_id: The Id for the YouTubeVideoEntry to be removed
        username: (optional) The username of the user's favorite feed. Defaults
            to the currently authenticated user.

    Returns:
        True if entry was successfully deleted
    """
    edit_link = YOUTUBE_USER_FEED_URI + username + '/favorites/' + video_id
    return self.Delete(edit_link)

  def AddPlaylist(self, playlist_title, playlist_description, 
                  playlist_private=None):
    """Add a new playlist to the currently authenticated users account

    Needs authentication

    Arguments:
        playlist_title: The title for the new playlist
        playlist_description: The description for the playlist
        playlist_private: (optiona) Submit as True if the playlist is to be
            private
    Returns:
        A new YouTubePlaylistEntry if successfully posted
    """
    playlist_entry = gdata.youtube.YouTubePlaylistEntry(
        title=atom.Title(text=playlist_title),
        description=gdata.youtube.Description(text=playlist_description))
    if playlist_private:
      playlist_entry.private = gdata.youtube.Private()

    playlist_post_uri = YOUTUBE_USER_FEED_URI + 'default/playlists'
    return self.Post(playlist_entry, playlist_post_uri,
                     converter=gdata.youtube.YouTubePlaylistEntryFromString)

  def DeletePlaylist(self, playlist_uri):
    """Delete a playlist from the currently authenticated users playlists

    Needs authentication

    Arguments:
        playlist_uri: The uri of the playlist to delete

    Returns:
        True if successfully deleted
    """
    return self.Delete(playlist_uri)

  def AddPlaylistVideoEntryToPlaylist(self, playlist_uri, video_id, 
                                      custom_video_title=None,
                                      custom_video_description=None):
    """Add a video entry to a playlist, optionally providing a custom title
    and description

    Needs authentication

    Arguments:
        playlist_uri: Uri of playlist to add this video to.
        video_id: Id of the video entry to add
        custom_video_title: (optional) Custom title for the video
        custom_video_description: (optional) Custom video description

    Returns:
        A YouTubePlaylistVideoEntry if successfully posted
    """

    playlist_video_entry = gdata.youtube.YouTubePlaylistVideoEntry(
        atom_id=atom.Id(text=video_id))
    if custom_video_title:
      playlist_video_entry.title = atom.Title(text=custom_video_title)
    if custom_video_description:
      playlist_video_entry.description = gdata.youtube.Description(
          text=custom_video_description)
    return self.Post(playlist_video_entry, playlist_uri,
                    converter=gdata.youtube.YouTubePlaylistVideoEntryFromString)

  def UpdatePlaylistVideoEntryMetaData(self, playlist_uri, playlist_entry_id,
                                       new_video_title,
                                       new_video_description,
                                       new_video_position):
    """Update the meta data for a YouTubePlaylistVideoEntry

    Needs authentication

    Arguments:
        playlist_uri: Uri of the playlist that contains the entry to be updated
        playlist_entry_id: Id of the entry to be updated
        new_video_title: New title for the video entry
        new_video_description: New description for the video entry
        new_video_position: New position for the video

    Returns:
        A YouTubePlaylistVideoEntry if the update was successful
    """
    playlist_video_entry = gdata.youtube.YouTubePlaylistVideoEntry(
        title=atom.Title(text=new_video_title),
        description=gdata.youtube.Description(text=new_video_description),
        position=gdata.youtube.Position(text=str(new_video_position)))

    playlist_put_uri = playlist_uri + '/' + playlist_entry_id

    return self.Put(playlist_video_entry, playlist_put_uri, 
                    converter=gdata.youtube.YouTubePlaylistVideoEntryFromString)


  def AddSubscriptionToChannel(self, username):
    """Add a new channel subscription to the currently authenticated users 
    account

    Needs authentication

    Arguments:
        username: The username of the channel to subscribe to.

    Returns:
        A new YouTubeSubscriptionEntry if successfully posted
    """
    subscription_category = atom.Category(
        scheme='http://gdata.youtube.com/schemas/2007/subscriptiontypes.cat',
        term='channel')
    subscription_username = gdata.youtube.Username(text=username)

    subscription_entry = gdata.youtube.YouTubeSubscriptionEntry(
        category=subscription_category,
        username=subscription_username)

    post_uri = YOUTUBE_USER_FEED_URI + 'default/subscriptions'
    return self.Post(subscription_entry, post_uri,
                     converter=gdata.youtube.YouTubeSubscriptionEntryFromString)

  def AddSubscriptionToFavorites(self, username):
    """Add a new subscription to a users favorites to the currently
    authenticated user's account

    Needs authentication

    Arguments:
        username: The username of the users favorite feed to subscribe to

    Returns:
        A new YouTubeSubscriptionEntry if successful
    """
    subscription_category = atom.Category(
        scheme='http://gdata.youtube.com/schemas/2007/subscriptiontypes.cat',
        term='favorites')
    subscription_username = gdata.youtube.Username(text=username)

    subscription_entry = gdata.youtube.YouTubeSubscriptionEntry(
        category=subscription_category,
        username=subscription_username)

    post_uri = YOUTUBE_USER_FEED_URI + 'default/subscriptions'
    return self.Post(subscription_entry, post_uri,
                     converter=gdata.youtube.YouTubeSubscriptionEntryFromString)

  def DeleteSubscription(self, subscription_uri):
    """Delete a subscription from the currently authenticated user's account

    Needs authentication

    Arguments:
        subscription_uri: The uri of a subscription

    Returns:
        True if successfully deleted
    """
    return self.Delete(subscription_uri)

  def AddContact(self, contact_username, my_username='default'):
    """Add a new contact to the currently authenticated user's contact feed.

    Needs authentication

    Arguments:
        contact_username: The username of the contact that you wish to add
        my_username: (optional) The username of the contact feed

    Returns:
        A YouTubeContactEntry if added successfully
    """
    contact_category = atom.Category(
        scheme = 'http://gdata.youtube.com/schemas/2007/contact.cat',
        term = 'Friends')
    contact_username = gdata.youtube.Username(text=contact_username)
    contact_entry = gdata.youtube.YouTubeContactEntry(
        category=contact_category,
        username=contact_username)
    contact_post_uri = YOUTUBE_USER_FEED_URI + my_username + '/contacts'
    return self.Post(contact_entry, contact_post_uri,
                     converter=gdata.youtube.YouTubeContactEntryFromString)

  def UpdateContact(self, contact_username, new_contact_status, 
                    new_contact_category, my_username='default'):
    """Update a contact, providing a new status and a new category

    Needs authentication

    Arguments:
        contact_username: The username of the contact to be updated
        new_contact_status: New status, either 'accepted' or 'rejected'
        new_contact_category: New category for the contact, either 'Friends' or
            'Family'
        my_username: (optional) Username of the user whose contact feed we are 
            modifying. Defaults to the currently authenticated user

    Returns:
        A YouTubeContactEntry if updated succesfully
    """
    if new_contact_status not in YOUTUBE_CONTACT_STATUS:
      raise YouTubeError('New contact status must be one of ' +
                         ' '.join(YOUTUBE_CONTACT_STATUS))
    if new_contact_category not in YOUTUBE_CONTACT_CATEGORY:
      raise YouTubeError('New contact category must be one of ' +
                         ' '.join(YOUTUBE_CONTACT_CATEGORY))

    contact_category = atom.Category(
        scheme='http://gdata.youtube.com/schemas/2007/contact.cat',
        term=new_contact_category)
    contact_status = gdata.youtube.Status(text=new_contact_status)
    contact_entry = gdata.youtube.YouTubeContactEntry(
        category=contact_category,
        status=contact_status)
    contact_put_uri = (YOUTUBE_USER_FEED_URI + my_username + '/contacts/' +
                       contact_id)
    return self.Put(contact_entry, contact_put_uri,
                    converter=gdata.youtube.YouTubeContactEntryFromString)

  def DeleteContact(self, contact_username, my_username='default'):
    """Delete a contact from a users contact feed

    Needs authentication

    Arguments:
        contact_username: Username of the contact to be deleted
        my_username: (optional) Username of the users contact feed that is to 
            be modified. Defaults to the currently authenticated user

    Returns:
        True if the contact was deleted successfully
    """
    contact_edit_uri = (YOUTUBE_USER_FEED_URI + my_username +
                        '/contacts/' + contact_username)
    return self.Delete(contact_edit_uri)


  def _GetDeveloperKey(self):
    """Getter for Developer Key property"""
    if '_developer_key' in self.keys():
      return self._developer_key
    else:
      return None

  def _SetDeveloperKey(self, developer_key):
    """Setter for Developer Key property"""
    self._developer_key = developer_key
    self.additional_headers['X-GData-Key'] = 'key=' + developer_key

  developer_key = property(_GetDeveloperKey, _SetDeveloperKey,
                           doc="""The Developer Key property""")

  def _GetClientId(self):
    """Getter for Client Id property"""
    if '_client_id' in self.keys():
      return self._client_id
    else:
      return None

  def _SetClientId(self, client_id):
    """Setter for Client Id property"""
    self._client_id = client_id
    self.additional_headers['X-Gdata-Client'] = client_id

  client_id = property(_GetClientId, _SetClientId,
                         doc="""The ClientId property""")

  def Query(self, uri):
    """Performs a query and returns a resulting feed or entry.

    Args:
      feed: string The feed which is to be queried

    Returns:
      On success, a tuple in the form
      (boolean succeeded=True, ElementTree._Element result)
      On failure, a tuple in the form
      (boolean succeeded=False, {'status': HTTP status code from server, 
                                 'reason': HTTP reason from the server, 
                                 'body': HTTP body of the server's response})
    """

    result = self.Get(uri)
    return result

  def YouTubeQuery(self, query):
    result = self.Query(query.ToUri())
    if isinstance(query, YouTubeVideoQuery):
      return gdata.youtube.YouTubeVideoFeedFromString(result.ToString())
    elif isinstance(query, YouTubeUserQuery):
      return gdata.youtube.YouTubeUserFeedFromString(result.ToString())
    elif isinstance(query, YouTubePlaylistQuery):
      return gdata.youtube.YouTubePlaylistFeedFromString(result.ToString())
    else:
      return result

class YouTubeVideoQuery(gdata.service.Query):

  def __init__(self, video_id=None, feed_type=None, text_query=None,
               params=None, categories=None):

    if feed_type in YOUTUBE_STANDARDFEEDS:
      feed = 'http://%s/feeds/standardfeeds/%s' % (YOUTUBE_SERVER, feed_type)
    elif feed_type is 'responses' or feed_type is 'comments' and video_id:
      feed = 'http://%s/feeds/videos/%s/%s' % (YOUTUBE_SERVER, video_id,
                                               feed_type)
    else:
      feed = 'http://%s/feeds/videos' % (YOUTUBE_SERVER)

    gdata.service.Query.__init__(self, feed, text_query=text_query,
                                 params=params, categories=categories)

  def _GetStartMin(self):
    if 'start-min' in self.keys():
      return self['start-min']
    else:
      return None

  def _SetStartMin(self, val):
    self['start-min'] = val

  start_min = property(_GetStartMin, _SetStartMin,
                       doc="""The start-min query parameter""")

  def _GetStartMax(self):
    if 'start-max' in self.keys():
      return self['start-max']
    else:
      return None

  def _SetStartMax(self, val):
    self['start-max'] = val

  start_max = property(_GetStartMax, _SetStartMax,
                       doc="""The start-max query parameter""")

  def _GetVideoQuery(self):
    if 'vq' in self.keys():
      return self['vq']
    else:
      return None

  def _SetVideoQuery(self, val):
    self['vq'] = val

  vq = property(_GetVideoQuery, _SetVideoQuery,
                doc="""The video query (vq) query parameter""")

  def _GetOrderBy(self):
    if 'orderby' in self.keys():
      return self['orderby']
    else:
      return None

  def _SetOrderBy(self, val):
    if val not in YOUTUBE_QUERY_VALID_ORDERBY_PARAMETERS:
      raise YouTubeError('OrderBy must be one of: %s ' %
                         ' '.join(YOUTUBE_QUERY_VALID_ORDERBY_PARAMETERS))
    self['orderby'] = val

  orderby = property(_GetOrderBy, _SetOrderBy,
                     doc="""The orderby query parameter""")

  def _GetTime(self):
    if 'time' in self.keys():
      return self['time']
    else:
      return None

  def _SetTime(self, val):
    if val not in YOUTUBE_QUERY_VALID_TIME_PARAMETERS:
      raise YouTubeError('Time must be one of: %s ' % 
                         ' '.join(YOUTUBE_QUERY_VALID_TIME_PARAMETERS))
    self['time'] = val

  time = property(_GetTime, _SetTime,
                  doc="""The time query parameter""")

  def _GetFormat(self):
    if 'format' in self.keys():
      return self['format']
    else:
      return None

  def _SetFormat(self, val):
    if val not in YOUTUBE_QUERY_VALID_FORMAT_PARAMETERS:
      raise YouTubeError('Format must be one of: %s ' % 
                         ' '.join(YOUTUBE_QUERY_VALID_FORMAT_PARAMETERS))
    self['format'] = val

  format = property(_GetFormat, _SetFormat,
                    doc="""The format query parameter""")

  def _GetRacy(self):
    if 'racy' in self.keys():
      return self['racy']
    else:
      return None

  def _SetRacy(self, val):
    if val not in YOUTUBE_QUERY_VALID_RACY_PARAMETERS:
      raise YouTubeError('Racy must be one of: %s ' % 
                         ' '.join(YOUTUBE_QUERY_VALID_RACY_PARAMETERS))
    self['racy'] = val

  racy = property(_GetRacy, _SetRacy, 
                  doc="""The racy query parameter""")

class YouTubeUserQuery(YouTubeVideoQuery):

  def __init__(self, username=None, feed_type=None, subscription_id=None,
               text_query=None, params=None, categories=None):

    uploads_favorites_playlists = ('uploads', 'favorites', 'playlists')

    if feed_type is 'subscriptions' and subscription_id and username:
      feed = "http://%s/feeds/users/%s/%s/%s" % (
          YOUTUBE_SERVER, username, feed_type, subscription_id)
    elif feed_type is 'subscriptions' and not subscription_id and username:
      feed = "http://%s/feeds/users/%s/%s" % (
          YOUTUBE_SERVER, username, feed_type)
    elif feed_type in uploads_favorites_playlists:
      feed = "http://%s/feeds/users/%s/%s" % (
          YOUTUBE_SERVER, username, feed_type)
    else:
      feed = "http://%s/feeds/users" % (YOUTUBE_SERVER)

    YouTubeVideoQuery.__init__(self, feed, text_query=text_query,
                               params=params, categories=categories)


class YouTubePlaylistQuery(YouTubeVideoQuery):

  def __init__(self, playlist_id, text_query=None, params=None,
               categories=None):
    if playlist_id:
      feed = "http://%s/feeds/playlists/%s" % (YOUTUBE_SERVER, playlist_id)
    else:
      feed = "http://%s/feeds/playlists" % (YOUTUBE_SERVER)

    YouTubeVideoQuery.__init__(self, feed, text_query=text_query,
                               params=params, categories=categories)
