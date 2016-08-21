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
import database as database_base


def com_config_read(open_database=True):
    """
    Read in the database connection and open unless specified not too
    """
    import ConfigParser
    config_handle = ConfigParser.ConfigParser()
    config_handle.read("MediaKraken.ini")
    if open_database:
        # open the database
        db_connection = database_base.MKServerDatabase()
        db_connection.db_open(config_handle.get('DB Connections', 'PostDBHost').strip(),\
            config_handle.get('DB Connections', 'PostDBPort').strip(),\
            config_handle.get('DB Connections', 'PostDBName').strip(),\
            config_handle.get('DB Connections', 'PostDBUser').strip(),\
            config_handle.get('DB Connections', 'PostDBPass').strip())
        return config_handle, option_config_json, db_connection.db_opt_status_read()['mm_options_json'], db_connection
    return config_handle
