#!/usr/bin/python
#
# Copyright (C) 2010-2011 Google Inc.
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


"""GData definitions for Content API for Shopping"""


__author__ = 'afshar (Ali Afshar), dhermes (Daniel Hermes)'


import atom.core
import atom.data
import atom.http_core
import gdata.data


GD_NAMESPACE = 'http://schemas.google.com/g/2005'
GD_NAMESPACE_TEMPLATE = '{http://schemas.google.com/g/2005}%s'
SC_NAMESPACE_TEMPLATE = ('{http://schemas.google.com/'
                        'structuredcontent/2009}%s')
SCP_NAMESPACE_TEMPLATE = ('{http://schemas.google.com/'
                         'structuredcontent/2009/products}%s')

# Content API for Shopping, general (sc) attributes

class ProductId(atom.core.XmlElement):
  """sc:id element

  It is required that all inserted products are provided with a unique
  alphanumeric ID, in this element.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'id'


class ImageLink(atom.core.XmlElement):
  """sc:image_link element

  This is the URL of an associated image for a product. Please use full size
  images (400x400 pixels or larger), not thumbnails.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'image_link'


class AdditionalImageLink(atom.core.XmlElement):
  """sc:additional_image_link element

  The URLs of any additional images for the product. This tag may be repeated.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'additional_image_link'


class Channel(atom.core.XmlElement):
  """
  sc:channel element

  The channel for the product. Supported values are: 'online', 'local'
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'channel'


class ContentLanguage(atom.core.XmlElement):
  """
  sc:content_language element

  Language used in the item content for the product
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'content_language'


class TargetCountry(atom.core.XmlElement):
  """
  sc:target_country element

  The target country of the product
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'target_country'


class ExpirationDate(atom.core.XmlElement):
  """sc:expiration_date

  This is the date when the product listing will expire. If omitted, this will
  default to 30 days after the product was created.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'expiration_date'


class Adult(atom.core.XmlElement):
  """sc:adult element

  Indicates whether the content is targeted towards adults, with possible
  values of "true" or "false". Defaults to "false".
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'adult'


class Attribute(atom.core.XmlElement):
  """sc:attribute element

  Generic attribute used for generic projection and to define
  custom elements.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'attribute'
  name = 'name'
  type = 'type'
  unit = 'unit'


class Group(atom.core.XmlElement):
  """sc:group element

  Generic group used for generic projection and to define
  custom elements groups.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'group'
  attribute = [Attribute]


# Destination Attributes (to be used with app:control element)

