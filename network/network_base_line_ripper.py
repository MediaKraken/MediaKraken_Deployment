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
import logging  # pylint: disable=W0611
import json
import subprocess
from twisted.internet import reactor, protocol
from twisted.protocols import basic
from common import common_discid


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

        if json_message['Type'] == "Rip":
            if json_message['Data'] == "CD":
                disc_id = common_discid.com_discid_spec_device(json_message['Target'])
                mbrainz_data = self.mbrainz_inst.com_mediabrainz_get_releases(disc_id)
                disc_id_found = False
                # TODO if NOT in DB already
                if disc_id_found is True:
                    pass
                else:
                    # call waits until done
                    subprocess.call(['abcde', '-d', json_message['Target']])
            elif json_message['Data'] == "DVD":
                # TODO id disc
                # TODO see if in db already
                subprocess.call(['makemkvcon', 'mkv', 'disc:%s' % json_message['Target'],
                                 'all', json_message['Location']])
            elif json_message['Data'] == "Bray":
                # TODO id disc
                # TODO see if in db already
                subprocess.call(['makemkvcon', 'mkv', 'disc:%s' % json_message['Target'],
                                 'all', json_message['Location']])
            elif json_message['Data'] == "UHD":
                # TODO id disc
                # TODO see if in db already
                subprocess.call(['makemkvcon', 'mkv', 'disc:%s' % json_message['Target'],
                                 'all', json_message['Location']])
            elif json_message['Data'] == "HDVD":
                # TODO id disc
                # TODO see if in db already
                subprocess.call(['makemkvcon', 'mkv', 'disc:%s' % json_message['Target'],
                                 'all', json_message['Location']])
            else:
                pass
        elif json_message['Type'] == "Ident":
            # have to create the self.player data so network knows how to send data back
            self.user_device_uuid = json_message['UUID']
            self.user_ip_addy = str(self.transport.getPeer()).split('\'')[1]
            self.users[self.user_device_uuid] = self
            logging.info("user: %s %s", self.user_device_uuid, self.user_ip_addy)
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
            logging.info('send all: %s', message)
            protocol.transport.write(message.encode("utf8"))
