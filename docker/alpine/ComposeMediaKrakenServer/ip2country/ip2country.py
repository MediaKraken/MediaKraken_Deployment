"""
ip2country - module for looking up the country a given IP address
resides in.

The method used for this is downloading/caching the APNIC database.

On initial use, a file of approx 300-400k gets downloaded. But on
successive usage, the table is read from disk (~/.apnicdb)

Apart from monthly download of the table, this module works
efficiently, since a web hit is not required for each lookup

For usage info, refer to the demo section at the bottom.
Run this file with python to invoke the simple demo.

Copyright (c) 2004 by David McNab <david@freenet.org.nz>
Released under the terms of the GNU General Public License (GPL)
You are free to copy, change, redistribute this code, within
the provisions of the GPL.

No warranty, yada yada - don't blame me if this module causes your
niece to elope on the back of a Harley with a purple alien.
"""

# CONFIGURATION SECTION
#
# Feel free to tweak these values if you need to

# FTP URL from which to download APNIC data
apnicUrl = "ftp://ftp.apnic.net/pub/stats/apnic/delegated-apnic-latest"

# pathname for caching APNIC file, '~' may be used
apnicFileDb = "~/.ip2countrydb"

ipCacheFile = "~/.ip2countryips"

# set the maximum age of a cached APNIC database in DAYS
# if the cached file is older than this, a new one will
# be downloaded
maxApnicDbAge = 30

