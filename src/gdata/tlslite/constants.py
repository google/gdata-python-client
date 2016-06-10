# Authors: 
#   Trevor Perrin
#   Google - defining ClientCertificateType
#   Google (adapted by Sam Rushing) - NPN support
#   Dimitris Moraitis - Anon ciphersuites
#   Dave Baggett (Arcode Corporation) - canonicalCipherName
#   Yngve Pettersen (ported by Paul Sokolovsky) - TLS 1.2
#
# See the LICENSE file for legal information regarding use of this file.

"""Constants used in various places."""

class CertificateType:
    x509 = 0
    openpgp = 1

class ClientCertificateType:
    rsa_sign = 1
    dss_sign = 2
    rsa_fixed_dh = 3
    dss_fixed_dh = 4
 
class HandshakeType:
    hello_request = 0
    client_hello = 1
    server_hello = 2
    certificate = 11
    server_key_exchange = 12
    certificate_request = 13
    server_hello_done = 14
    certificate_verify = 15
    client_key_exchange = 16
    finished = 20
    next_protocol = 67

class ContentType:
    change_cipher_spec = 20
    alert = 21
    handshake = 22
    application_data = 23
    all = (20,21,22,23)

class ExtensionType:    # RFC 6066 / 4366
    server_name = 0     # RFC 6066 / 4366
    srp = 12            # RFC 5054  
    cert_type = 9       # RFC 6091
    tack = 0xF300
    supports_npn = 13172

class HashAlgorithm:
    none = 0
    md5 = 1
    sha1 = 2
    sha224 = 3
    sha256 = 4
    sha384 = 5

class SignatureAlgorithm:
    anonymous = 0
    rsa = 1
    dsa = 2
    ecdsa = 3
    
class NameType:
    host_name = 0

class AlertLevel:
    warning = 1
    fatal = 2

class AlertDescription:
    """
    @cvar bad_record_mac: A TLS record failed to decrypt properly.

    If this occurs during a SRP handshake it most likely
    indicates a bad password.  It may also indicate an implementation
    error, or some tampering with the data in transit.

    This alert will be signalled by the server if the SRP password is bad.  It
    may also be signalled by the server if the SRP username is unknown to the
    server, but it doesn't wish to reveal that fact.


    @cvar handshake_failure: A problem occurred while handshaking.

    This typically indicates a lack of common ciphersuites between client and
    server, or some other disagreement (about SRP parameters or key sizes,
    for example).

    @cvar protocol_version: The other party's SSL/TLS version was unacceptable.

    This indicates that the client and server couldn't agree on which version
    of SSL or TLS to use.

    @cvar user_canceled: The handshake is being cancelled for some reason.

    """

    close_notify = 0
    unexpected_message = 10
    bad_record_mac = 20
    decryption_failed = 21
    record_overflow = 22
    decompression_failure = 30
    handshake_failure = 40
    no_certificate = 41 #SSLv3
    bad_certificate = 42
    unsupported_certificate = 43
    certificate_revoked = 44
    certificate_expired = 45
    certificate_unknown = 46
    illegal_parameter = 47
    unknown_ca = 48
    access_denied = 49
    decode_error = 50
    decrypt_error = 51
    export_restriction = 60
    protocol_version = 70
    insufficient_security = 71
    internal_error = 80
    inappropriate_fallback = 86
    user_canceled = 90
    no_renegotiation = 100
    unknown_psk_identity = 115


