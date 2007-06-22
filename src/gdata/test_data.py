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



XML_ENTRY_1 = """<?xml version='1.0'?>
<entry xmlns='http://www.w3.org/2005/Atom'
       xmlns:g='http://base.google.com/ns/1.0'>
  <category scheme="http://base.google.com/categories/itemtypes"
            term="products"/>
  <id>    http://www.google.com/test/id/url   </id>
  <title type='text'>Testing 2000 series laptop</title>
  <content type='xhtml'>
    <div xmlns='http://www.w3.org/1999/xhtml'>A Testing Laptop</div>
  </content>
  <link rel='alternate' type='text/html'
        href='http://www.provider-host.com/123456789'/>
  <link rel='license' 
        href='http://creativecommons.org/licenses/by-nc/2.5/rdf'/>
  <g:label>Computer</g:label>
  <g:label>Laptop</g:label>
  <g:label>testing laptop</g:label>
  <g:item_type>products</g:item_type>
</entry>"""


TEST_BASE_ENTRY = """<?xml version='1.0'?>
<entry xmlns='http://www.w3.org/2005/Atom'
       xmlns:g='http://base.google.com/ns/1.0'>
  <category scheme="http://base.google.com/categories/itemtypes"
            term="products"/>
  <title type='text'>Testing 2000 series laptop</title>
  <content type='xhtml'>
    <div xmlns='http://www.w3.org/1999/xhtml'>A Testing Laptop</div>
  </content>
  <app:control xmlns:app='http://purl.org/atom/app#'>
    <app:draft>yes</app:draft>
    <gm:disapproved xmlns:gm='http://base.google.com/ns-metadata/1.0'/>   
  </app:control>
  <link rel='alternate' type='text/html'
        href='http://www.provider-host.com/123456789'/>
  <g:label>Computer</g:label>
  <g:label>Laptop</g:label>
  <g:label>testing laptop</g:label>
  <g:item_type>products</g:item_type>
</entry>"""


BIG_FEED = """<?xml version="1.0" encoding="utf-8"?>
   <feed xmlns="http://www.w3.org/2005/Atom">
     <title type="text">dive into mark</title>
     <subtitle type="html">
       A &lt;em&gt;lot&lt;/em&gt; of effort
       went into making this effortless
     </subtitle>
     <updated>2005-07-31T12:29:29Z</updated>
     <id>tag:example.org,2003:3</id>
     <link rel="alternate" type="text/html"
      hreflang="en" href="http://example.org/"/>
     <link rel="self" type="application/atom+xml"
      href="http://example.org/feed.atom"/>
     <rights>Copyright (c) 2003, Mark Pilgrim</rights>
     <generator uri="http://www.example.com/" version="1.0">
       Example Toolkit
     </generator>
     <entry>
       <title>Atom draft-07 snapshot</title>
       <link rel="alternate" type="text/html"
        href="http://example.org/2005/04/02/atom"/>
       <link rel="enclosure" type="audio/mpeg" length="1337"
        href="http://example.org/audio/ph34r_my_podcast.mp3"/>
       <id>tag:example.org,2003:3.2397</id>
       <updated>2005-07-31T12:29:29Z</updated>
       <published>2003-12-13T08:29:29-04:00</published>
       <author>
         <name>Mark Pilgrim</name>
         <uri>http://example.org/</uri>
         <email>f8dy@example.com</email>
       </author>
       <contributor>
         <name>Sam Ruby</name>
       </contributor>
       <contributor>
         <name>Joe Gregorio</name>
       </contributor>
       <content type="xhtml" xml:lang="en"
        xml:base="http://diveintomark.org/">
         <div xmlns="http://www.w3.org/1999/xhtml">
           <p><i>[Update: The Atom draft is finished.]</i></p>
         </div>
       </content>
     </entry>
   </feed>
"""

SMALL_FEED = """<?xml version="1.0" encoding="utf-8"?>
   <feed xmlns="http://www.w3.org/2005/Atom">
     <title>Example Feed</title>
     <link href="http://example.org/"/>
     <updated>2003-12-13T18:30:02Z</updated>
     <author>
       <name>John Doe</name>
     </author>
     <id>urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6</id>
     <entry>
       <title>Atom-Powered Robots Run Amok</title>
       <link href="http://example.org/2003/12/13/atom03"/>
       <id>urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a</id>
       <updated>2003-12-13T18:30:02Z</updated>
       <summary>Some text.</summary>
     </entry>
   </feed>
"""

