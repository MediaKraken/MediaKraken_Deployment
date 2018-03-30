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

from __future__ import absolute_import, division, print_function, unicode_literals
import os
import subprocess
from common import common_global
from common import common_hardware_hdhomerun
from common import common_hardware_roku_network
from common import common_file
from common import common_logging_elasticsearch
from common import common_string

if os.environ['DEBUG']:
    # start logging
    common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_hardware_discover')

media_devices = []

# tuner discovery
tuner_api = common_hardware_hdhomerun.CommonHardwareHDHomeRun()
tuner_api.com_hdhomerun_discover()
for row_tuner in tuner_api.com_hdhomerun_list():
    media_devices.append({'Model': row_tuner.get_var(item='/sys/model'),
                          'HWModel': row_tuner.get_var(item='/sys/hwmodel'),
                          'Name': row_tuner.get_name(),
                          'ID': str(hex(row_tuner.get_device_id())),
                          'IP': common_string.com_string_ip_int_to_ascii(row_tuner.get_device_ip()),
                          'Firmware': row_tuner.get_version(),
                          'Active': True,
                          'Channels': {}})

# chromecast discover
chrome_pid = subprocess.Popen(['python', './stream2chromecast/stream2chromecast.py',
                               '-devicelist'], shell=False, stdout=subprocess.PIPE)
while True:
    line = chrome_pid.stdout.readline()
    if line != '':
        if os.environ['DEBUG']:
            common_global.es_inst.com_elastic_index('info', {'chromescan out': line.rstrip()})
        if line.find(":") != -1:
            media_devices.append({'Chrome IP': line.split(':')[0].strip(),
                                  'Chrome Name': line.split(':')[1].strip()})
    else:
        break
chrome_pid.wait()

# roku discover
for roku in common_hardware_roku_network.com_roku_network_discovery():
    media_devices.append({'Roku': roku})

common_file.com_file_save_data('/mediakraken/devices/device_scan.txt',
                               media_devices, True, False, None)
