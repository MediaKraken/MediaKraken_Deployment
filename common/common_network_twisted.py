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
try:
    import cPickle as pickle
except:
    import pickle
import sys
import subprocess
import platform
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, ssl
from twisted.protocols.basic import Int32StringReceiver


networkProtocol = None
metaapp = None


def signal_receive(signum, frame): # pylint: disable=W0613
    """
    Handle signal interupt
    """
    global proc_ffserver
    print('CHILD Slave: Received USR1')
    sys.stdout.flush()
    sys.exit(0)


class TheaterClient(Int32StringReceiver):
    STARTED = 0
    CHECKING_PORT = 1
    CONNECTED = 2
    NOTSTARTED = 3
    PORTCLOSED = 4
    CLOSED = 5


    def __init__(self):
        self.MAX_LENGTH = 32000000
        self.connStatus = TheaterClient.STARTED


    def connectionMade(self):
        global networkProtocol
        self.connStatus = TheaterClient.CONNECTED
        networkProtocol = self


    def stringReceived(self, data):
        MediaKrakenApp.process_message(metaapp, data)


class TheaterFactory(ClientFactory):


    def __init__(self, app):
        self.app = app
        self.protocol = None


    def startedConnecting(self, connector):
        logging.info('Started to connect to %s', connector.getDestination())


    def clientConnectionLost(self, conn, reason):
        logging.info("Connection Lost")


    def clientConnectionFailed(self, conn, reason):
        logging.info("Connection Failed")


    def buildProtocol(self, addr):
        logging.info('Connected to %s', str(addr))
        self.protocol = TheaterClient()
        return self.protocol


class MediaKrakenApp(object):
    connection = None


    def exit_program(self):
        pass


    def build(self):
        global metaapp
        root = MediaKrakenApp()
        metaapp = self
        self.connect_to_server()
        return root


    def connect_to_server(self, host_port, host_addr, use_ssl=True):
        """
        Connect to debug server
        """
        if use_ssl:
            reactor.connectSSL(host_addr, host_port,
                TheaterFactory(self), ssl.ClientContextFactory())
        else:
            reactor.connectTCP(host_addr, host_port,
                TheaterFactory(self), ssl.ClientContextFactory())
        reactor.run()


    def process_message(self, server_msg):
        """
        Process network message from server
        """
        message_words = server_msg.split(' ', 1)
        logging.info('message: %s', message_words[0])
        logging.info("len: %s", len(server_msg))
        logging.info("chunks: %s", len(message_words))
        msg = None
        if message_words[0] == "IDENT":
            msg = "VALIDATE " + "slave" + " " + "password" + " " + platform.node()
        # user commands
        elif message_words[0] == "PLAYMEDIA":
            self.proc_ffmpeg_stream = subprocess.Popen(pickle.loads(message_words[1], shell=False))
        else:
            logging.info("unknown message type")
        if msg is not None:
            logging.info("should be sending data")
            networkProtocol.sendString(msg)


if __name__ == '__main__':
    MediaKrakenApp().build()