GBASE_FEED = """<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom' xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/' xmlns:g='http://base.google.com/ns/1.0' xmlns:batch='http://schemas.google.com/gdata/batch'>
<id>http://www.google.com/base/feeds/snippets</id>
<updated>2007-02-08T23:18:21.935Z</updated>
<title type='text'>Items matching query: digital camera</title>
<link rel='alternate' type='text/html' href='http://base.google.com'>
</link>
<link rel='http://schemas.google.com/g/2005#feed' type='application/atom+xml' href='http://www.google.com/base/feeds/snippets'>
</link>
<link rel='self' type='application/atom+xml' href='http://www.google.com/base/feeds/snippets?start-index=1&amp;max-results=25&amp;bq=digital+camera'>
</link>
<link rel='next' type='application/atom+xml' href='http://www.google.com/base/feeds/snippets?start-index=26&amp;max-results=25&amp;bq=digital+camera'>
</link>
<generator version='1.0' uri='http://base.google.com'>GoogleBase              </generator>
<openSearch:totalResults>2171885</openSearch:totalResults>
<openSearch:startIndex>1</openSearch:startIndex>
<openSearch:itemsPerPage>25</openSearch:itemsPerPage>
<entry>
<id>http://www.google.com/base/feeds/snippets/13246453826751927533</id>
<published>2007-02-08T13:23:27.000Z</published>
<updated>2007-02-08T16:40:57.000Z</updated>
<category scheme='http://base.google.com/categories/itemtypes' term='Products'>
</category>
<title type='text'>Digital Camera Battery Notebook Computer 12v DC Power Cable - 5.5mm x 2.5mm (Center +) Camera Connecting Cables</title>
<content type='html'>Notebook Computer 12v DC Power Cable - 5.5mm x 2.1mm (Center +) This connection cable will allow any Digital Pursuits battery pack to power portable computers that operate with 12v power and have a 2.1mm power connector (center +) Digital  ...</content>
<link rel='alternate' type='text/html' href='http://www.bhphotovideo.com/bnh/controller/home?O=productlist&amp;A=details&amp;Q=&amp;sku=305668&amp;is=REG&amp;kw=DIDCB5092&amp;BI=583'>
</link>
<link rel='self' type='application/atom+xml' href='http://www.google.com/base/feeds/snippets/13246453826751927533'>
</link>
<author>
<name>B&amp;H Photo-Video</name>
<email>anon-szot0wdsq0at@base.google.com</email>
</author>
<g:payment_notes type='text'>PayPal &amp; Bill Me Later credit available online only.</g:payment_notes>
<g:condition type='text'>new</g:condition>
<g:location type='location'>420 9th Ave. 10001</g:location>
<g:id type='text'>305668-REG</g:id>
<g:item_type type='text'>Products</g:item_type>
<g:brand type='text'>Digital Camera Battery</g:brand>
<g:expiration_date type='dateTime'>2007-03-10T13:23:27.000Z</g:expiration_date>
<g:customer_id type='int'>1172711</g:customer_id>
<g:price type='floatUnit'>34.95 usd</g:price>
<g:product_type type='text'>Digital Photography&gt;Camera Connecting Cables</g:product_type>
<g:item_language type='text'>EN</g:item_language>
<g:manufacturer_id type='text'>DCB5092</g:manufacturer_id>
<g:target_country type='text'>US</g:target_country>
<g:weight type='float'>1.0</g:weight>
<g:image_link type='url'>http://base.google.com/base_image?q=http%3A%2F%2Fwww.bhphotovideo.com%2Fimages%2Fitems%2F305668.jpg&amp;dhm=ffffffff84c9a95e&amp;size=6</g:image_link>
</entry>
<entry>
<id>http://www.google.com/base/feeds/snippets/10145771037331858608</id>
<published>2007-02-08T13:23:27.000Z</published>
<updated>2007-02-08T16:40:57.000Z</updated>
<category scheme='http://base.google.com/categories/itemtypes' term='Products'>
</category>
<title type='text'>Digital Camera Battery Electronic Device 5v DC Power Cable - 5.5mm x 2.5mm (Center +) Camera Connecting Cables</title>
<content type='html'>Electronic Device 5v DC Power Cable - 5.5mm x 2.5mm (Center +) This connection cable will allow any Digital Pursuits battery pack to power any electronic device that operates with 5v power and has a 2.5mm power connector (center +) Digital  ...</content>
<link rel='alternate' type='text/html' href='http://www.bhphotovideo.com/bnh/controller/home?O=productlist&amp;A=details&amp;Q=&amp;sku=305656&amp;is=REG&amp;kw=DIDCB5108&amp;BI=583'>
</link>
<link rel='self' type='application/atom+xml' href='http://www.google.com/base/feeds/snippets/10145771037331858608'>
</link>
<author>
<name>B&amp;H Photo-Video</name>
<email>anon-szot0wdsq0at@base.google.com</email>
</author>
<g:location type='location'>420 9th Ave. 10001</g:location>
<g:condition type='text'>new</g:condition>
<g:weight type='float'>0.18</g:weight>
<g:target_country type='text'>US</g:target_country>
<g:product_type type='text'>Digital Photography&gt;Camera Connecting Cables</g:product_type>
<g:payment_notes type='text'>PayPal &amp; Bill Me Later credit available online only.</g:payment_notes>
<g:id type='text'>305656-REG</g:id>
<g:image_link type='url'>http://base.google.com/base_image?q=http%3A%2F%2Fwww.bhphotovideo.com%2Fimages%2Fitems%2F305656.jpg&amp;dhm=7315bdc8&amp;size=6</g:image_link>
<g:manufacturer_id type='text'>DCB5108</g:manufacturer_id>
<g:upc type='text'>838098005108</g:upc>
<g:price type='floatUnit'>34.95 usd</g:price>
<g:item_language type='text'>EN</g:item_language>
<g:brand type='text'>Digital Camera Battery</g:brand>
<g:customer_id type='int'>1172711</g:customer_id>
<g:item_type type='text'>Products</g:item_type>
<g:expiration_date type='dateTime'>2007-03-10T13:23:27.000Z</g:expiration_date>
</entry>
<entry>
<id>http://www.google.com/base/feeds/snippets/3128608193804768644</id>
<published>2007-02-08T02:21:27.000Z</published>
<updated>2007-02-08T15:40:13.000Z</updated>
<category scheme='http://base.google.com/categories/itemtypes' term='Products'>
</category>
<title type='text'>Digital Camera Battery Power Cable for Kodak 645 Pro-Back ProBack &amp; DCS-300 Series Camera Connecting Cables</title>
<content type='html'>Camera Connection Cable - to Power Kodak 645 Pro-Back DCS-300 Series Digital Cameras This connection cable will allow any Digital Pursuits battery pack to power the following digital cameras: Kodak DCS Pro Back 645 DCS-300 series Digital Photography ...</content>
<link rel='alternate' type='text/html' href='http://www.bhphotovideo.com/bnh/controller/home?O=productlist&amp;A=details&amp;Q=&amp;sku=305685&amp;is=REG&amp;kw=DIDCB6006&amp;BI=583'>
</link>
<link rel='self' type='application/atom+xml' href='http://www.google.com/base/feeds/snippets/3128608193804768644'>
</link>
<author>
<name>B&amp;H Photo-Video</name>
<email>anon-szot0wdsq0at@base.google.com</email>
</author>
<g:weight type='float'>0.3</g:weight>
<g:manufacturer_id type='text'>DCB6006</g:manufacturer_id>
<g:image_link type='url'>http://base.google.com/base_image?q=http%3A%2F%2Fwww.bhphotovideo.com%2Fimages%2Fitems%2F305685.jpg&amp;dhm=72f0ca0a&amp;size=6</g:image_link>
<g:location type='location'>420 9th Ave. 10001</g:location>
<g:payment_notes type='text'>PayPal &amp; Bill Me Later credit available online only.</g:payment_notes>
<g:item_type type='text'>Products</g:item_type>
<g:target_country type='text'>US</g:target_country>
<g:accessory_for type='text'>digital kodak camera</g:accessory_for>
<g:brand type='text'>Digital Camera Battery</g:brand>
<g:expiration_date type='dateTime'>2007-03-10T02:21:27.000Z</g:expiration_date>
<g:item_language type='text'>EN</g:item_language>
<g:condition type='text'>new</g:condition>
<g:price type='floatUnit'>34.95 usd</g:price>
<g:customer_id type='int'>1172711</g:customer_id>
<g:product_type type='text'>Digital Photography&gt;Camera Connecting Cables</g:product_type>
<g:id type='text'>305685-REG</g:id>
</entry>
</feed>"""

EXTENSION_TREE = """<?xml version="1.0" encoding="utf-8"?>
   <feed xmlns="http://www.w3.org/2005/Atom">
     <g:author xmlns:g="http://www.google.com">
       <g:name>John Doe
         <g:foo yes="no" up="down">Bar</g:foo>
       </g:name>
     </g:author>
   </feed>
"""

TEST_AUTHOR = """<?xml version="1.0" encoding="utf-8"?>
   <author xmlns="http://www.w3.org/2005/Atom">
       <name xmlns="http://www.w3.org/2005/Atom">John Doe</name>
       <email xmlns="http://www.w3.org/2005/Atom">johndoes@someemailadress.com</email>
       <uri xmlns="http://www.w3.org/2005/Atom">http://www.google.com</uri>
   </author>
"""

TEST_LINK = """<?xml version="1.0" encoding="utf-8"?>
   <link xmlns="http://www.w3.org/2005/Atom" href="http://www.google.com" 
       rel="test rel" foo1="bar" foo2="rab"/>
"""

TEST_GBASE_ATTRIBUTE = """<?xml version="1.0" encoding="utf-8"?>
   <g:brand type='text' xmlns:g="http://base.google.com/ns/1.0">Digital Camera Battery</g:brand>
"""
   

CALENDAR_FEED = """<?xml version='1.0' encoding='utf-8'?>
<feed xmlns='http://www.w3.org/2005/Atom'
xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/'
xmlns:gd='http://schemas.google.com/g/2005'
xmlns:gCal='http://schemas.google.com/gCal/2005'>
  <id>http://www.google.com/calendar/feeds/default</id>
  <updated>2007-03-20T22:48:57.833Z</updated>
  <title type='text'>GData Ops Demo's Calendar List</title>
  <link rel='http://schemas.google.com/g/2005#feed'
  type='application/atom+xml'
  href='http://www.google.com/calendar/feeds/default'></link>
  <link rel='http://schemas.google.com/g/2005#post'
  type='application/atom+xml'
  href='http://www.google.com/calendar/feeds/default'></link>
  <link rel='self' type='application/atom+xml'
  href='http://www.google.com/calendar/feeds/default'></link>
  <author>
    <name>GData Ops Demo</name>
    <email>gdata.ops.demo@gmail.com</email>
  </author>
  <generator version='1.0' uri='http://www.google.com/calendar'>
  Google Calendar</generator>
  <openSearch:startIndex>1</openSearch:startIndex>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/gdata.ops.demo%40gmail.com</id>
    <published>2007-03-20T22:48:57.837Z</published>
    <updated>2007-03-20T22:48:52.000Z</updated>
    <title type='text'>GData Ops Demo</title>
    <link rel='alternate' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/gdata.ops.demo%40gmail.com/private/full'>
    </link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/gdata.ops.demo%40gmail.com'>
    </link>
    <author>
      <name>GData Ops Demo</name>
      <email>gdata.ops.demo@gmail.com</email>
    </author>
    <gCal:color value='#2952A3'></gCal:color>
    <gCal:accesslevel value='owner'></gCal:accesslevel>
    <gCal:hidden value='false'></gCal:hidden>
    <gCal:timezone value='America/Los_Angeles'></gCal:timezone>
  </entry>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/jnh21ovnjgfph21h32gvms2758%40group.calendar.google.com</id>
    <published>2007-03-20T22:48:57.837Z</published>
    <updated>2007-03-20T22:48:53.000Z</updated>
    <title type='text'>GData Ops Demo Secondary Calendar</title>
    <summary type='text'></summary>
    <link rel='alternate' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/jnh21ovnjgfph21h32gvms2758%40group.calendar.google.com/private/full'>
    </link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/jnh21ovnjgfph21h32gvms2758%40group.calendar.google.com'>
    </link>
    <author>
      <name>GData Ops Demo Secondary Calendar</name>
    </author>
    <gCal:color value='#528800'></gCal:color>
    <gCal:accesslevel value='owner'></gCal:accesslevel>
    <gCal:hidden value='false'></gCal:hidden>
    <gCal:timezone value='America/Los_Angeles'></gCal:timezone>
    <gd:where valueString=''></gd:where>
  </entry>
</feed>
"""

