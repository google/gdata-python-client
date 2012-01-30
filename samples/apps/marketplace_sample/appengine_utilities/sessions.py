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
import os
import time
import datetime
import random
import hashlib
import Cookie
import pickle
import sys
import logging
from time import strftime

# google appengine imports
from google.appengine.ext import db
from google.appengine.api import memcache

from django.utils import simplejson

# settings
try:
    import settings_default
    import settings

    if settings.__name__.rsplit('.', 1)[0] != settings_default.__name__.rsplit('.', 1)[0]:
        settings = settings_default
except:
    settings = settings_default




class _AppEngineUtilities_Session(db.Model):
    """
    Model for the sessions in the datastore. This contains the identifier and
    validation information for the session.
    """

    sid = db.StringListProperty()
    ip = db.StringProperty()
    ua = db.StringProperty()
    last_activity = db.DateTimeProperty()
    dirty = db.BooleanProperty(default=False)
    working = db.BooleanProperty(default=False)
    deleted = db.BooleanProperty(default=False) 

    def put(self):
        """
        Extends put so that it writes vaules to memcache as well as the
        datastore, and keeps them in sync, even when datastore writes fails.

        Returns the session object.
        """
        try:
            memcache.set(u"_AppEngineUtilities_Session_%s" % \
                (str(self.key())), self)
        except:
            # new session, generate a new key, which will handle the
            # put and set the memcache
            db.put(self)

        self.last_activity = datetime.datetime.now()

        try:
            self.dirty = False
            db.put(self)
            memcache.set(u"_AppEngineUtilities_Session_%s" % \
                (str(self.key())), self)
        except:
            self.dirty = True
            memcache.set(u"_AppEngineUtilities_Session_%s" % \
                (str(self.key())), self)

        return self

    @classmethod
    def get_session(cls, session_obj=None):
        """
        Uses the passed objects sid to get a session object from memcache,
        or datastore if a valid one exists.

        Args:
            session_obj: a session object

        Returns a validated session object.
        """
        if session_obj.sid == None:
            return None
        session_key = session_obj.sid.split(u'_')[0]
        session = memcache.get(u"_AppEngineUtilities_Session_%s" % \
            (str(session_key)))
        if session:
            if session.deleted == True:
                session.delete()
                return None
            if session.dirty == True and session.working != False:
                # the working bit is used to make sure multiple requests,
                # which can happen with ajax oriented sites, don't try to put
                # at the same time
                session.working = True
                memcache.set(u"_AppEngineUtilities_Session_%s" % \
                    (str(session_key)), session)
                session.put()
            if session_obj.sid in session.sid:
                sessionAge = datetime.datetime.now() - session.last_activity
                if sessionAge.seconds > session_obj.session_expire_time:
                    session.delete()
                    return None
                return session
            else:
                return None
 
        # Not in memcache, check datastore
        
        ds_session = db.get(str(session_key))
        if ds_session:
          sessionAge = datetime.datetime.now() - ds_session.last_activity
          if sessionAge.seconds > session_obj.session_expire_time:
              ds_session.delete()
              return None
          memcache.set(u"_AppEngineUtilities_Session_%s" % \
              (str(session_key)), ds_session)
          memcache.set(u"_AppEngineUtilities_SessionData_%s" % \
              (str(session_key)), ds_session.get_items_ds())
        return ds_session


    def get_items(self):
        """
        Returns all the items stored in a session. Queries memcache first
        and will try the datastore next.
        """
        items = memcache.get(u"_AppEngineUtilities_SessionData_%s" % \
            (str(self.key())))
        if items:
            for item in items:
                if item.deleted == True:
                    item.delete()
                    items.remove(item)
            return items

        query = _AppEngineUtilities_SessionData.all()
        query.filter(u"session", self)
        results = query.fetch(1000)
        return results

    def get_item(self, keyname = None):
        """
        Returns a single session data item from the memcache or datastore

        Args:
            keyname: keyname of the session data object

        Returns the session data object if it exists, otherwise returns None
        """
        mc = memcache.get(u"_AppEngineUtilities_SessionData_%s" % \
            (str(self.key())))
        if mc:
            for item in mc:
                if item.keyname == keyname:
                    if item.deleted == True:
                        item.delete()
                        return None
                    return item
        query = _AppEngineUtilities_SessionData.all()
        query.filter(u"session = ", self)
        query.filter(u"keyname = ", keyname)
        results = query.fetch(1)
        if len(results) > 0:
            memcache.set(u"_AppEngineUtilities_SessionData_%s" % \
                (str(self.key())), self.get_items_ds())
            return results[0]
        return None

    def get_items_ds(self):
        """
        This gets all session data objects from the datastore, bypassing
        memcache.

        Returns a list of session data entities.
        """
        query = _AppEngineUtilities_SessionData.all()
        query.filter(u"session", self)
        results = query.fetch(1000)
        return results

    def delete(self):
        """
        Deletes a session and all it's associated data from the datastore and
        memcache.

        Returns True
        """
        try:
            query = _AppEngineUtilities_SessionData.all()
            query.filter(u"session = ", self)
            results = query.fetch(1000)
            db.delete(results)
            db.delete(self)
            memcache.delete_multi([u"_AppEngineUtilities_Session_%s" % \
                (str(self.key())), \
                u"_AppEngineUtilities_SessionData_%s" % \
                (str(self.key()))])
        except:
            mc = memcache.get(u"_AppEngineUtilities_Session_%s" %+ \
                (str(self.key())))
            if mc:
                mc.deleted = True
            else:
                # not in the memcache, check to see if it should be
                query = _AppEngineUtilities_Session.all()
                query.filter(u"sid = ", self.sid)
                results = query.fetch(1)
                if len(results) > 0:
                    results[0].deleted = True
                    memcache.set(u"_AppEngineUtilities_Session_%s" % \
                        (unicode(self.key())), results[0])
        return True
            
