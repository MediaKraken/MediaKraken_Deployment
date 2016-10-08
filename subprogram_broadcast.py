from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import socket
from common import common_logging
from common import common_config_ini


address = ('', 9101)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(address)


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Broadcast')


config_handle, option_config_json, db_connection = common_config_ini.com_config_read()

# begin loop to respond to all broastcast messages
while True:
    recv_data, addr = server_socket.recvfrom(2048)
    logging.info(str(addr) + ': %s', recv_data)
    if recv_data == "who is MediaKrakenServer?":
        # TODO   mk_network_ip_addr()
        server_socket.sendto("http:localhost:"\
            + option_config_json['MediaKrakenServer']['APIPort'], addr)