CALENDAR_FULL_EVENT_FEED = """<?xml version='1.0' encoding='utf-8'?>
<feed xmlns='http://www.w3.org/2005/Atom'
xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/'
xmlns:gd='http://schemas.google.com/g/2005'
xmlns:gCal='http://schemas.google.com/gCal/2005'>
  <id>
  http://www.google.com/calendar/feeds/default/private/full</id>
  <updated>2007-03-20T21:29:57.000Z</updated>
  <category scheme='http://schemas.google.com/g/2005#kind'
  term='http://schemas.google.com/g/2005#event'></category>
  <title type='text'>GData Ops Demo</title>
  <subtitle type='text'>GData Ops Demo</subtitle>
  <link rel='http://schemas.google.com/g/2005#feed'
  type='application/atom+xml'
  href='http://www.google.com/calendar/feeds/default/private/full'>
  </link>
  <link rel='http://schemas.google.com/g/2005#post'
  type='application/atom+xml'
  href='http://www.google.com/calendar/feeds/default/private/full'>
  </link>
  <link rel='self' type='application/atom+xml'
  href='http://www.google.com/calendar/feeds/default/private/full?updated-min=2001-01-01&amp;max-results=25'>
  </link>
  <author>
    <name>GData Ops Demo</name>
    <email>gdata.ops.demo@gmail.com</email>
  </author>
  <generator version='1.0' uri='http://www.google.com/calendar'>
  Google Calendar</generator>
  <openSearch:totalResults>10</openSearch:totalResults>
  <openSearch:startIndex>1</openSearch:startIndex>
  <openSearch:itemsPerPage>25</openSearch:itemsPerPage>
  <gCal:timezone value='America/Los_Angeles'></gCal:timezone>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/private/full/o99flmgmkfkfrr8u745ghr3100</id>
    <published>2007-03-20T21:29:52.000Z</published>
    <updated>2007-03-20T21:29:57.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
    <title type='text'>test deleted</title>
    <content type='text'></content>
    <link rel='alternate' type='text/html'
    href='http://www.google.com/calendar/event?eid=bzk5ZmxtZ21rZmtmcnI4dTc0NWdocjMxMDAgZ2RhdGEub3BzLmRlbW9AbQ'
    title='alternate'></link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/o99flmgmkfkfrr8u745ghr3100'>
    </link>
    <link rel='edit' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/o99flmgmkfkfrr8u745ghr3100/63310109397'>
    </link>
    <author>
      <name>GData Ops Demo</name>
      <email>gdata.ops.demo@gmail.com</email>
    </author>
    <gCal:sendEventNotifications value='false'>
    </gCal:sendEventNotifications>
    <gd:eventStatus value='http://schemas.google.com/g/2005#event.canceled'>
    </gd:eventStatus>
    <gd:comments>
      <gd:feedLink href='http://www.google.com/calendar/feeds/default/private/full/o99flmgmkfkfrr8u745ghr3100/comments'>
      </gd:feedLink>
    </gd:comments>
    <gd:visibility value='http://schemas.google.com/g/2005#event.default'>
    </gd:visibility>
    <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
    </gd:transparency>
    <gd:when startTime='2007-03-23T12:00:00.000-07:00'
    endTime='2007-03-23T13:00:00.000-07:00'>
      <gd:reminder minutes='10'></gd:reminder>
    </gd:when>
    <gd:where></gd:where>
  </entry>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/private/full/2qt3ao5hbaq7m9igr5ak9esjo0</id>
    <published>2007-03-20T21:26:04.000Z</published>
    <updated>2007-03-20T21:28:46.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
    <title type='text'>Afternoon at Dolores Park with Kim</title>
    <content type='text'></content>
    <link rel='alternate' type='text/html'
    href='http://www.google.com/calendar/event?eid=MnF0M2FvNWhiYXE3bTlpZ3I1YWs5ZXNqbzAgZ2RhdGEub3BzLmRlbW9AbQ'
    title='alternate'></link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/2qt3ao5hbaq7m9igr5ak9esjo0'>
    </link>
    <link rel='edit' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/2qt3ao5hbaq7m9igr5ak9esjo0/63310109326'>
    </link>
    <author>
      <name>GData Ops Demo</name>
      <email>gdata.ops.demo@gmail.com</email>
    </author>
    <gCal:sendEventNotifications value='false'>
    </gCal:sendEventNotifications>
    <gd:eventStatus value='http://schemas.google.com/g/2005#event.confirmed'>
    </gd:eventStatus>
    <gd:comments>
      <gd:feedLink href='http://www.google.com/calendar/feeds/default/private/full/2qt3ao5hbaq7m9igr5ak9esjo0/comments'>
      </gd:feedLink>
    </gd:comments>
    <gd:visibility value='http://schemas.google.com/g/2005#event.private'>
    </gd:visibility>
    <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
    </gd:transparency>
    <gd:who rel='http://schemas.google.com/g/2005#event.organizer'
    valueString='GData Ops Demo' email='gdata.ops.demo@gmail.com'>
      <gd:attendeeStatus value='http://schemas.google.com/g/2005#event.accepted'>
      </gd:attendeeStatus>
    </gd:who>
    <gd:who rel='http://schemas.google.com/g/2005#event.attendee'
    valueString='Ryan Boyd (API)' email='api.rboyd@gmail.com'>
      <gd:attendeeStatus value='http://schemas.google.com/g/2005#event.invited'>
      </gd:attendeeStatus>
    </gd:who>
    <gd:when startTime='2007-03-24T12:00:00.000-07:00'
    endTime='2007-03-24T15:00:00.000-07:00'>
      <gd:reminder minutes='20'></gd:reminder>
    </gd:when>
    <gd:where valueString='Dolores Park with Kim'></gd:where>
  </entry>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/private/full/uvsqhg7klnae40v50vihr1pvos</id>
    <published>2007-03-20T21:28:37.000Z</published>
    <updated>2007-03-20T21:28:37.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
    <title type='text'>Team meeting</title>
    <content type='text'></content>
    <link rel='alternate' type='text/html'
    href='http://www.google.com/calendar/event?eid=dXZzcWhnN2tsbmFlNDB2NTB2aWhyMXB2b3NfMjAwNzAzMjNUMTYwMDAwWiBnZGF0YS5vcHMuZGVtb0Bt'
    title='alternate'></link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/uvsqhg7klnae40v50vihr1pvos'>
    </link>
    <link rel='edit' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/uvsqhg7klnae40v50vihr1pvos/63310109317'>
    </link>
    <author>
      <name>GData Ops Demo</name>
      <email>gdata.ops.demo@gmail.com</email>
    </author>
    <gd:recurrence>DTSTART;TZID=America/Los_Angeles:20070323T090000
    DTEND;TZID=America/Los_Angeles:20070323T100000
    RRULE:FREQ=WEEKLY;BYDAY=FR;UNTIL=20070817T160000Z;WKST=SU
    BEGIN:VTIMEZONE TZID:America/Los_Angeles
    X-LIC-LOCATION:America/Los_Angeles BEGIN:STANDARD
    TZOFFSETFROM:-0700 TZOFFSETTO:-0800 TZNAME:PST
    DTSTART:19701025T020000 RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
    END:STANDARD BEGIN:DAYLIGHT TZOFFSETFROM:-0800 TZOFFSETTO:-0700
    TZNAME:PDT DTSTART:19700405T020000
    RRULE:FREQ=YEARLY;BYMONTH=4;BYDAY=1SU END:DAYLIGHT
    END:VTIMEZONE</gd:recurrence>
    <gCal:sendEventNotifications value='true'>
    </gCal:sendEventNotifications>
    <gd:eventStatus value='http://schemas.google.com/g/2005#event.confirmed'>
    </gd:eventStatus>
    <gd:visibility value='http://schemas.google.com/g/2005#event.public'>
    </gd:visibility>
    <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
    </gd:transparency>
    <gd:reminder minutes='10'></gd:reminder>
    <gd:where valueString=''></gd:where>
  </entry>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/private/full/st4vk9kiffs6rasrl32e4a7alo</id>
    <published>2007-03-20T21:25:46.000Z</published>
    <updated>2007-03-20T21:25:46.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
    <title type='text'>Movie with Kim and danah</title>
    <content type='text'></content>
    <link rel='alternate' type='text/html'
    href='http://www.google.com/calendar/event?eid=c3Q0dms5a2lmZnM2cmFzcmwzMmU0YTdhbG8gZ2RhdGEub3BzLmRlbW9AbQ'
    title='alternate'></link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/st4vk9kiffs6rasrl32e4a7alo'>
    </link>
    <link rel='edit' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/st4vk9kiffs6rasrl32e4a7alo/63310109146'>
    </link>
    <author>
      <name>GData Ops Demo</name>
      <email>gdata.ops.demo@gmail.com</email>
    </author>
    <gCal:sendEventNotifications value='false'>
    </gCal:sendEventNotifications>
    <gd:eventStatus value='http://schemas.google.com/g/2005#event.confirmed'>
    </gd:eventStatus>
    <gd:comments>
      <gd:feedLink href='http://www.google.com/calendar/feeds/default/private/full/st4vk9kiffs6rasrl32e4a7alo/comments'>
      </gd:feedLink>
    </gd:comments>
    <gd:visibility value='http://schemas.google.com/g/2005#event.default'>
    </gd:visibility>
    <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
    </gd:transparency>
    <gd:when startTime='2007-03-24T20:00:00.000-07:00'
    endTime='2007-03-24T21:00:00.000-07:00'>
      <gd:reminder minutes='10'></gd:reminder>
    </gd:when>
    <gd:where></gd:where>
  </entry>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/private/full/ofl1e45ubtsoh6gtu127cls2oo</id>
    <published>2007-03-20T21:24:43.000Z</published>
    <updated>2007-03-20T21:25:08.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
    <title type='text'>Dinner with Kim and Sarah</title>
    <content type='text'></content>
    <link rel='alternate' type='text/html'
    href='http://www.google.com/calendar/event?eid=b2ZsMWU0NXVidHNvaDZndHUxMjdjbHMyb28gZ2RhdGEub3BzLmRlbW9AbQ'
    title='alternate'></link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/ofl1e45ubtsoh6gtu127cls2oo'>
    </link>
    <link rel='edit' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/ofl1e45ubtsoh6gtu127cls2oo/63310109108'>
    </link>
    <author>
      <name>GData Ops Demo</name>
      <email>gdata.ops.demo@gmail.com</email>
    </author>
    <gCal:sendEventNotifications value='false'>
    </gCal:sendEventNotifications>
    <gd:eventStatus value='http://schemas.google.com/g/2005#event.confirmed'>
    </gd:eventStatus>
    <gd:comments>
      <gd:feedLink href='http://www.google.com/calendar/feeds/default/private/full/ofl1e45ubtsoh6gtu127cls2oo/comments'>
      </gd:feedLink>
    </gd:comments>
    <gd:visibility value='http://schemas.google.com/g/2005#event.default'>
    </gd:visibility>
    <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
    </gd:transparency>
    <gd:when startTime='2007-03-20T19:00:00.000-07:00'
    endTime='2007-03-20T21:30:00.000-07:00'>
      <gd:reminder minutes='10'></gd:reminder>
    </gd:when>
    <gd:where></gd:where>
  </entry>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/private/full/b69s2avfi2joigsclecvjlc91g</id>
    <published>2007-03-20T21:24:19.000Z</published>
    <updated>2007-03-20T21:25:05.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
    <title type='text'>Dinner with Jane and John</title>
    <content type='text'></content>
    <link rel='alternate' type='text/html'
    href='http://www.google.com/calendar/event?eid=YjY5czJhdmZpMmpvaWdzY2xlY3ZqbGM5MWcgZ2RhdGEub3BzLmRlbW9AbQ'
    title='alternate'></link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/b69s2avfi2joigsclecvjlc91g'>
    </link>
    <link rel='edit' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/b69s2avfi2joigsclecvjlc91g/63310109105'>
    </link>
    <author>
      <name>GData Ops Demo</name>
      <email>gdata.ops.demo@gmail.com</email>
    </author>
    <gCal:sendEventNotifications value='false'>
    </gCal:sendEventNotifications>
    <gd:eventStatus value='http://schemas.google.com/g/2005#event.confirmed'>
    </gd:eventStatus>
    <gd:comments>
      <gd:feedLink href='http://www.google.com/calendar/feeds/default/private/full/b69s2avfi2joigsclecvjlc91g/comments'>
      </gd:feedLink>
    </gd:comments>
    <gd:visibility value='http://schemas.google.com/g/2005#event.default'>
    </gd:visibility>
    <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
    </gd:transparency>
    <gd:when startTime='2007-03-22T17:00:00.000-07:00'
    endTime='2007-03-22T19:30:00.000-07:00'>
      <gd:reminder minutes='10'></gd:reminder>
    </gd:when>
    <gd:where></gd:where>
  </entry>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/private/full/u9p66kkiotn8bqh9k7j4rcnjjc</id>
    <published>2007-03-20T21:24:33.000Z</published>
    <updated>2007-03-20T21:24:33.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
    <title type='text'>Tennis with Elizabeth</title>
    <content type='text'></content>
    <link rel='alternate' type='text/html'
    href='http://www.google.com/calendar/event?eid=dTlwNjZra2lvdG44YnFoOWs3ajRyY25qamMgZ2RhdGEub3BzLmRlbW9AbQ'
    title='alternate'></link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/u9p66kkiotn8bqh9k7j4rcnjjc'>
    </link>
    <link rel='edit' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/u9p66kkiotn8bqh9k7j4rcnjjc/63310109073'>
    </link>
    <author>
      <name>GData Ops Demo</name>
      <email>gdata.ops.demo@gmail.com</email>
    </author>
    <gCal:sendEventNotifications value='false'>
    </gCal:sendEventNotifications>
    <gd:eventStatus value='http://schemas.google.com/g/2005#event.confirmed'>
    </gd:eventStatus>
    <gd:comments>
      <gd:feedLink href='http://www.google.com/calendar/feeds/default/private/full/u9p66kkiotn8bqh9k7j4rcnjjc/comments'>
      </gd:feedLink>
    </gd:comments>
    <gd:visibility value='http://schemas.google.com/g/2005#event.default'>
    </gd:visibility>
    <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
    </gd:transparency>
    <gd:when startTime='2007-03-24T10:00:00.000-07:00'
    endTime='2007-03-24T11:00:00.000-07:00'>
      <gd:reminder minutes='10'></gd:reminder>
    </gd:when>
    <gd:where></gd:where>
  </entry>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/private/full/76oj2kceidob3s708tvfnuaq3c</id>
    <published>2007-03-20T21:24:00.000Z</published>
    <updated>2007-03-20T21:24:00.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
    <title type='text'>Lunch with Jenn</title>
    <content type='text'></content>
    <link rel='alternate' type='text/html'
    href='http://www.google.com/calendar/event?eid=NzZvajJrY2VpZG9iM3M3MDh0dmZudWFxM2MgZ2RhdGEub3BzLmRlbW9AbQ'
    title='alternate'></link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/76oj2kceidob3s708tvfnuaq3c'>
    </link>
    <link rel='edit' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/76oj2kceidob3s708tvfnuaq3c/63310109040'>
    </link>
    <author>
      <name>GData Ops Demo</name>
      <email>gdata.ops.demo@gmail.com</email>
    </author>
    <gCal:sendEventNotifications value='false'>
    </gCal:sendEventNotifications>
    <gd:eventStatus value='http://schemas.google.com/g/2005#event.confirmed'>
    </gd:eventStatus>
    <gd:comments>
      <gd:feedLink href='http://www.google.com/calendar/feeds/default/private/full/76oj2kceidob3s708tvfnuaq3c/comments'>
      </gd:feedLink>
    </gd:comments>
    <gd:visibility value='http://schemas.google.com/g/2005#event.default'>
    </gd:visibility>
    <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
    </gd:transparency>
    <gd:when startTime='2007-03-20T11:30:00.000-07:00'
    endTime='2007-03-20T12:30:00.000-07:00'>
      <gd:reminder minutes='10'></gd:reminder>
    </gd:when>
    <gd:where></gd:where>
  </entry>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/private/full/5np9ec8m7uoauk1vedh5mhodco</id>
    <published>2007-03-20T07:50:02.000Z</published>
    <updated>2007-03-20T20:39:26.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
    <title type='text'>test entry</title>
    <content type='text'>test desc</content>
    <link rel='alternate' type='text/html'
    href='http://www.google.com/calendar/event?eid=NW5wOWVjOG03dW9hdWsxdmVkaDVtaG9kY28gZ2RhdGEub3BzLmRlbW9AbQ'
    title='alternate'></link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/5np9ec8m7uoauk1vedh5mhodco'>
    </link>
    <link rel='edit' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/5np9ec8m7uoauk1vedh5mhodco/63310106366'>
    </link>
    <author>
      <name>GData Ops Demo</name>
      <email>gdata.ops.demo@gmail.com</email>
    </author>
    <gCal:sendEventNotifications value='false'>
    </gCal:sendEventNotifications>
    <gd:eventStatus value='http://schemas.google.com/g/2005#event.confirmed'>
    </gd:eventStatus>
    <gd:comments>
      <gd:feedLink href='http://www.google.com/calendar/feeds/default/private/full/5np9ec8m7uoauk1vedh5mhodco/comments'>
      </gd:feedLink>
    </gd:comments>
    <gd:visibility value='http://schemas.google.com/g/2005#event.private'>
    </gd:visibility>
    <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
    </gd:transparency>
    <gd:who rel='http://schemas.google.com/g/2005#event.attendee'
    valueString='Vivian Li' email='vli@google.com'>
      <gd:attendeeStatus value='http://schemas.google.com/g/2005#event.declined'>
      </gd:attendeeStatus>
    </gd:who>
    <gd:who rel='http://schemas.google.com/g/2005#event.organizer'
    valueString='GData Ops Demo' email='gdata.ops.demo@gmail.com'>
      <gd:attendeeStatus value='http://schemas.google.com/g/2005#event.accepted'>
      </gd:attendeeStatus>
    </gd:who>
    <gd:when startTime='2007-03-21T08:00:00.000-07:00'
    endTime='2007-03-21T09:00:00.000-07:00'>
      <gd:reminder minutes='10'></gd:reminder>
    </gd:when>
    <gd:where valueString='anywhere'></gd:where>
  </entry>
  <entry>
    <id>
    http://www.google.com/calendar/feeds/default/private/full/fu6sl0rqakf3o0a13oo1i1a1mg</id>
    <published>2007-02-14T23:23:37.000Z</published>
    <updated>2007-02-14T23:25:30.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
    <title type='text'>test</title>
    <content type='text'></content>
    <link rel='alternate' type='text/html'
    href='http://www.google.com/calendar/event?eid=ZnU2c2wwcnFha2YzbzBhMTNvbzFpMWExbWcgZ2RhdGEub3BzLmRlbW9AbQ'
    title='alternate'></link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/fu6sl0rqakf3o0a13oo1i1a1mg'>
    </link>
    <link rel='edit' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/full/fu6sl0rqakf3o0a13oo1i1a1mg/63307178730'>
    </link>
    <author>
      <name>GData Ops Demo</name>
      <email>gdata.ops.demo@gmail.com</email>
    </author>
    <gCal:sendEventNotifications value='false'>
    </gCal:sendEventNotifications>
    <gd:eventStatus value='http://schemas.google.com/g/2005#event.confirmed'>
    </gd:eventStatus>
    <gd:comments>
      <gd:feedLink href='http://www.google.com/calendar/feeds/default/private/full/fu6sl0rqakf3o0a13oo1i1a1mg/comments'>
      </gd:feedLink>
    </gd:comments>
    <gd:visibility value='http://schemas.google.com/g/2005#event.default'>
    </gd:visibility>
    <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
    </gd:transparency>
    <gd:when startTime='2007-02-15T08:30:00.000-08:00'
    endTime='2007-02-15T09:30:00.000-08:00'>
      <gd:reminder minutes='10'></gd:reminder>
    </gd:when>
    <gd:where></gd:where>
  </entry>
</feed>
"""

