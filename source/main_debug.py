'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

# will most likely need to run following on HOST
# sysctl -w vm.max_map_count=262144
import sys

try:
    from common import common_docker
except ModuleNotFoundError:
    print('Must install docker via "pip3 install docker".  Exiting...')
    sys.exit()
# map count limit, vm.max_map_count
with open('/proc/sys/vm/max_map_count') as f:
    max_map_count = int(f.read())
if max_map_count < 262144:
    print(
        'Map count too small.  Run "sysctl -w vm.max_map_count=262144" as root and rerun.'
        '  Exiting...')
    sys.exit()

docker_inst = common_docker.CommonDocker()

# get current working directory from host maps
# this is used so ./data can be used for all the containers launched from docker-py
# using reactor since it should always be running
current_host_working_directory = docker_inst.com_docker_container_bind(container_name='/mkreactor',
                                                                       bind_match='/data/certs')
if current_host_working_directory is None:
    print('Please start the containers so path can be found.'
          '  Exiting...')
    sys.exit()

docker_inst.com_docker_network_prune()
docker_inst.com_docker_network_create()
docker_inst.com_docker_run_elk(current_host_working_directory)
docker_inst.com_docker_run_pgadmin()
docker_inst.com_docker_run_portainer(current_host_working_directory)