class _AppEngineUtilities_SessionData(db.Model):
    """
    Model for the session data in the datastore.
    """

    # session_key = db.FloatProperty()
    keyname = db.StringProperty()
    content = db.BlobProperty()
    model = db.ReferenceProperty()
    session = db.ReferenceProperty(_AppEngineUtilities_Session)
    dirty = db.BooleanProperty(default=False)
    deleted = db.BooleanProperty(default=False)

    def put(self):
        """
        Adds a keyname/value for session to the datastore and memcache

        Returns the key from the datastore put or u"dirty"
        """
        # update or insert in datastore
        try:
            return_val = db.put(self)
            self.dirty = False
        except:
            return_val = u"dirty"
            self.dirty = True

        # update or insert in memcache
        mc_items = memcache.get(u"_AppEngineUtilities_SessionData_%s" % \
            (str(self.session.key())))
        if mc_items:
            value_updated = False
            for item in mc_items:
                if value_updated == True:
                    break
                if item.keyname == self.keyname:
                    item.content = self.content
                    item.model = self.model
                    memcache.set(u"_AppEngineUtilities_SessionData_%s" % \
                        (str(self.session.key())), mc_items)
                    value_updated = True
                    break
            if value_updated == False:
                mc_items.append(self)
                memcache.set(u"_AppEngineUtilities_SessionData_%s" % \
                    (str(self.session.key())), mc_items)
        return return_val

    def delete(self):
        """
        Deletes an entity from the session in memcache and the datastore

        Returns True
        """
        try:
            db.delete(self)
        except:
            self.deleted = True
        mc_items = memcache.get(u"_AppEngineUtilities_SessionData_%s" % \
            (str(self.session.key())))
        value_handled = False
        for item in mc_items:
            if value_handled == True:
                break
            if item.keyname == self.keyname:
                if self.deleted == True:
                    item.deleted = True
                else:
                    mc_items.remove(item)
                memcache.set(u"_AppEngineUtilities_SessionData_%s" % \
                    (str(self.session.key())), mc_items)
        return True
        