GBASE_ATTRIBUTE_FEED = """<?xml version='1.0' encoding='UTF-8'?>
    <feed xmlns='http://www.w3.org/2005/Atom' xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/' xmlns:gm='http://base.google.com/ns-metadata/1.0'>
      <id>http://www.google.com/base/feeds/attributes</id>
      <updated>2006-11-01T20:35:59.578Z</updated>
      <category scheme='http://base.google.com/categories/itemtypes' term='online jobs'></category>
      <category scheme='http://base.google.com/categories/itemtypes' term='jobs'></category>
      <title type='text'>Attribute histogram for query: [item type:jobs]</title>
      <link rel='alternate' type='text/html' href='http://base.google.com'></link>
      <link rel='http://schemas.google.com/g/2005#feed' type='application/atom+xml' href='http://www.google.com/base/feeds/attributes'></link>
      <link rel='self' type='application/atom+xml' href='http://www.google.com/base/feeds/attributes/-/jobs'></link>
      <generator version='1.0' uri='http://base.google.com'>GoogleBase</generator>
      <openSearch:totalResults>16</openSearch:totalResults>
      <openSearch:startIndex>1</openSearch:startIndex>
      <openSearch:itemsPerPage>16</openSearch:itemsPerPage>
      <entry>
        <id>http://www.google.com/base/feeds/attributes/job+industry%28text%29N%5Bitem+type%3Ajobs%5D</id>
        <updated>2006-11-01T20:36:00.100Z</updated>
        <title type='text'>job industry(text)</title>
        <content type='text'>Attribute"job industry" of type text.
        </content>
        <link rel='self' type='application/atom+xml' href='http://www.google.com/base/feeds/attributes/job+industry%28text%29N%5Bitem+type%3Ajobs%5D'></link>
        <gm:attribute name='job industry' type='text' count='4416629'>
          <gm:value count='380772'>it internet</gm:value>
          <gm:value count='261565'>healthcare</gm:value>
          <gm:value count='142018'>information technology</gm:value>
          <gm:value count='124622'>accounting</gm:value>
          <gm:value count='111311'>clerical and administrative</gm:value>
          <gm:value count='82928'>other</gm:value>
          <gm:value count='77620'>sales and sales management</gm:value>
          <gm:value count='68764'>information systems</gm:value>
          <gm:value count='65859'>engineering and architecture</gm:value>
          <gm:value count='64757'>sales</gm:value>
        </gm:attribute>
      </entry>
    </feed>
"""


