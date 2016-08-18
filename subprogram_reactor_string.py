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
import ConfigParser
config_handle = ConfigParser.ConfigParser()
config_handle.read("MediaKraken.ini")
from twisted.internet import ssl
from twisted.internet import reactor
from twisted.internet import protocol
from twisted.internet.protocol import Factory
import sys
from network import network_base_string as network_base
import database as database_base
from common import common_file
from common import common_logging
from time import time
import time  # yes, use both otherwise some time code below breaks
import os
import signal


# create the file for pid
pid_file = './pid/' + str(os.getpid())
common_file.com_file_save_data(pid_file, 'Sub_Reactor_String', False, False, None)


def signal_receive(signum, frame):
    print('CHILD Reactor String: Received USR1')
    # remove pid
    os.remove(pid_file)
    # cleanup db
    self.db_connection.db_rollback()
    self.db_connection.db_close()
    sys.stdout.flush()
    sys.exit(0)


class MediaKrakenServerApp(Factory):
    def __init__(self):
        # start logging
        common_logging.com_logging_start('./log/MediaKraken_Subprogram_Reactor_String')
        # set other data
        self.server_start_time = time.mktime(time.gmtime())
        self.users = {} # maps user names to network instances
        # open the database
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(config_handle.get('DB Connections', 'PostDBHost').strip(),\
            config_handle.get('DB Connections', 'PostDBPort').strip(),\
            config_handle.get('DB Connections', 'PostDBName').strip(),\
            config_handle.get('DB Connections', 'PostDBUser').strip(),\
            config_handle.get('DB Connections', 'PostDBPass').strip())
        # preload some data from database
        self.genre_list = self.db_connection.db_meta_genre_list()
        logging.info("Ready for connections!")


    def buildProtocol(self, addr):
        return network_base.Metaman_Network_Events(self.users, self.db_connection. self.genre_list)


if __name__ == '__main__':
    if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
        signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
    else:
        signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
        signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c
    # setup for the ssl keys
    sslContext = ssl.DefaultOpenSSLContextFactory('key/privkey.pem', 'key/cacert.pem')
    reactor.listenSSL(int(config_handle.get('MediaKrakenServer', 'ListenPort').strip()),\
        MediaKrakenServerApp(), sslContext)
    reactor.run()
    # remove pid
    os.remove(pid_file)
