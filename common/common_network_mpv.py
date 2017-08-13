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
import socket
import json


class CommonNetMPV(object):

    def __init__(self, sockfile='./mk_mpv.sock'):
        self.socket_stream = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket_stream.connect(sockfile)

    def execute(self, command):
        self.socket_stream.send(bytes(json.dumps(command) + '\r\n', encoding='utf-8'))
        result = json.loads(self.socket_stream.recv(1024).decode('utf-8'))
        if result['error'] == 'success':
            return result

    def close(self):
        self.socket_stream.close()
