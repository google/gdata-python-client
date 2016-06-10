# Copyright (c) 2014, Hubert Kario
#
# See the LICENSE file for legal information regarding use of this file.

""" Helper package for handling TLS extensions encountered in ClientHello
and ServerHello messages.
"""

from __future__ import generators
from .utils.codec import Writer, Parser
from collections import namedtuple
from .constants import NameType, ExtensionType
from .errors import TLSInternalError

class TLSExtension(object):
    """
    This class handles the generic information about TLS extensions used by
    both sides of connection in Client Hello and Server Hello messages.
    See U{RFC 4366<https://tools.ietf.org/html/rfc4366>} for more info.

    It is used as a base class for specific users and as a way to store
    extensions that are not implemented in library.

    @type extType: int
    @ivar extType: a 2^16-1 limited integer specifying the type of the
        extension that it contains, e.g. 0 indicates server name extension

    @type extData: bytearray
    @ivar extData: a byte array containing the value of the extension as
        to be written on the wire

    @type serverType: boolean
    @ivar serverType: indicates that the extension was parsed with ServerHello
        specific parser, otherwise it used universal or ClientHello specific
        parser

    @type _universalExtensions: dict
    @cvar _universalExtensions: dictionary with concrete implementations of
        specific TLS extensions where key is the numeric value of the extension
        ID. Contains ClientHello version of extensions or universal
        implementations

    @type _serverExtensions: dict
    @cvar _serverExtensions: dictionary with concrete implementations of
        specific TLS extensions where key is the numeric value of the extension
        ID. Includes only those extensions that require special handlers for
        ServerHello versions.
    """
    # actual definition at the end of file, after definitions of all classes
    _universalExtensions = {}
    _serverExtensions = {}

    def __init__(self, server=False):
        """
        Creates a generic TLS extension that can be used either for
        client hello or server hello message parsing or creation.

        You'll need to use L{create} or L{parse} methods to create an extension
        that is actually usable.

        @type server: boolean
        @param server: whatever to select ClientHello or ServerHello version
            for parsing
        """
        self.extType = None
        self.extData = bytearray(0)
        self.serverType = server

    def create(self, extType, data):
        """
        Initializes a generic TLS extension that can later be used in
        client hello or server hello messages

        @type  extType: int
        @param extType: type of the extension encoded as an integer between
            M{0} and M{2^16-1}
        @type  data: bytearray
        @param data: raw data representing extension on the wire
        @rtype: L{TLSExtension}
        """
        self.extType = extType
        self.extData = data
        return self

    def write(self):
        """ Returns encoded extension, as encoded on the wire

        @rtype: bytearray
        @return: An array of bytes formatted as is supposed to be written on
           the wire, including the extension_type, length and the extension
           data

        @raise AssertionError: when the object was not initialized
        """

        assert self.extType is not None

        w = Writer()
        w.add(self.extType, 2)
        w.add(len(self.extData), 2)
        w.addFixSeq(self.extData, 1)
        return w.bytes

    def parse(self, p):
        """ Parses extension from the wire format

        @type p: L{tlslite.util.codec.Parser}
        @param p:  data to be parsed

        @raise SyntaxError: when the size of the passed element doesn't match
        the internal representation

        @rtype: L{TLSExtension}
        """

        extType = p.get(2)
        ext_length = p.get(2)

        # first check if we shouldn't use server side parser
        if self.serverType and extType in self._serverExtensions:
            ext = self._serverExtensions[extType]()
            ext_parser = Parser(p.getFixBytes(ext_length))
            ext = ext.parse(ext_parser)
            return ext

        # then fallback to universal/ClientHello-specific parsers
        if extType in self._universalExtensions:
            ext = self._universalExtensions[extType]()
            ext_parser = Parser(p.getFixBytes(ext_length))
            ext = ext.parse(ext_parser)
            return ext

        # finally, just save the extension data as there are extensions which
        # don't require specific handlers and indicate option by mere presence
        self.extType = extType
        self.extData = p.getFixBytes(ext_length)
        assert len(self.extData) == ext_length
        return self

    def __eq__(self, that):
        """ Test if two TLS extensions will result in the same on the wire
        representation.

        Will return False for every object that's not an extension.
        """
        if hasattr(that, 'extType') and hasattr(that, 'extData'):
            return self.extType == that.extType and \
                    self.extData == that.extData
        else:
            return False

    def __repr__(self):
        """ Output human readable representation of object

        @rtype: str
        """
        return "TLSExtension(extType={0!r}, extData={1!r},"\
                " serverType={2!r})".format(self.extType, self.extData,
                                            self.serverType)

