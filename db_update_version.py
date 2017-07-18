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
import subprocess
import psycopg2
from common import common_config_ini
from common import common_version


# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# not really needed if common_version.DB_VERSION == 4:

if db_connection.db_version_check() == 1:
    # add download image que
    proc = subprocess.Popen(['python', './db_create_update.py'], shell=False)
    proc.wait()
    db_connection.db_version_update(2)
    db_connection.db_commit()

if db_connection.db_version_check() == 2:
    # add image for periodical
    db_connection.db_query('ALTER TABLE mm_metadata_book ADD COLUMN mm_metadata_book_image_json jsonb')
    db_connection.db_version_update(3)
    db_connection.db_commit()

if db_connection.db_version_check() == 3:
    # add docker info to options
    option_config_json.update({'Docker': {'Nodes': 0, 'SwarmID': None, 'Instances': 0}})
    db_connection.db_opt_update(option_config_json)
    db_connection.db_version_update(4)
    db_connection.db_commit()

if db_connection.db_version_check() == 4:
    # add cron job
    db_connection.db_cron_insert('Trailer', 'Download new trailers', False, 'Days 1',
        psycopg2.Timestamp(1970, 1, 1, 0, 0, 1), './subprogram_metadata_trailer_download.py')
    db_connection.db_version_update(5)
    db_connection.db_commit()

# drop trigger table since moving to celery?

# close the database
db_connection.db_close()
