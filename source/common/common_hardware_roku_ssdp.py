#   Copyright 2014 Dan Krause, Python 3 hack 2016 Adam Baxter
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# https://gist.github.com/dankrause/6000248

import http.client
import io
import socket


class SSDPResponse(object):
    """
    Class for interfacing via SSDP
    """

    class _FakeSocket(io.BytesIO):
        def makefile(self, *args, **kw):
            return self

    def __init__(self, response):
        ssdp_response = http.client.HTTPResponse(self._FakeSocket(response))
        ssdp_response.begin()
        self.location = ssdp_response.getheader("location")
        self.usn = ssdp_response.getheader("usn")
        self.st = ssdp_response.getheader("st")
        self.cache = ssdp_response.getheader("cache-control").split("=")[1]

    def __repr__(self):
        return "<SSDPResponse({location}, {st}, {usn})>".format(**self.__dict__)


def roku_discover(service="roku:ecp", timeout=5, retries=1, mx=3):
    """
    Discover Roku devices
    """
    group = ("239.255.255.250", 1900)
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        'HOST: {0}:{1}',
        'MAN: "ssdp:discover"',
        'ST: {st}', 'MX: {mx}', '', ''])
    socket.setdefaulttimeout(timeout)
    responses = {}
    for _ in range(retries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        message_bytes = message.format(*group, st=service, mx=mx).encode('utf-8')
        sock.sendto(message_bytes, group)
        while True:
            try:
                response = SSDPResponse(sock.recv(1024))
                responses[response.location] = response
            except socket.timeout:
                break
        sock.close()
    return list(responses.values())
