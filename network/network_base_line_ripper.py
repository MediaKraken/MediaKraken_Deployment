'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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
import subprocess
from twisted.internet import reactor, protocol
from twisted.protocols import basic
from common import common_network


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

    def connectionMade(self):
        """
        Network connection made from client so ask for ident
        """
        logging.info('Got Connection')
        self.sendLine(json.dumps({'Type': 'Ident'}).encode("utf8"))


    def connectionLost(self, reason):
        """
        Network connection dropped so remove client
        """
        logging.info('Lost Connection')
        if self.users.has_key(self.user_user_name):
            del self.users[self.user_user_name]


    def lineReceived(self, data):
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
            msg = json.dumps({'Type': 'Genre List',
                              'Data': self.db_connection.db_meta_genre_list()})

        elif json_message['Type'] == "Ident":
            # have to create the self.player data so network knows how to send data back
            self.user_device_uuid = json_message['UUID']
            self.user_ip_addy = str(self.transport.getPeer()).split('\'')[1]
            self.user_user_name = None
            self.user_platform = json_message['Platform']
            self.users[self.user_device_uuid] = self
            logging.info("user: %s %s", self.user_device_uuid, self.user_ip_addy)
            if self.user_user_name == 'Link':
                pass
            else:
                user_data = []
                for user in self.db_connection.db_user_list_name():
                    if user['active'] == True:
                        user_data.append((user['id'], user['username']))
                msg = json.dumps({'Type': 'User', 'Data': user_data})

        elif json_message['Type'] == "Login":
            self.db_connection.db_user_login(json_message['User'], json_message['Password'])

        elif json_message['Type'] == "Media":
            if json_message['Sub'] == 'Detail':
                mm_media_ffprobe_json, mm_metadata_json, mm_metadata_localimage_json \
                    = self.db_connection.db_read_media_metadata_movie_both(json_message['UUID'])

        else:
            logging.error("UNKNOWN TYPE: %s", json_message['Type'])
            msg = "UNKNOWN_TYPE"
        if msg is not None:
            logging.info("should be sending data len: %s", len(msg))
            self.sendLine(msg.encode("utf8"))

    def send_all_users(self, message):
        """
        Send message to all users
        """
        for user_device_uuid, protocol in self.users.iteritems():
            if self.users[user_device_uuid].user_verified == 1:
                logging.info('send all: %s', message)
                protocol.transport.write(message.encode("utf8"))
