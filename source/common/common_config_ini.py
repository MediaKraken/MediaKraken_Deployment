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

import database as database_base


def com_config_read():
    """
    Read in the database connection and open unless specified not too
    """
    # open the database
    db_connection = database_base.MKServerDatabase()
    db_connection.db_open()
    db_options_json = db_connection.db_opt_status_read()['mm_options_json']
    if close_db:
        db_connection.db_close()
        return db_options_json
    return db_options_json, db_connection
