"""
  Copyright (C) 2019 Quinn D Granfor <spootdev@gmail.com>

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
"""

import os
import shlex
import subprocess

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

with open('./docker-compose.yml') as file_handle:
    for line in file_handle:
        if line.find('image: ') > 0:
            pull_pid = subprocess.Popen(shlex.split('docker pull %s'
                                                    % (line.split('image: ')[1].strip() \
                                                       .replace('${BRANCH}',
                                                                os.environ['BRANCH']))),
                                        stdout=subprocess.PIPE, shell=False)
            pull_pid.wait()
file_handle.close()
