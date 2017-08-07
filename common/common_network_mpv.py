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
from functools import partial

class Mpv(object):
    commands = ['']
    def __init__(self, sockfile='/tmp/mpvsock'):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            s.connect(sockfile)
        except OSError as e:
            pass
        self.fd = s

    def execute(self, command):
        data = bytes(json.dumps(command) + '\r\n', encoding='utf-8')
        try:
            self.fd.send(data)
            buf = self.fd.recv(1024)
        except OSError as e:
            pass
        print('DEBUG', buf)
        result = json.loads(buf.decode('utf-8'))
        status = result['error']
        if status == 'success':
            return result

    def command(self, command, *args):
        return self.execute({'command': [command, args]})

    def close(self):
        self.fd.close()

    def __getattr__(self, name):
        mpv_name = name.replace('_', '-')
        return partial(self.command, mpv_name)