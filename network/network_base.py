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
import json
import sys
import os
import signal
sys.path.append("./vault/lib")
import subprocess
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.internet import ssl
import ip2country
from common import common_docker
from common import common_network


class NetworkEvents(Protocol):
    """
    Process the network events for the server
    """
    # init is called on every connection
    def __init__(self, users, db_connection):
        # server info
        self.db_connection = db_connection
        self.users = users
        self.user_device_uuid = None
        self.user_ip_addy = None
        self.user_user_name = None
        self.user_platform = None
        self.user_slave = False
        self.user_verified = 0
        self.user_country_code = None
        self.user_country_name = None
        self.user_cpu_usage = 0
        self.proc_file_scan = None
        self.proc_media_match = None
        self.proc_chapter_create = None
        self.proc_anime_match = None
        self.proc_subtitle_media_match = None


    def connectionMade(self):
        """
        Network connection made from client so ask for ident
        """
        logging.info('Got Connection')
        self.transport.write(json.dumps({'Type': 'Ident'}).encode("utf8"))


    def connectionLost(self, reason):
        """
        Network connection dropped so remove client
        """
        logging.info('Lost Connection')
        if self.users.has_key(self.user_user_name):
            del self.users[self.user_user_name]


    def dataReceived(self, data):
        """
        Message received from client
        """
        msg = None
        logging.info('GOT Data: %s', data)
        json_message = json.loads(data)
        logging.info('Message: %s', json_message)

        if json_message['Type'] == "CPU Usage":
            self.user_cpu_usage[self.user_ip_addy] = json_message['Data']

        elif json_message['Type'] == "Genre List":
            msg = json.dumps({"Genre List": self.db_connection.db_meta_genre_list()})

        elif json_message['Type'] == "Flag Mismatch UUID":
            pass

        elif json_message['Type'] == "Ident":
            # have to create the self.player data so network knows how to send data back
            self.user_device_uuid = json_message['UUID']
            self.user_ip_addy = str(self.transport.getPeer()).split('\'')[1]
            self.user_user_name = None
            self.user_platform = json_message['Platform']
            # lookup the country
            country_data = ip2country.IP2Country(verbose=1).lookup(self.user_ip_addy)
            self.user_country_code = country_data[0]
            self.user_country_name = country_data[1]
            self.users[self.user_device_uuid] = self
            logging.info("user: %s %s", self.user_device_uuid, self.user_ip_addy)
            if self.user_user_name == 'Link':
                pass

        elif json_message['Type'] == "Image":
            lookup_id = None
            media_id = None
            if json_message['Sub'] == 'Album':
                pass
            elif json_message['Sub'] == 'Book':
                pass
            elif json_message['Sub'] == 'Game':
                pass
            elif json_message['Sub'] == 'Movie':
                lookup_id, media_id = self.db_connection.db_media_random('Poster')
            elif json_message['Sub'] == 'TV Show':
                pass
            else:
                # fetch specific id
                try:
                    lookup_id = self.db_connection.db_media_image_path(json_message['Data'])
                except:
                    pass
            if lookup_id is not None:
                msg = json.dumps({"Type": "Image", "Data": 'https://' + self.server_ip.strip()
                                + ':' + self.server_port_image.strip() + '/'
                                + lookup_id, "UUID": media_id})

        elif json_message['Type'] == "Login":
            pass

        elif json_message['Type'] == "Media":
            if json_message['Sub'] == 'Detail':
                mm_media_ffprobe_json, mm_metadata_json, mm_metadata_localimage_json \
                    = self.db_connection.db_read_media_metadata_movie_both(json_message['UUID'])
                msg = json.dumps({'Type': 'Media', 'Sub': 'Detail',
                    'Data': mm_metadata_json, 'Data2': mm_media_ffprobe_json, 'Data3': mm_metadata_localimage_json})
            elif json_message['Sub'] == 'List':
                # (Offset, Limit)
                if json_message['Data'] == 'Movie':
                    if 'Offset' in json_message:
                        msg = json.dumps({'Type': 'Media', 'Sub': 'List', 'Data':
                            self.db_connection.db_web_media_list(
                            self.db_connection.db_media_uuid_by_class(json_message['Data']),
                            json_message['Type'], offset=json_message['Offset'],
                            list_limit=json_message['Limit'])})
                    else:
                        msg = json.dumps({'Type': 'Media', 'Sub': 'List', 'Data': self.db_connection.db_web_media_list(
                                         self.db_connection.db_media_uuid_by_class(json_message['Data']),
                                         json_message['Type'])})
            elif json_message['Sub'] == 'In Progress':
                # (Offset, Limit)
                pass
            elif json_message['Sub'] == 'New':
                msg = json.dumps({'Type': 'Media', 'Sub': 'New',
                    'Data': self.db_connection.db_read_media_new(json_message['Offset'], json_message['Limit'])})
            elif json_message['Sub'] == 'Update':
                # (playback, love, hate, etc)
                pass

        elif json_message['Type'] == "Metadata":
            pass

        elif json_message['Type'] == "Play":
            media_path = self.db_connection.db_media_path_by_uuid(json_message['UUID'])[0]
            if media_path is not None:
                # launch and attach to local running ffserver
                http_link = 'http://localhost:' + self.server_port_ffmpeg + '/stream.ffm'
                self.proc_ffmpeg_stream = subprocess.Popen(['ffmpeg', '-i',
                    media_path, http_link], shell=False)
                http_link = 'http://' + common_network.mk_network_get_default_ip() + ':'\
                    + self.server_port_ffmpeg + '/stream.ffm'
            msg = json.dumps({"Type": 'Play', 'Data': http_link})

        elif json_message['Type'] == "User":
            pass

        #  elif json_message['Type'] == "MediaIDUpdateUUID":
        #     # media id, metadata id
        #     self.db_connection.db_update_media_id(message_words[1], message_words[2])
        #
        # elif json_message['Type'] == "VIDEOGENRELIST":
        #     msg = "VIDEOLIST " + pickle.dumps(self.db_connection.db_web_media_list(
        #         self.db_connection.db_media_uuid_by_class("Movie"),
        #         json_message['Type'], message_words[1]))
        #
        # elif json_message['Type']== "movie" or json_message['Type'] == "recent_addition"\
        #         or json_message['Type'] == 'in_progress' or json_message['Type'] == 'video':
        #     msg = "VIDEOLIST " + json.dumps(self.db_connection.db_web_media_list(
        #         self.db_connection.db_media_uuid_by_class("Movie"), json_message['Type']))

        else:
            logging.error("UNKNOWN TYPE: %s", json_message['Type'])
            msg = "UNKNOWN_TYPE"
        if msg is not None:
            logging.info("should be sending data len: %s", len(msg))
            self.transport.write(msg.encode("utf8"))


    def send_single_user(self, message):
        """
        Send message to single user
        """
        for user_device_uuid, protocol in self.users.iteritems(): # pylint: disable=W0612
            if protocol == self:
                logging.info('send single: %s', message)
                protocol.transport.write(message.encode("utf8"))
                break


    def send_all_users(self, message):
        """
        Send message to all users
        """
        for user_device_uuid, protocol in self.users.iteritems():
            if self.users[user_device_uuid].user_verified == 1:
                logging.info('send all: %s', message)
                protocol.transport.write(message.encode("utf8"))


    def send_all_links(self, message):
        """
        Send to all linked servers
        """
        for user_device_uuid, protocol in self.users.iteritems():
            if self.users[user_device_uuid].user_link:
                logging.info('send all link: %s', message)
                protocol.transport.write(message.encode("utf8"))
