'''
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
'''

'''
# TODO redo this for debian probably!!!
'''
import os
import shlex
import subprocess


'''
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
'''

centos_packages = {'python3-devel'}
debian_packages = {'libssl-dev', 'pkg-config'}
# install base packages per OS (centos, debian)
pid_proc = subprocess.Popen(shlex.split('yum install -y', centos_packages),
                            stdout=subprocess.PIPE, shell=False)
pid_proc.wait()

# install pypi packages
pid_proc = subprocess.Popen(shlex.split('pip3 install -r requirements.txt'),
                            stdout=subprocess.PIPE, shell=False)
pid_proc.wait()

# Dockerfile linter
pid_proc = subprocess.Popen(shlex.split('docker pull hadolint/hadolint'),
                            stdout=subprocess.PIPE, shell=False)
pid_proc.wait()

# Image security scanner
pid_proc = subprocess.Popen(shlex.split('docker pull anchore/anchore-engine'),
                            stdout=subprocess.PIPE, shell=False)
pid_proc.wait()

# install graudit
os.chdir('/home')
pid_proc = subprocess.Popen(shlex.split('git clone https://github.com/wireghoul/graudit'))
pid_proc.wait()
os.chdir('/home/graudit')
pid_proc = subprocess.Popen(shlex.split('make install'))
pid_proc.wait()

# install trivy (rhel, centos)
pid_proc = subprocess.Popen(
    shlex.split('rpm -ivh https://github.com/aquasecurity/trivy/releases/download/v0.1.6/trivy_0.1.6_Linux-64bit.rpm'))
pid_proc.wait()

# Download all the images for Clair
os.chdir('../docker/clair')
pid_proc = subprocess.Popen(shlex.split('docker-compose pull'),
                            stdout=subprocess.PIPE, shell=False)
pid_proc.wait()

# Download all the images for Mailcow
os.chdir('../docker/mailcow')
pid_proc = subprocess.Popen(shlex.split('docker-compose pull'),
                            stdout=subprocess.PIPE, shell=False)
pid_proc.wait()

# setup killshot
os.chdir('../tools/killshot')
pid_proc = subprocess.Popen(shlex.split('ruby setup.rb'),
                            stdout=subprocess.PIPE, shell=False)
pid_proc.wait()