class SNIExtension(TLSExtension):
    """
    Class for handling Server Name Indication (server_name) extension from
    RFC 4366.

    Note that while usually the client does advertise just one name, it is
    possible to provide a list of names, each of different type.
    The type is a single byte value (represented by ints), the names are
    opaque byte strings, in case of DNS host names (records of type 0) they
    are UTF-8 encoded domain names (without the ending dot).

    @type hostNames: tuple of bytearrays
    @ivar hostNames: tuple of hostnames (server name records of type 0)
        advertised in the extension. Note that it may not include all names
        from client hello as the client can advertise other types. Also note
        that while it's not possible to change the returned array in place, it
        is possible to assign a new set of names. IOW, this won't work::

           sni_extension.hostNames[0] = bytearray(b'example.com')

        while this will work::

           names = list(sni_extension.hostNames)
           names[0] = bytearray(b'example.com')
           sni_extension.hostNames = names


    @type serverNames: list of L{ServerName}
    @ivar serverNames: list of all names advertised in extension.
        L{ServerName} is a namedtuple with two elements, the first
        element (type) defines the type of the name (encoded as int)
        while the other (name) is a bytearray that carries the value.
        Known types are defined in L{tlslite.constants.NameType}.
        The list will be empty if the on the wire extension had and empty
        list while it will be None if the extension was empty.

    @type extType: int
    @ivar extType: numeric type of SNIExtension, i.e. 0

    @type extData: bytearray
    @ivar extData: raw representation of the extension
    """

    ServerName = namedtuple('ServerName', 'name_type name')

    def __init__(self):
        """
        Create an instance of SNIExtension.

        See also: L{create} and L{parse}.
        """
        self.serverNames = None

    def __repr__(self):
        """
        Return programmer-readable representation of extension

        @rtype: str
        """
        return "SNIExtension(serverNames={0!r})".format(self.serverNames)

    def create(self, hostname=None, hostNames=None, serverNames=None):
        """
        Initializes an instance with provided hostname, host names or
        raw server names.

        Any of the parameters may be None, in that case the list inside the
        extension won't be defined, if either hostNames or serverNames is
        an empty list, then the extension will define a list of lenght 0.

        If multiple parameters are specified at the same time, then the
        resulting list of names will be concatenated in order of hostname,
        hostNames and serverNames last.

        @type  hostname: bytearray
        @param hostname: raw UTF-8 encoding of the host name

        @type  hostNames: list of bytearrays
        @param hostNames: list of raw UTF-8 encoded host names

        @type  serverNames: list of L{ServerName}
        @param serverNames: pairs of name_type and name encoded as a namedtuple

        @rtype: L{SNIExtension}
        """
        if hostname is None and hostNames is None and serverNames is None:
            self.serverNames = None
            return self
        else:
            self.serverNames = []

        if hostname:
            self.serverNames += [SNIExtension.ServerName(NameType.host_name,\
                    hostname)]

        if hostNames:
            self.serverNames +=\
                    [SNIExtension.ServerName(NameType.host_name, x) for x in\
                    hostNames]

        if serverNames:
            self.serverNames += serverNames

        return self

    @property
    def extType(self):
        """ Return the type of TLS extension, in this case - 0

        @rtype: int
        """
        return ExtensionType.server_name

    @property
    def hostNames(self):
        """ Returns a simulated list of hostNames from the extension.

        @rtype: tuple of bytearrays
        """
        # because we can't simulate assignments to array elements we return
        # an immutable type
        if self.serverNames is None:
            return tuple()
        else:
            return tuple([x.name for x in self.serverNames if \
                x.name_type == NameType.host_name])

    @hostNames.setter
    def hostNames(self, hostNames):
        """ Removes all host names from the extension and replaces them by
        names in X{hostNames} parameter.

        Newly added parameters will be added at the I{beginning} of the list
        of extensions.

        @type hostNames: iterable of bytearrays
        @param hostNames: host names to replace the old server names of type 0
        """

        self.serverNames = \
                [SNIExtension.ServerName(NameType.host_name, x) for x in \
                    hostNames] + \
                [x for x in self.serverNames if \
                    x.name_type != NameType.host_name]

    @hostNames.deleter
    def hostNames(self):
        """ Remove all host names from extension, leaves other name types
        unmodified
        """
        self.serverNames = [x for x in self.serverNames if \
                x.name_type != NameType.host_name]

    @property
    def extData(self):
        """ raw encoding of extension data, without type and length header

        @rtype: bytearray
        """
        if self.serverNames is None:
            return bytearray(0)

        w2 = Writer()
        for server_name in self.serverNames:
            w2.add(server_name.name_type, 1)
            w2.add(len(server_name.name), 2)
            w2.bytes += server_name.name

        # note that when the array is empty we write it as array of length 0
        w = Writer()
        w.add(len(w2.bytes), 2)
        w.bytes += w2.bytes
        return w.bytes

    def write(self):
        """ Returns encoded extension, as encoded on the wire

        @rtype: bytearray
        @return: an array of bytes formatted as they are supposed to be written
            on the wire, including the type, length and extension data
        """

        raw_data = self.extData

        w = Writer()
        w.add(self.extType, 2)
        w.add(len(raw_data), 2)
        w.bytes += raw_data

        return w.bytes

    def parse(self, p):
        """
        Deserialise the extension from on-the-wire data

        The parser should not include the type or length of extension!

        @type p: L{tlslite.util.codec.Parser}
        @param p: data to be parsed

        @rtype: L{SNIExtension}
        @raise SyntaxError: when the internal sizes don't match the attached
            data
        """
        if p.getRemainingLength() == 0:
            return self

        self.serverNames = []

        p.startLengthCheck(2)
        while not p.atLengthCheck():
            sn_type = p.get(1)
            sn_name = p.getVarBytes(2)
            self.serverNames += [SNIExtension.ServerName(sn_type, sn_name)]
        p.stopLengthCheck()

        return self

