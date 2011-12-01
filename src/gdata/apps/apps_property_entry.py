#!/usr/bin/python2.4
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generic class for Set/Get properties of GData Provisioning clients."""


__author__ = 'Gunjan Sharma <gunjansharma@google.com>'


import gdata.apps
import gdata.apps_property
import gdata.data


class AppsPropertyEntry(gdata.data.GDEntry):
  """Represents a  generic entry in object form."""

  property = [gdata.apps_property.AppsProperty]

  def _GetProperty(self, name):
    """Get the apps:property value with the given name.

    Args:
      name: string Name of the apps:property value to get.

    Returns:
      The apps:property value with the given name, or None if the name was
          invalid.
    """
    value = None
    for p in self.property:
      if p.name == name:
        value = p.value
        break
    return value

  def _SetProperty(self, name, value):
    """Set the apps:property value with the given name to the given value.

    Args:
      name: string Name of the apps:property value to set.
      value: string Value to give the apps:property value with the given name.
    """
    found = False
    for i in range(len(self.property)):
      if self.property[i].name == name:
        self.property[i].value = value
        found = True
        break
    if not found:
      self.property.append(
          gdata.apps_property.AppsProperty(name=name, value=value))
