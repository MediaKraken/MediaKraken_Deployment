import socket

from common import common_docker
from common import common_global
from common import common_logging_elasticsearch

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_broadcast')

address = ('', 9101)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(address)

docker_inst = common_docker.CommonDocker()
# it returns a dict, not a json
mediakraken_ip = docker_inst.com_docker_info()['Swarm']['NodeAddr']

# begin loop to respond to all broadcast messages
while True:
    recv_data, addr = server_socket.recvfrom(2048)
    if recv_data == "who is MediaKrakenServer?":
        common_global.es_inst.com_elastic_index('info', {'addr': str(addr),
                                                         'data': str(recv_data)})
        # TODO should anounce the correct port
        server_socket.sendto(mediakraken_ip + ":" + '8903', addr)