GBASE_ATTRIBUTE_ENTRY = """<?xml version='1.0' encoding='UTF-8'?>
 <entry xmlns='http://www.w3.org/2005/Atom' xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/' xmlns:gm='http://base.google.com/ns-metadata/1.0'>
        <id>http://www.google.com/base/feeds/attributes/job+industry%28text%29N%5Bitem+type%3Ajobs%5D</id>
        <updated>2006-11-01T20:36:00.100Z</updated>
        <title type='text'>job industry(text)</title>
        <content type='text'>Attribute"job industry" of type text.
        </content>
        <link rel='self' type='application/atom+xml' href='http://www.google.com/base/feeds/attributes/job+industry%28text%29N%5Bitem+type%3Ajobs%5D'></link>
        <gm:attribute name='job industry' type='text' count='4416629'>
          <gm:value count='380772'>it internet</gm:value>
          <gm:value count='261565'>healthcare</gm:value>
          <gm:value count='142018'>information technology</gm:value>
          <gm:value count='124622'>accounting</gm:value>
          <gm:value count='111311'>clerical and administrative</gm:value>
          <gm:value count='82928'>other</gm:value>
          <gm:value count='77620'>sales and sales management</gm:value>
          <gm:value count='68764'>information systems</gm:value>
          <gm:value count='65859'>engineering and architecture</gm:value>
          <gm:value count='64757'>sales</gm:value>
        </gm:attribute>
      </entry>
""" 

GBASE_LOCALES_FEED = """<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom'
      xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/'
      xmlns:gm='http://base.google.com/ns-metadata/1.0'>
         <id> http://www.google.com/base/feeds/locales/</id>
  <updated>2006-06-13T18:11:40.120Z</updated>
  <title type="text">Locales</title> 
  <link rel="alternate" type="text/html" href="http://base.google.com"/>
  <link rel="http://schemas.google.com/g/2005#feed" type="application/atom+xml"

       href="http://www.google.com/base/feeds/locales/"/>
  <link rel="self" type="application/atom+xml" href="http://www.google.com/base/feeds/locales/"/>
         <author>
    <name>Google Inc.</name>
    <email>base@google.com</email>
  </author>
  <generator version="1.0" uri="http://base.google.com">GoogleBase</generator>
  <openSearch:totalResults>3</openSearch:totalResults>
  <openSearch:itemsPerPage>25</openSearch:itemsPerPage>

<entry>
  <id>http://www.google.com/base/feeds/locales/en_US</id>
  <updated>2006-03-27T22:27:36.658Z</updated>
  <category scheme="http://base.google.com/categories/locales" term="en_US"/>

  <title type="text">en_US</title>
  <content type="text">en_US</content>
  <link rel="self" type="application/atom+xml" 
     href="http://www.google.com/base/feeds/locales/en_US"></link>

  <link rel="related" type="application/atom+xml" 
     href="http://www.google.com/base/feeds/itemtypes/en_US" title="Item types in en_US"/>
</entry>
<entry>
         <id>http://www.google.com/base/feeds/locales/en_GB</id>
  <updated>2006-06-13T18:14:18.601Z</updated>
  <category scheme="http://base.google.com/categories/locales" term="en_GB"/>
  <title type="text">en_GB</title>
  <content type="text">en_GB</content>
  <link rel="related" type="application/atom+xml" 
     href="http://www.google.com/base/feeds/itemtypes/en_GB" title="Item types in en_GB"/>
  <link rel="self" type="application/atom+xml" 
     href="http://www.google.com/base/feeds/locales/en_GB"/>
</entry>
<entry>
  <id>http://www.google.com/base/feeds/locales/de_DE</id>
  <updated>2006-06-13T18:14:18.601Z</updated>
  <category scheme="http://base.google.com/categories/locales" term="de_DE"/>
  <title type="text">de_DE</title>
  <content type="text">de_DE</content>
  <link rel="related" type="application/atom+xml" 
     href="http://www.google.com/base/feeds/itemtypes/de_DE" title="Item types in de_DE"/>
  <link rel="self" type="application/atom+xml" 
     href="http://www.google.com/base/feeds/locales/de_DE"/>
</entry>
</feed>"""

