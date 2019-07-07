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

import platform
import subprocess
import sys
from shlex import split

import distro

LINUX_VERSIONS = {
    'alpine': (3.6, 'apk add'),
    'debian': (8.4, 'apt_get -y install'),
    'redhat': (7.1, 'yum install'),
    'ubuntu': (17.04, 'apt_get -y install')}

print('1:', platform.platform())
print('2:', platform.system())
print('3:', platform.release())
print('4:', platform.version())
print('5:', distro.linux_distribution(full_distribution_name=False))
print('6:', platform.system())
print('7:', platform.machine())
print('8:', platform.platform())
print('9:', platform.uname())
print('10:', platform.version())
print('11:', platform.mac_ver())


def wget_wait(wget_addr):
    wget_pid = subprocess.Popen(['wget', wget_addr], stdout=subprocess.PIPE, shell=False)
    wget_pid.wait()


# determine platform (windows, posix)
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    print('Windows or Cygwin system found. Use the Windows installer! Exiting....')
    sys.exit(0)
elif platform.system() != 'Linux':
    print('Non-Linux system found. Exiting...')
    sys.exit(0)

# check minimum linux versions
print('Checking linux version...')
print(('I see you\'re running', platform.dist()[0], 'version', platform.dist()[1]))
try:
    if float(distro.linux_distribution(full_distribution_name=False)[1]) < \
            LINUX_VERSIONS[distro.linux_distribution(full_distribution_name=False)[0].lower()][0]:
        print(('minimum required version is',
               LINUX_VERSIONS[platform.dist()[0].lower()][0]))
except KeyError:
    print('Unsupported linux distribution. Exiting...')
    sys.exit(0)

# install wget
# print('Installing wget...')
# install_pid = subprocess.Popen([, 'wget'], stdout=subprocess.PIPE, shell=False)
# install_pid.wait()


# find current version
wget_wait('http://www.mediakraken.org/current_version.txt')
file_handle = open('newfile.txt', 'r')
current_version = file_handle.read()
file_handle.close()

# fetch the application tarball
file_name = 'MediaKraken_' + current_version + '.tar.bz2'
wget_wait('http://www.mediakraken.org/%s' % file_name)

# untar to home directory
tar_pid = subprocess.Popen(split('tar xvjf \"' + file_name + '\" -C ~'), stdout=subprocess.PIPE,
                           shell=False)
tar_pid.wait()
