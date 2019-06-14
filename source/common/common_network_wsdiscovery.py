import time
import urllib.parse

from WSDiscovery import WSDiscovery, QName
from onvif import ONVIFCamera, ONVIFError

ONVIF_TYPE_NVT = QName('http://www.onvif.org/ver10/network/wsdl', 'NetworkVideoTransmitter')
try_auth = [
    ('admin', ''),
    ('admin', 'ms1234'),
]

wsd = WSDiscovery()
wsd.start()

started = time.time()
seen_services = []
while time.time() - started < 10:
    services = wsd.searchServices(types=[ONVIF_TYPE_NVT])
    for service in services:
        if service.getXAddrs()[0] in seen_services:
            continue
        seen_services.append(service.getXAddrs()[0])
        parsed = urllib.parse.urlparse(service.getXAddrs()[0])
        parts = parsed.netloc.split(':')
        ip = parts[0]
        if len(parts) > 1:
            port = parts[1]
        else:
            port = 80
        for authinfo in try_auth:
            try:
                print("Trying ONVIFCamera({ip}, {port}, {user}, {passwd})".format(
                    ip=ip, port=port, user=authinfo[0], passwd=authinfo[1]
                ))
                mycam = ONVIFCamera(ip, port, authinfo[0], authinfo[1])
            except ONVIFError as e:
                print("Got error {}".format(e))
                continue
            print(" Scopes:")
            scopes = service.getScopes()
            for scope in scopes:
                print("  {}({})".format(type(scope), repr(scope)))
            print(" Streams:")
            media_service = mycam.create_media_service()
            profiles = media_service.GetProfiles()
            for profile in profiles:
                try:
                    params = media_service.create_type('GetStreamUri')
                    params.ProfileToken = profile._token
                    resp = media_service.GetStreamUri(params)
                    print("  {}".format(resp.Uri))
                except ONVIFError as e:
                    print("Got error {} from GetStreamUri({})".format(e, params))
                    print("Encoder config was {}".format(enc))
                    continue
            break
wsd.stop()
