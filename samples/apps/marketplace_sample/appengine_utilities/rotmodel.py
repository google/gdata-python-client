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

import time
from google.appengine.api import datastore
from google.appengine.ext import db

# settings
try:
    import settings_default
    import settings

    if settings.__name__.rsplit('.', 1)[0] != settings_default.__name__.rsplit('.', 1)[0]:
        settings = settings_default
except:
    settings = settings_default

class ROTModel(db.Model):
    """
    ROTModel overrides the db.Model functions, retrying each method each time
    a timeout exception is raised.

    Methods superclassed from db.Model are:
        get(cls, keys)
        get_by_id(cls, ids, parent)
        get_by_key_name(cls, key_names, parent)
        get_or_insert(cls, key_name, kwargs)
        put(self)
    """

    @classmethod
    def get(cls, keys):
        count = 0
        while count < settings.rotmodel["RETRY_ATTEMPTS"]:
            try:
                return db.Model.get(keys)
            except db.Timeout:
                count += 1
                time.sleep(count * settings.rotmodel["RETRY_INTERVAL"])
        else:
            raise db.Timeout()

    @classmethod
    def get_by_id(cls, ids, parent=None):
        count = 0
        while count < settings.rotmodel["RETRY_ATTEMPTS"]:
            try:
                return db.Model.get_by_id(ids, parent)
            except db.Timeout:
                count += 1
                time.sleep(count * settings.rotmodel["RETRY_INTERVAL"])
        else:
            raise db.Timeout()

    @classmethod
    def get_by_key_name(cls, key_names, parent=None):
        if isinstance(parent, db.Model):
            parent = parent.key()
        key_names, multiple = datastore.NormalizeAndTypeCheck(key_names, basestring)
        keys = [datastore.Key.from_path(cls.kind(), name, parent=parent)
                for name in key_names]
        count = 0
        if multiple:
            while count < settings.rotmodel["RETRY_ATTEMPTS"]:
                try:
                    return db.get(keys)
                except db.Timeout:
                    count += 1
                    time.sleep(count * settings.rotmodel["RETRY_INTERVAL"])
        else:
            while count < settings.rotmodel["RETRY_ATTEMPTS"]:
                try:
                    return db.get(*keys)
                except db.Timeout:
                    count += 1
                    time.sleep(count * settings.rotmodel["RETRY_INTERVAL"])

    @classmethod
    def get_or_insert(cls, key_name, **kwargs):
        def txn():
            entity = cls.get_by_key_name(key_name, parent=kwargs.get('parent'))
            if entity is None:
                entity = cls(key_name=key_name, **kwargs)
                entity.put()
            return entity
        return db.run_in_transaction(txn)

    def put(self):
        count = 0
        while count < settings.rotmodel["RETRY_ATTEMPTS"]:
            try:
                return db.Model.put(self)
            except db.Timeout:
                count += 1
                time.sleep(count * settings.rotmodel["RETRY_INTERVAL"])
        else:
            raise db.Timeout()

    def delete(self):
        count = 0
        while count < settings.rotmodel["RETRY_ATTEMPTS"]:
            try:
                return db.Model.delete(self)
            except db.Timeout:
                count += 1
                time.sleep(count * settings.rotmodel["RETRY_INTERVAL"])
        else:
            raise db.Timeout()


