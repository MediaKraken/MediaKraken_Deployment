'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
from twisted.internet import ssl
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.internet import defer, reactor, protocol,task
from network import network_base_string as network_base
import time


class MediaKrakenServerApp(Factory):
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return network_base.NetworkEvents()


if __name__ == '__main__':
    reactor.listenSSL(7500, MediaKrakenServerApp(),
                      ssl.DefaultOpenSSLContextFactory('./key/privkey.pem', './key/cacert.pem'))
    reactor.run()
