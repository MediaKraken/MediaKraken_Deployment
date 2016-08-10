import socket
import logging
import sys
sys.path.append("../MediaKraken_Common")
import MK_Common_Logging
import MK_Common_Network
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")


address = ('', 9101)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(address)


# start logging
MK_Common_Logging.MK_Common_Logging_Start('./log/MediaKraken_Subprogram_Broadcast')


# begin loop to respond to all broastcast messages
while True:
    recv_data, addr = server_socket.recvfrom(2048)
    logging.debug(str(addr) + ': %s', recv_data)
    if recv_data == "who is MediaKrakenServer?":
        # TODO   MK_Network_IP_Addr()
        server_socket.sendto("http:localhost:" + Config.get('MediaKrakenServer', 'APIPort').strip(), addr)
