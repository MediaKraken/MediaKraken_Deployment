"""
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
"""

import socket
import sys
import time

from common import common_logging_elasticsearch_httpx

from . import common_global


def com_net_mediakraken_find_server(server_seconds=2):
    """
    # create dictionary containing
    # Address = Id, Name
    """
    # search for servers for n second
    t_end = time.time() + server_seconds
    # create upd socket
    try:
        search_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # allow broadcast otherwise you'll get permission denied 10013 error
        search_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    except socket.error:
        common_global.es_inst.com_elastic_index('critical', {'Network_Find_Server: Failed to '
                                                             'create socket'})
        sys.exit()
    server_hosts_found = []
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text={"end time": t_end})
    while time.time() < t_end:
        try:
            search_socket.sendto(b"who is MediaKrakenServer?", ('<broadcast>', 9101))
            server_reply = search_socket.recvfrom(1024)[0]
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
                'Server reply': server_reply})
            if server_reply not in server_hosts_found:
                server_hosts_found.append(server_reply)
        except socket.error as msg:
            common_global.es_inst.com_elastic_index('critical', {'Network_Find_Server Error '
                                                                 'Code': str(msg[0])
                                                                         + ' Message ' + msg[1]})
            sys.exit()
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
        "hosts found": server_hosts_found})
    return server_hosts_found
