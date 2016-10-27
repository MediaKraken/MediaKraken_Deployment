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
from docker import Client

# notes on how to use the cli for the apps
# https://docker-py.readthedocs.io/en/latest/api/


class CommonDocker(object):
    """
    Class for interfacing with docker
    """
    def __init__(self, host_name, host_ip):
        self.host_name = host_name
        self.host_ip = host_ip


    def com_docker_connect(self):
        self.cli = Client(base_url='tcp://%s:%s', self.host_name, self.host_ip)
