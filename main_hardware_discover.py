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
import logging # pylint: disable=W0611
import subprocess
from common import common_hardware_hdhomerun
from common import common_hardware_roku_network
from common import common_file
from common import common_logging
from common import common_string
from common import common_signal


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Hardware_Discovery')


# tuner discovery
media_devices = []
tuner_api = common_hardware_hdhomerun.CommonHardwareHDHomeRun()
tuner_api.com_hdhomerun_discover()
for row_tuner in tuner_api.com_hdhomerun_list():
    media_devices.append({'Model': row_tuner.get_var(item='/sys/model'),\
        'HWModel': row_tuner.get_var(item='/sys/hwmodel'),\
        'Name': row_tuner.get_name(),\
        'ID': str(hex(row_tuner.get_device_id())),\
        'IP': common_string.com_string_ip_int_to_ascii(row_tuner.get_device_ip()),\
        'Firmware': row_tuner.get_version(),\
        'Active': True,\
        'Channels': {}})


# chromecast discover
chrome_pid = subprocess.Popen(['python', './stream2chromecast/stream2chromecast.py'],\
                              shell=False, stdout=subprocess.PIPE)
while True:
    line = chrome_pid.stdout.readline()
    if line != '':
        logging.info('chromescan out: %' % line.rstrip())
        if line.find(":") != -1:
            media_devices.append({'Chrome IP': line.split(':')[0].strip(),\
                                 'Chrome Name': line.split(':')[1].strip()})
    else:
        break
chrome_pid.wait()


# roku discover
common_hardware_roku_network.com_roku_network_discovery()


common_file.com_file_save_data('Device_Scan', media_devices, True, False, None)
