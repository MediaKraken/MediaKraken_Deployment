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

# check to see if docker is installed
if not os.path.isfile('/usr/bin/docker'):
    # setup docker dependencies
    install_pid = subprocess.Popen(shlex.split('apt install -y apt-transport-https'
                                               ' ca-certificates curl gnupg lsb-release'),
                                   stdout=subprocess.PIPE, shell=False)
    while True:
        line = install_pid.stdout.readline()
        if not line:
            break
        print(line.rstrip(), flush=True)
    install_pid.wait()
    # setup the docker keyring
    install_pid = subprocess.Popen(shlex.split('curl -fsSL https://download.docker.com/linux/'
                                               'debian/gpg'),
                                   stdout=subprocess.PIPE, shell=False)
    output = subprocess.check_output(shlex.split('gpg --dearmor -o /usr/share/keyrings/'
                                                 'docker-archive-keyring.gpg'),
                                     stdin=install_pid.stdout)
    while True:
        line = install_pid.stdout.readline()
        if not line:
            break
        print(line.rstrip(), flush=True)
    install_pid.wait()
    # setup the docker repository
    install_pid = subprocess.Popen(shlex.split('echo "deb [arch=amd64 signed-by=/usr/share/'
                                               'keyrings/docker-archive-keyring.gpg]'
                                               ' https://download.docker.com/linux/debian'
                                               ' buster stable"'),
                                   stdout=subprocess.PIPE, shell=False)
    output = subprocess.check_output(shlex.split('tee /etc/apt/sources.list.d/docker.list '
                                                 '> /dev/null'),
                                     stdin=install_pid.stdout)
    while True:
        line = install_pid.stdout.readline()
        if not line:
            break
        print(line.rstrip(), flush=True)
    install_pid.wait()
    # general update to grab new package list from new repo
    install_pid = subprocess.Popen(shlex.split('apt update -y'),
                                   stdout=subprocess.PIPE, shell=False)
    while True:
        line = install_pid.stdout.readline()
        if not line:
            break
        print(line.rstrip(), flush=True)
    install_pid.wait()
    # finalize docker install
    install_pid = subprocess.Popen(shlex.split('apt install -y'
                                               ' docker-ce docker-ce-cli containerd.io'),
                                   stdout=subprocess.PIPE, shell=False)
    while True:
        line = install_pid.stdout.readline()
        if not line:
            break
        print(line.rstrip(), flush=True)
    install_pid.wait()

# verify docker-compose is installed
if not os.path.isfile('/usr/local/bin/docker-compose'):
    install_pid = subprocess.Popen(shlex.split('curl -L "https://github.com/docker/compose/'
                                               'releases/download/1.29.1/docker-compose-'
                                               'Linux-x86_64" '
                                               '-o /usr/local/bin/docker-compose'),
                                   stdout=subprocess.PIPE, shell=False)
    install_pid.wait()
    install_pid = subprocess.Popen(shlex.split('chmod +x /usr/local/bin/docker-compose'),
                                   stdout=subprocess.PIPE, shell=False)
    install_pid.wait()

if not os.path.isfile('.env'):
    file_handle = open('.env', 'w+')
    file_handle.write('DBPASS=')
    random_key = b64encode(os.urandom(32)).decode('utf-8')
    file_handle.write(random_key.replace('"', '').replace("'", ''))
    file_handle.write('\nSECURE=')
    random_key = b64encode(os.urandom(32)).decode('utf-8')
    file_handle.write(random_key.replace('"', '').replace("'", ''))
    file_handle.write('\nCSRF_SECRET_KEY=')
    random_key = b64encode(os.urandom(32)).decode('utf-8')
    file_handle.write(random_key.replace('"', '').replace("'", ''))
    file_handle.write('\nSWARMIP=None\nDEBUG=False')
    file_handle.write('\nBRANCH=dev2021_07')
    file_handle.close()

subprocess.call(shlex.split('python3 mediakraken_update_images.py'),
                stdout=subprocess.PIPE, shell=False)
