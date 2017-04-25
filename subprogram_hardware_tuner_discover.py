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
from common import common_config_ini
from common import common_hardware_hdhomerun
from common import common_logging
from common import common_string
from common import common_signal
import json
import locale
locale.setlocale(locale.LC_ALL, '')


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Tuner_Discovery')


# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server Tuner Scan Start', None,
    'System: Server Tuner Scan Start', 'ServerTunerScanStart', None, None, 'System')


tuners_added = 0
# tuner discovery
tuner_api = common_hardware_hdhomerun.CommonHardwareHDHomeRun()
tuner_api.com_hdhomerun_discover()
for row_tuner in tuner_api.com_hdhomerun_list():
    json_data = {'Model': row_tuner.get_var(item='/sys/model'),
        'HWModel': row_tuner.get_var(item='/sys/hwmodel'), 'Name': row_tuner.get_name(),
        'ID': str(hex(row_tuner.get_device_id())),
        'IP': common_string.com_string_ip_int_to_ascii(row_tuner.get_device_ip()),
        'Firmware': row_tuner.get_version(), 'Active': True, 'Channels': {}}
    # check for exienence
    current_data = db_connection.db_tuner_by_serial(str(hex(row_tuner.get_device_id())))
    if current_data is not None:
        db_connection.db_tuner_update(current_data['mm_tuner_id'], json.dumps(json_data))
    else:
        db_connection.db_tuner_insert(json.dumps(json_data))
    tuners_added += 1


if tuners_added > 0:
    db_connection.db_notification_insert(locale.format('%d', tuners_added, True)
        + " tuners added.", True)


# log end
db_connection.db_activity_insert('MediaKraken_Server Tuner Scan Stop', None,
    'System: Server Tuner Scan Stop', 'ServerTunerScanStop', None, None, 'System')

# commit
db_connection.db_commit()


# close the database
db_connection.db_close()
