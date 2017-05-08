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
import os
import platform
import subprocess
from threading import Event, Thread
try:
    import cPickle as pickle
except:
    import pickle
import sys
import uuid
from common import common_celery
from common import common_logging
from common import common_network_share
from common import common_signal
from common import common_system
from common import common_version
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, protocol
from twisted.internet import ssl

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        #self.factory.app.print_message(data)
        self.factory.app.process_message(data)
        logging.info(data)

        """
        Process network message from server
        """
        # otherwise the pickle can end up in thousands of chunks
        message_words = data.split(' ', 1)
        logging.info('message: %s', message_words[0])
        logging.info("len: %s", len(data))
        logging.info("chunks: %s", len(message_words))
        msg = None
        try:
            pickle_data = pickle.loads(message_words[1])
        except:
            pickle_data = None
        if message_words[0] == "IDENT":
            msg = "VALIDATE " + "slave-" + str(uuid.uuid4()) + " " + " " + " " + platform.node()
        # user commands
        elif message_words[0] == "PLAYMEDIA":
            self.proc_ffmpeg_stream = subprocess.Popen(pickle.loads(message_words[1]),
                                                       shell=False)
        elif message_words[0] == "CASTMEDIA":
            self.proc_ffmpeg_cast = subprocess.Popen(("python stream2chromecast.py " \
                                                      "-devicename %s -transcodeopts '-c:v copy -c:a ac3 " \
                                                      "-movflags faststart+empty_moov' -transcode %s",
                                                      (pickle_data[0],
                                                       pickle_data[1])), shell=False)
        # admin commands
        elif message_words[0] == "CPUUSAGE":
            msg = 'CPUUSAGE ' + pickle.dumps(common_system.com_system_cpu_usage(False))
        elif message_words[0] == "DISKUSAGE":
            msg = 'DISKUSAGE ' + pickle.dumps(common_system.com_system_disk_usage_all(True))
        elif message_words[0] == "MEMUSAGE":
            msg = 'MEMUSAGE ' + pickle.dumps(common_system.com_system_virtual_memory(False))
        elif message_words[0] == "SYSSTATS":
            msg = 'SYSSTATS ' + pickle.dumps((common_system.com_system_cpu_usage(True),
                                              common_system.com_system_disk_usage_all(True),
                                              common_system.com_system_virtual_memory(False)))
        else:
            logging.info("unknown message type")
        if msg is not None:
            logging.info("should be sending data")
            self.transport.write(msg.encode("utf8"))


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        #self.app.print_message("connection lost")
        logging.info('connection lost')

    def clientConnectionFailed(self, conn, reason):
        #self.app.print_message("connection failed")
        logging.info('connection failed')


class MediaKrakenApp():

    def exit_program(self):
        pass

    def build(self):
        root = MediaKrakenApp()
        self.connect_to_server()
        return root

    def connect_to_server(self):
        """
        Connect to media server
        """
        reactor.connectSSL('mkserver', 8903,
                           EchoFactory(self), ssl.ClientContextFactory())
        reactor.run()

if __name__ == '__main__':
    # start logging
    common_logging.com_logging_start('./log/MediaKraken_Slave')
    # set signal exit breaks
    common_signal.com_signal_set_break()
    MediaKrakenApp().build()
