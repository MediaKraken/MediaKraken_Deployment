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
import socket
import json
import sys
import time


def com_net_mediakraken_find_server(server_seconds=1):
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
        logging.critical('Network_Find_Server: Failed to create socket')
        sys.exit()
    server_hosts_found = {}
    logging.info("end time %s", t_end)
    while time.time() < t_end:
        try:
            search_socket.sendto("who is MediaKrakenServer?", ('<broadcast>', 9101))
            server_reply = search_socket.recvfrom(1024)[0]
            logging.info('Server reply: ' + server_reply)
            try:
                data_block = json.loads(server_reply)
            except:
                break # drop out of while loop as no server found
            if data_block["Address"] in server_hosts_found.keys():
                pass
            else:
                logging.info("addr: %s %s %s", data_block["Address"], data_block["Id"],
                    data_block["Name"])
                server_hosts_found[data_block["Address"]] = (data_block["Id"], data_block["Name"])
        except socket.error, msg:
            logging.critical('Network_Find_Server Error Code : ' + str(msg[0])\
                + ' Message ' + msg[1])
            sys.exit()
    logging.info("hosts found %s", server_hosts_found)
    return server_hosts_found
