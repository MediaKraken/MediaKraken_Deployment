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

from common import common_file
# from common import common_global
from common import common_hardware_chromecast
from common import common_hardware_hdhomerun
from common import common_hardware_roku_network
# from common import common_logging_elasticsearch
from common import common_string

# start logging - REMOVED SINCE RUNS AS HOST NETWORK
#common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('main_hardware_discover')

media_devices = []

# hdhomerun tuner discovery
tuner_api = common_hardware_hdhomerun.CommonHardwareHDHomeRun()
tuner_api.com_hdhomerun_discover()
for row_tuner in tuner_api.com_hdhomerun_list():
    # common_global.es_inst.com_elastic_index('info', {
    #     'hdhomerun out': common_string.com_string_ip_int_to_ascii(row_tuner.get_device_ip())})
    media_devices.append({'HDHomeRun': {'Model': row_tuner.get_var(item='/sys/model'),
                                        'HWModel': row_tuner.get_var(item='/sys/hwmodel'),
                                        'Name': row_tuner.get_name(),
                                        'ID': str(hex(row_tuner.get_device_id())),
                                        'IP': common_string.com_string_ip_int_to_ascii(
                                            row_tuner.get_device_ip()),
                                        'Firmware': row_tuner.get_version(),
                                        'Active': True,
                                        'Channels': {}}})

# chromecast discover
for chromecast_ip, data_value in common_hardware_chromecast.com_hard_chrome_discover():
    # common_global.es_inst.com_elastic_index('info', {'chromecast out': chromecast_ip})
    media_devices.append({'Chromecast': {'Chrome IP': chromecast_ip,
                                         'Chrome Model': data_value[0],
                                         'Chrome Name': data_value[1]}})

# roku discover
for roku in common_hardware_roku_network.com_roku_network_discovery():
    # common_global.es_inst.com_elastic_index('info', {'roku out': roku})
    media_devices.append({'Roku': roku})

common_file.com_file_save_data('/mediakraken/devices/device_scan.txt',
                               media_devices, True, False, None)