class RequiredDestination(atom.core.XmlElement):
  """sc:required_destination element

  This element defines the required destination for a product, namely
  "ProductSearch", "ProductAds" or "CommerceSearch". It should be added to the
  app:control element (ProductEntry's "control" attribute) to specify where the
  product should appear in search APIs.

  By default, when omitted, the api attempts to upload to as many destinations
  as possible.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'required_destination'
  dest = 'dest'


class ValidateDestination(atom.core.XmlElement):
  """sc:validate_destination element

  This element defines the validate destination for a product, namely
  "ProductSearch", "ProductAds" or "CommerceSearch". It should be added to the
  app:control element (ProductEntry's "control" attribute) to specify which the
  destinations you would like error info for.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'validate_destination'
  dest = 'dest'


class ExcludedDestination(atom.core.XmlElement):
  """sc:excluded_destination element

  This element defines the required destination for a product, namely
  "ProductSearch", "ProductAds" or "CommerceSearch". It should be added to the
  app:control element (ProductEntry's "control" attribute) to specify where the
  product should not appear in search APIs.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'excluded_destination'
  dest = 'dest'

# Warning Attributes (to be used with app:control element)

class Code(atom.core.XmlElement):
  """sc:code element

  The warning code. Currently validation/missing_recommended is the
  only code used.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'code'


class Domain(atom.core.XmlElement):
  """sc:domain element

  The scope of the warning. A comma-separated list of destinations,
  for example: ProductSearch.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'domain'


class Location(atom.core.XmlElement):
  """sc:location element

  The name of the product element that has raised the warning. This may be
  any valid product element.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'location'


class Message(atom.core.XmlElement):
  """sc:message element

  A plain text description of the warning.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'message'


class WarningElement(atom.core.XmlElement):
  """sc:warning element

  Container element for an individual warning.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'warning'
  code = Code
  domain = Domain
  location = Location
  message = Message


class Warnings(atom.core.XmlElement):
  """sc:warnings element

  Container element for the list of warnings.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'warnings'
  warnings = [WarningElement]


class Datapoint(atom.core.XmlElement):
  """sc:datapoint element

  Datapoint representing click data for an item on
  a given day.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'datapoint'
  clicks = 'clicks'
  date = 'date'


class Performance(atom.core.XmlElement):
  """sc:performance element

  Container element for daily click data.
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'performance'
  datapoint = [Datapoint]


class ProductControl(atom.data.Control):
  """
  app:control element

  overridden to provide additional elements in the sc namespace.
  """
  _qname = atom.data.Control._qname[1]
  required_destination = [RequiredDestination]
  validate_destination = [ValidateDestination]
  excluded_destination = [ExcludedDestination]
  warnings = Warnings

# Content API for Shopping, product (scp) attributes

class Author(atom.core.XmlElement):
  """
  scp:author element

  Defines the author of the information, recommended for books.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'author'


class Availability(atom.core.XmlElement):
  """
  scp:availability element

  The retailer's suggested label for product availability. Supported values
  include: 'in stock', 'out of stock', 'limited availability',
           'available for order', and 'preorder'.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'availability'


class Brand(atom.core.XmlElement):
  """
  scp:brand element

  The brand of the product
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'brand'


class Color(atom.core.XmlElement):
  """scp:color element

  The color of the product.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'color'


class Condition(atom.core.XmlElement):
  """scp:condition element

  The condition of the product, one of "new", "used", "refurbished"
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'condition'


class Edition(atom.core.XmlElement):
  """scp:edition element

  The edition of the product. Recommended for products with multiple editions
  such as collectors' editions etc, such as books.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'edition'


class Feature(atom.core.XmlElement):
  """scp:feature element

  A product feature. A product may have multiple features, each being text, for
  example a smartphone may have features: "wifi", "gps" etc.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'feature'


class FeaturedProduct(atom.core.XmlElement):
  """scp:featured_product element

  Used to indicate that this item is a special, featured product; Supported
  values are: "true", "false".
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'featured_product'


class Gender(atom.core.XmlElement):
  """scp:gender element

  The gender for the item. Supported values are: 'unisex', 'female', 'male'

  Note: This tag is required if the google product type is part of
        Apparel & Accessories.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'gender'


class Genre(atom.core.XmlElement):
  """scp:genre element

  Describes the genre of a product, eg "comedy". Strongly recommended for media.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'genre'


class GoogleProductCategory(atom.core.XmlElement):
  """scp:google_product_category element

  The product's google category. The value must be one of the categories listed
  in the Product type taxonomy, which can be found at
  http://www.google.com/support/merchants/bin/answer.py?answer=160081.

  Note that & and > characters must be encoded as &amp; and &gt;
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'google_product_category'


class Gtin(atom.core.XmlElement):
  """scp:gtin element

  GTIN of the product (isbn/upc/ean)
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'gtin'


class ItemGroupID(atom.core.XmlElement):
  """scp:item_group_id element

  The identifier for products with variants. This id is used to link items which
  have different values for the fields:

      'color', 'material', 'pattern', 'size'

  but are the same item, for example a shirt with different sizes.

  Note: This tag is required for all product variants.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'item_group_id'


class Manufacturer(atom.core.XmlElement):
  """scp:manufacturer element

  Manufacturer of the product.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'manufacturer'


class Material(atom.core.XmlElement):
  """scp:material element

  The material the product is made of.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'material'


class Mpn(atom.core.XmlElement):
  """scp:mpn element

  Manufacturer's Part Number. A unique code determined by the manufacturer for
  the product.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'mpn'


class Pattern(atom.core.XmlElement):
  """scp:pattern element

  The pattern of the product. (e.g. polka dots)
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'pattern'


class Price(atom.core.XmlElement):
  """scp:price element

  The price of the product. The unit attribute must be set, and should represent
  the currency.

  Note: Required Element
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'price'
  unit = 'unit'


class ProductType(atom.core.XmlElement):
  """scp:product_type element

  Describes the type of product. A taxonomy of available product types is
  listed at http://www.google.com/basepages/producttype/taxonomy.txt and the
  entire line in the taxonomy should be included, for example "Electronics >
  Video > Projectors".
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'product_type'


class Quantity(atom.core.XmlElement):
  """scp:quantity element

  The number of items available. A value of 0 indicates items that are
  currently out of stock.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'quantity'


class ShippingPrice(atom.core.XmlElement):
  """scp:shipping_price element

  Fixed shipping price, represented as a number. Specify the currency as the
  "unit" attribute".

  This element should be placed inside the scp:shipping element.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'shipping_price'
  unit = 'unit'


class ShippingCountry(atom.core.XmlElement):
  """scp:shipping_country element

  The two-letter ISO 3166 country code for the country to which an item will
  ship.

  This element should be placed inside the scp:shipping element.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'shipping_country'


class ShippingRegion(atom.core.XmlElement):
  """scp:shipping_region element

  The geographic region to which a shipping rate applies, e.g., in the US, the
  two-letter state abbreviation, ZIP code, or ZIP code range using * wildcard.

  This element should be placed inside the scp:shipping element.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'shipping_region'


class ShippingService(atom.core.XmlElement):
  """scp:shipping_service element

  A free-form description of the service class or delivery speed.

  This element should be placed inside the scp:shipping element.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'shipping_service'


class Shipping(atom.core.XmlElement):
  """scp:shipping element

  Container for the shipping rules as provided by the shipping_country,
  shipping_price, shipping_region and shipping_service tags.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'shipping'
  shipping_price = ShippingPrice
  shipping_country = ShippingCountry
  shipping_service = ShippingService
  shipping_region = ShippingRegion


class ShippingWeight(atom.core.XmlElement):
  """scp:shipping_weight element

  The shipping weight of a product. Requires a value and a unit using the unit
  attribute. Valid units include lb, pound, oz, ounce, g, gram, kg, kilogram.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'shipping_weight'
  unit = 'unit'


class Size(atom.core.XmlElement):
  """scp:size element

  Available sizes of an item.  Appropriate values include: "small", "medium",
  "large", etc. The product enttry may contain multiple sizes, to indicate the
  available sizes.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'size'


class TaxRate(atom.core.XmlElement):
  """scp:tax_rate element

  The tax rate as a percent of the item price, i.e., number, as a percentage.

  This element should be placed inside the scp:tax (Tax class) element.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'tax_rate'


class TaxCountry(atom.core.XmlElement):
  """scp:tax_country element

  The country an item is taxed in (as a two-letter ISO 3166 country code).

  This element should be placed inside the scp:tax (Tax class) element.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'tax_country'


class TaxRegion(atom.core.XmlElement):
  """scp:tax_region element

  The geographic region that a tax rate applies to, e.g., in the US, the
  two-letter state abbreviation, ZIP code, or ZIP code range using * wildcard.

  This element should be placed inside the scp:tax (Tax class) element.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'tax_region'


class TaxShip(atom.core.XmlElement):
  """scp:tax_ship element

  Whether tax is charged on shipping for this product. The default value is
  "false".

  This element should be placed inside the scp:tax (Tax class) element.
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'tax_ship'


class Tax(atom.core.XmlElement):
  """scp:tax element

  Container for the tax rules for this product. Containing the tax_rate,
  tax_country, tax_region, and tax_ship elements
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'tax'
  tax_rate = TaxRate
  tax_country = TaxCountry
  tax_region = TaxRegion
  tax_ship = TaxShip


class Year(atom.core.XmlElement):
  """scp:year element

  The year the product was produced. Expects four digits
  """
  _qname = SCP_NAMESPACE_TEMPLATE % 'year'


class ProductEntry(gdata.data.BatchEntry):
  """Product entry containing product information

  The elements of this entry that are used are made up of five different
  namespaces. They are:

  atom: - Atom
  app: - Atom Publishing Protocol
  gd: - Google Data API
  sc: - Content API for Shopping, general attributes
  scp: - Content API for Shopping, product attributes

  Only the sc and scp namespace elements are defined here, but additional useful
  elements are defined in superclasses.

  The following attributes are encoded as XML elements in the Atomn (atom:)
  namespace: title, link, entry, id, category, content, author, created
  updated. Among these, the title, content and link tags are part of the
  required Content for Shopping API so we document them here.

  .. attribute:: title

    The title of the product.

    This should be a :class:`atom.data.Title` element, for example::

      entry = ProductEntry()
      entry.title = atom.data.Title(u'32GB MP3 Player')

  .. attribute:: content

    The description of the item.

    This should be a :class:`atom.data.Content` element, for example::

      entry = ProductEntry()
      entry.content = atom.data.Content('My item description')

  .. attribute:: link

    A link to a page where the item can be purchased.

    This should be a :class:`atom.data.Link` element, for example::

      link = atom.data.Link(rel='alternate', type='text/html',
                            href='http://www.somehost.com/123456jsh9')
      entry = ProductEntry()
      entry.link.append(link)

  .. attribute:: additional_image_link

    A list of additional links to images of the product. Each link should be an
    :class:`AdditionalImageLink` element, for example::

      entry = ProductEntry()
      entry.additional_image_link.append(
          AdditionalImageLink('http://myshop/cdplayer.jpg'))

  .. attribute:: author

    The author of the product.

    This should be a :class:`Author` element, for example::

      entry = ProductEntry()
      entry.author = atom.data.Author(u'Isaac Asimov')

  .. attribute:: attribute

    List of generic attributes.

    This should be a list of :class:`Attribute` elements, for example::

      attribute = Attribute('foo')
      attribute.name = 'bar'
      attribute.type = 'baz'
      attribute.unit = 'kg'
      entry = ProductEntry()
      entry.attributes.append(attribute)

  .. attribute:: availability

    The avilability of a product.

    This should be an :class:`Availability` instance, for example::

      entry = ProductEntry()
      entry.availability = Availability('in stock')

  .. attribute:: brand

    The brand of a product.

    This should be a :class:`Brand` element, for example::

      entry = ProductEntry()
      entry.brand = Brand(u'Sony')

  .. attribute:: channel

    The channel for the product. Supported values are: 'online', 'local'

    This should be a :class:`Channel` element, for example::

      entry = ProductEntry()
      entry.channel = Channel('online')

  .. attribute:: color

    The color of a product.

    This should be a :class:`Color` element, for example::

      entry = ProductEntry()
      entry.color = Color(u'purple')

  .. attribute:: condition

    The condition of a product.

    This should be a :class:`Condition` element, for example::

      entry = ProductEntry()
      entry.condition = Condition(u'new')

  .. attribute:: content_language

    The language for the product.

    This should be a :class:`ContentLanguage` element, for example::

      entry = ProductEntry()
      entry.content_language = ContentLanguage('EN')

  .. attribute:: control

    Overrides :class:`atom.data.Control` to provide additional elements
    required_destination and excluded_destination in the sc namespace

    This should be a :class:`ProductControl` element.

  .. attribute:: edition

    The edition of the product.

    This should be a :class:`Edition` element, for example::

      entry = ProductEntry()
      entry.edition = Edition('1')

  .. attribute:: expiration_date

    The expiration date of this product listing.

    This should be a :class:`ExpirationDate` element, for example::

      entry = ProductEntry()
      entry.expiration_date = ExpirationDate('2011-22-03')

  .. attribute:: feature

    A list of features for this product.

    Each feature should be a :class:`Feature` element, for example::

      entry = ProductEntry()
      entry.feature.append(Feature(u'wifi'))
      entry.feature.append(Feature(u'gps'))

  .. attribute:: featured_product

    Whether the product is featured.

    This should be a :class:`FeaturedProduct` element, for example::

      entry = ProductEntry()
      entry.featured_product = FeaturedProduct('true')

  .. attribute:: gender

    The gender for the item. Supported values are: 'unisex', 'female', 'male'

    This should be a :class:`Gender` element, for example::

      entry = ProductEntry()
      entry.gender = Gender('female')

  .. attribute:: genre

    The genre of the product.

    This should be a :class:`Genre` element, for example::

      entry = ProductEntry()
      entry.genre = Genre(u'comedy')

  .. attribute:: google_product_category

    The product's google category. Value must come from taxonomy listed at

      http://www.google.com/support/merchants/bin/answer.py?answer=160081

    This should be a :class:`GoogleProductCategory` element, for example::

      entry = ProductEntry()
      entry.google_product_category = GoogleProductCategory(
          'Animals &gt; Live Animals')

  .. attribute:: gtin

    The gtin for this product.

    This should be a :class:`Gtin` element, for example::

      entry = ProductEntry()
      entry.gtin = Gtin('A888998877997')

  .. attribute:: image_link

    A link to the product image. This link should be an
    :class:`ImageLink` element, for example::

      entry = ProductEntry()
      entry.image_link = ImageLink('http://myshop/cdplayer.jpg')

  .. attribute:: item_group_id

    The identifier for products with variants. This id is used to link items
    which have different values for the fields:

      'color', 'material', 'pattern', 'size'

    but are the same item, for example a shirt with different sizes.

    This should be a :class:`ItemGroupID` element, for example::

      entry = ProductEntry()
      entry.item_group_id = ItemGroupID('R1726122')

  .. attribute:: manufacturer

    The manufacturer of the product.

    This should be a :class:`Manufacturer` element, for example::

      entry = ProductEntry()
      entry.manufacturer = Manufacturer('Sony')

  .. attribute:: material

    The material the product is made of.

    This should be a :class:`Material` element, for example::

      entry = ProductEntry()
      entry.material = Material('cotton')

  .. attribute:: mpn

    The manufacturer's part number for this product.

    This should be a :class:`Mpn` element, for example::

      entry = ProductEntry()
      entry.mpn = Mpn('cd700199US')

  .. attribute:: pattern

    The pattern of the product.

    This should be a :class:`Pattern` element, for example::

      entry = ProductEntry()
      entry.pattern = Pattern('polka dots')

  .. attribute:: performance

    The performance of the product.

    This should be a :class:`Performance` element.

  .. attribute:: price

    The price for this product.

    This should be a :class:`Price` element, including a unit argument to
    indicate the currency, for example::

      entry = ProductEntry()
      entry.price = Price('20.00', unit='USD')

  .. attribute:: product_id

    A link to the product image. This link should be an
    :class:`ProductId` element, for example::

      entry = ProductEntry()
      entry.product_id = ProductId('ABC1234')

  .. attribute:: product_type

    The type of product.

    This should be a :class:`ProductType` element, for example::

      entry = ProductEntry()
      entry.product_type = ProductType("Electronics > Video > Projectors")

  .. attribute:: quantity

    The quantity of product available in stock.

    This should be a :class:`Quantity` element, for example::

      entry = ProductEntry()
      entry.quantity = Quantity('100')

  .. attribute:: shipping

    The shipping rules for the product.

    This should be a :class:`Shipping` with the necessary rules embedded as
    elements, for example::

      shipping = Shipping()
      shipping.shipping_price = ShippingPrice('10.00', unit='USD')
      entry = ProductEntry()
      entry.shipping.append(shipping)

  .. attribute:: shipping_weight

    The shipping weight for this product.

    This should be a :class:`ShippingWeight` element, including a unit parameter
    for the unit of weight, for example::

      entry = ProductEntry()
      entry.shipping_weight = ShippingWeight('10.45', unit='kg')

  .. attribute:: size

    A list of the available sizes for this product.

    Each item in this list should be a :class:`Size` element, for example::

      entry = ProductEntry()
      entry.size.append(Size('Small'))
      entry.size.append(Size('Medium'))
      entry.size.append(Size('Large'))

  .. attribute:: target_country

    The target country for the product.

    This should be a :class:`TargetCountry` element, for example::

      entry = ProductEntry()
      entry.target_country = TargetCountry('US')

  .. attribute:: tax

    The tax rules for this product.

    This should be a :class:`Tax` element, with the tax rule elements embedded
    within, for example::

      tax = Tax()
      tax.tax_rate = TaxRate('17.5')
      entry = ProductEntry()
      entry.tax.append(tax)

  .. attribute:: year

    The year the product was created.

    This should be a :class:`Year` element, for example::

      entry = ProductEntry()
      entry.year = Year('2001')
  """

  additional_image_link = [AdditionalImageLink]
  author = Author
  attribute = [Attribute]
  availability = Availability
  brand = Brand
  channel = Channel
  color = Color
  condition = Condition
  content_language = ContentLanguage
  control = ProductControl
  edition = Edition
  expiration_date = ExpirationDate
  feature = [Feature]
  featured_product = FeaturedProduct
  gender = Gender
  genre = Genre
  google_product_category = GoogleProductCategory
  group = [Group]
  gtin = Gtin
  image_link = ImageLink
  item_group_id = ItemGroupID
  manufacturer = Manufacturer
  material = Material
  mpn = Mpn
  pattern = Pattern
  performance = Performance
  price = Price
  product_id = ProductId
  product_type = ProductType
  quantity = Quantity
  shipping = [Shipping]
  shipping_weight = ShippingWeight
  size = [Size]
  target_country = TargetCountry
  tax = [Tax]
  year = Year

  def get_batch_errors(self):
    """Attempts to parse errors from atom:content element.

    If the atom:content element is type application/vnd.google.gdata.error+xml,
    then it will contain a gd:errors block.

    Returns:
      If the type of the content element is not
          'application/vnd.google.gdata.error+xml', or 0 or more than 1
          gd:errors elements are found within the <content type='app...'> block,
          then None is returned. Other wise, the gd:errors element parsed
          as a ContentForShoppingErrors object is returned.
    """
    if self.content.type == 'application/vnd.google.gdata.error+xml':
      errors_elements = self.content.get_elements(tag='errors',
                                                  namespace=GD_NAMESPACE)
      if len(errors_elements) == 1:
        errors_block = errors_elements[0]
        return atom.core.parse(errors_block.to_string(),
                               ContentForShoppingErrors)
    return None

  GetBatchErrors = get_batch_errors


class ErrorDomain(atom.core.XmlElement):
  """gd:domain element

  The scope of the error. If the error is global (e.g. missing title) then sc
  value is returned. Otherwise a comma-separated list of destinations is
  returned.

  This element should be placed inside the gd:error (ContentForShoppingError)
  element.
  """
  _qname = GD_NAMESPACE_TEMPLATE % 'domain'


class ErrorCode(atom.core.XmlElement):
  """gd:code element

  A code to categorize the errors.

  This element should be placed inside the gd:error (ContentForShoppingError)
  element.
  """
  _qname = GD_NAMESPACE_TEMPLATE % 'code'


class ErrorLocation(atom.core.XmlElement):
  """gd:location element

  The name of the attribute that failed validation.

  This element should be placed inside the gd:error (ContentForShoppingError)
  element.
  """
  _qname = GD_NAMESPACE_TEMPLATE % 'location'
  type = 'type'


class InternalReason(atom.core.XmlElement):
  """gd:internalReason element

  A more detailed message to explain the cause of the error.

  This element should be placed inside the gd:error (ContentForShoppingError)
  element.
  """
  _qname = GD_NAMESPACE_TEMPLATE % 'internalReason'


class ContentForShoppingError(atom.core.XmlElement):
  """gd:error element

  This element should be placed inside the gd:errors (ContentForShoppingErrors)
  element.
  """
  _qname = GD_NAMESPACE_TEMPLATE % 'error'
  domain = ErrorDomain
  code = ErrorCode
  location = ErrorLocation
  internal_reason = InternalReason
  id = atom.data.Id


class ContentForShoppingErrors(atom.core.XmlElement):
  """The gd:errors element."""
  _qname = GD_NAMESPACE_TEMPLATE % 'errors'
  errors = [ContentForShoppingError]


# opensearch needs overriding for wrong version
# see http://code.google.com/p/gdata-python-client/issues/detail?id=483
class TotalResults(gdata.data.TotalResults):

    _qname = gdata.data.TotalResults._qname[1]


class ItemsPerPage(gdata.data.ItemsPerPage):

    _qname = gdata.data.ItemsPerPage._qname[1]


class StartIndex(gdata.data.StartIndex):

    _qname = gdata.data.StartIndex._qname[1]


class ProductFeed(gdata.data.BatchFeed):
  """Represents a feed of a merchant's products."""
  entry = [ProductEntry]
  total_results = TotalResults
  items_per_page = ItemsPerPage
  start_index = StartIndex

  def get_start_token(self):
    """Attempts to parse start-token from rel="next" link.

    A products feed may contain a rel="next" atom:link and the
    href contained in the link may have a start-token query parameter.

    Returns:
      If there is no rel="next" link or the rel="next" link doesn't contain
      the start-token query parameter, None is returned. Otherwise, the
      string value of the start-token query parameter is returned.
    """
    next_link = self.get_next_link()
    if next_link is not None:
      uri = atom.http_core.parse_uri(next_link.href)
      if 'start-token' in uri.query:
        return uri.query['start-token']
    return None

  GetStartToken = get_start_token


class Edited(atom.core.XmlElement):
  """sc:edited element
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'edited'


class AttributeLanguage(atom.core.XmlElement):
  """sc:attribute_language element
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'attribute_language'


class FeedFileName(atom.core.XmlElement):
  """sc:feed_file_name element
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'feed_file_name'


class FeedType(atom.core.XmlElement):
  """sc:feed_type element
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'feed_type'


class UseQuotedFields(atom.core.XmlElement):
  """sc:use_quoted_fields element
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'use_quoted_fields'


class FileFormat(atom.core.XmlElement):
  """sc:file_format element
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'file_format'
  use_quoted_fields = UseQuotedFields
  format = 'format'


class ProcessingStatus(atom.core.XmlElement):
  """sc:processing_status element
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'processing_status'


class DatafeedEntry(gdata.data.GDEntry):
  """An entry for a Datafeed
  """
  content_language = ContentLanguage
  target_country = TargetCountry
  feed_file_name = FeedFileName
  file_format = FileFormat
  attribute_language = AttributeLanguage
  processing_status = ProcessingStatus
  edited = Edited
  feed_type = FeedType


class DatafeedFeed(gdata.data.GDFeed):
  """A datafeed feed
  """
  entry = [DatafeedEntry]


class AdultContent(atom.core.XmlElement):
  """sc:adult_content element
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'adult_content'


class InternalId(atom.core.XmlElement):
  """sc:internal_id element
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'internal_id'


class ReviewsUrl(atom.core.XmlElement):
  """sc:reviews_url element
  """
  _qname = SC_NAMESPACE_TEMPLATE % 'reviews_url'


class ClientAccount(gdata.data.GDEntry):
  """A multiclient account entry
  """
  adult_content = AdultContent
  internal_id = InternalId
  reviews_url = ReviewsUrl


class ClientAccountFeed(gdata.data.GDFeed):
  """A multiclient account feed
  """
  entry = [ClientAccount]
