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
from subprocess import Popen
import shutil
import sys
import os


# generate key
PROC = Popen(['openssl', 'req', '-x509', '-nodes', '-newkey', 'rsa:2048',
    '-keyout', 'privkey.pem', '-out', 'cacert.pem', '-days', '1000',
    '-subj', '/C=US/ST=ND/L=./CN=www.mediakraken.org'], shell=False)
PROC.wait() # have to do here so the move has sumthing to move
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    shutil.move('privkey.pem', './key/.')
    shutil.move('cacert.pem', './key/.')
else:
    os.system('mv %s %s' % ('*.pem', './key/.'))