class _DatastoreWriter(object):

    def put(self, keyname, value, session):
        """
        Insert a keyname/value pair into the datastore for the session.

        Args:
            keyname: The keyname of the mapping.
            value: The value of the mapping.

        Returns the model entity key
        """
        keyname = session._validate_key(keyname)
        if value is None:
            raise ValueError(u"You must pass a value to put.")

        # datestore write trumps cookie. If there is a cookie value
        # with this keyname, delete it so we don't have conflicting
        # entries.
        if session.cookie_vals.has_key(keyname):
            del(session.cookie_vals[keyname])
            session.output_cookie["%s_data" % (session.cookie_name)] = \
                simplejson.dumps(session.cookie_vals)
            session.output_cookie["%s_data" % (session.cookie_name)]["path"] = \
                session.cookie_path
            if session.cookie_domain:
                session.output_cookie["%s_data" % \
                    (session.cookie_name)]["domain"] = session.cookie_domain
            print session.output_cookie.output()

        sessdata = session._get(keyname=keyname)
        if sessdata is None:
            sessdata = _AppEngineUtilities_SessionData()
            # sessdata.session_key = session.session.key()
            sessdata.keyname = keyname
        try:
            db.model_to_protobuf(value)
            if not value.is_saved():
                value.put()
            sessdata.model = value
        except:
            sessdata.content = pickle.dumps(value)
            sessdata.model = None
        sessdata.session = session.session
            
        session.cache[keyname] = value
        return sessdata.put()


class _CookieWriter(object):
    def put(self, keyname, value, session):
        """
        Insert a keyname/value pair into the datastore for the session.

        Args:
            keyname: The keyname of the mapping.
            value: The value of the mapping.

        Returns True
        """
        keyname = session._validate_key(keyname)
        if value is None:
            raise ValueError(u"You must pass a value to put.")

        # Use simplejson for cookies instead of pickle.
        session.cookie_vals[keyname] = value
        # update the requests session cache as well.
        session.cache[keyname] = value
        # simplejson will raise any error I'd raise about an invalid value
        # so let it raise exceptions
        session.output_cookie["%s_data" % (session.cookie_name)] = \
            simplejson.dumps(session.cookie_vals)
        session.output_cookie["%s_data" % (session.cookie_name)]["path"] = \
            session.cookie_path
        if session.cookie_domain:
            session.output_cookie["%s_data" % \
                (session.cookie_name)]["domain"] = session.cookie_domain
        print session.output_cookie.output()
        return True