class ClientCertTypeExtension(TLSExtension):
    """
    This class handles the Certificate Type extension (variant sent by client)
    defined in RFC 6091.

    @type extType: int
    @ivar extType: numeric type of Certificate Type extension, i.e. 9

    @type extData: bytearray
    @ivar extData: raw representation of the extension data

    @type certTypes: list of int
    @ivar certTypes: list of certificate type identifiers (each one byte long)
    """

    def __init__(self):
        """
        Create an instance of ClientCertTypeExtension

        See also: L{create} and L{parse}
        """

        self.certTypes = None

    def __repr__(self):
        """ Return programmer-centric representation of extension

        @rtype: str
        """
        return "ClientCertTypeExtension(certTypes={0!r})"\
                .format(self.certTypes)

    @property
    def extType(self):
        """
        Return the type of TLS extension, in this case - 9

        @rtype: int
        """

        return ExtensionType.cert_type

    @property
    def extData(self):
        """
        Return the raw encoding of this extension

        @rtype: bytearray
        """

        if self.certTypes is None:
            return bytearray(0)

        w = Writer()
        w.add(len(self.certTypes), 1)
        for c_type in self.certTypes:
            w.add(c_type, 1)

        return w.bytes

    def create(self, certTypes=None):
        """
        Return instance of this extension with specified certificate types

        @type certTypes: iterable list of int
        @param certTypes: list of certificate types to advertise, all values
            should be between 0 and 2^8-1 inclusive

        @raises ValueError: when the list includes too big or negative integers
        """
        self.certTypes = certTypes
        return self

    def parse(self, p):
        """
        Parse the extension from binary data

        @type p: L{tlslite.util.codec.Parser}
        @param p: data to be parsed

        @raise SyntaxError: when the size of the passed element doesn't match
            the internal representation

        @rtype: L{ClientCertTypeExtension}
        """

        self.certTypes = p.getVarList(1, 1)

        return self

class ServerCertTypeExtension(TLSExtension):
    """
    This class handles the Certificate Type extension (variant sent by server)
    defined in RFC 6091.

    @type extType: int
    @ivar extType: byneruc ttoe if Certificate Type extension, i.e. 9

    @type extData: bytearray
    @ivar extData: raw representation of the extension data

    @type cert_type: int
    @ivar cert_type: the certificate type selected by server
    """

    def __init__(self):
        """
        Create an instance of ServerCertTypeExtension

        See also: L{create} and L{parse}
        """

        self.cert_type = None

    def __repr__(self):
        """ Return programmer-centric description of object

        @rtype: str
        """
        return "ServerCertTypeExtension(cert_type={0!r})".format(self.cert_type)

    @property
    def extType(self):
        """
        Return the type of TLS extension, in this case - 9

        @rtype: int
        """
        return ExtensionType.cert_type

    @property
    def extData(self):
        """
        Return the raw encoding of the extension data

        @rtype: bytearray
        """
        if self.cert_type is None:
            return bytearray(0)

        w = Writer()
        w.add(self.cert_type, 1)

        return w.bytes

    def create(self, val):
        """Create an instance for sending the extension to client.

        @type val: int
        @param val: selected type of certificate
        """
        self.cert_type = val
        return self

    def parse(self, p):
        """Parse the extension from on the wire format

        @type p: L{Parser}
        @param p: parser with data
        """
        self.cert_type = p.get(1)
        if p.getRemainingLength() > 0:
            raise SyntaxError()

        return self

