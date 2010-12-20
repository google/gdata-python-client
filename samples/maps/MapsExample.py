#!/usr/bin/python
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


__author__ = 'api.roman.public@gmail.com (Roman Nurik)'


import gdata.maps.client
import gdata.client
import gdata.sample_util
import gdata.data
import atom.data


class MapsExample:

  def __init__(self):
    """Creates a GDataService and provides ClientLogin auth details to it."""

    # Authenticate using ClientLogin, AuthSub, or OAuth.
    self.client = gdata.maps.client.MapsClient()
    #self.client.http_client.debug = True
    gdata.sample_util.authorize_client(
        self.client, service='local', source='MapsData_Python_Sample-2.0',
        scopes=['http://maps.google.com/maps/feeds/'])

  def PrintAllMaps(self):
    """Prints a list of all the user's maps."""

    # Request the feed.
    feed = self.client.get_maps()

    # Print the results.
    print feed.title.text
    for entry in feed.entry:
      print "\t%s (map id=%s)" % (entry.title.text, entry.get_map_id())
    print

  def CreateMap(self, title, description, is_unlisted):
    """Creates a new map."""
    return self.client.create_map(title, description, unlisted=is_unlisted)

  def CreateFeature(self, map_id, title, content):
    """Adds a feature with the given title and content to the map."""
    return self.client.add_feature(map_id, title, content)

  def PrintAllFeatures(self, map_id):
    """Displays all features in a map."""

    # Request the feed.
    feed = self.client.get_features(map_id)

    # Print the results.
    print feed.title.text
    for entry in feed.entry:      
      if not entry.title.text:
        print "\tNo Title"
      else:
        print "\t%s (feature id=%s)" % (entry.title.text.encode('utf-8'),
                                        entry.get_feature_id())
    print

  def UpdateMapTitle(self, entry_to_update, new_title):
    """Updates the title of the given entry.
    
    If the insertion is successful, the updated feature will be returned.
    """
    
    # Set the new title in the Entry object
    entry_to_update.title = atom.data.Title(type='text', text=new_title)
    return self.client.update(entry_to_update)

  def DeleteFeature(self, feature_entry):
    """Removes the feature specified by the given edit_link_href."""

    self.client.delete(feature_entry)

  def DeleteMap(self, map_entry):
    """Removes the map specified by the given edit_link_href."""

    self.client.delete(map_entry)
  
  def run(self):
    """Runs each of the example methods defined above, demonstrating how to
    interface with the Maps Data service.
    """

    # Demonstrate retrieving a list of the user's maps.
    self.PrintAllMaps()

    # Demonstrate how to create an unlisted map.
    unlisted_map = self.CreateMap('Whoa an unlisted map', 'a description',
                                  is_unlisted=True)
    print 'Successfully created unlisted map: %s' % unlisted_map.title.text

    # Delete the unlisted map.
    self.client.delete(unlisted_map)
  
    # Demonstrate how to publish a public map.
    public_map = self.CreateMap('Some cool new public map', 'a description',
                                is_unlisted=False)
    print "Successfully created unlisted map: %s" % public_map.title.text

    # Demonstrate updating a map's title.
    print "Now updating the title of the map we just created:"
    public_map = self.UpdateMapTitle(public_map, 'GData sample public map')
    print "Successfully changed the map's title to: %s" % public_map.title.text
  
    # Demonstrate how to retrieve the features for a map.

    # Get the map ID and build the feature feed URI for the specified map
    map_id = public_map.get_map_id()
    
    print "Now adding a feature to the map titled: %s" % public_map.title.text
    feature = self.CreateFeature(map_id, "A point feature",
        '<Placemark><description>Hello there!</description>'
        '<Point><coordinates>-122,37</coordinates></Point></Placemark>')
    print ("Successfully created feature '%s' on the map titled '%s'"
           % (feature.title.text, public_map.title.text))
    
    feature_id = feature.get_feature_id()
    
    print "Now printing all features"
    self.PrintAllFeatures(map_id)
   
    # Delete the feature we just added
    print "Now deleting the feature we just added"
    self.DeleteFeature(feature)
    print "Successfully deleted feature." 
    self.PrintAllFeatures(map_id)

    # Demonstrate deleting maps.
    print "Now deleting the map titled: %s" % public_map.title.text
    self.DeleteMap(public_map)
    print "Successfully deleted map." 
    self.PrintAllMaps()


def main():
  """The main function runs the MapsExample application.
  
  NOTE:  It is recommended that you run this sample using a test account.
  """
  sample = MapsExample()
  sample.run()


if __name__ == '__main__':
  main()
