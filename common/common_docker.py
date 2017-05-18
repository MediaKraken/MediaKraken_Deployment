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
#from docker import Client
import docker

# notes on how to use the cli for the apps
# https://docker-py.readthedocs.io/en/latest

# c = Client(base_url='unix://var/run/docker.sock')


class CommonDocker(object):
    """
    Class for interfacing with docker
    """
    def __init__(self):
        self.cli = docker.from_env()
        self.cli_api = docker.APIClient(base_url='unix://var/run/docker.sock')

    # def com_docker_connect(self):
    #     """
    #     Connect to specified machine
    #     """
    #     self.cli = Client(base_url=('tcp://%s:%s', (self.host_name, self.host_ip)))


    def com_docker_container_list(self):
        """
        List containers on host
        """
        return self.cli.containers()


    def com_docker_info(self):
        """
        docker info on host
        """
        return self.cli.info()


    def com_docker_swarm_init(self):
        """
        initialize swarm on host
        """
        return self.cli_api.init_swarm()


    def com_docker_swarm_inspect(self):
        """
        swarm info on host
        """
        return self.cli_api.inspect_swarm()


    def com_docker_swarm_leave(self):
        """
        leave current swarm
        """
        return self.cli_api.leave_swarm()


    def com_docker_node_list(self):
        """
        List nodes in swarm
        """
        return self.cli_api.nodes()


    def com_docker_version(self):
        """
        return docker version on host
        """
        return self.cli.version()


    def com_docker_volume_info(self, volume_name):
        """
        return info no specified volume
        """
        return self.cli.inspect_volume(volume_name)


    def com_docker_volume_remove(self, volume_name):
        """
        remove volume from docker
        """
        return self.cli.remove_volume(volume_name)


    def com_docker_volume_list(self):
        """
        list docker volumes
        """
        return self.cli.volumes()


    # name = container name   TODO
    def com_docker_run_container(self, container_command, container_image_name='mediakraken/mkslave',
                                 container_detach=True,
                                 container_network='mediakraken-network', # 'mediakraken-mq'],
                                 container_volumes=['/var/log/mediakraken:/mediakraken/log',
                                                    '/home/mediakraken:/mediakraken/mnt'],
                                 container_remove=True):
        """
        Launch container (usually for slave play)
        """
        return self.cli.containers.run(image=container_image_name, network=container_network,
                                       detach=container_detach,
                                       command=container_command, volumes=container_volumes,
                                       auto_remove=container_remove)
