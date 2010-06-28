'''
Created on 21.05.2010
'''
__author__ = 'seriyPS (Sergey Prokhorov)'

import unittest
try:
    from xml.etree import ElementTree
except ImportError:
    from elementtree import ElementTree
import gdata.base.service
import gdata.service
import atom.service
import gdata.base
import atom

TST_XML="""<?xml version="1.0" encoding="UTF-8"?>
    <entry  xmlns='http://www.w3.org/2005/Atom' 
            xmlns:openSearch='http://a9.com/-/spec/opensearchrss/1.0/' 
            xmlns:gm='http://base.google.com/ns-metadata/1.0'
            xmlns:g='http://base.google.com/ns/1.0'
            xmlns:batch='http://schemas.google.com/gdata/batch'>
      <id>http://www.google.com/base/feeds/snippets/3804629571624093811</id>
      <published>2010-03-28T06:55:40.000Z</published>
      <updated>2010-05-23T06:46:27.000Z</updated>
      <category scheme='http://base.google.com/categories/itemtypes' term='Products'/>
      <title type='text'>Cables to Go Ultimate iPod Companion Kit</title>
      <content type='html'>Ramp up your portable music experience and enjoyment with the Cables to Go Ultimate iPod Companion Kit. This bundle includes all the connections and accessories necessary to enjoy your iPod-compatible device on your TV or home stereo. Cables to Go  ...</content>
      <link rel='alternate' type='text/html' href='http://www.hsn.com/redirect.aspx?pfid=1072528&amp;sz=6&amp;sf=EC0210&amp;ac=GPT&amp;cm_mmc=Shopping%20Engine-_-Froogle-_-Electronics-_-5948880&amp;CAWELAID=491871036'/>
      <link rel='self' type='application/atom+xml' href='http://www.google.com/base/feeds/snippets/3804629571624093811'/>
      <author>
        <name>HSN</name>
      </author>
      <g:condition type='text'>new</g:condition>
      <g:product_type type='text'>Electronics&gt;MP3 Players&gt;iPod Accessories</g:product_type>
      <g:image_link type='url'>http://dyn-images.hsn.com/is/image/HomeShoppingNetwork/5948880w?$pd500$</g:image_link>
      <g:upc type='text'>757120355120</g:upc>
      <g:item_language type='text'>EN</g:item_language>
      <g:id type='text'>5948880</g:id>
      <g:shipping type='shipping'><g:price type='floatUnit'>7.95 usd</g:price>
        <g:country type="text">US</g:country>
      </g:shipping>
      <g:price type='floatUnit'>64.95 usd</g:price>
      <g:target_country type='text'>US</g:target_country>
      <g:expiration_date type='dateTime'>2010-06-21T00:00:00Z</g:expiration_date>
      <g:brand type='text'>Cables to Go</g:brand>
      <g:customer_id type='int'>8717</g:customer_id>
      <g:item_type type='text'>Products</g:item_type>
    </entry>
"""


class Test(unittest.TestCase):

    def testConstruct(self):
        thumb_url='http://base.googlehosted.com/base_media?q=http%3A%2F%2Fexample.com%2FEOS%2F1AEOS01008.jpg'
        
        item = gdata.base.GBaseItem()
        item.title = atom.Title(text='Olds Cutlass Supreme Oxygen O2 Sensor')
        item.link.append(atom.Link(rel='alternate', link_type='text/html',
            href='http://www.example.com/123456jsh9'))
        item.item_type = gdata.base.ItemType(text='Products')
        item.AddItemAttribute(name='price', value_type='floatUnit', value='41.94 usd')
        item.AddItemAttribute(name='id', value_type='text', value='1AEOS01008-415676-XXX')
        item.AddItemAttribute(name='quantity', value_type='int', value='5')
        attr=item.AddItemAttribute(name='image_link', value_type='url', value=None)
        attr.AddItemAttribute(name='thumb', value=thumb_url, value_type='url')
        image_attr=item.GetItemAttributes("image_link")[0]
        self.assert_(isinstance(image_attr, gdata.base.ItemAttributeContainer))
        self.assert_(isinstance(image_attr.item_attributes[0], gdata.base.ItemAttributeContainer))
        self.assert_(isinstance(image_attr.item_attributes[0], gdata.base.ItemAttribute))
        self.assert_(image_attr.item_attributes[0].type=='url')
        self.assert_(image_attr.item_attributes[0].text==thumb_url)
        self.assert_(len(image_attr.item_attributes)==1)
        new_item = gdata.base.GBaseItemFromString(item.ToString())
	image_attr=item.GetItemAttributes("image_link")[0]
        self.assert_(isinstance(image_attr.item_attributes[0], gdata.base.ItemAttributeContainer))
        self.assert_(image_attr.item_attributes[0].type=='url')
        self.assert_(image_attr.item_attributes[0].text==thumb_url)
        self.assert_(len(image_attr.item_attributes)==1)
        
    def testFromXML(self):
        item = gdata.base.GBaseItemFromString(TST_XML)
        attr=item.GetItemAttributes("shipping")[0]
        self.assert_(isinstance(attr, gdata.base.ItemAttributeContainer))
        self.assert_(isinstance(attr.item_attributes[0], gdata.base.ItemAttributeContainer))
        self.assert_(isinstance(attr.item_attributes[0], gdata.base.ItemAttribute))
        self.assert_(attr.item_attributes[0].type=='floatUnit')
        self.assert_(len(attr.item_attributes)==2)


if __name__ == "__main__":
    unittest.main()

