'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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
import socket
import json
import os
import time
import subprocess
from common import common_network_mpv


mpv_process = subprocess.Popen(['mpv', '--no-config', '--ontop', '--no-osc', '--no-osd-bar',
                             '--aid=2',
                             '--audio-spdif=ac3,dts,dts-hd,truehd,eac3',
                             '--audio-device=pulse', '--hwdec=auto',
                             '--input-ipc-server', './mk_mpv.sock',
                             '/home/spoot/github/MediaKraken/mkarchive/big_buck_bunny.avi'],
                             shell=False)
mpv_connection = common_network_mpv.CommonNetMPVSocat()
time.sleep(5)
mpv_connection.execute('{ "command": ["set_property", "pause", true] }')
time.sleep(5)
mpv_connection.execute('{ "command": quit-watch-later}')
