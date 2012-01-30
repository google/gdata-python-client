# -*- coding: utf-8 -*-
"""
Copyright (c) 2008, appengine-utilities project
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
- Neither the name of the appengine-utilities project nor the names of its
  contributors may be used to endorse or promote products derived from this
  software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# main python imports
import datetime
import pickle
import random
import sys

# google appengine import
from google.appengine.ext import db
from google.appengine.api import memcache

# settings
try:
    import settings_default
    import settings

    if settings.__name__.rsplit('.', 1)[0] != settings_default.__name__.rsplit('.', 1)[0]:
        settings = settings_default
except:
    settings = settings_default
    
class _AppEngineUtilities_Cache(db.Model):
    cachekey = db.StringProperty()
    createTime = db.DateTimeProperty(auto_now_add=True)
    timeout = db.DateTimeProperty()
    value = db.BlobProperty()


class Cache(object):
    """
    Cache is used for storing pregenerated output and/or objects in the Big
    Table datastore to minimize the amount of queries needed for page
    displays. The idea is that complex queries that generate the same
    results really should only be run once. Cache can be used to store
    pregenerated value made from queries (or other calls such as
    urlFetch()), or the query objects themselves.

    Cache is a standard dictionary object and can be used as such. It attesmpts
    to store data in both memcache, and the datastore. However, should a
    datastore write fail, it will not try again. This is for performance
    reasons.
    """

    def __init__(self, clean_check_percent = settings.cache["CLEAN_CHECK_PERCENT"],
      max_hits_to_clean = settings.cache["MAX_HITS_TO_CLEAN"],
        default_timeout = settings.cache["DEFAULT_TIMEOUT"]):
        """
        Initializer

        Args:
            clean_check_percent: how often cache initialization should
                run the cache cleanup
            max_hits_to_clean: maximum number of stale hits to clean
            default_timeout: default length a cache item is good for
        """
        self.clean_check_percent = clean_check_percent
        self.max_hits_to_clean = max_hits_to_clean
        self.default_timeout = default_timeout

        if random.randint(1, 100) < self.clean_check_percent:
            try:
                self._clean_cache()
            except:
                pass

        if 'AEU_Events' in sys.modules['__main__'].__dict__:
            sys.modules['__main__'].AEU_Events.fire_event('cacheInitialized')

    def _clean_cache(self):
        """
        _clean_cache is a routine that is run to find and delete cache
        items that are old. This helps keep the size of your over all
        datastore down.

        It only deletes the max_hits_to_clean per attempt, in order
        to maximize performance. Default settings are 20 hits, 50%
        of requests. Generally less hits cleaned on more requests will
        give you better performance.

        Returns True on completion
        """
        query = _AppEngineUtilities_Cache.all()
        query.filter('timeout < ', datetime.datetime.now())
        results = query.fetch(self.max_hits_to_clean)
        db.delete(results)

        return True

    def _validate_key(self, key):
        """
        Internal method for key validation. This can be used by a superclass
        to introduce more checks on key names.
        
        Args:
            key: Key name to check

        Returns True is key is valid, otherwise raises KeyError.
        """
        if key == None:
            raise KeyError
        return True

    def _validate_value(self, value):
        """
        Internal method for value validation. This can be used by a superclass
        to introduce more checks on key names.

        Args:
            value: value to check

        Returns True is value is valid, otherwise raises ValueError.
        """
        if value == None:
            raise ValueError
        return True

    def _validate_timeout(self, timeout):
        """
        Internal method to validate timeouts. If no timeout
        is passed, then the default_timeout is used.

        Args:
            timeout: datetime.datetime format

        Returns the timeout
        """
        if timeout == None:
            timeout = datetime.datetime.now() +\
            datetime.timedelta(seconds=self.default_timeout)
        if type(timeout) == type(1):
            timeout = datetime.datetime.now() + \
                datetime.timedelta(seconds = timeout)
        if type(timeout) != datetime.datetime:
            raise TypeError
        if timeout < datetime.datetime.now():
            raise ValueError

        return timeout

    def add(self, key = None, value = None, timeout = None):
        """
        Adds an entry to the cache, if one does not already exist. If they key
        already exists, KeyError will be raised.

        Args:
            key: Key name of the cache object
            value: Value of the cache object
            timeout: timeout value for the cache object.

        Returns the cache object.
        """
        self._validate_key(key)
        self._validate_value(value)
        timeout = self._validate_timeout(timeout)

        if key in self:
            raise KeyError

        cacheEntry = _AppEngineUtilities_Cache()
        cacheEntry.cachekey = key
        cacheEntry.value = pickle.dumps(value)
        cacheEntry.timeout = timeout

        # try to put the entry, if it fails silently pass
        # failures may happen due to timeouts, the datastore being read
        # only for maintenance or other applications. However, cache
        # not being able to write to the datastore should not
        # break the application
        try:
            cacheEntry.put()
        except:
            pass

        memcache_timeout = timeout - datetime.datetime.now()
        memcache.set('cache-%s' % (key), value, int(memcache_timeout.seconds))

        if 'AEU_Events' in sys.modules['__main__'].__dict__:
            sys.modules['__main__'].AEU_Events.fire_event('cacheAdded')

        return self.get(key)

    def set(self, key = None, value = None, timeout = None):
        """
        Sets an entry to the cache, overwriting an existing value
        if one already exists.

        Args:
            key: Key name of the cache object
            value: Value of the cache object
            timeout: timeout value for the cache object.

        Returns the cache object.
        """
        self._validate_key(key)
        self._validate_value(value)
        timeout = self._validate_timeout(timeout)

        cacheEntry = self._read(key)
        if not cacheEntry:
            cacheEntry = _AppEngineUtilities_Cache()
            cacheEntry.cachekey = key
        cacheEntry.value = pickle.dumps(value)
        cacheEntry.timeout = timeout

        try:
            cacheEntry.put()
        except:
            pass

        memcache_timeout = timeout - datetime.datetime.now()
        memcache.set('cache-%s' % (key), value, int(memcache_timeout.seconds))

        if 'AEU_Events' in sys.modules['__main__'].__dict__:
            sys.modules['__main__'].AEU_Events.fire_event('cacheSet')

        return value

    def _read(self, key = None):
        """
        _read is an internal method that will get the cache entry directly
        from the datastore, and return the entity. This is used for datastore
        maintenance within the class.

        Args:
            key: The key to retrieve

        Returns the cache entity
        """
        query = _AppEngineUtilities_Cache.all()
        query.filter('cachekey', key)
        query.filter('timeout > ', datetime.datetime.now())
        results = query.fetch(1)
        if len(results) is 0:
            return None

        if 'AEU_Events' in sys.modules['__main__'].__dict__:
            sys.modules['__main__'].AEU_Events.fire_event('cacheReadFromDatastore')
        if 'AEU_Events' in sys.modules['__main__'].__dict__:
            sys.modules['__main__'].AEU_Events.fire_event('cacheRead')

        return results[0]

    def delete(self, key = None):
        """
        Deletes a cache object.

        Args:
            key: The key of the cache object to delete.

        Returns True.
        """
        memcache.delete('cache-%s' % (key))
        result = self._read(key)
        if result:
            if 'AEU_Events' in sys.modules['__main__'].__dict__:
                sys.modules['__main__'].AEU_Events.fire_event('cacheDeleted')
            result.delete()
        return True

    def get(self, key):
        """
        Used to return the cache value associated with the key passed.

        Args:
            key: The key of the value to retrieve.

        Returns the value of the cache item.
        """
        mc = memcache.get('cache-%s' % (key))
        if mc:
            if 'AEU_Events' in sys.modules['__main__'].__dict__:
                sys.modules['__main__'].AEU_Events.fire_event('cacheReadFromMemcache')
            if 'AEU_Events' in sys.modules['__main__'].__dict__:
                sys.modules['__main__'].AEU_Events.fire_event('cacheRead')
            return mc
        result = self._read(key)
        if result:
            timeout = result.timeout - datetime.datetime.now()
            memcache.set('cache-%s' % (key), pickle.loads(result.value),
               int(timeout.seconds))
            if 'AEU_Events' in sys.modules['__main__'].__dict__:
                sys.modules['__main__'].AEU_Events.fire_event('cacheRead')
            return pickle.loads(result.value)
        else:
            raise KeyError

    def get_many(self, keys):
        """
        Returns a dict mapping each key in keys to its value. If the given
        key is missing, it will be missing from the response dict.

        Args:
            keys: A list of keys to retrieve.

        Returns a dictionary of key/value pairs.
        """
        dict = {}
        for key in keys:
            value = self.get(key)
            if value is not None:
                dict[key] = value
        return dict

    def __getitem__(self, key):
        """
        __getitem__ is necessary for this object to emulate a container.
        """
        return self.get(key)

    def __setitem__(self, key, value):
        """
        __setitem__ is necessary for this object to emulate a container.
        """
        return self.set(key, value)

    def __delitem__(self, key):
        """
        Implement the 'del' keyword
        """
        return self.delete(key)

    def __contains__(self, key):
        """
        Implements "in" operator
        """
        try:
            self.__getitem__(key)
        except KeyError:
            return False
        return True

    def has_key(self, keyname):
        """
        Equivalent to k in a, use that form in new code
        """
        return self.__contains__(keyname)
