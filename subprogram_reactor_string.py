'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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
from network import network_base_string as network_base
from common import common_celery
from common import common_config_ini
from common import common_logging
from common import common_signal
import time


class MediaKrakenServerApp(Factory):
    def __init__(self):
        # start logging
        common_logging.com_logging_start('./log/MediaKraken_Subprogram_Reactor_String')
        # set other data
        self.server_start_time = time.mktime(time.gmtime())
        self.users = {} # maps user names to network instances
        # preload some data from database
        self.option_config_json, self.db_connection = common_config_ini.com_config_read()
        self.genre_list = self.db_connection.db_meta_genre_list()
        logging.info("Ready for connections!")

        # setup celery instance for consumer
        self.celery = common_celery.app
        # concurrency arg is threads but defaults to number of CPUs available
        self.celery.start(argv=['celery', 'worker', '-Q', 'mkque', '-E'])
#        self.celery.start(argv=['celery', '-A', 'mkque', 'worker'])

#        celery -A tasks worker -Q high --concurrency=2
#        celery -A tasks worker -Q normal --concurrency=1
#        celery -A tasks worker -Q low,normal --concurrency=1


    def buildProtocol(self, addr):
        return network_base.NetworkEvents(self.users, self.db_connection,
            self.genre_list, self.option_config_json)


if __name__ == '__main__':
    # set signal exit breaks
    common_signal.com_signal_set_break()
    # setup for the ssl keys
    reactor.listenTCP(8903, MediaKrakenServerApp())
#    reactor.listenSSL(8903, MediaKrakenServerApp(),
#                      ssl.DefaultOpenSSLContextFactory('./key/privkey.pem', './key/cacert.pem'))
    reactor.run()
