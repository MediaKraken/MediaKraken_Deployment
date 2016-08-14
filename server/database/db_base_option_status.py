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
#import logging
import json


def srv_db_option_status_read(self):
    """
    Read options
    """
    self.db_cursor.execute('select mm_options_json, mm_status_json from mm_options_and_status')
    return self.db_cursor.fetchone() # no [0] as two fields


def srv_db_option_status_update(self, option_json, status_json):
    """
    Update option and status json
    """
    # no need for where clause as it's only the one record
    self.db_cursor.execute('update mm_options_and_status set mm_options_json = %s,'\
        ' mm_status_json = %s', (option_json, status_json))


def srv_db_option_status_update_scan_json(self, scan_json):
    """
    Update scan info
    """
    # no need for where clause as it's only the one record
    self.db_cursor.execute('update mm_options_and_status set mm_status_json = %s', (scan_json,))


def srv_db_option_status_update_scan_json_rec(self, dir_path, scan_status, scan_percent):
    """
    Update scan data
    """
    self.db_cursor.execute('select mm_status_json from mm_options_and_status')
    status_json = self.db_cursor.fetchone()['mm_status_json'] # will always have the one record
    status_json.update({'Scan':{dir_path:{'Status':scan_status, 'Pct': scan_percent}}})

# how about have the status on the lib record itself
# then in own thread....no, read to update....just update
# so faster
#    json_data = self.db_cursor.fetchone()[0]
#    json_data.update({'UserStats':{user_id:{'Watched':status_bool}}})
#    json_data = json.dumps(json_data)

    # no need for where clause as it's only the one record
    self.db_cursor.execute('update mm_options_and_status set mm_status_json = %s',\
        (json.dumps(status_json),))
    # 'update objects set mm_options_and_status=jsonb_set(mm_options_and_status,
        #'{name}', '"Mary"', true)'