class SRPExtension(TLSExtension):
    """
    This class handles the Secure Remote Password protocol TLS extension
    defined in RFC 5054.

    @type extType: int
    @ivar extType: numeric type of SRPExtension, i.e. 12

    @type extData: bytearray
    @ivar extData: raw representation of extension data

    @type identity: bytearray
    @ivar identity: UTF-8 encoding of user name
    """

    def __init__(self):
        """
        Create an instance of SRPExtension

        See also: L{create} and L{parse}
        """

        self.identity = None

    def __repr__(self):
        """
        Return programmer-centric description of extension

        @rtype: str
        """
        return "SRPExtension(identity={0!r})".format(self.identity)

    @property
    def extType(self):
        """
        Return the type of TLS extension, in this case - 12

        @rtype: int
        """

        return ExtensionType.srp

    @property
    def extData(self):
        """
        Return raw data encoding of the extension

        @rtype: bytearray
        """

        if self.identity is None:
            return bytearray(0)

        w = Writer()
        w.add(len(self.identity), 1)
        w.addFixSeq(self.identity, 1)

        return w.bytes

    def create(self, identity=None):
        """ Create and instance of SRPExtension with specified protocols

        @type identity: bytearray
        @param identity: UTF-8 encoded identity (user name) to be provided
            to user. MUST be shorter than 2^8-1.

        @raise ValueError: when the identity lenght is longer than 2^8-1
        """

        if identity is None:
            return self

        if len(identity) >= 2**8:
            raise ValueError()

        self.identity = identity
        return self

    def parse(self, p):
        """
        Parse the extension from on the wire format

        @type p: L{tlslite.util.codec.Parser}
        @param p: data to be parsed

        @raise SyntaxError: when the data is internally inconsistent

        @rtype: L{SRPExtension}
        """

        self.identity = p.getVarBytes(1)

        return self

class NPNExtension(TLSExtension):
    """
    This class handles the unofficial Next Protocol Negotiation TLS extension.

    @type protocols: list of bytearrays
    @ivar protocols: list of protocol names supported by the server

    @type extType: int
    @ivar extType: numeric type of NPNExtension, i.e. 13172

    @type extData: bytearray
    @ivar extData: raw representation of extension data
    """

    def __init__(self):
        """
        Create an instance of NPNExtension

        See also: L{create} and L{parse}
        """

        self.protocols = None

    def __repr__(self):
        """
        Create programmer-readable version of representation

        @rtype: str
        """
        return "NPNExtension(protocols={0!r})".format(self.protocols)

    @property
    def extType(self):
        """ Return the type of TLS extension, in this case - 13172

        @rtype: int
        """
        return ExtensionType.supports_npn

    @property
    def extData(self):
        """ Return the raw data encoding of the extension

        @rtype: bytearray
        """
        if self.protocols is None:
            return bytearray(0)

        w = Writer()
        for prot in self.protocols:
            w.add(len(prot), 1)
            w.addFixSeq(prot, 1)

        return w.bytes

    def create(self, protocols=None):
        """ Create an instance of NPNExtension with specified protocols

        @type protocols: list of bytearray
        @param protocols: list of protocol names that are supported
        """
        self.protocols = protocols
        return self

    def parse(self, p):
        """ Parse the extension from on the wire format

        @type p: L{tlslite.util.codec.Parser}
        @param p: data to be parsed

        @raise SyntaxError: when the size of the passed element doesn't match
            the internal representation

        @rtype: L{NPNExtension}
        """
        self.protocols = []

        while p.getRemainingLength() > 0:
            self.protocols += [p.getVarBytes(1)]

        return self

