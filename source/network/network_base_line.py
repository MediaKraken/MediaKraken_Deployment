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

import base64
import json
import uuid

from common import common_docker
from common import common_global
from common import common_network
from twisted.protocols import basic


class NetworkEvents(basic.LineReceiver):
    """
    Process the network events for the server
    """
    MAX_LENGTH = 32000000  # pylint: disable=C0103

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
        ip_addr, port = self.transport.client
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Got Connection', 'ip': ip_addr})
        self.sendLine(json.dumps({'Type': 'Ident'}).encode("utf8"))

    def connectionLost(self, reason):
        """
        Network connection dropped so remove client
        """
        ip_addr, port = self.transport.client
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Lost Connection',
                                                         'ip': ip_addr})
        for user_device_uuid, protocol in self.users.items():
            if self.users[user_device_uuid].user_ip_addy == ip_addr:
                del self.users[user_device_uuid]
                break

    def lineReceived(self, data):
        """
        Message received from client
        """
        msg = None
        json_message = json.loads(data.decode())
        common_global.es_inst.com_elastic_index('info', {'Message': json_message})

        if json_message['Type'] == "CPU Usage":
            self.user_cpu_usage[self.user_ip_addy] = json_message['Data']

        elif json_message['Type'] == 'Device Cast List':
            msg = json.dumps({'Type': 'Device Cast List',
                              'Data': self.db_connection.db_device_list(device_type='cast')})

        elif json_message['Type'] == 'Device Play List':
            play_device = []
            # load cast devices
            for cast_device in self.db_connection.db_device_list(device_type='cast'):
                play_device.append((cast_device['mm_device_id'], 'Cast',
                                    cast_device['mm_device_json']['Name']))
            # load user clients
            for user_device_uuid, protocol in self.users.items():
                play_device.append((user_device_uuid, 'Client',
                                    self.users[user_device_uuid].user_ip_addy))
            # TODO ip addy for now on above
            #                                   self.users[user_device_uuid].user_user_name))
            msg = json.dumps({'Type': 'Device Play List', 'Data': play_device})

        elif json_message['Type'] == "Genre List":
            msg = json.dumps({'Type': 'Genre List',
                              'Data': self.db_connection.db_meta_genre_list()})

        elif json_message['Type'] == "Flag Mismatch UUID":
            pass

        elif json_message['Type'] == "Ident":
            # have to create the self.player data so network knows how to send data back
            self.user_device_uuid = json_message['UUID']
            ip_addr, port = self.transport.client
            self.user_ip_addy = ip_addr
            self.user_user_name = None
            self.user_platform = json_message['Platform']
            # lookup the country
            country_data = common_network.mk_network_country_code()
            self.user_country_code = country_data['country_code']
            self.user_country_name = country_data['country_name']
            self.users[self.user_device_uuid] = self
            common_global.es_inst.com_elastic_index('info', {"user": self.user_device_uuid,
                                                             'ip': self.user_ip_addy})
            if self.user_user_name == 'Link':
                pass
            else:
                user_data = []
                for user in self.db_connection.db_user_list_name():
                    if user['active'] == True:
                        user_data.append((user['id'], user['username']))
                msg = json.dumps({'Type': 'User', 'Data': user_data})
        elif json_message['Type'] == "Image":
            metadata_id = None
            image_json = None
            if json_message['Subtype'] == 'Album':
                # metadata_id is needed so client can id the media when clicked
                image_json, metadata_id = self.db_connection.db_meta_album_image_random()
            elif json_message['Subtype'] == 'Book':
                # metadata_id is needed so client can id the media when clicked
                image_json, metadata_id \
                    = self.db_connection.db_meta_book_image_random(json_message['Image Type'])
            elif json_message['Subtype'] == 'Game':
                # metadata_id is needed so client can id the media when clicked
                image_json, metadata_id \
                    = self.db_connection.db_meta_game_image_random(json_message['Image Type'])
            elif json_message['Subtype'] == 'Movie':
                # metadata_id is needed so client can id the media when clicked
                if json_message['Image Media Type'] == 'Main' or json_message[
                    'Image Media Type'] == 'Movie' \
                        or json_message['Image Media Type'] == 'Demo':
                    image_json, metadata_id \
                        = self.db_connection.db_meta_movie_image_random(json_message['Image Type'])
                elif json_message['Image Media Type'] == 'New Movie':
                    pass
                elif json_message['Image Media Type'] == 'In Progress':
                    pass
            elif json_message['Subtype'] == 'TV Show':
                # metadata_id is needed so client can id the media when clicked
                image_json, metadata_id \
                    = self.db_connection.db_meta_tvshow_image_random(json_message['Image Type'])
            if metadata_id is not None and image_json is not None:
                common_global.es_inst.com_elastic_index('info', {"metadata_id": metadata_id,
                                                                 "image_json": image_json})
                image_handle = open(image_json, "rb")
                image_data = image_handle.read()
                image_data = base64.b64encode(image_data)
                image_handle.close()
                msg = json.dumps({"Type": "Image", "Subtype": json_message['Subtype'],
                                  "Image Media Type": json_message['Image Media Type'],
                                  "Data": image_data, "UUID": metadata_id})

        elif json_message['Type'] == "Login":
            self.db_connection.db_user_login(
                json_message['User'], json_message['Password'])

        elif json_message['Type'] == "Media":
            if json_message['Subtype'] == 'Controller':
                pass
            elif json_message['Subtype'] == 'Detail':
                mm_media_ffprobe_json, mm_metadata_json, mm_metadata_localimage_json \
                    = self.db_connection.db_read_media_metadata_movie_both(json_message['UUID'])
                msg = json.dumps({'Type': 'Media', 'Subtype': 'Detail',
                                  'Data': mm_metadata_json, 'Data2': mm_media_ffprobe_json,
                                  'Data3': mm_metadata_localimage_json})
            elif json_message['Subtype'] == 'List':
                # (Offset, Limit)
                if json_message['Data'] == 'Movie':
                    if 'Offset' in json_message:
                        msg = json.dumps({'Type': 'Media', 'Subtype': 'List', 'Data':
                            self.db_connection.db_web_media_list(
                                self.db_connection.db_media_uuid_by_class(
                                    json_message['Data']),
                                json_message['Type'], offset=json_message['Offset'],
                                list_limit=json_message['Limit'])})
                    else:
                        msg = json.dumps({'Type': 'Media', 'Subtype': 'List',
                                          'Data': self.db_connection.db_web_media_list(
                                              self.db_connection.db_media_uuid_by_class(
                                                  json_message['Data']),
                                              json_message['Type'])})
            elif json_message['Subtype'] == 'In Progress':
                # (Offset, Limit)
                pass
            elif json_message['Subtype'] == 'New':
                msg = json.dumps({'Type': 'Media', 'Subtype': 'New',
                                  'Data': self.db_connection.db_read_media_new(
                                      json_message['Offset'],
                                      json_message['Limit'])})
            elif json_message['Subtype'] == 'Update':
                # (playback, love, hate, etc)
                pass

        elif json_message['Type'] == "Play":
            # TODO send this to pika so only have to code once and will be in the current running
            if json_message['Subtype'] == 'Cast':
                for client in common_global.client_devices:
                    if json_message['Target'] == client[1]:
                        # to address the 30 char name limit for container
                        name_container = ((json_message['User'] + '_'
                                           + str(uuid.uuid4()).replace('-', ''))[-30:])
                        cast_docker_inst = common_docker.CommonDocker()
                        cast_docker_inst.com_docker_run_slave(hwaccel=False,
                                                              name_container=name_container,
                                                              container_command=("python3 "
                                                                                 "./stream2chromecast/stream2chromecast.py -devicename %s -transcodeopts '-vcodec libx264 -acodec aac -movflags frag_keyframe+empty_moov' -transcode %s" % (
                                                                                     json_message[
                                                                                         'Target'],
                                                                                     self.db_connection.db_media_path_by_uuid(
                                                                                         json_message[
                                                                                             'UUID']))))
                # TODO obviously send to the proper client
                self.send_all_users(json_message)
            else:
                media_path = self.db_connection.db_media_path_by_uuid(json_message['UUID'])
                common_global.es_inst.com_elastic_index('info', {"media_path": media_path})
                if media_path is not None:
                    if json_message['Subtype'] == 'Client':
                        self.send_single_ip(
                            json.dumps({'Type': 'Play', 'Data': media_path}),
                            json_message['Target'])

        elif json_message['Type'] == "MPV":
            self.send_all_users(json_message['Data'])

        else:
            common_global.es_inst.com_elastic_index('error', {"UNKNOWN TYPE": json_message['Type']})
            msg = "UNKNOWN_TYPE"
        if msg is not None:
            common_global.es_inst.com_elastic_index('info',
                                                    {"should be sending data len": len(msg)})
            self.sendLine(msg.encode("utf8"))

    def send_single_ip(self, message, ip_addr):
        """
        Send message to ip addr
        """
        for user_device_uuid, protocol in self.users.items():
            common_global.es_inst.com_elastic_index('info',
                                                    {"user_ip_addy": self.users[
                                                        user_device_uuid].user_ip_addy,
                                                     'ip': ip_addr})
            if self.users[user_device_uuid].user_ip_addy == ip_addr:
                common_global.es_inst.com_elastic_index('info', {'send ip': ip_addr,
                                                                 'message': message})
                protocol.sendLine(message.encode("utf8"))
                break

    def send_single_user(self, message):
        """
        Send message to single user
        """
        for user_device_uuid, protocol in self.users.items():  # pylint: disable=W0612
            if protocol == self:
                common_global.es_inst.com_elastic_index('info', {'send single': message})
                protocol.sendLine(message.encode("utf8"))
                break

    def send_all_users(self, message):
        """
        Send message to all users
        """
        for user_device_uuid, protocol in self.users.items():
            if self.users[user_device_uuid].user_verified == 1:
                common_global.es_inst.com_elastic_index('info', {'send all': message})
                protocol.sendLine(message.encode("utf8"))

    def send_all_links(self, message):
        """
        Send to all linked servers
        """
        for user_device_uuid, protocol in self.users.items():
            if self.users[user_device_uuid].user_link:
                common_global.es_inst.com_elastic_index('info', {'send all links': message})
                protocol.sendLine(message.encode("utf8"))
