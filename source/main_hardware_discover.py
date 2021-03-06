"""
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
"""

from common import common_file
from common import common_hardware_chromecast
from common import common_hardware_hdhomerun_py
from common import common_hardware_roku_network
from common import common_hardware_soco
from common import common_logging_elasticsearch_httpx
from common import common_signal

# start logging
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text='START',
                                                     index_name='main_hardware_discover')

# set signal exit breaks
common_signal.com_signal_set_break()

media_devices = []

common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text={'before chromecast'})

# chromecast discover
for chromecast_ip, model_name, friendly_name \
        in common_hardware_chromecast.com_hard_chrome_discover():
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text={
                                                             'chromecast out': chromecast_ip})
    media_devices.append({'IP': chromecast_ip,
                          'Model': model_name,
                          'Name': friendly_name})
common_logging_elasticsearch_httpx.com_es_httpx_post(
    message_type='info',
    message_text={'after chromecast'})

# dlna devices
# TODO looks like debugging shows up if run from this program
# for dlna_devices in common_network_dlna.com_net_dlna_discover():
#     if dlna_devices.find('No compatible devices found.') != -1:
#         break
#     media_devices.append({'DLNA': dlna_devices})
# common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'after dlna'})

# hdhomerun tuner discovery
tuner_api = common_hardware_hdhomerun_py.CommonHardwareHDHomeRunPY()
tuner_api.com_hdhomerun_discover()
for row_tuner in tuner_api.com_hdhomerun_list():
    print(row_tuner, flush=True)
# tuner_api = common_hardware_hdhomerun.CommonHardwareHDHomeRun()
# tuner_api.com_hdhomerun_discover()
# for row_tuner in tuner_api.com_hdhomerun_list():
#     common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {
#         'hdhomerun out': common_string.com_string_ip_int_to_ascii(row_tuner.get_device_ip())})
#     media_devices.append({'HDHomeRun': {'Model': row_tuner.get_var(item='/sys/model'),
#                                         'HWModel': row_tuner.get_var(item='/sys/hwmodel'),
#                                         'Name': row_tuner.get_name(),
#                                         'ID': str(hex(row_tuner.get_device_id())),
#                                         'IP': common_string.com_string_ip_int_to_ascii(
#                                             row_tuner.get_device_ip()),
#                                         'Firmware': row_tuner.get_version(),
#                                         'Active': True,
#                                         'Channels': {}}})
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text={'after hdhomerun'})

# phillips hue discover
# TODO this does NOT do discovery
# hue_inst = common_hardware_hue.CommonHardwareHue()
# media_devices.append({'Phue': hue_inst.com_hardware_hue_get_api()})
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text={'after phue'})

# roku discover
for roku in common_hardware_roku_network.com_roku_network_discovery():
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                         message_text={'roku out': roku})
    media_devices.append({'Roku': roku})
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text={'after roku'})

# soco discover
soco_devices = common_hardware_soco.com_hardware_soco_discover()
if soco_devices is not None:
    for soco in soco_devices:
        common_logging_elasticsearch_httpx.com_es_httpx_post(
            message_type='info',
            message_text={'soco out': soco})
        media_devices.append({'Soco': soco})
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text={'after soco'})

# crestron device discover
# TODO need to port the script to py3
# crestron_devices = common_hardware_crestron.com_hardware_crestron_discover()
# if crestron_devices is not None:
#     for crestron in crestron_devices:
#         common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'crestron out': crestron})
#         media_devices.append({'Crestron': crestron})
common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text={'after crestron'})

common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                     message_text={'devices': media_devices})

common_file.com_file_save_data(file_name='/mediakraken/devices/device_scan.txt',
                               data_block=media_devices,
                               as_pickle=True,
                               with_timestamp=False,
                               file_ext=None)
