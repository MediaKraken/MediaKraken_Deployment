import os
import socket

from common import common_docker
from common import common_logging_elasticsearch_httpx
from common import common_signal

# start logging
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text='START')

# set signal exit breaks
common_signal.com_signal_set_break()

address = ('', 9101)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(address)

docker_inst = common_docker.CommonDocker()
try:
    if os.environ['SWARMIP'] != 'None':
        mediakraken_ip = os.environ['SWARMIP']
    else:
        mediakraken_ip = os.environ['HOST_IP']
except KeyError:  # this is to handle running from local host and NOT within docker
    mediakraken_ip = socket.gethostbyname(socket.gethostname())

common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
    'mediakraken_ip': mediakraken_ip})

# TODO?  # grab container list - do here since server could have restarted on other port
# TODO?  how/why would the above happen
# TODO I have this hardcoded........not good
docker_port = None
while docker_port is None:
    for container_json in docker_inst.com_docker_container_list():
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            'container_json': container_json})
        # grab ports for server
        if container_json['Names'][0].find('mkstack_reactor') != -1:
            docker_port = str(
                docker_inst.com_docker_port(container_json['Id'], 8903)[0]['HostPort'])
            break
while True:
    # begin loop to respond to all broadcast messages
    recv_data, addr = server_socket.recvfrom(2048)
    if recv_data == b"who is MediaKrakenServer?":
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={'addr': str(addr),
                                                                           'data': str(recv_data)})
        server_socket.sendto((mediakraken_ip + ":" + docker_port).encode(), addr)