RECURRENCE_EXCEPTION_ENTRY = """<entry xmlns='http://www.w3.org/2005/Atom'
xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/'
xmlns:gd='http://schemas.google.com/g/2005'
xmlns:gCal='http://schemas.google.com/gCal/2005'>
    <id>
    http://www.google.com/calendar/feeds/default/private/composite/i7lgfj69mjqjgnodklif3vbm7g</id>
    <published>2007-04-05T21:51:49.000Z</published>
    <updated>2007-04-05T21:51:49.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/g/2005#event'></category>
    <title type='text'>testDavid</title>
    <content type='text'></content>
    <link rel='alternate' type='text/html'
    href='http://www.google.com/calendar/event?eid=aTdsZ2ZqNjltanFqZ25vZGtsaWYzdmJtN2dfMjAwNzA0MDNUMTgwMDAwWiBnZGF0YS5vcHMudGVzdEBt'
    title='alternate'></link>
    <link rel='self' type='application/atom+xml'
    href='http://www.google.com/calendar/feeds/default/private/composite/i7lgfj69mjqjgnodklif3vbm7g'>
    </link>
    <author>
      <name>gdata ops</name>
      <email>gdata.ops.test@gmail.com</email>
    </author>
    <gd:visibility value='http://schemas.google.com/g/2005#event.default'>
    </gd:visibility>
    <gCal:sendEventNotifications value='true'>
    </gCal:sendEventNotifications>
    <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
    </gd:transparency>
    <gd:eventStatus value='http://schemas.google.com/g/2005#event.confirmed'>
    </gd:eventStatus>
    <gd:recurrence>DTSTART;TZID=America/Anchorage:20070403T100000
    DTEND;TZID=America/Anchorage:20070403T110000
    RRULE:FREQ=DAILY;UNTIL=20070408T180000Z;WKST=SU
    EXDATE;TZID=America/Anchorage:20070407T100000
    EXDATE;TZID=America/Anchorage:20070405T100000
    EXDATE;TZID=America/Anchorage:20070404T100000 BEGIN:VTIMEZONE
    TZID:America/Anchorage X-LIC-LOCATION:America/Anchorage
    BEGIN:STANDARD TZOFFSETFROM:-0800 TZOFFSETTO:-0900 TZNAME:AKST
    DTSTART:19701025T020000 RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
    END:STANDARD BEGIN:DAYLIGHT TZOFFSETFROM:-0900 TZOFFSETTO:-0800
    TZNAME:AKDT DTSTART:19700405T020000
    RRULE:FREQ=YEARLY;BYMONTH=4;BYDAY=1SU END:DAYLIGHT
    END:VTIMEZONE</gd:recurrence>
    <gd:where valueString=''></gd:where>
    <gd:reminder minutes='10'></gd:reminder>
    <gd:recurrenceException specialized='true'>
      <gd:entryLink>
        <entry>
          <id>i7lgfj69mjqjgnodklif3vbm7g_20070407T180000Z</id>
          <published>2007-04-05T21:51:49.000Z</published>
          <updated>2007-04-05T21:52:58.000Z</updated>
          <category scheme='http://schemas.google.com/g/2005#kind'
          term='http://schemas.google.com/g/2005#event'></category>
          <title type='text'>testDavid</title>
          <content type='text'></content>
          <link rel='alternate' type='text/html'
          href='http://www.google.com/calendar/event?eid=aTdsZ2ZqNjltanFqZ25vZGtsaWYzdmJtN2dfMjAwNzA0MDdUMTgwMDAwWiBnZGF0YS5vcHMudGVzdEBt'
          title='alternate'></link>
          <author>
            <name>gdata ops</name>
            <email>gdata.ops.test@gmail.com</email>
          </author>
          <gd:visibility value='http://schemas.google.com/g/2005#event.default'>
          </gd:visibility>
          <gd:originalEvent id='i7lgfj69mjqjgnodklif3vbm7g'
          href='http://www.google.com/calendar/feeds/default/private/composite/i7lgfj69mjqjgnodklif3vbm7g'>

            <gd:when startTime='2007-04-07T13:00:00.000-05:00'>
            </gd:when>
          </gd:originalEvent>
          <gCal:sendEventNotifications value='false'>
          </gCal:sendEventNotifications>
          <gd:transparency value='http://schemas.google.com/g/2005#event.opaque'>
          </gd:transparency>
          <gd:eventStatus value='http://schemas.google.com/g/2005#event.canceled'>
          </gd:eventStatus>
          <gd:comments>
            <gd:feedLink href='http://www.google.com/calendar/feeds/default/private/full/i7lgfj69mjqjgnodklif3vbm7g_20070407T180000Z/comments'>

              <feed>
                <updated>2007-04-05T21:54:09.285Z</updated>
                <category scheme='http://schemas.google.com/g/2005#kind'
                term='http://schemas.google.com/g/2005#message'>
                </category>
                <title type='text'>Comments for: testDavid</title>
                <link rel='alternate' type='text/html'
                href='http://www.google.com/calendar/feeds/default/private/full/i7lgfj69mjqjgnodklif3vbm7g_20070407T180000Z/comments'
                title='alternate'></link>
              </feed>
            </gd:feedLink>
          </gd:comments>
          <gd:when startTime='2007-04-07T13:00:00.000-05:00'
          endTime='2007-04-07T14:00:00.000-05:00'>
            <gd:reminder minutes='10'></gd:reminder>
          </gd:when>
          <gd:where valueString=''></gd:where>
        </entry>
      </gd:entryLink>
    </gd:recurrenceException>
  </entry>"""

NICK_ENTRY = """<?xml version="1.0" encoding="UTF-8"?>
<atom:entry xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:apps="http://schemas.google.com/apps/2006"
  xmlns:gd="http://schemas.google.com/g/2005">
  <atom:id>https://www.google.com/a/feeds/example.com/nickname/2.0/Foo</atom:id>
  <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
  <atom:category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/apps/2006#nickname'/>
  <atom:title type="text">Foo</atom:title>
  <atom:link rel="self" type="application/atom+xml"
    href="https://www.google.com/a/feeds/example.com/nickname/2.0/Foo"/>
  <atom:link rel="edit" type="application/atom+xml"
    href="https://www.google.com/a/feeds/example.com/nickname/2.0/Foo"/>
  <apps:nickname name="Foo"/>
  <apps:login userName="TestUser"/>
</atom:entry>"""

NICK_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<atom:feed xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:openSearch="http://a9.com/-/spec/opensearchrss/1.0/"
  xmlns:apps="http://schemas.google.com/apps/2006">
  <atom:id>
    http://www.google.com/a/feeds/example.com/nickname/2.0
  </atom:id>
  <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
  <atom:category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/apps/2006#nickname'/>
  <atom:title type="text">Nicknames for user SusanJones</atom:title>
  <atom:link rel='http://schemas.google.com/g/2005#feed'
    type="application/atom+xml"
    href="http://www.google.com/a/feeds/example.com/nickname/2.0"/>
  <atom:link rel='http://schemas.google.com/g/2005#post'
    type="application/atom+xml"
    href="http://www.google.com/a/feeds/example.com/nickname/2.0"/>
  <atom:link rel="self" type="application/atom+xml"
    href="http://www.google.com/a/feeds/example.com/nickname/2.0?username=TestUser"/>
  <openSearch:startIndex>1</openSearch:startIndex>
  <openSearch:itemsPerPage>2</openSearch:itemsPerPage>
  <atom:entry>
    <atom:id>
      http://www.google.com/a/feeds/example.com/nickname/2.0/Foo
    </atom:id>
    <atom:category scheme='http://schemas.google.com/g/2005#kind'
      term='http://schemas.google.com/apps/2006#nickname'/>
    <atom:title type="text">Foo</atom:title>
    <atom:link rel="self" type="application/atom+xml"
      href="http://www.google.com/a/feeds/example.com/nickname/2.0/Foo"/>
    <atom:link rel="edit" type="application/atom+xml"
      href="http://www.google.com/a/feeds/example.com/nickname/2.0/Foo"/>
    <apps:nickname name="Foo"/>
    <apps:login userName="TestUser"/>
  </atom:entry>
  <atom:entry>
    <atom:id>
      http://www.google.com/a/feeds/example.com/nickname/2.0/suse
    </atom:id>
    <atom:category scheme='http://schemas.google.com/g/2005#kind'
      term='http://schemas.google.com/apps/2006#nickname'/>
    <atom:title type="text">suse</atom:title>
    <atom:link rel="self" type="application/atom+xml"
      href="http://www.google.com/a/feeds/example.com/nickname/2.0/Bar"/>
    <atom:link rel="edit" type="application/atom+xml"
      href="http://www.google.com/a/feeds/example.com/nickname/2.0/Bar"/>
    <apps:nickname name="Bar"/>
    <apps:login userName="TestUser"/>
  </atom:entry>
