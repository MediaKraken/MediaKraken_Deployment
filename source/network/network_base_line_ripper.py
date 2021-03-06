"""
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
"""

import json
import shlex
import subprocess

from common import common_discid
from common import common_global
from common import common_logging_elasticsearch_httpx
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

    def connectionMade(self):
        """
        Network connection made from client so ask for ident
        """
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'stuff': 'Got Connection'})
        self.sendLine(json.dumps({'Type': 'Ident'}).encode("utf8"))

    def connectionLost(self, reason):
        """
        Network connection dropped so remove client
        """
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'stuff': 'Lost Connection'})
        if self.user_user_name in self.users:
            del self.users[self.user_user_name]

    def lineReceived(self, data):
        """
        Message received from client
        """
        msg = None
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={'GOT Data': data})
        json_message = json.loads(data)
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={'Message': json_message})

        if json_message['Type'] == "Rip":
            if json_message['Data'] == "CD":
                disc_id = common_discid.com_discid_spec_device(json_message['Target'])
                mbrainz_data = self.mbrainz_inst.com_mediabrainz_get_releases(disc_id)
                disc_id_found = False
                # TODO if NOT in DB already
                if disc_id_found is True:
                    # put disc in duplicate output spindle
                    pass
                else:
                    subprocess.Popen(shlex.split(['abcde', '-d', json_message['Target']]))
            else:  # as rest will call makemkv
                if json_message['Data'] == "DVD":
                    # TODO id disc
                    # TODO see if in db already
                    pass
                elif json_message['Data'] == "BRAY":
                    # TODO id disc
                    # TODO see if in db already
                    pass
                elif json_message['Data'] == "UHD":
                    # TODO id disc
                    # TODO see if in db already
                    pass
                elif json_message['Data'] == "HDVD":
                    # TODO id disc
                    # TODO see if in db already
                    pass
                # catchall makemkvcon
                subprocess.Popen(
                    shlex.split(['makemkvcon', 'mkv', 'disc:%s' % json_message['Target'],
                                 'all', json_message['Location']]))
        elif json_message['Type'] == "Ident":
            # have to create the self.player data so network knows how to send data back
            self.user_device_uuid = json_message['UUID']
            self.user_ip_addy = str(self.transport.getPeer()).split('\'')[1]
            self.users[self.user_device_uuid] = self
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                "user": self.user_device_uuid,
                'ip': self.user_ip_addy})
        else:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='error', message_text={"UNKNOWN TYPE": json_message['Type']})
            msg = "UNKNOWN_TYPE"
        if msg is not None:
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text=
            {"should be sending data len": len(msg)})
            self.sendLine(msg.encode("utf8"))

    def send_all_users(self, message):
        """
        Send message to all users
        """
        for user_device_uuid, protocol in self.users.items():
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                                 message_text={'send all': message})
            protocol.transport.write(message.encode("utf8"))
