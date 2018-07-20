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

import json
import platform
import sys

from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from twisted.internet import reactor, ssl
# import twisted files that are required
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import Int32StringReceiver

networkProtocol = None
metaapp = None


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
        common_global.es_inst.com_elastic_index('info', {
            'Started to connect to': connector.getDestination()})

    def clientConnectionLost(self, conn, reason):
        common_global.es_inst.com_elastic_index('info', {'Connection Lost'})

    def clientConnectionFailed(self, conn, reason):
        common_global.es_inst.com_elastic_index('info', {'Connection Failed'})

    def buildProtocol(self, addr):
        common_global.es_inst.com_elastic_index('info', {'Connected to': str(addr)})
        self.protocol = TheaterClient()
        return self.protocol


class MediaKrakenApp(object):
    connection = None

    def exit_program(self):
        # close the database
        self.db_connection.db_close()

    def build(self):
        global metaapp
        root = MediaKrakenApp()
        metaapp = self
        # start logging
        common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
            'main_server_link')
        # open the database
        option_config_json, self.db_connection = common_config_ini.com_config_read()
        self.connect_to_server()
        return root

    def connect_to_server(self):
        """
        Connect to media server
        """
        reactor.connectSSL(sys.argv[1], int(sys.argv[2]),
                           TheaterFactory(self), ssl.ClientContextFactory())
        reactor.run()

    def process_message(self, server_msg):
        """
        Process network message from server
        """
        common_global.es_inst.com_elastic_index('info', {"body": server_msg})
        # network_base.NetworkEvents.ampq_message_received(body)
        json_message = json.loads(server_msg)
        common_global.es_inst.com_elastic_index('info', {'json body': json_message})
        msg = None
        if json_message['Type'] == "Ident":
            msg = "VALIDATE " + "link" + " " + "password" + " " + platform.node()
        elif json_message['Type'] == "Receive New Media":
            for new_media in json_message['Data']:
                common_global.es_inst.com_elastic_index('info', {'new_media': new_media})
                # returns: 0-mm_media_guid, 1-'Movie', 2-mm_media_ffprobe_json,
                # 3-mm_metadata_media_id jsonb
                metadata_guid = None
                if new_media[1] == 'Movie':
                    metadata_guid = self.db_connection.db_meta_guid_by_imdb(
                        new_media[3]['imdb'])
                    if metadata_guid is None:
                        metadata_guid = self.db_connection.db_meta_guid_by_tmdb(
                            new_media[3]['themoviedb'])
                        if metadata_guid is None:
                            metadata_guid = self.db_connection.db_meta_guid_by_tvdb(
                                new_media[3]['thetvdb'])
                elif new_media[1] == 'TV Show':
                    metadata_guid \
                        = self.db_connection.db_metatv_guid_by_imdb(new_media[3]['imdb'])
                    if metadata_guid is None:
                        metadata_guid = self.db_connection.db_metatv_guid_by_tvmaze(
                            new_media[3]['tvmaze'])
                        if metadata_guid is None:
                            metadata_guid = self.db_connection.db_metatv_guid_by_tvdb(
                                new_media[3]['thetvdb'])
                            if metadata_guid is None:
                                metadata_guid = self.db_connection.db_metatv_guid_by_tvrage(
                                    new_media[3]['tvrage'])
                elif new_media[1] == 'Sports':
                    metadata_guid = self.db_connection.db_metasports_guid_by_thesportsdb(
                        new_media[3]['thesportsdb'])
                elif new_media[1] == 'Music':
                    pass
                elif new_media[1] == 'Book':
                    pass
                if metadata_guid is None:
                    # find on internet
                    # for "keys" in new_media[3]
                    pass
                self.db_connection.db_insert_remote_media(json_message['Target'], new_media[0],
                                                          self.db_connection.db_media_uuid_by_class(
                                                              new_media[1]),
                                                          new_media[2], metadata_guid)
            self.db_connection.db_commit()
        else:
            common_global.es_inst.com_elastic_index('info', {'stuff': 'unknown message type'})
        if msg is not None:
            common_global.es_inst.com_elastic_index('info', {'stuff': 'should be sending data'})
            networkProtocol.sendString(msg)


if __name__ == '__main__':
    MediaKrakenApp().build()
