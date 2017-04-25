'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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
#from twisted.internet import protocol
from twisted.internet.protocol import Factory
from network import network_base_string_weblog as network_base
from common import common_logging
from common import common_signal
import time


class MediaKrakenServerApp(Factory):
    def __init__(self):
        # start logging
        common_logging.com_logging_start('./log_debug/WebLog_Subprogram_Reactor_String')
        # set other data
        self.server_start_time = time.mktime(time.gmtime())
        self.users = {} # maps user names to network instances
        logging.info("Ready for connections!")


    def buildProtocol(self, addr):
        return network_base.mediakraken_network_events(self.users, self.db_connection,
            self.genre_list)


if __name__ == '__main__':
    # set signal exit breaks
    common_signal.com_signal_set_break()
    # setup for the ssl keys
    reactor.listenSSL(5002, MediaKrakenServerApp(),
        ssl.DefaultOpenSSLContextFactory('./key/privkey.pem', './key/cacert.pem'))
    reactor.run()
