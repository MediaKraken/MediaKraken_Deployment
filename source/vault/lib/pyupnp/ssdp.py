from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from pyupnp.upnp import Device
from pyupnp.util import http_parse_raw

__author__ = 'Dean Gardiner'

SSDP_ADDR = "239.255.255.250"
SSDP_PORT = 1900


class SSDP_MSearch(DatagramProtocol):
    def __init__(self, cbFoundDevice=None, cbFinishedSearching=None, debug=False):
        self.port = None
        self.running = False
        self.debug = debug

        self.stopCall = None
        self.stopDelay = 10

        self.cbFoundDevice = cbFoundDevice
        self.cbFinishedSearching = cbFinishedSearching

        self.devices = {}

    @staticmethod
    def search(cbFoundDevice=None, cbFinishedSearching=None, target='ssdp:all', mx=5, stopDelay=10, debug=False):
        s = SSDP_MSearch(cbFoundDevice, cbFinishedSearching, debug=debug)
        s.listen()

        s.sendDiscover(target=target, mx=mx)
        s.sendDiscover(target=target, mx=mx)

        s.stopLater(construct=True, delay=stopDelay)

    def discover(self, target='ssdp:all', mx=5):
        self.sendDiscover(target=target, mx=mx)
        self.sendDiscover(target=target, mx=mx)

        self.stopLater(construct=True, delay=self.stopDelay)

    def listen(self):
        self._log("listen()")
        self.port = reactor.listenUDP(0, self)
        self.running = True

    def stopLater(self, construct=False, delay=None):
        if delay:
            self.stopDelay = delay

        if self.stopCall or construct:
            if self.stopCall:
                self.stopCall.cancel()
            self.stopCall = reactor.callLater(self.stopDelay, self.stop)

    def stop(self):
        self._log("stop()")
        self.port.stopListening()
        self.running = False
        if self.cbFinishedSearching:
            self.cbFinishedSearching(self.devices)

    def _log(self, *message):
        if self.debug:
            for m in list(message):
                print m,
            print

    def datagramReceived(self, data, (host, port)):
        self.stopLater()  # Reset Stop Delay

        version, respCode, respText, headers = http_parse_raw(data)

        if respCode == 200:
            valid = True
            valid = valid and self.header_exists(headers, 'usn')
            valid = valid and self.header_exists(headers, 'location')
            valid = valid and self.header_exists(headers, 'server')

            if not valid:
                return

            # Parse USN
            uuid, root, schema, name, type, version = None, None, None, None, None, None
            parsedUsn = self.parse_usn(headers['usn'])
            if not parsedUsn:
                return
            if len(parsedUsn) == 1:
                if parsedUsn[0]:
                    uuid = parsedUsn[0]
                    root = True
                else:
                    return
            elif parsedUsn[1]:
                uuid, root = parsedUsn
            else:
                uuid, root, schema, name, type, version = parsedUsn

            if not self.devices.has_key(uuid):
                self.devices[uuid] = Device(uuid, headers=headers, found=True)
                self.cbFoundDevice(self.devices[uuid])

            if not root and name == 'service':
                self.devices[uuid].set_service(schema, type, version)

    @staticmethod
    def header_exists(headers, key):
        if not key in headers.keys():
            return False
        return True

    @staticmethod
    def parse_usn(usn):
        usn_split = str(usn).split('::')

        uuid = None
        # Parse UUID
        if len(usn_split) > 0 and usn_split[0].startswith('uuid:'):
            _tmp = usn_split[0].index('uuid:') + 5
            if ':' in usn_split[0][_tmp:]:
                return None
            uuid = usn_split[0][_tmp:]

        schema = None
        name = None
        type = None
        version = None
        # Parse URN / upnp:rootdevice
        if len(usn_split) > 1:
            _urn = usn_split[1].split(':')

            # sanity check
            if len(_urn) <= 0:
                return None

            if _urn[0] == 'upnp':
                if len(_urn) != 2:
                    return None
                return uuid, True  # [1] = Root?
            elif _urn[0] == 'urn':
                if len(_urn) != 5:
                    return None
                schema = _urn[1]
                name = _urn[2].lower()
                type = _urn[3]
                version = _urn[4]

                return uuid, False, schema, name, type, version  # [1] = Root?

        return uuid,  # [1] = urn type

    def sendDiscover(self, target='ssdp:all', mx=5):
        msg = '\r\n'.join(['M-SEARCH * HTTP/1.1',
                           'HOST: %s:%d' % (SSDP_ADDR, SSDP_PORT),
                           'MAN: "ssdp:discover"',
                           'MX: %d' % mx,
                           'ST: %s' % target,
                           '', ''])

        self.transport.write(msg, (SSDP_ADDR, SSDP_PORT))