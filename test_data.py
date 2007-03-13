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
  <id>http://www.google.com/test/id/url</id>
  <title type='text'>Testing 2000 series laptop</title>
  <content type='xhtml'>
    <div xmlns='http://www.w3.org/1999/xhtml'>A Testing Laptop</div>
  </content>
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
<generator version='1.0' uri='http://base.google.com'>GoogleBase</generator>
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
