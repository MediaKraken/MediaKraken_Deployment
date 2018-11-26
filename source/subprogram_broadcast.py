import socket

from common import common_docker
# from common import common_global
# from common import common_logging_elasticsearch
from common import common_signal

# can't use elasticsearch......this runs as "host" so mkelk won't be available
# start logging
# common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_broadcast')

# set signal exit breaks
common_signal.com_signal_set_break()

address = ('', 9101)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(address)

docker_inst = common_docker.CommonDocker()
# it returns a dict, not a json
mediakraken_ip = docker_inst.com_docker_info()['Swarm']['NodeAddr']

# common_global.es_inst.com_elastic_index('info', {'mediakraken_ip': mediakraken_ip })
print('mkip: %s', (mediakraken_ip,))

# begin loop to respond to all broadcast messages
while True:
    recv_data, addr = server_socket.recvfrom(2048)
    if recv_data == b"who is MediaKrakenServer?":
        # grab container list - do here since server could have restarted on other port
        for container_json in docker_inst.com_docker_container_list():
            # grab ports for server
            if container_json['Names'][0] == '/mkreactor':
                docker_port = str(
                    docker_inst.com_docker_port(container_json['Id'], 8903)[0]['HostPort'])
                break
        # common_global.es_inst.com_elastic_index('info', {'addr': str(addr),
        #                                                  'data': str(recv_data)})
        print('addr: %s, data: %s', (str(addr), str(recv_data)))
        server_socket.sendto((mediakraken_ip + ":" + docker_port).encode(), addr)
