"""
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
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging  # pylint: disable=W0611
import socket


# from kodipydent import Kodi
# https://github.com/haikuginger/kodipydent


def com_net_kodi_command(host_ip, host_port, kodi_command):
    """
    # send commands to kodi via raw tcp and json
    """
    kodi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    kodi_socket.connect((host_ip, host_port))
    kodi_socket.sendall(kodi_command.split('|', 1)[1])
    kodi_response = ''
    # if subscript 0 is true then a response is expected
    if kodi_command.split('|', 1)[0]:
        while 1:
            kodi_response += kodi_socket.recv(1024)
            logging.info("kodi response: %s", kodi_response)
            brackets_match = (kodi_response.count('{') - kodi_response.count('}'))
            # if proper termination then exit loop
            if brackets_match == 0:
                break
    kodi_socket.close()
    return kodi_response

# com_net_kodi_command('10.1.0.20', 9090, KODI_SHOW_INFO)
