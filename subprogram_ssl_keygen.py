'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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
from subprocess import Popen, PIPE
from time import sleep
import shutil
import sys
import os


# generate key
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    PROC = Popen(['openssl', 'req', '-x509', '-nodes', '-newkey', 'rsa:2048',\
        '-keyout', 'privkey.pem', '-out', 'cacert.pem', '-days', '1000', '-config',\
        './key/windows_openssl.cfg'], shell=False)
    PROC.wait() # have to do here so the move has sumthing to move
    shutil.move('privkey.pem', './key/.')
    shutil.move('cacert.pem', './key/.')
else:
    PROC = Popen(['openssl', 'req', '-x509', '-nodes', '-newkey', 'rsa:2048',\
        '-keyout', 'privkey.pem', '-out', 'cacert.pem', '-days', '1000'], shell=False, stdin=PIPE)
    sleep(5)
    # country code
    PROC.stdin.write('US\n')
    PROC.stdin.flush()
    sleep(2)
    # state or prov
    PROC.stdin.write('ND\n')
    PROC.stdin.flush()
    sleep(2)
    # city
    PROC.stdin.write(b'\n')
    PROC.stdin.flush()
    sleep(2)
    # organization
    PROC.stdin.write('MediaKraken\n')
    PROC.stdin.flush()
    sleep(2)
    # org unit name
    PROC.stdin.write('MKServer\n')
    PROC.stdin.flush()
    sleep(2)
    # common name
    PROC.stdin.write('www.mediakraken.org\n')
    PROC.stdin.flush()
    # email addy
    PROC.stdin.write('spootdev@gmail.com\n')
    PROC.stdin.flush()
    PROC.wait() # have to do here so the move has sumthing to move
    os.system('mv %s %s' % ('*.pem', './key/.'))