class CipherSuite:
    # Weird pseudo-ciphersuite from RFC 5746
    # Signals that "secure renegotiation" is supported
    # We actually don't do any renegotiation, but this
    # prevents renegotiation attacks
    TLS_EMPTY_RENEGOTIATION_INFO_SCSV = 0x00FF

    # draft-ietf-tls-downgrade-scsv-03
    TLS_FALLBACK_SCSV = 0x5600
    
    TLS_SRP_SHA_WITH_3DES_EDE_CBC_SHA  = 0xC01A
    TLS_SRP_SHA_WITH_AES_128_CBC_SHA = 0xC01D
    TLS_SRP_SHA_WITH_AES_256_CBC_SHA = 0xC020

    TLS_SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA = 0xC01B
    TLS_SRP_SHA_RSA_WITH_AES_128_CBC_SHA = 0xC01E
    TLS_SRP_SHA_RSA_WITH_AES_256_CBC_SHA = 0xC021


    TLS_RSA_WITH_3DES_EDE_CBC_SHA = 0x000A
    TLS_RSA_WITH_AES_128_CBC_SHA = 0x002F
    TLS_RSA_WITH_AES_256_CBC_SHA = 0x0035
    TLS_RSA_WITH_RC4_128_SHA = 0x0005
    
    TLS_RSA_WITH_RC4_128_MD5 = 0x0004

    TLS_DH_ANON_WITH_AES_128_CBC_SHA = 0x0034
    TLS_DH_ANON_WITH_AES_256_CBC_SHA = 0x003A

    TLS_RSA_WITH_AES_128_CBC_SHA256 = 0x003C
    TLS_RSA_WITH_AES_256_CBC_SHA256 = 0x003D

    tripleDESSuites = []
    tripleDESSuites.append(TLS_SRP_SHA_WITH_3DES_EDE_CBC_SHA)
    tripleDESSuites.append(TLS_SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA)
    tripleDESSuites.append(TLS_RSA_WITH_3DES_EDE_CBC_SHA)

    aes128Suites = []
    aes128Suites.append(TLS_SRP_SHA_WITH_AES_128_CBC_SHA)
    aes128Suites.append(TLS_SRP_SHA_RSA_WITH_AES_128_CBC_SHA)
    aes128Suites.append(TLS_RSA_WITH_AES_128_CBC_SHA)
    aes128Suites.append(TLS_DH_ANON_WITH_AES_128_CBC_SHA)
    aes128Suites.append(TLS_RSA_WITH_AES_128_CBC_SHA256)

    aes256Suites = []
    aes256Suites.append(TLS_SRP_SHA_WITH_AES_256_CBC_SHA)
    aes256Suites.append(TLS_SRP_SHA_RSA_WITH_AES_256_CBC_SHA)
    aes256Suites.append(TLS_RSA_WITH_AES_256_CBC_SHA)
    aes256Suites.append(TLS_DH_ANON_WITH_AES_256_CBC_SHA)
    aes256Suites.append(TLS_RSA_WITH_AES_256_CBC_SHA256)

    rc4Suites = []
    rc4Suites.append(TLS_RSA_WITH_RC4_128_SHA)
    rc4Suites.append(TLS_RSA_WITH_RC4_128_MD5)
    
    shaSuites = []
    shaSuites.append(TLS_SRP_SHA_WITH_3DES_EDE_CBC_SHA)
    shaSuites.append(TLS_SRP_SHA_WITH_AES_128_CBC_SHA)
    shaSuites.append(TLS_SRP_SHA_WITH_AES_256_CBC_SHA)
    shaSuites.append(TLS_SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA)
    shaSuites.append(TLS_SRP_SHA_RSA_WITH_AES_128_CBC_SHA)
    shaSuites.append(TLS_SRP_SHA_RSA_WITH_AES_256_CBC_SHA)
    shaSuites.append(TLS_RSA_WITH_3DES_EDE_CBC_SHA)
    shaSuites.append(TLS_RSA_WITH_AES_128_CBC_SHA)
    shaSuites.append(TLS_RSA_WITH_AES_256_CBC_SHA)
    shaSuites.append(TLS_RSA_WITH_RC4_128_SHA)
    shaSuites.append(TLS_DH_ANON_WITH_AES_128_CBC_SHA)
    shaSuites.append(TLS_DH_ANON_WITH_AES_256_CBC_SHA)
    
    sha256Suites = []
    sha256Suites.append(TLS_RSA_WITH_AES_128_CBC_SHA256)
    sha256Suites.append(TLS_RSA_WITH_AES_256_CBC_SHA256)

    md5Suites = []
    md5Suites.append(TLS_RSA_WITH_RC4_128_MD5)

    @staticmethod
    def filterForVersion(suites, minVersion, maxVersion):
        """ Returns a copy of suites after removing any entries which are not
        enabled by any version of TLS between minVersion and maxVersion. """
        excludeSuites = []
        if maxVersion < (3, 3):
            excludeSuites += CipherSuite.sha256Suites
        return [s for s in suites if s not in excludeSuites]

    @staticmethod
    def _filterSuites(suites, settings):
        macNames = settings.macNames
        cipherNames = settings.cipherNames
        macSuites = []
        if "sha" in macNames:
            macSuites += CipherSuite.shaSuites
        if "sha256" in macNames:
            macSuites += CipherSuite.sha256Suites
        if "md5" in macNames:
            macSuites += CipherSuite.md5Suites

        cipherSuites = []
        if "aes128" in cipherNames:
            cipherSuites += CipherSuite.aes128Suites
        if "aes256" in cipherNames:
            cipherSuites += CipherSuite.aes256Suites
        if "3des" in cipherNames:
            cipherSuites += CipherSuite.tripleDESSuites
        if "rc4" in cipherNames:
            cipherSuites += CipherSuite.rc4Suites

        return [s for s in suites if s in macSuites and s in cipherSuites]

    srpSuites = []
    srpSuites.append(TLS_SRP_SHA_WITH_AES_256_CBC_SHA)
    srpSuites.append(TLS_SRP_SHA_WITH_AES_128_CBC_SHA)
    srpSuites.append(TLS_SRP_SHA_WITH_3DES_EDE_CBC_SHA)
    
    @staticmethod
    def getSrpSuites(settings):
        return CipherSuite._filterSuites(CipherSuite.srpSuites, settings)

    srpCertSuites = []
    srpCertSuites.append(TLS_SRP_SHA_RSA_WITH_AES_256_CBC_SHA)
    srpCertSuites.append(TLS_SRP_SHA_RSA_WITH_AES_128_CBC_SHA)
    srpCertSuites.append(TLS_SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA)
    
    @staticmethod
    def getSrpCertSuites(settings):
        return CipherSuite._filterSuites(CipherSuite.srpCertSuites, settings)

    srpAllSuites = srpSuites + srpCertSuites

    @staticmethod
    def getSrpAllSuites(settings):
        return CipherSuite._filterSuites(CipherSuite.srpAllSuites, settings)

    certSuites = []
    certSuites.append(TLS_RSA_WITH_AES_256_CBC_SHA256)
    certSuites.append(TLS_RSA_WITH_AES_128_CBC_SHA256)
    certSuites.append(TLS_RSA_WITH_AES_256_CBC_SHA)
    certSuites.append(TLS_RSA_WITH_AES_128_CBC_SHA)
    certSuites.append(TLS_RSA_WITH_3DES_EDE_CBC_SHA)
    certSuites.append(TLS_RSA_WITH_RC4_128_SHA)
    certSuites.append(TLS_RSA_WITH_RC4_128_MD5)
    certAllSuites = srpCertSuites + certSuites
    
    @staticmethod
    def getCertSuites(settings):
        return CipherSuite._filterSuites(CipherSuite.certSuites, settings)

    anonSuites = []
    anonSuites.append(TLS_DH_ANON_WITH_AES_256_CBC_SHA)
    anonSuites.append(TLS_DH_ANON_WITH_AES_128_CBC_SHA)
    
    @staticmethod
    def getAnonSuites(settings):
        return CipherSuite._filterSuites(CipherSuite.anonSuites, settings)

    @staticmethod
    def canonicalCipherName(ciphersuite):
        "Return the canonical name of the cipher whose number is provided."
        if ciphersuite in CipherSuite.aes128Suites:
            return "aes128"
        elif ciphersuite in CipherSuite.aes256Suites:
            return "aes256"
        elif ciphersuite in CipherSuite.rc4Suites:
            return "rc4"
        elif ciphersuite in CipherSuite.tripleDESSuites:
            return "3des"
        else:
            return None

    @staticmethod
    def canonicalMacName(ciphersuite):
        "Return the canonical name of the MAC whose number is provided."
        if ciphersuite in CipherSuite.shaSuites:
            return "sha"
        elif ciphersuite in CipherSuite.md5Suites:
            return "md5"
        else:
            return None


