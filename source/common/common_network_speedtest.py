"""
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
"""

import subprocess


def com_net_speedtest():
    p = subprocess.Popen(['speedtest-cli'], stdout=subprocess.PIPE, shell=False)
    output, err = p.communicate()
    rc = p.returncode
    speed_download = None
    speed_upload = None
    for speed_list in output.split('\n'):
        if speed_list.find('Download: ') != -1:
            speed_download = speed_list.split(' ', 1)[1]
        if speed_list.find('Upload: ') != -1:
            speed_upload = speed_list.split(' ', 1)[1]
    return speed_download, speed_upload
