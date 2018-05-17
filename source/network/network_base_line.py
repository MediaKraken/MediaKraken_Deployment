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

import base64
import json
import sys
import uuid

sys.path.append("./vault/lib")
from twisted.protocols import basic
import ip2country
from common import common_docker
from common import common_global


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
        ip_addr = str(self.transport.getPeer()).split('\'')[1]
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Got Connection', 'ip': ip_addr})
        self.sendLine(json.dumps({'Type': 'Ident'}).encode("utf8"))

    def connectionLost(self, reason):
        """
        Network connection dropped so remove client
        """
        ip_addr = str(self.transport.getPeer()).split('\'')[1]
        common_global.es_inst.com_elastic_index('info', {'stuff': 'Lost Connection',
                                                         'ip': ip_addr})
        for user_device_uuid, protocol in self.users.iteritems():
            if self.users[user_device_uuid].user_ip_addy == ip_addr:
                del self.users[user_device_uuid]
                break

    def lineReceived(self, data):
        """
        Message received from client
        """
        msg = None
        common_global.es_inst.com_elastic_index('info', {'GOT Data': data})
        json_message = json.loads(data)
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
            for user_device_uuid, protocol in self.users.iteritems():
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
            self.user_ip_addy = str(self.transport.getPeer()).split('\'')[1]
            self.user_user_name = None
            self.user_platform = json_message['Platform']
            # lookup the country
            country_data = ip2country.IP2Country(verbose=1).lookup(self.user_ip_addy)
            self.user_country_code = country_data[0]
            self.user_country_name = country_data[1]
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
            if json_message['Sub'] == 'Album':
                # metadata_id is needed so client can id the media when clicked
                image_json, metadata_id = self.db_connection.db_meta_album_image_random()
            elif json_message['Sub'] == 'Book':
                # metadata_id is needed so client can id the media when clicked
                image_json, metadata_id \
                    = self.db_connection.db_meta_book_image_random(json_message['Sub3'])
            elif json_message['Sub'] == 'Game':
                # metadata_id is needed so client can id the media when clicked
                image_json, metadata_id \
                    = self.db_connection.db_meta_book_image_random(json_message['Sub3'])
            elif json_message['Sub'] == 'Movie':
                # metadata_id is needed so client can id the media when clicked
                if json_message['Sub2'] == 'Main' or json_message['Sub2'] == 'Movie' \
                        or json_message['Sub2'] == 'Demo':
                    image_json, metadata_id \
                        = self.db_connection.db_meta_movie_image_random(json_message['Sub3'])
                elif json_message['Sub2'] == 'New Movie':
                    pass
                elif json_message['Sub2'] == 'In Progress':
                    pass
            elif json_message['Sub'] == 'TV Show':
                # metadata_id is needed so client can id the media when clicked
                image_json, metadata_id \
                    = self.db_connection.db_meta_tvshow_image_random(json_message['Sub3'])
            if metadata_id is not None and image_json is not None:
                image_handle = open(image_json, "rb")
                image_data = image_handle.read()
                image_data = base64.b64encode(image_data)
                image_handle.close()
                msg = json.dumps({"Type": "Image", "Sub": json_message['Sub'],
                                  "Sub2": json_message['Sub2'],
                                  "Data": image_data, "UUID": metadata_id})

        elif json_message['Type'] == "Login":
            self.db_connection.db_user_login(
                json_message['User'], json_message['Password'])

        elif json_message['Type'] == "Media":
            if json_message['Sub'] == 'Detail':
                mm_media_ffprobe_json, mm_metadata_json, mm_metadata_localimage_json \
                    = self.db_connection.db_read_media_metadata_movie_both(json_message['UUID'])
                msg = json.dumps({'Type': 'Media', 'Sub': 'Detail',
                                  'Data': mm_metadata_json, 'Data2': mm_media_ffprobe_json,
                                  'Data3': mm_metadata_localimage_json})
            elif json_message['Sub'] == 'List':
                # (Offset, Limit)
                if json_message['Data'] == 'Movie':
                    if 'Offset' in json_message:
                        msg = json.dumps({'Type': 'Media', 'Sub': 'List', 'Data':
                            self.db_connection.db_web_media_list(
                                self.db_connection.db_media_uuid_by_class(
                                    json_message['Data']),
                                json_message['Type'], offset=json_message['Offset'],
                                list_limit=json_message['Limit'])})
                    else:
                        msg = json.dumps({'Type': 'Media', 'Sub': 'List',
                                          'Data': self.db_connection.db_web_media_list(
                                              self.db_connection.db_media_uuid_by_class(
                                                  json_message['Data']),
                                              json_message['Type'])})
            elif json_message['Sub'] == 'In Progress':
                # (Offset, Limit)
                pass
            elif json_message['Sub'] == 'New':
                msg = json.dumps({'Type': 'Media', 'Sub': 'New',
                                  'Data': self.db_connection.db_read_media_new(
                                      json_message['Offset'],
                                      json_message['Limit'])})
            elif json_message['Sub'] == 'Update':
                # (playback, love, hate, etc)
                pass

        elif json_message['Type'] == "Play":
            # TODO send this to pika so only have to code once and will be in the current running
            if json_message['Sub'] == 'Cast':
                for client in common_global.client_devices:
                    if json_message['Target'] == client[1]:
                        # to address the 30 char name limit for container
                        name_container = ((json_message['User'] + '_'
                                           + str(uuid.uuid4()).replace('-', ''))[-30:])
                        cast_docker_inst = common_docker.CommonDocker()
                        cast_docker_inst.com_docker_run_slave(hwaccel=False,
                                                              name_container=name_container,
                                                              container_command=("python "
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
                    if json_message['Sub'] == 'Client':
                        self.send_single_ip(
                            json.dumps({'Type': 'Play', 'Data': media_path}),
                            json_message['Target'])
                #     # launch and attach to local running ffserver
                #     # TODO set server port for ffmpeg
                #     http_link = 'http://localhost:' + self.server_port_ffmpeg + '/stream.ffm'
                #     self.proc_ffmpeg_stream = subprocess.Popen(['ffmpeg', '-i',
                #                                                 media_path, http_link], shell=False)
                #     http_link = 'http://' + common_network.mk_network_get_default_ip() + ':' \
                #                 + self.server_port_ffmpeg + '/stream.ffm'
                # msg = json.dumps({"Type": 'Play', 'Data': http_link})

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
        for user_device_uuid, protocol in self.users.iteritems():
            common_global.es_inst.com_elastic_index('info',
                                                    {"user_ip_addy": self.users[
                                                        user_device_uuid].user_ip_addy,
                                                     'ip': ip_addr})
            if self.users[user_device_uuid].user_ip_addy == ip_addr:
                common_global.es_inst.com_elastic_index('info', {'send ip': ip_addr,
                                                                 'message': message})
                protocol.sendString(message.encode("utf8"))
                break

    def send_single_user(self, message):
        """
        Send message to single user
        """
        for user_device_uuid, protocol in self.users.iteritems():  # pylint: disable=W0612
            if protocol == self:
                common_global.es_inst.com_elastic_index('info', {'send single': message})
                protocol.sendString(message.encode("utf8"))
                break

    def send_all_users(self, message):
        """
        Send message to all users
        """
        for user_device_uuid, protocol in self.users.iteritems():
            if self.users[user_device_uuid].user_verified == 1:
                common_global.es_inst.com_elastic_index('info', {'send all': message})
                protocol.sendString(message.encode("utf8"))

    def send_all_links(self, message):
        """
        Send to all linked servers
        """
        for user_device_uuid, protocol in self.users.iteritems():
            if self.users[user_device_uuid].user_link:
                common_global.es_inst.com_elastic_index('info', {'send all links': message})
                protocol.sendString(message.encode("utf8"))
