from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import socket
import sys
sys.path.append("../MediaKraken_Common")
from common import common_logging
from common import common_network
import ConfigParser
config_handle = ConfigParser.ConfigParser()
config_handle.read("MediaKraken.ini")


address = ('', 9101)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(address)


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Broadcast')


# begin loop to respond to all broastcast messages
while True:
    recv_data, addr = server_socket.recvfrom(2048)
    logging.debug(str(addr) + ': %s', recv_data)
    if recv_data == "who is MediaKrakenServer?":
        # TODO   mk_network_ip_addr()
        server_socket.sendto("http:localhost:"\
            + config_handle.get('MediaKrakenServer', 'APIPort').strip(), addr)
