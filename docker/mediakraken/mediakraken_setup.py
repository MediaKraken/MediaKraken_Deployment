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
from base64 import b64encode

if not os.path.isfile('mkstack_db_password.txt'):
    file_handle = open('mkstack_db_password.txt', 'w+')
    file_handle.write(b64encode(os.urandom(32).decode('utf-8')))
    file_handle.close()
    subprocess.call(shlex.split('docker secret create db_password ./mkstack_db_password.txt'),
                    stdout=subprocess.PIPE, shell=False)

if not os.path.isfile('mkstack_secure_key.txt'):
    file_handle = open('mkstack_secure_key.txt', 'w+')
    file_handle.write(b64encode(os.urandom(32).decode('utf-8')))
    file_handle.close()
    subprocess.call(shlex.split('docker secret create secure_key ./mkstack_secure_key.txt'),
                    stdout=subprocess.PIPE, shell=False)
