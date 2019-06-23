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

import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_docker


class TestCommonDocker:

    @classmethod
    def setup_class(self):
        self.docker_handle = common_docker.CommonDocker()  # 'tcp://127.0.0.1', 2375)

    @classmethod
    def teardown_class(self):
        pass

    def test_com_docker_container_list(self):
        """
        List containers on host
        """
        self.docker_handle.com_docker_container_list()

    def test_com_docker_info(self):
        """
        docker info on host
        """
        self.docker_handle.com_docker_info()

    def test_com_docker_swarm_init(self):
        """
        initialize swarm on host
        """
        self.docker_handle.com_docker_swarm_init()

    def test_com_docker_swarm_inspect(self):
        """
        swarm info on host
        """
        self.docker_handle.com_docker_swarm_inspect()

    def test_com_docker_swarm_leave(self):
        """
        leave current swarm
        """
        self.docker_handle.com_docker_swarm_leave()

    def test_com_docker_node_list(self):
        """
        List nodes in swarm
        """
        self.docker_handle.com_docker_node_list()

    def test_com_docker_version(self):
        """
        return docker version on host
        """
        self.docker_handle.com_docker_version()

    @pytest.mark.parametrize(("volume_name"), [
        ('fake')])
    def test_com_docker_volume_info(self, volume_name):
        """
        return info no specified volume
        """
        self.docker_handle.com_docker_volume_info(volume_name)

    @pytest.mark.parametrize(("volume_name"), [
        ('fake')])
    def test_com_docker_volume_remove(self, volume_name):
        """
        remove volume from docker
        """
        self.docker_handle.com_docker_volume_remove(volume_name)

    def test_com_docker_volume_list(self):
        """
        list docker volumes
        """
        self.docker_handle.com_docker_volume_list()

    def test_com_docker_create_network(self):
        """
        create network test
        """
        self.docker_handle.com_docker_network_create('mk_mediakraken_network')

    def test_com_docker_prune_network(self):
        """
        prune network test
        """
        self.docker_handle.com_docker_network_prune()
