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

from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess
import time

from common import common_docker

# setup the docker environment
docker_inst = common_docker.CommonDocker()

# startup the elk
docker_inst.com_docker_network_create('mk_mediakraken_network')
docker_inst.com_docker_run_elk()
time.sleep(30)

# startup the app
subprocess.Popen(['docker-compose', '-f', './docker/alpine/docker-compose.yml', 'up', '-d'],
                 shell=False)