class Session(object):
    """
    Sessions are used to maintain user presence between requests.

    Sessions can either be stored server side in the datastore/memcache, or
    be kept entirely as cookies. This is set either with the settings file
    or on initialization, using the writer argument/setting field. Valid
    values are "datastore" or "cookie".

    Session can be used as a standard dictionary object.
        session = appengine_utilities.sessions.Session()
        session["keyname"] = "value" # sets keyname to value
        print session["keyname"] # will print value

    Datastore Writer:
        The datastore writer was written with the focus being on security,
        reliability, and performance. In that order.

        It is based off of a session token system. All data is stored
        server side in the datastore and memcache. A token is given to
        the browser, and stored server side. Optionally (and on by default),
        user agent and ip checking is enabled. Tokens have a configurable
        time to live (TTL), which defaults to 5 seconds. The current token,
        plus the previous 2, are valid for any request. This is done in order
        to manage ajax enabled sites which may have more than on request
        happening at a time. This means any token is valid for 15 seconds.
        A request with a token who's TTL has passed will have a new token
        generated.

        In order to take advantage of the token system for an authentication
        system, you will want to tie sessions to accounts, and make sure
        only one session is valid for an account. You can do this by setting
        a db.ReferenceProperty(_AppEngineUtilities_Session) attribute on
        your user Model, and use the get_ds_entity() method on a valid
        session to populate it on login.

        Note that even with this complex system, sessions can still be hijacked
        and it will take the user logging in to retrieve the account. In the
        future an ssl only cookie option may be implemented for the datastore
        writer, which would further protect the session token from being
        sniffed, however it would be restricted to using cookies on the
        .appspot.com domain, and ssl requests are a finite resource. This is
        why such a thing is not currently implemented.

        Session data objects are stored in the datastore pickled, so any
        python object is valid for storage.

    Cookie Writer:
        Sessions using the cookie writer are stored entirely in the browser
        and no interaction with the datastore is required. This creates
        a drastic improvement in performance, but provides no security for
        session hijack. This is useful for requests where identity is not
        important, but you wish to keep state between requests.

        Information is stored in a json format, as pickled data from the
        server is unreliable.

        Note: There is no checksum validation of session data on this method,
        it's streamlined for pure performance. If you need to make sure data
        is not tampered with, use the datastore writer which stores the data
        server side.

    django-middleware:
        Included with the GAEUtilties project is a
        django-middleware.middleware.SessionMiddleware which can be included in
        your settings file. This uses the cookie writer for anonymous requests,
        and you can switch to the datastore writer on user login. This will
        require an extra set in your login process of calling
        request.session.save() once you validated the user information. This
        will convert the cookie writer based session to a datastore writer.
    """

    # cookie name declaration for class methods
    COOKIE_NAME = settings.session["COOKIE_NAME"]

    def __init__(self, cookie_path=settings.session["DEFAULT_COOKIE_PATH"],
            cookie_domain=settings.session["DEFAULT_COOKIE_DOMAIN"],
            cookie_name=settings.session["COOKIE_NAME"],
            session_expire_time=settings.session["SESSION_EXPIRE_TIME"],
            clean_check_percent=settings.session["CLEAN_CHECK_PERCENT"],
            integrate_flash=settings.session["INTEGRATE_FLASH"],
            check_ip=settings.session["CHECK_IP"],
            check_user_agent=settings.session["CHECK_USER_AGENT"],
            set_cookie_expires=settings.session["SET_COOKIE_EXPIRES"],
            session_token_ttl=settings.session["SESSION_TOKEN_TTL"],
            last_activity_update=settings.session["UPDATE_LAST_ACTIVITY"],
            writer=settings.session["WRITER"]):
        """
        Initializer

        Args:
          cookie_path: The path setting for the cookie.
          cookie_domain: The domain setting for the cookie. (Set to False
                        to not use)
          cookie_name: The name for the session cookie stored in the browser.
          session_expire_time: The amount of time between requests before the
              session expires.
          clean_check_percent: The percentage of requests the will fire off a
              cleaning routine that deletes stale session data.
          integrate_flash: If appengine-utilities flash utility should be
              integrated into the session object.
          check_ip: If browser IP should be used for session validation
          check_user_agent: If the browser user agent should be used for
              sessoin validation.
          set_cookie_expires: True adds an expires field to the cookie so
              it saves even if the browser is closed.
          session_token_ttl: Number of sessions a session token is valid
              for before it should be regenerated.
        """

        self.cookie_path = cookie_path
        self.cookie_domain = cookie_domain
        self.cookie_name = cookie_name
        self.session_expire_time = session_expire_time
        self.integrate_flash = integrate_flash
        self.check_user_agent = check_user_agent
        self.check_ip = check_ip
        self.set_cookie_expires = set_cookie_expires
        self.session_token_ttl = session_token_ttl
        self.last_activity_update = last_activity_update
        self.writer = writer

        # make sure the page is not cached in the browser
        print self.no_cache_headers()
        # Check the cookie and, if necessary, create a new one.
        self.cache = {}
        string_cookie = os.environ.get(u"HTTP_COOKIE", u"")
        self.cookie = Cookie.SimpleCookie()
        self.output_cookie = Cookie.SimpleCookie()
        if string_cookie == "":
          self.cookie_vals = {}
        else:
            self.cookie.load(string_cookie)
            try:
                self.cookie_vals = \
                    simplejson.loads(self.cookie["%s_data" % (self.cookie_name)].value)
                    # sync self.cache and self.cookie_vals which will make those
                    # values available for all gets immediately.
                for k in self.cookie_vals:
                    self.cache[k] = self.cookie_vals[k]
                    # sync the input cookie with the output cookie
                    self.output_cookie["%s_data" % (self.cookie_name)] = \
                        simplejson.dumps(self.cookie_vals) #self.cookie["%s_data" % (self.cookie_name)]
            except Exception, e:
                self.cookie_vals = {}


        if writer == "cookie":
            pass
        else:
            self.sid = None
            new_session = True

            # do_put is used to determine if a datastore write should
            # happen on this request.
            do_put = False

            # check for existing cookie
            if self.cookie.get(cookie_name):
                self.sid = self.cookie[cookie_name].value
                # The following will return None if the sid has expired.
                self.session = _AppEngineUtilities_Session.get_session(self)
                if self.session:
                    new_session = False

            if new_session:
                # start a new session
                self.session = _AppEngineUtilities_Session()
                self.session.put()
                self.sid = self.new_sid()
                if u"HTTP_USER_AGENT" in os.environ:
                    self.session.ua = os.environ[u"HTTP_USER_AGENT"]
                else:
                    self.session.ua = None
                if u"REMOTE_ADDR" in os.environ:
                    self.session.ip = os.environ["REMOTE_ADDR"]
                else:
                    self.session.ip = None
                self.session.sid = [self.sid]
                # do put() here to get the session key
                self.session.put()
            else:
                # check the age of the token to determine if a new one
                # is required
                duration = datetime.timedelta(seconds=self.session_token_ttl)
                session_age_limit = datetime.datetime.now() - duration
                if self.session.last_activity < session_age_limit:
                    self.sid = self.new_sid()
                    if len(self.session.sid) > 2:
                        self.session.sid.remove(self.session.sid[0])
                    self.session.sid.append(self.sid)
                    do_put = True
                else:
                    self.sid = self.session.sid[-1]
                    # check if last_activity needs updated
                    ula = datetime.timedelta(seconds=self.last_activity_update)
                    if datetime.datetime.now() > self.session.last_activity + \
                        ula:
                        do_put = True

            self.output_cookie[cookie_name] = self.sid
            self.output_cookie[cookie_name]["path"] = self.cookie_path
            if self.cookie_domain:
                self.output_cookie[cookie_name]["domain"] = self.cookie_domain
            if self.set_cookie_expires:
                self.output_cookie[cookie_name]["expires"] = \
                    self.session_expire_time

            self.cache[u"sid"] = self.sid

            if do_put:
                if self.sid != None or self.sid != u"":
                    self.session.put()

        if self.set_cookie_expires:
            if not self.output_cookie.has_key("%s_data" % (cookie_name)):
                self.output_cookie["%s_data" % (cookie_name)] = u""
            self.output_cookie["%s_data" % (cookie_name)]["expires"] = \
                self.session_expire_time
        print self.output_cookie.output()

        # fire up a Flash object if integration is enabled
        if self.integrate_flash:
            import flash
            self.flash = flash.Flash(cookie=self.cookie)

        # randomly delete old stale sessions in the datastore (see
        # CLEAN_CHECK_PERCENT variable)
        if random.randint(1, 100) < clean_check_percent:
            self._clean_old_sessions() 

    def new_sid(self):
        """
        Create a new session id.

        Returns session id as a unicode string.
        """
        sid = u"%s_%s" % (str(self.session.key()),
            hashlib.md5(repr(time.time()) + \
            unicode(random.random())).hexdigest()
        )
        #sid = unicode(self.session.session_key) + "_" + \
        #        hashlib.md5(repr(time.time()) + \
        #        unicode(random.random())).hexdigest()
        return sid

    def _get(self, keyname=None):
        """
        private method
        
        Return all of the SessionData object data from the datastore only,
        unless keyname is specified, in which case only that instance of 
        SessionData is returned.

        Important: This does not interact with memcache and pulls directly
        from the datastore. This also does not get items from the cookie
        store.

        Args:
            keyname: The keyname of the value you are trying to retrieve.

        Returns a list of datastore entities.
        """
        if hasattr(self, 'session'):
            if keyname != None:
                return self.session.get_item(keyname)
            return self.session.get_items()
        return None
    
    def _validate_key(self, keyname):
        """
        private method
        
        Validate the keyname, making sure it is set and not a reserved name.

        Returns the validated keyname.
        """
        if keyname is None:
            raise ValueError(
                u"You must pass a keyname for the session data content."
            )
        elif keyname in (u"sid", u"flash"):
            raise ValueError(u"%s is a reserved keyname." % keyname)

        if type(keyname) != type([str, unicode]):
            return unicode(keyname)
        return keyname

    def _put(self, keyname, value):
        """
        Insert a keyname/value pair into the datastore for the session.

        Args:
            keyname: The keyname of the mapping.
            value: The value of the mapping.

        Returns the value from the writer put operation, varies based on writer.
        """
        if self.writer == "datastore":
            writer = _DatastoreWriter()
        else:
            writer = _CookieWriter()

        return writer.put(keyname, value, self)

    def _delete_session(self):
        """
        private method
        
        Delete the session and all session data.

        Returns True.
        """
        # if the event class has been loaded, fire off the preSessionDelete event
        if u"AEU_Events" in sys.modules['__main__'].__dict__:
            sys.modules['__main__'].AEU_Events.fire_event(u"preSessionDelete")
        if hasattr(self, u"session"):
            self.session.delete()
        self.cookie_vals = {}
        self.cache = {}
        self.output_cookie["%s_data" % (self.cookie_name)] = \
            simplejson.dumps(self.cookie_vals)
        self.output_cookie["%s_data" % (self.cookie_name)]["path"] = \
            self.cookie_path
        if self.cookie_domain:
            self.output_cookie["%s_data" % \
                (self.cookie_name)]["domain"] = self.cookie_domain

        print self.output_cookie.output()
        # if the event class has been loaded, fire off the sessionDelete event
        if u"AEU_Events" in sys.modules['__main__'].__dict__:
            sys.modules['__main__'].AEU_Events.fire_event(u"sessionDelete")
        return True

    def delete(self):
        """
        Delete the current session and start a new one.

        This is useful for when you need to get rid of all data tied to a
        current session, such as when you are logging out a user.

        Returns True
        """
        self._delete_session()

    @classmethod
    def delete_all_sessions(cls):
        """
        Deletes all sessions and session data from the data store. This
        does not delete the entities from memcache (yet). Depending on the
        amount of sessions active in your datastore, this request could
        timeout before completion and may have to be called multiple times.

        NOTE: This can not delete cookie only sessions as it has no way to
        access them. It will only delete datastore writer sessions.

        Returns True on completion.
        """
        all_sessions_deleted = False

        while not all_sessions_deleted:
            query = _AppEngineUtilities_Session.all()
            results = query.fetch(75)
            if len(results) is 0:
                all_sessions_deleted = True
            else:
                for result in results:
                    result.delete()
        return True


    def _clean_old_sessions(self):
        """
        Delete 50 expired sessions from the datastore.

        This is only called for CLEAN_CHECK_PERCENT percent of requests because
        it could be rather intensive.

        Returns True on completion
        """
        self.clean_old_sessions(self.session_expire_time, 50)


    @classmethod
    def clean_old_sessions(cls, session_expire_time, count=50):
        """
        Delete expired sessions from the datastore.

        This is a class method which can be used by applications for
        maintenance if they don't want to use the built in session
        cleaning.

        Args:
          count: The amount of session to clean.
          session_expire_time: The age in seconds to determine outdated
                               sessions.

        Returns True on completion
        """
        duration = datetime.timedelta(seconds=session_expire_time)
        session_age = datetime.datetime.now() - duration
        query = _AppEngineUtilities_Session.all()
        query.filter(u"last_activity <", session_age)
        results = query.fetch(50)
        for result in results:
            result.delete()
        return True

    def cycle_key(self):
        """
        Changes the session id/token.

        Returns new token.
        """
        self.sid = self.new_sid()
        if len(self.session.sid) > 2:
            self.session.sid.remove(self.session.sid[0])
        self.session.sid.append(self.sid)
        
        return self.sid

    def flush(self):
        """
        Delete's the current session, creating a new one.

        Returns True
        """
        self._delete_session()
        self.__init__()
        return True

    def no_cache_headers(self):
        """
        Generates headers to avoid any page caching in the browser.
        Useful for highly dynamic sites.

        Returns a unicode string of headers.
        """
        return u"".join([u"Expires: Tue, 03 Jul 2001 06:00:00 GMT",
            strftime("Last-Modified: %a, %d %b %y %H:%M:%S %Z").decode("utf-8"),
            u"Cache-Control: no-store, no-cache, must-revalidate, max-age=0",
            u"Cache-Control: post-check=0, pre-check=0",
            u"Pragma: no-cache",
        ])

    def clear(self):
        """
        Removes session data items, doesn't delete the session. It does work
        with cookie sessions, and must be called before any output is sent
        to the browser, as it set cookies.

        Returns True
        """
        sessiondata = self._get()
        # delete from datastore
        if sessiondata is not None:
            for sd in sessiondata:
                sd.delete()
        # delete from memcache
        self.cache = {}
        self.cookie_vals = {}
        self.output_cookie["%s_data" %s (self.cookie_name)] = \
            simplejson.dumps(self.cookie_vals)
        self.output_cookie["%s_data" % (self.cookie_name)]["path"] = \
            self.cookie_path
        if self.cookie_domain:
            self.output_cookie["%s_data" % \
                (self.cookie_name)]["domain"] = self.cookie_domain

        print self.output_cookie.output()
        return True

    def has_key(self, keyname):
        """
        Equivalent to k in a, use that form in new code

        Args:
            keyname: keyname to check

        Returns True/False
        """
        return self.__contains__(keyname)

    def items(self):
        """
        Creates a copy of just the data items.

        Returns dictionary of session data objects.
        """
        op = {}
        for k in self:
            op[k] = self[k]
        return op

    def keys(self):
        """
        Returns a list of keys.
        """
        l = []
        for k in self:
            l.append(k)
        return l

    def update(self, *dicts):
        """
        Updates with key/value pairs from b, overwriting existing keys

        Returns None
        """
        for dict in dicts:
            for k in dict:
                self._put(k, dict[k])
        return None

    def values(self):
        """
        Returns a list object of just values in the session.
        """
        v = []
        for k in self:
            v.append(self[k])
        return v

    def get(self, keyname, default = None):
        """
        Returns either the value for the keyname or a default value
        passed.

        Args:
            keyname: keyname to look up
            default: (optional) value to return on keyname miss

        Returns value of keyname, or default, or None
        """
        try:
            return self.__getitem__(keyname)
        except KeyError:
            if default is not None:
                return default
            return None

    def setdefault(self, keyname, default = None):
        """
        Returns either the value for the keyname or a default value
        passed. If keyname lookup is a miss, the keyname is set with
        a value of default.

        Args:
            keyname: keyname to look up
            default: (optional) value to return on keyname miss

        Returns value of keyname, or default, or None
        """
        try:
            return self.__getitem__(keyname)
        except KeyError:
            if default is not None:
                self.__setitem__(keyname, default)
                return default
            return None

    @classmethod
    def check_token(cls, cookie_name=COOKIE_NAME, delete_invalid=True):
        """
        Retrieves the token from a cookie and validates that it is
        a valid token for an existing cookie. Cookie validation is based
        on the token existing on a session that has not expired.

        This is useful for determining if datastore or cookie writer
        should be used in hybrid implementations.

        Args:
            cookie_name: Name of the cookie to check for a token.
            delete_invalid: If the token is not valid, delete the session
                            cookie, to avoid datastore queries on future
                            requests.

        Returns True/False
        """

        string_cookie = os.environ.get(u"HTTP_COOKIE", u"")
        cookie = Cookie.SimpleCookie()
        cookie.load(string_cookie)
        if cookie.has_key(cookie_name):
            query = _AppEngineUtilities_Session.all()
            query.filter(u"sid", cookie[cookie_name].value)
            results = query.fetch(1)
            if len(results) > 0:
                return True
            else:
                if delete_invalid:
                    output_cookie = Cookie.SimpleCookie()
                    output_cookie[cookie_name] = cookie[cookie_name]
                    output_cookie[cookie_name][u"expires"] = 0
                    print output_cookie.output()
        return False

    def get_ds_entity(self):
        """
        Will return the session entity from the datastore if one
        exists, otherwise will return None (as in the case of cookie writer
        session.
        """
        if hasattr(self, u"session"):
            return self.session
        return None

    # Implement Python container methods

    def __getitem__(self, keyname):
        """
        Get item from session data.

        keyname: The keyname of the mapping.
        """
        # flash messages don't go in the datastore

        if self.integrate_flash and (keyname == u"flash"):
            return self.flash.msg
        if keyname in self.cache:
            return self.cache[keyname]
        if keyname in self.cookie_vals:
            return self.cookie_vals[keyname]
        if hasattr(self, u"session"):
            data = self._get(keyname)
            if data:
                # TODO: It's broke here, but I'm not sure why, it's
                # returning a model object, but I can't seem to modify
                # it.
                try:
                    if data.model != None:
                        self.cache[keyname] = data.model
                        return self.cache[keyname]
                    else:
                        self.cache[keyname] = pickle.loads(data.content)
                        return self.cache[keyname]
                except:
                    self.delete_item(keyname)

            else:
                raise KeyError(unicode(keyname))
        raise KeyError(unicode(keyname))

    def __setitem__(self, keyname, value):
        """
        Set item in session data.

        Args:
            keyname: They keyname of the mapping.
            value: The value of mapping.
        """

        if self.integrate_flash and (keyname == u"flash"):
            self.flash.msg = value
        else:
            keyname = self._validate_key(keyname)
            self.cache[keyname] = value
            return self._put(keyname, value)

    def delete_item(self, keyname, throw_exception=False):
        """
        Delete item from session data, ignoring exceptions if
        necessary.

        Args:
            keyname: The keyname of the object to delete.
            throw_exception: false if exceptions are to be ignored.
        Returns:
            Nothing.
        """
        if throw_exception:
            self.__delitem__(keyname)
            return None
        else:
            try:
                self.__delitem__(keyname)
            except KeyError:
                return None

    def __delitem__(self, keyname):
        """
        Delete item from session data.

        Args:
            keyname: The keyname of the object to delete.
        """
        bad_key = False
        sessdata = self._get(keyname = keyname)
        if sessdata is None:
            bad_key = True
        else:
            sessdata.delete()
        if keyname in self.cookie_vals:
            del self.cookie_vals[keyname]
            bad_key = False
            self.output_cookie["%s_data" % (self.cookie_name)] = \
                simplejson.dumps(self.cookie_vals)
            self.output_cookie["%s_data" % (self.cookie_name)]["path"] = \
                self.cookie_path
            if self.cookie_domain:
                self.output_cookie["%s_data" % \
                    (self.cookie_name)]["domain"] = self.cookie_domain

            print self.output_cookie.output()
        if bad_key:
            raise KeyError(unicode(keyname))
        if keyname in self.cache:
            del self.cache[keyname]

    def __len__(self):
        """
        Return size of session.
        """
        # check memcache first
        if hasattr(self, u"session"):
            results = self._get()
            if results is not None:
                return len(results) + len(self.cookie_vals)
            else:
                return 0
        return len(self.cookie_vals)

    def __contains__(self, keyname):
        """
        Check if an item is in the session data.

        Args:
            keyname: The keyname being searched.
        """
        try:
            self.__getitem__(keyname)
        except KeyError:
            return False
        return True

    def __iter__(self):
        """
        Iterate over the keys in the session data.
        """
        # try memcache first
        if hasattr(self, u"session"):
            vals = self._get()
            if vals is not None:
                for k in vals:
                    yield k.keyname
        for k in self.cookie_vals:
            yield k

    def __str__(self):
        """
        Return string representation.
        """
        return u"{%s}" % ', '.join(['"%s" = "%s"' % (k, self[k]) for k in self])
