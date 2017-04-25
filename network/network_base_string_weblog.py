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
import bz2
from twisted.protocols.basic import Int32StringReceiver
from common import common_file


class NetworkEvents(Int32StringReceiver):
    """
    Process the network events for the server
    """
    # init is called on every connection
    def __init__(self, users):
        self.MAX_LENGTH = 32000000 # pylint: disable=C0103
        self.cpu_use_table = {}
        # server info
        self.users = users
        self.user_host_name = None
        self.user_ip_addy = None
        self.user_user_name = None
        self.user_verified = 0


    def connectionMade(self):
        """
        Network connection made from client so ask for ident
        """
        logging.info('Got Connection')
        self.sendString('IDENT')


    def connectionLost(self, reason):
        """
        Network connection dropped so remove client
        """
        logging.info('Lost Connection')
        if self.users.has_key(self.user_user_name):
            del self.users[self.user_user_name]


    def stringReceived(self, data):
        """
        Message received from client
        """
        msg = None
        message_words = data.split(' ')
        logging.info('GOT Data: %s', data)
        logging.info('Message: %s', message_words[0])
        if message_words[0] == "VALIDATE":
            # have to create the self.player data so network knows how to send data back
            self.user_host_name = message_words[1]
            self.user_ip_addy = str(self.transport.getPeer()).split('\'')[1]
            self.user_user_name = message_words[1]
            self.users[message_words[1]] = self
            logging.info("user: %s %s", self.user_host_name, self.user_ip_addy)
        # user commands
        elif message_words[0] == "LOGIN":
            pass
        elif message_words[0] == "KODI_LOG":
            common_file.com_file_save_data(
                './log_debug/Kodi', bz2.decompress(message_words[1]), False, True, '.log')
        elif message_words[0] == "DEBUG_LOG":
            common_file.com_file_save_data(
                './log_debug/Debug', bz2.decompress(message_words[1]), False, True, '.log')
        else:
            logging.error("UNKNOWN TYPE: %s", message_words[0])
            msg = "UNKNOWN_TYPE"
        if msg is not None:
            logging.info("should be sending data")
            self.send_single_user(msg)


    def send_single_user(self, message):
        """
        Send message to single user
        """
        for user_host_name, protocol in self.users.iteritems(): # pylint: disable=W0612
            if protocol == self:
                logging.info('send single: %s', message)
                protocol.sendString(message.encode("utf8"))
                break


    def send_all_users(self, message):
        """
        Send message to all users
        """
        for user_host_name, protocol in self.users.iteritems():
            if self.users[user_host_name].user_verified == 1:
                logging.info('send all: %s', message)
                protocol.sendString(message.encode("utf8"))