# The following faults are induced as part of testing.  The faultAlerts
# dictionary describes the allowed alerts that may be triggered by these
# faults.
class Fault:
    badUsername = 101
    badPassword = 102
    badA = 103
    clientSrpFaults = list(range(101,104))

    badVerifyMessage = 601
    clientCertFaults = list(range(601,602))

    badPremasterPadding = 501
    shortPremasterSecret = 502
    clientNoAuthFaults = list(range(501,503))

    badB = 201
    serverFaults = list(range(201,202))

    badFinished = 300
    badMAC = 301
    badPadding = 302
    genericFaults = list(range(300,303))

    ignoreVersionForCipher = 400

    faultAlerts = {\
        badUsername: (AlertDescription.unknown_psk_identity, \
                      AlertDescription.bad_record_mac),\
        badPassword: (AlertDescription.bad_record_mac,),\
        badA: (AlertDescription.illegal_parameter,),\
        badPremasterPadding: (AlertDescription.bad_record_mac,),\
        shortPremasterSecret: (AlertDescription.bad_record_mac,),\
        badVerifyMessage: (AlertDescription.decrypt_error,),\
        badFinished: (AlertDescription.decrypt_error,),\
        badMAC: (AlertDescription.bad_record_mac,),\
        badPadding: (AlertDescription.bad_record_mac,),\
        ignoreVersionForCipher: (AlertDescription.illegal_parameter,\
                                 AlertDescription.handshake_failure)
        }

    faultNames = {\
        badUsername: "bad username",\
        badPassword: "bad password",\
        badA: "bad A",\
        badPremasterPadding: "bad premaster padding",\
        shortPremasterSecret: "short premaster secret",\
        badVerifyMessage: "bad verify message",\
        badFinished: "bad finished message",\
        badMAC: "bad MAC",\
        badPadding: "bad padding",\
        ignoreVersionForCipher: "ignore version for cipher"
        }