class TACKExtension(TLSExtension):
    """
    This class handles the server side TACK extension (see
    draft-perrin-tls-tack-02).

    @type tacks: list
    @ivar tacks: list of L{TACK}'s supported by server

    @type activation_flags: int
    @ivar activation_flags: activation flags for the tacks
    """

    class TACK(object):
        """
        Implementation of the single TACK
        """
        def __init__(self):
            """
            Create a single TACK object
            """
            self.public_key = bytearray(64)
            self.min_generation = 0
            self.generation = 0
            self.expiration = 0
            self.target_hash = bytearray(32)
            self.signature = bytearray(64)

        def __repr__(self):
            """
            Return programmmer readable representation of TACK object

            @rtype: str
            """
            return "TACK(public_key={0!r}, min_generation={1!r}, "\
                    "generation={2!r}, expiration={3!r}, target_hash={4!r}, "\
                    "signature={5!r})".format(
                            self.public_key, self.min_generation,
                            self.generation, self.expiration, self.target_hash,
                            self.signature)

        def create(self, public_key, min_generation, generation, expiration,
                target_hash, signature):
            """
            Initialise the TACK with data
            """
            self.public_key = public_key
            self.min_generation = min_generation
            self.generation = generation
            self.expiration = expiration
            self.target_hash = target_hash
            self.signature = signature
            return self

        def write(self):
            """
            Convert the TACK into on the wire format

            @rtype: bytearray
            """
            w = Writer()
            if len(self.public_key) != 64:
                raise TLSInternalError("Public_key must be 64 bytes long")
            w.bytes += self.public_key
            w.add(self.min_generation, 1)
            w.add(self.generation, 1)
            w.add(self.expiration, 4)
            if len(self.target_hash) != 32:
                raise TLSInternalError("Target_hash must be 32 bytes long")
            w.bytes += self.target_hash
            if len(self.signature) != 64:
                raise TLSInternalError("Signature must be 64 bytes long")
            w.bytes += self.signature
            return w.bytes

        def parse(self, p):
            """
            Parse the TACK from on the wire format

            @type p: L{tlslite.util.codec.Parser}
            @param p: data to be parsed

            @rtype: L{TACK}
            @raise SyntaxError: when the internal sizes don't match the
                provided data
            """

            self.public_key = p.getFixBytes(64)
            self.min_generation = p.get(1)
            self.generation = p.get(1)
            self.expiration = p.get(4)
            self.target_hash = p.getFixBytes(32)
            self.signature = p.getFixBytes(64)
            return self

        def __eq__(self, other):
            """
            Tests if the other object is equivalent to this TACK

            Returns False for every object that's not a TACK
            """
            if hasattr(other, 'public_key') and\
                    hasattr(other, 'min_generation') and\
                    hasattr(other, 'generation') and\
                    hasattr(other, 'expiration') and\
                    hasattr(other, 'target_hash') and\
                    hasattr(other, 'signature'):
                if self.public_key == other.public_key and\
                   self.min_generation == other.min_generation and\
                   self.generation == other.generation and\
                   self.expiration == other.expiration and\
                   self.target_hash == other.target_hash and\
                   self.signature == other.signature:
                    return True
                else:
                    return False
            else:
                return False

    def __init__(self):
        """
        Create an instance of TACKExtension

        See also: L{create} and L{parse}
        """

        self.tacks = []
        self.activation_flags = 0

    def __repr__(self):
        """
        Create a programmer readable representation of TACK extension

        @rtype: str
        """
        return "TACKExtension(activation_flags={0!r}, tacks={1!r})".format(
                self.activation_flags, self.tacks)

    @property
    def extType(self):
        """
        Returns the type of TLS extension, in this case - 62208

        @rtype: int
        """
        return ExtensionType.tack

    @property
    def extData(self):
        """
        Return the raw data encoding of the extension

        @rtype: bytearray
        """
        w2 = Writer()
        for t in self.tacks:
            w2.bytes += t.write()

        w = Writer()
        w.add(len(w2.bytes), 2)
        w.bytes += w2.bytes
        w.add(self.activation_flags, 1)
        return w.bytes

    def create(self, tacks, activation_flags):
        """
        Initialize the insance of TACKExtension

        @rtype: TACKExtension
        """

        self.tacks = tacks
        self.activation_flags = activation_flags
        return self

    def parse(self, p):
        """
        Parse the extension from on the wire format

        @type p: L{tlslite.util.codec.Parser}
        @param p: data to be parsed

        @rtype: L{TACKExtension}
        """
        self.tacks = []

        p.startLengthCheck(2)
        while not p.atLengthCheck():
            tack = TACKExtension.TACK().parse(p)
            self.tacks += [tack]
        p.stopLengthCheck()
        self.activation_flags = p.get(1)

        return self

TLSExtension._universalExtensions = {
        ExtensionType.server_name : SNIExtension,
        ExtensionType.cert_type : ClientCertTypeExtension,
        ExtensionType.srp : SRPExtension,
        ExtensionType.supports_npn : NPNExtension}

TLSExtension._serverExtensions = {
        ExtensionType.cert_type : ServerCertTypeExtension,
        ExtensionType.tack : TACKExtension}
