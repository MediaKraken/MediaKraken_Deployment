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
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet import reactor


class NetworkEvents(Int32StringReceiver):
    # init is called on every connection
    def __init__(self):
        self.MAX_LENGTH = 32000000 # pylint: disable=C0103
        # server info
        self.user_host_name = None


    def connectionMade(self):
        self.user_ip_addy = str(self.transport.getPeer()).split('\'')[1]
        print('Got Connection')


    def connectionLost(self, reason):
        print('Lost Connection')


    def stringReceived(self, data):
        msg = "test"
        print('GOT Data: %s', len(data))
        self.send_single_user(msg.encode("utf8"))


    # def send_all_users(self, message):
    #     for user_host_name, protocol in self.users.iteritems():
    #         if self.users[user_host_name].user_verified == 1:
    #             logging.info('send all: %s', message)
    #             protocol.sendString(message.encode("utf8"))