</atom:feed>"""

USER_ENTRY = """<?xml version="1.0" encoding="UTF-8"?>
<atom:entry xmlns:atom="http://www.w3.org/2005/Atom"
            xmlns:apps="http://schemas.google.com/apps/2006"
            xmlns:gd="http://schemas.google.com/g/2005">
  <atom:id>https://www.google.com/a/feeds/example.com/user/2.0/TestUser</atom:id>
  <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
  <atom:category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/apps/2006#user'/>
  <atom:title type="text">TestUser</atom:title>
  <atom:link rel="self" type="application/atom+xml"
    href="https://www.google.com/a/feeds/example.com/user/2.0/TestUser"/>
  <atom:link rel="edit" type="application/atom+xml"
    href="https://www.google.com/a/feeds/example.com/user/2.0/TestUser"/>
  <apps:login userName="TestUser" password="password" suspended="false"
    ipWhitelisted='false' hashFunctionName="SHA-1"/>
  <apps:name familyName="Test" givenName="User"/>
  <apps:quota limit="1024"/>
  <gd:feedLink rel='http://schemas.google.com/apps/2006#user.nicknames'
    href="https://www.google.com/a/feeds/example.com/nickname/2.0?username=Test-3121"/>
  <gd:feedLink rel='http://schemas.google.com/apps/2006#user.emailLists'
    href="https://www.google.com/a/feeds/example.com/emailList/2.0?recipient=testlist@example.com"/>
</atom:entry>"""

USER_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<atom:feed xmlns:atom="http://www.w3.org/2005/Atom" 
  xmlns:apps="http://schemas.google.com/apps/2006"
  xmlns:openSearch="http://a9.com/-/spec/opensearchrss/1.0/"
  xmlns:gd="http://schemas.google.com/g/2005">
    <atom:id>
        http://www.google.com/a/feeds/example.com/user/2.0
    </atom:id>
    <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
    <atom:category scheme='http://schemas.google.com/g/2005#kind' 
        term='http://schemas.google.com/apps/2006#user'/>
    <atom:title type="text">Users</atom:title>
    <atom:link rel="next" type="application/atom+xml" 
        href="http://www.google.com/a/feeds/example.com/user/2.0?startUsername=john"/>
    <atom:link rel='http://schemas.google.com/g/2005#feed' 
        type="application/atom+xml" 
        href="http://www.google.com/a/feeds/example.com/user/2.0"/>
    <atom:link rel='http://schemas.google.com/g/2005#post'
        type="application/atom+xml"
        href="http://www.google.com/a/feeds/example.com/user/2.0"/>
    <atom:link rel="self" type="application/atom+xml" 
        href="http://www.google.com/a/feeds/example.com/user/2.0"/>
    <openSearch:startIndex>1</openSearch:startIndex>
    <atom:entry>
        <atom:id>
            http://www.google.com/a/feeds/example.com/user/2.0/TestUser
        </atom:id>
        <atom:category scheme='http://schemas.google.com/g/2005#kind'
            term='http://schemas.google.com/apps/2006#user'/>
        <atom:title type="text">TestUser</atom:title>
        <atom:link rel="self" type="application/atom+xml" 
            href="http://www.google.com/a/feeds/example.com/user/2.0/TestUser"/>
        <atom:link rel="edit" type="application/atom+xml"
            href="http://www.google.com/a/feeds/example.com/user/2.0/TestUser"/>
        <gd:who rel='http://schemas.google.com/apps/2006#user.recipient' 
            email="TestUser@example.com"/>
        <apps:login userName="TestUser" suspended="false"/>
        <apps:quota limit="2048"/>
        <apps:name familyName="Test" givenName="User"/>
        <gd:feedLink rel='http://schemas.google.com/apps/2006#user.nicknames'
            href="http://www.google.com/a/feeds/example.com/nickname/2.0?username=TestUser"/>
        <gd:feedLink rel='http://schemas.google.com/apps/2006#user.emailLists'
            href="http://www.google.com/a/feeds/example.com/emailList/2.0?recipient=TestUser@example.com"/>
    </atom:entry>
    <atom:entry>
        <atom:id>
            http://www.google.com/a/feeds/example.com/user/2.0/JohnSmith
        </atom:id>
        <atom:category scheme='http://schemas.google.com/g/2005#kind'
            term='http://schemas.google.com/apps/2006#user'/>
        <atom:title type="text">JohnSmith</atom:title>
        <atom:link rel="self" type="application/atom+xml" 
            href="http://www.google.com/a/feeds/example.com/user/2.0/JohnSmith"/>
        <atom:link rel="edit" type="application/atom+xml"
            href="http://www.google.com/a/feeds/example.com/user/2.0/JohnSmith"/>
        <gd:who rel='http://schemas.google.com/apps/2006#user.recipient'
            email="JohnSmith@example.com"/>
        <apps:login userName="JohnSmith" suspended="false"/>
        <apps:quota limit="2048"/>
        <apps:name familyName="Smith" givenName="John"/>
        <gd:feedLink rel='http://schemas.google.com/apps/2006#user.nicknames'
            href="http://www.google.com/a/feeds/example.com/nickname/2.0?username=JohnSmith"/>
        <gd:feedLink rel='http://schemas.google.com/apps/2006#user.emailLists'
            href="http://www.google.com/a/feeds/example.com/emailList/2.0?recipient=JohnSmith@example.com"/>
    </atom:entry>
</atom:feed>"""

EMAIL_LIST_ENTRY = """<?xml version="1.0" encoding="UTF-8"?>
<atom:entry xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:apps="http://schemas.google.com/apps/2006"
  xmlns:gd="http://schemas.google.com/g/2005">
    <atom:id>
      https://www.google.com/a/feeds/example.com/emailList/2.0/testlist
    </atom:id>
    <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
    <atom:category scheme='http://schemas.google.com/g/2005#kind'
      term='http://schemas.google.com/apps/2006#emailList'/>
    <atom:title type="text">testlist</atom:title>
    <atom:link rel="self" type="application/atom+xml" 
      href="https://www.google.com/a/feeds/example.com/emailList/2.0/testlist"/>
    <atom:link rel="edit" type="application/atom+xml" 
      href="https://www.google.com/a/feeds/example.com/emailList/2.0/testlist"/>
    <apps:emailList name="testlist"/>
    <gd:feedLink rel='http://schemas.google.com/apps/2006#emailList.recipients'
        href="http://www.google.com/a/feeds/example.com/emailList/2.0/testlist/recipient/"/>
</atom:entry>"""

EMAIL_LIST_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<atom:feed xmlns:atom="http://www.w3.org/2005/Atom" 
  xmlns:openSearch="http://a9.com/-/spec/opensearchrss/1.0/"
  xmlns:apps="http://schemas.google.com/apps/2006"
  xmlns:gd="http://schemas.google.com/g/2005">
    <atom:id>
        http://www.google.com/a/feeds/example.com/emailList/2.0
    </atom:id>
    <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
    <atom:category scheme='http://schemas.google.com/g/2005#kind'
        term='http://schemas.google.com/apps/2006#emailList'/>
    <atom:title type="text">EmailLists</atom:title>
    <atom:link rel="next" type="application/atom+xml" 
        href="http://www.google.com/a/feeds/example.com/emailList/2.0?startEmailListName=john"/>
    <atom:link rel='http://schemas.google.com/g/2005#feed'
        type="application/atom+xml" 
        href="http://www.google.com/a/feeds/example.com/emailList/2.0"/>
    <atom:link rel='http://schemas.google.com/g/2005#post' 
        type="application/atom+xml"
        href="http://www.google.com/a/feeds/example.com/emailList/2.0"/>
    <atom:link rel="self" type="application/atom+xml" 
        href="http://www.google.com/a/feeds/example.com/emailList/2.0"/>
    <openSearch:startIndex>1</openSearch:startIndex>
    <atom:entry>
        <atom:id>
            http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales
        </atom:id>
        <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
        <atom:category scheme='http://schemas.google.com/g/2005#kind'
            term='http://schemas.google.com/apps/2006#emailList'/>
        <atom:title type="text">us-sales</atom:title>
        <atom:link rel="self" type="application/atom+xml" 
            href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales"/>
        <atom:link rel="edit" type="application/atom+xml"
            href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales"/>
        <apps:emailList name="us-sales"/>
        <gd:feedLink rel='http://schemas.google.com/apps/2006#emailList.recipients'
            href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient/"/>
    </atom:entry>
    <atom:entry>
        <atom:id>
            http://www.google.com/a/feeds/example.com/emailList/2.0/us-eng
        </atom:id>
        <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
        <atom:category scheme='http://schemas.google.com/g/2005#kind'
            term='http://schemas.google.com/apps/2006#emailList'/>
        <atom:title type="text">us-eng</atom:title>
        <atom:link rel="self" type="application/atom+xml" 
            href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-eng"/>
        <atom:link rel="edit" type="application/atom+xml"
            href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-eng"/>
        <apps:emailList name="us-eng"/>
        <gd:feedLink rel='http://schemas.google.com/apps/2006#emailList.recipients'
            href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-eng/recipient/"/>
    </atom:entry>