#
# END OF CONFIGURATION SECTION
import sys, os, time, stat, StringIO, commands, re
class IP2Country:
    """
    Looks up IP addresses in APNIC database
    
    Caches the APNIC database locally, downloading it when
    it gets more than a month old (or whatever you set maxApmicDbAge to
    """
    apnicUrl = apnicUrl
    apnicFileDb = apnicFileDb
    ipCacheFile = ipCacheFile
    
    updateInterval = 86400 * maxApnicDbAge
    
    countryCodes = {
        "AD":"Andorra",
        "AE":"United Arab Emirates",
        "AF":"Afghanistan",
        "AG":"Antigua and Barbuda",
        "AI":"Anguilla",
        "AL":"Albania",
        "AM":"Armenia",
        "AN":"Netherlands Antilles",
        "AO":"Angola",
        "AQ":"Antarctica",
        "AR":"Argentina",
        "AS":"American Samoa",
        "AT":"Austria",
        "AU":"Australia",
        "AW":"Aruba",
        "AZ":"Azerbaijan",
        "BA":"Bosnia and Herzegowina",
        "BB":"Barbados",
        "BD":"Bangladesh",
        "BE":"Belgium",
        "BF":"Burkina Faso",
        "BG":"Bulgaria",
        "BH":"Bahrain",
        "BI":"Burundi",
        "BJ":"Benin",
        "BM":"Bermuda",
        "BN":"Brunei Darussalam",
        "BO":"Bolivia",
        "BR":"Brazil",
        "BS":"Bahamas",
        "BT":"Bhutan",
        "BV":"Bouvet Island",
        "BW":"Botswana",
        "BY":"Belarus",
        "BZ":"Belize",
        "CA":"Canada",
        "CC":"Cocos (Keeling) Islands",
        "CD":"Congo, The Democratic Republic of the",
        "CF":"Central African Republic",
        "CG":"Congo",
        "CH":"Switzerland",
        "CI":"Cote D'Ivoire",
        "CK":"Cook Islands",
        "CL":"Chile",
        "CM":"Cameroon",
        "CN":"China",
        "CO":"Colombia",
        "CR":"Costa Rica",
        "CU":"Cuba",
        "CV":"Cape Verde",
        "CX":"Christmas Island",
        "CY":"Cyprus",
        "CZ":"Czech Republic",
        "DE":"Germany",
        "DJ":"Djibouti",
        "DK":"Denmark",
        "DM":"Dominica",
        "DO":"Dominican Republic",
        "DZ":"Algeria",
        "EC":"Ecuador",
        "EE":"Estonia",
        "EG":"Egypt",
        "EH":"Western Sahara",
        "ER":"Eritrea",
        "ES":"Spain",
        "ET":"Ethiopia",
        "FI":"Finland",
        "FJ":"Fiji",
        "FK":"Falkland Islands (Malvinas)",
        "FM":"Micronesia, Federated States of",
        "FO":"Faroe Islands",
        "FR":"France",
        "FX":"France, Metropolitan",
        "GA":"Gabon",
        "GB":"United Kingdom",
        "GD":"Grenada",
        "GE":"Georgia",
        "GF":"French Guiana",
        "GH":"Ghana",
        "GI":"Gibraltar",
        "GL":"Greenland",
        "GM":"Gambia",
        "GN":"Guinea",
        "GP":"Guadeloupe",
        "GQ":"Equatorial Guinea",
        "GR":"Greece",
        "GS":"South Georgia and the South Sandwich Islands",
        "GT":"Guatemala",
        "GU":"Guam",
        "GW":"Guinea-Bissau",
        "GY":"Guyana",
        "HK":"Hong Kong",
        "HM":"Heard and Mc Donald Islands",
        "HN":"Honduras",
        "HR":"Croatia (local name: Hrvatska)",
        "HT":"Haiti",
        "HU":"Hungary",
        "ID":"Indonesia",
        "IE":"Ireland",
        "IL":"Israel",
        "IN":"India",
        "IO":"British Indian Ocean Territory",
        "IQ":"Iraq",
        "IR":"Iran (Islamic Republic of)",
        "IS":"Iceland",
        "IT":"Italy",
        "JM":"Jamaica",
        "JO":"Jordan",
        "JP":"Japan",
        "KE":"Kenya",
        "KG":"Kyrgyzstan",
        "KH":"Cambodia",
        "KI":"Kiribati",
        "KM":"Comoros",
        "KN":"Saint Kitts and Nevis",
        "KP":"Korea, Democratic People's Republic of",
        "KR":"Korea, Republic of",
        "KW":"Kuwait",
        "KY":"Cayman Islands",
        "KZ":"Kazakhstan",
        "LA":"Lao People's Democratic Republic",
        "LB":"Lebanon",
        "LC":"Saint Lucia",
        "LI":"Liechtenstein",
        "LK":"Sri Lanka",
        "LR":"Liberia",
        "LS":"Lesotho",
        "LT":"Lithuania",
        "LU":"Luxembourg",
        "LV":"Latvia",
        "LY":"Libyan Arab Jamahiriya",
        "MA":"Morocco",
        "MC":"Monaco",
        "MD":"Moldova, Republic of",
        "MG":"Madagascar",
        "MH":"Marshall Islands",
        "MK":"Macedonia, The Former Yugoslav republic OF",
        "ML":"Mali",
        "MM":"Myanmar",
        "MN":"Mongolia",
        "MO":"Macau",
        "MP":"Northern Mariana Islands",
        "MQ":"Martinique",
        "MR":"Mauritania",
        "MS":"Montserrat",
        "MT":"Malta",
        "MU":"Mauritius",
        "MV":"Maldives",
        "MW":"Malawi",
        "MX":"Mexico",
        "MY":"Malaysia",
        "MZ":"Mozambique",
        "NA":"Namibia",
        "NC":"New Caledonia",
        "NE":"Niger",
        "NF":"Norfolk Island",
        "NG":"Nigeria",
        "NI":"Nicaragua",
        "NL":"Netherlands",
        "NO":"Norway",
        "NP":"Nepal",
        "NR":"Nauru",
        "NU":"Niue",
        "NZ":"New Zealand",
        "OM":"Oman",
        "PA":"Panama",
        "PE":"Peru",
        "PF":"French Polynesia",
        "PG":"Papua New Guinea",
        "PH":"Philippines",
        "PK":"Pakistan",
        "PL":"Poland",
        "PM":"St. Pierre and Miquelon",
        "PN":"Pitcairn",
        "PR":"Puerto Rico",
        "PT":"Portugal",
        "PW":"Palau",
        "PY":"Paraguay",
        "QA":"Qatar",
        "RE":"Reunion",
        "RO":"Romania",
        "RU":"Russian Federation",
        "RW":"Rwanda",
        "SA":"Saudi Arabia",
        "SB":"Solomon Islands",
        "SC":"Seychelles",
        "SD":"Sudan",
        "SE":"Sweden",
        "SG":"Singapore",
        "SH":"St. Helena",
        "SI":"Slovenia",
        "SJ":"Svalbard and Jan Mayen Islands",
        "SK":"Slovakia (Slovak Republic)",
        "SL":"Sierra Leone",
        "SM":"San Marino",
        "SN":"Senegal",
        "SO":"Somalia",
        "SR":"Suriname",
        "ST":"Sao Tome and Principe",
        "SV":"El Salvador",
        "SY":"Syrian Arab Republic",
        "SZ":"Swaziland",
        "TC":"Turks and Caicos Islands",
        "TD":"Chad",
        "TF":"French Southern Territories",
        "TG":"Togo",
        "TH":"Thailand",
        "TJ":"Tajikistan",
        "TK":"Tokelau",
        "TM":"Turkmenistan",
        "TN":"Tunisia",
        "TO":"Tonga",
        "TP":"East Timor",
        "TR":"Turkey",
        "TT":"Trinidad and Tobago",
        "TV":"Tuvalu",
        "TW":"Taiwan, Province of China",
        "TZ":"Tanzania, United Republic of",
        "UA":"Ukraine",
        "UG":"Uganda",
        "UM":"United States Minor Outlying Islands",
        "US":"United States",
        "UY":"Uruguay",
        "UZ":"Uzbekistan",
        "VA":"Holy See (Vatican City State)",
        "VC":"Saint Vincent and The Grenadines",
        "VE":"Venezuela",
        "VG":"Virgin Islands (British)",
        "VI":"Virgin Islands (US)",
        "VN":"Viet Nam",
        "VU":"Vanuatu",
        "WF":"Wallis and Futuna Islands",
        "WS":"Samoa",
        "YE":"Yemen",
        "YT":"Mayotte",
        "YU":"Yugoslavia",
        "ZA":"South Africa",
        "ZM":"Zambia",
        "ZW":"Zimbabwe",
        }
    
    def __init__(self, **kw):
    
        self.verbose = kw.get('verbose', False)
    
        # normalise dbpath if it contains a '~'
        if self.apnicFileDb.startswith("~/"):
            self.apnicFileDb = os.path.expanduser(self.apnicFileDb)
        if self.ipCacheFile.startswith("~/"):
            self.ipCacheFile = os.path.expanduser(self.ipCacheFile)
    
        self.load()
    def load(self):
    
        now = time.time()
    
        gotLatest = False
        if os.path.isfile(self.apnicFileDb):
            if os.stat(self.apnicFileDb)[stat.ST_MTIME] - now < self.updateInterval:
                self.log("Got latest apnic db, no need to download")
                gotLatest = True
    
        if not gotLatest:
            self.download()
    
        lines = file(self.apnicFileDb).read().split("\n")
    
        ipv4Recs = []
        self.db = ipTree = {}
        for line in lines:
            parts = line.split("|")
            if len(parts) < 7:
                continue
            if parts[0] != 'apnic' or parts[2] != 'ipv4':
                continue
    
            # got an alloc
            country = parts[1]
            ip = parts[3]
    
            ipbit0, ipbit1, ipbit2, ipbit3 = ip.split(".")
    
            if not ipTree.has_key(ipbit0):
                ipTree0 = ipTree[ipbit0] = {}
            else:
                ipTree0 = ipTree[ipbit0]
    
            if not ipTree0.has_key(ipbit1):
                ipTree1 = ipTree0[ipbit1] = {}
            else:
                ipTree1 = ipTree0[ipbit1]
    
            if not ipTree1.has_key(ipbit2):
                ipTree2 = ipTree1[ipbit2] = {}
            else:
                ipTree2 = ipTree1[ipbit2]
    
            if not ipTree2.has_key(ipbit3):
                ipTree3 = ipTree2[ipbit3] = country
            else:
                ipTree3 = ipTree2[ipbit3]
    
        # read in IP address cache
        if not os.path.isfile(self.ipCacheFile):
            file(self.ipCacheFile, "w")
        self.specificIPs = specificIPs = {}
        lines = file(self.ipCacheFile).read().strip().split("\n")
        #print lines
        for line in lines:
            if not line:
                continue
            #print "line: %s" % repr(line)
            ip, country = line.split(":")
            specificIPs[ip] = country
        
        self.log("Created apnic lookup tables")
    
    def lookup(self, ipaddr):
        """
        Looks up an IP address, returns tuple (countrycode, country) if IP is
        found, or (None, None) if not
        """
        bit0, bit1, bit2, bit3 = ipaddr.split(".")
    
        # consult cached IPs
        if self.specificIPs.has_key(ipaddr):
            cc = self.specificIPs[ipaddr]
            return cc, self.countryCodes.get(cc, '???')
    
        # screen Class C addresses
        if bit0 in ['127', '192', '10']:
            return None, None
    
        # not in cache IPs - consult APNIC database
        db = self.db
       
        if db.has_key(bit0):
            db1 = db[bit0]
        elif db.has_key("0"):
            db1 = db["0"]
        else:
            return self.lookupWhois(ipaddr) # not found
        
        if db1.has_key(bit1):
            db2 = db1[bit1]
        elif db1.has_key("0"):
            db2 = db1["0"]
        else:
            return self.lookupWhois(ipaddr) # not found
        
        if db2.has_key(bit2):
            db3 = db2[bit2]
        elif db2.has_key("0"):
            db3 = db2["0"]
        else:
            return self.lookupWhois(ipaddr) # not found
        
        if db3.has_key(bit3):
            cc = db3[bit3]
        elif db3.has_key("0"):
            cc = db3["0"]
        else:
            cc = None
    
        #print repr(cc)
    
        if not cc:
            return self.lookupWhois(ipaddr)
            
        if cc:
            return cc, self.countryCodes.get(cc, "???")
        else:
            return None, None
    
    def lookupWhois(self, ipaddr):
        """
        Fallback - perform a whois query and extracts the
        first 'Country:' line from reply
        """
        self.log("Performing whois query for %s" % ipaddr)
        cc = None
        lines = commands.getoutput("whois %s" % ipaddr).strip().split("\n")
    
        #print "\n * ".join(lines)
    
        for line in lines:
            if line.lower().startswith("country:"):
                cc = line[8:].strip()
    
        if cc:
            # got it - add to memory and file cache
            self.specificIPs[ipaddr] = cc
            file(self.ipCacheFile, "a").write("%s:%s\n" % (ipaddr, cc))
    
            # return it along with country name
            return cc, self.countryCodes.get(cc, "???")
        else:
            return None, None
    def download(self):
        """
        Downloads the latest apnic database
        """
        from ftplib import FTP
        
        url = self.apnicUrl
    
        # strip off 'ftp://' prefix if any
        if url.startswith("ftp://"):
            url = url[6:]
    
        host, path = url.split("/", 1)
    
        self.log("Cached DB is old or missing, need a new one")
    
        self.log("Connecting to apnic db server...")
        conn = FTP(host)
        self.log("Logging in...")
        conn.login()
        
        s = StringIO.StringIO()
    
        self.log("Downloading ftp://%s" % path)
        conn.retrbinary("RETR /"+path, file(self.apnicFileDb, "wb").write)
        self.log("Download complete!")
        conn.quit()
        self.log("Closing server connection")
    def log(self, msg):
        if self.verbose:
            print "IP2Country:%s" % msg
if __name__ == '__main__':
    
    import traceback, readline

    # run a demo
    print "I2PCountry demo"

    i2pc = IP2Country(verbose=True)

    while True:
        print "Enter an IP address, or empty line to quit"
        raw = raw_input("> ").strip()
        if raw == '':
            sys.exit(0)
        try:
            cc, country = i2pc.lookup(raw)
            print "%s => %s (%s)" % (raw, cc, country)
        except:
            traceback.print_exc()
            print "Lookup of IP address %s failed" % repr(raw)
