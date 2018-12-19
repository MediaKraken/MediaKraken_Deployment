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

# https://github.com/MediaKraken-Dependancies/Crestron-List-Devices-On-Network
import subprocess


def com_hardware_crestron_discover(ip_addr=None):
    if ip_addr is None:
        return subprocess.check_output(split(
            'python3 /mediakraken/common/Crestron-List-Devices-On-Network/List_Crestron_Devices -alc'))
    else:
        return subprocess.check_output(
            split(
                'python3 /mediakraken/common/Crestron-List-Devices-On-Network/List_Crestron_Devices -ala %s' %
                ip_addr.rsplit('.', 1)[0]))
