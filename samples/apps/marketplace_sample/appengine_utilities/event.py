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
import sys


class Event(object):
    """
    Event is a simple publish/subscribe based event dispatcher. It's a way
    to add, or take advantage of, hooks in your application. If you want to
    tie actions in with lower level classes you're developing within your
    application, you can set events to fire, and then subscribe to them with
    callback methods in other methods in your application.

    It sets itself to the sys.modules['__main__'] function. In order to use it,
    you must import it with your sys.modules['__main__'] method, and make sure
    you import sys.modules['__main__'] and it's accessible for the methods where
    you want to use it.

    For example, from sessions.py

            # if the event class has been loaded, fire off the sessionDeleted
            # event
        if u"AEU_Events" in sys.modules['__main__'].__dict__:
            sys.modules['__main__'].AEU_Events.fire_event(u"sessionDelete")

    You can the subscribe to session delete events, adding a callback

        if u"AEU_Events" in sys.modules['__main__'].__dict__:
            sys.modules['__main__'].AEU_Events.subscribe(u"sessionDelete", \
            clear_user_session)
    """

    def __init__(self):
        self.events = []

    def subscribe(self, event, callback, args = None):
        """
        This method will subscribe a callback function to an event name.

        Args:
            event: The event to subscribe to.
            callback: The callback method to run.
            args: Optional arguments to pass with the callback.

        Returns True
        """
        if not {"event": event, "callback": callback, "args": args, } \
            in self.events:
            self.events.append({"event": event, "callback": callback, \
                "args": args, })
        return True

    def unsubscribe(self, event, callback, args = None):
        """
        This method will unsubscribe a callback from an event.

        Args:
            event: The event to subscribe to.
            callback: The callback method to run.
            args: Optional arguments to pass with the callback.

        Returns True
        """
        if {"event": event, "callback": callback, "args": args, }\
            in self.events:
            self.events.remove({"event": event, "callback": callback,\
                "args": args, })

        return True

    def fire_event(self, event = None):
        """
        This method is what a method uses to fire an event,
        initiating all registered callbacks

        Args:
            event: The name of the event to fire.

        Returns True
        """
        for e in self.events:
            if e["event"] == event:
                if type(e["args"]) == type([]):
                    e["callback"](*e["args"])
                elif type(e["args"]) == type({}):
                    e["callback"](**e["args"])
                elif e["args"] == None:
                    e["callback"]()
                else:
                    e["callback"](e["args"])
        return True
"""
Assign to the event class to sys.modules['__main__']
"""
sys.modules['__main__'].AEU_Events = Event()
