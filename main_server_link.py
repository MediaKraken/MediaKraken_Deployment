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

__version__ = '0.1.0'

# pull in the ini file config
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import os
import platform
import subprocess
from threading import Timer
from threading import Event, Thread
try:
    import cPickle as pickle
except:
    import pickle
import sys
import logging
sys.path.append("./MediaKraken_Common")
import MK_Common_Logging
import MK_Common_System
sys.path.append("./") # for db import
import database as database_base

# import twisted files that are required
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor, ssl
from twisted.protocols.basic import Int32StringReceiver

networkProtocol = None
metaapp = None


def signal_receive(signum, frame):
    global proc_ffserver
    print 'CHILD Link: Received USR1'
    os.kill(proc_ffserver.pid)
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


class MediaKrakenApp():
    connection = None


    def exit_program(self):
        # close the database
        self.db.MK_Server_Database_Close()


    def build(self):
        global metaapp
        root = MediaKrakenApp()
        metaapp = self
        # start logging
        MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Link')
        # open the database
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open(Config.get('DB Connections', 'PostDBHost').strip(), Config.get('DB Connections', 'PostDBPort').strip(), Config.get('DB Connections', 'PostDBName').strip(), Config.get('DB Connections', 'PostDBUser').strip(), Config.get('DB Connections', 'PostDBPass').strip())
        self.connect_to_server()
        return root


    def connect_to_server(self):
        reactor.connectSSL(sys.argv[1], int(sys.argv[2]), TheaterFactory(self), ssl.ClientContextFactory())
        reactor.run()


    def process_message(self, server_msg):
        messageWords = server_msg.split(' ', 1)  # otherwise the pickle can end up in thousands of chunks
        logging.debug('message: %s', messageWords[0])
        logging.debug("len: %s", len(server_msg))
        logging.debug("chunks: %s", len(messageWords))
        msg = None
        try:
            pickle_data = pickle.loads(messageWords[1])
        except:
            pickle_data = None
        if messageWords[0] == "IDENT":
            msg = "VALIDATE " + "link" + " " + "password" + " " + platform.node()
        elif messageWords[0] == "PING":  # Client_Network
            msg = "PONG"
        elif messageWords[0] == "SHUTDOWN":
            sys.exit(0)
        elif messageWords[0] == "RECEIVENEWMEDIA":
            for new_media in pickle.loads(messageWords[1]):
                logging.debgu("new media: %s", new_media)
                # returns: 0-mm_media_guid, 1-'Movie', 2-mm_media_ffprobe_json, 3-mm_metadata_media_id jsonb
                metadata_guid = None
                if new_media[1] == 'Movie':
                    metadata_guid = self.db.MK_Server_Database_Metadata_GUID_By_IMDB(new_media[3]['IMDB'])
                    if metadata_guid is None:
                        metadata_guid = self.db.MK_Server_Database_Metadata_GUID_By_TMDB(new_media[3]['TMDB'])
                        if metadata_guid is None:
                            metadata_guid = self.db.MK_Server_Database_Metadata_GUID_By_TVDB(new_media[3]['theTVDB'])
                elif new_media[1] == 'TV Show':
                    metadata_guid = self.db.MK_Server_Database_MetadataTV_GUID_By_IMDB(new_media[3]['IMDB'])
                    if metadata_guid is None:
                        metadata_guid = self.db.MK_Server_Database_MetadataTV_GUID_By_TVMaze(new_media[3]['TVMaze'])
                        if metadata_guid is None:
                            metadata_guid = self.db.MK_Server_Database_MetadataTV_GUID_By_TVDB(new_media[3]['theTVDB'])
                            if metadata_guid is None:
                                metadata_guid = self.db.MK_Server_Database_MetadataTV_GUID_By_TVRage(new_media[3]['TVRage'])
                elif new_media[1] == 'Sports':
                    metadata_guid = self.db.MK_Server_Database_MetadataSports_GUID_By_TheSportsDB(new_media[3]['TheSportsDB'])
                elif new_media[1] == 'Music':
                    pass
                elif new_media[1] == 'Book':
                    pass
                if metadata_guid is None:
                    # find on internet
                    # for "keys" in new_media[3]
                    pass
                self.db.MK_Server_Database_Insert_Remote_Media(link_server, new_media[0], self.db.MK_Server_Database_Media_UUID_By_Class(new_media[1]), new_media[2], metadata_guid)
            self.db.MK_Server_Database_Commit()
        else:
            logging.debug("unknown message type")
        if msg is not None:
            logging.debug("should be sending data")
            networkProtocol.sendString(msg)


if __name__ == '__main__':
    # store pid for initd
    pid = os.getpid()
    op = open("/var/mm_link.pid", "w")
    op.write("%s" % pid)
    op.close()
    MediaKrakenApp().build()