</atom:feed>"""

EMAIL_LIST_RECIPIENT_ENTRY = """<?xml version="1.0" encoding="UTF-8"?>
<atom:entry xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:apps="http://schemas.google.com/apps/2006"
  xmlns:gd="http://schemas.google.com/g/2005">
    <atom:id>https://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient/TestUser%40example.com</atom:id>
    <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
    <atom:category scheme='http://schemas.google.com/g/2005#kind'
        term='http://schemas.google.com/apps/2006#emailList.recipient'/>
    <atom:title type="text">TestUser</atom:title>
    <atom:link rel="self" type="application/atom+xml" 
        href="https://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient/TestUser%40example.com"/>
    <atom:link rel="edit" type="application/atom+xml" 
        href="https://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient/TestUser%40example.com"/>
    <gd:who email="TestUser@example.com"/>
</atom:entry>"""

EMAIL_LIST_RECIPIENT_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<atom:feed xmlns:atom="http://www.w3.org/2005/Atom" 
  xmlns:openSearch="http://a9.com/-/spec/opensearchrss/1.0/"
  xmlns:gd="http://schemas.google.com/g/2005">
    <atom:id>
        http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient
    </atom:id>
    <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
    <atom:category scheme='http://schemas.google.com/g/2005#kind'
        term='http://schemas.google.com/apps/2006#emailList.recipient'/>
    <atom:title type="text">Recipients for email list us-sales</atom:title>
    <atom:link rel="next" type="application/atom+xml" 
        href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient/?startRecipient=terry@example.com"/>
    <atom:link rel='http://schemas.google.com/g/2005#feed'
        type="application/atom+xml" 
        href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient"/>
    <atom:link rel='http://schemas.google.com/g/2005#post'
        type="application/atom+xml"
        href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient"/>
    <atom:link rel="self" type="application/atom+xml" 
        href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient"/>
    <openSearch:startIndex>1</openSearch:startIndex>
    <atom:entry>
        <atom:id>
            http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient/joe%40example.com
        </atom:id>
        <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
        <atom:category scheme='http://schemas.google.com/g/2005#kind'
            term='http://schemas.google.com/apps/2006#emailList.recipient'/>
        <atom:title type="text">joe@example.com</atom:title>
        <atom:link rel="self" type="application/atom+xml" 
            href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient/joe%40example.com"/>
        <atom:link rel="edit" type="application/atom+xml"
            href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient/joe%40example.com"/>
        <gd:who email="joe@example.com"/>
    </atom:entry>
    <atom:entry>
        <atom:id>
            http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient/susan%40example.com
        </atom:id>
        <atom:updated>1970-01-01T00:00:00.000Z</atom:updated>
        <atom:category scheme='http://schemas.google.com/g/2005#kind'
            term='http://schemas.google.com/apps/2006#emailList.recipient'/>
        <atom:title type="text">susan@example.com</atom:title>
        <atom:link rel="self" type="application/atom+xml" 
            href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient/susan%40example.com"/>
        <atom:link rel="edit" type="application/atom+xml"
            href="http://www.google.com/a/feeds/example.com/emailList/2.0/us-sales/recipient/susan%40example.com"/>
        <gd:who email="susan@example.com"/>
    </atom:entry>
</atom:feed>"""

ACL_FEED = """<?xml version='1.0' encoding='UTF-8'?>
  <feed xmlns='http://www.w3.org/2005/Atom'
      xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/'
      xmlns:gAcl='http://schemas.google.com/acl/2007'>
    <id>http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full</id>
    <updated>2007-04-21T00:52:04.000Z</updated>
    <title type='text'>Elizabeth Bennet's access control list</title>
    <link rel='http://schemas.google.com/acl/2007#controlledObject'
      type='application/atom+xml'
      href='http://www.google.com/calendar/feeds/liz%40gmail.com/private/full'>
    </link>
    <link rel='http://schemas.google.com/g/2005#feed'
      type='application/atom+xml'
      href='http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full'>
    </link>
    <link rel='http://schemas.google.com/g/2005#post'
      type='application/atom+xml'
      href='http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full'>
    </link>
    <link rel='self' type='application/atom+xml'
      href='http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full'>
    </link>
    <generator version='1.0'
      uri='http://www.google.com/calendar'>Google Calendar</generator>
    <openSearch:totalResults>2</openSearch:totalResults>
    <openSearch:startIndex>1</openSearch:startIndex>
    <entry>
      <id>http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full/user%3Aliz%40gmail.com</id>
      <updated>2007-04-21T00:52:04.000Z</updated>
      <category scheme='http://schemas.google.com/g/2005#kind'
        term='http://schemas.google.com/acl/2007#accessRule'>
      </category>
      <title type='text'>owner</title>
      <content type='text'></content>
      <link rel='self' type='application/atom+xml'
        href='http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full/user%3Aliz%40gmail.com'>
      </link>
      <link rel='edit' type='application/atom+xml'
        href='http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full/user%3Aliz%40gmail.com'>
      </link>
      <author>
        <name>Elizabeth Bennet</name>
        <email>liz@gmail.com</email>
      </author>
      <gAcl:scope type='user' value='liz@gmail.com'></gAcl:scope>
      <gAcl:role value='http://schemas.google.com/gCal/2005#owner'>
      </gAcl:role>
    </entry>
    <entry>
      <id>http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full/default</id>
      <updated>2007-04-21T00:52:04.000Z</updated>
      <category scheme='http://schemas.google.com/g/2005#kind'
        term='http://schemas.google.com/acl/2007#accessRule'>
      </category>
      <title type='text'>read</title>
      <content type='text'></content>
      <link rel='self' type='application/atom+xml'
        href='http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full/default'>
      </link>
      <link rel='edit' type='application/atom+xml'
        href='http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full/default'>
      </link>
      <author>
        <name>Elizabeth Bennet</name>
        <email>liz@gmail.com</email>
      </author>
      <gAcl:scope type='default'></gAcl:scope>
      <gAcl:role value='http://schemas.google.com/gCal/2005#read'>
      </gAcl:role>
    </entry>
  </feed>"""

ACL_ENTRY = """<?xml version='1.0' encoding='UTF-8'?>
  <entry xmlns='http://www.w3.org/2005/Atom' xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/' xmlns:gd='http://schemas.google.com/g/2005' xmlns:gCal='http://schemas.google.com/gCal/2005' xmlns:gAcl='http://schemas.google.com/acl/2007'>
    <id>http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full/user%3Aliz%40gmail.com</id>
    <updated>2007-04-21T00:52:04.000Z</updated>
    <category scheme='http://schemas.google.com/g/2005#kind'
      term='http://schemas.google.com/acl/2007#accessRule'>
    </category>
    <title type='text'>owner</title>
    <content type='text'></content>
    <link rel='self' type='application/atom+xml'
      href='http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full/user%3Aliz%40gmail.com'>
    </link>
    <link rel='edit' type='application/atom+xml'
      href='http://www.google.com/calendar/feeds/liz%40gmail.com/acl/full/user%3Aliz%40gmail.com'>
    </link>
    <author>
      <name>Elizabeth Bennet</name>
      <email>liz@gmail.com</email>
    </author>
    <gAcl:scope type='user' value='liz@gmail.com'></gAcl:scope>
    <gAcl:role value='http://schemas.google.com/gCal/2005#owner'>
    </gAcl:role>
  </entry>"""
