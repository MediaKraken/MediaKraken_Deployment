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


def com_config_read(close_db=False, force_local=False,
                    loop=None, as_pool=False):
    """
    Read in the database connection and open unless specified not too
    """
    # open the database
    import database as database_base
    db_connection = database_base.MKServerDatabase()
    db_connection.db_open(force_local=force_local, loop=None, as_pool=False)
    db_options_json = db_connection.db_opt_status_read()
    if close_db:
        db_connection.db_close()
        return db_options_json['mm_options_json']
    return db_options_json['mm_options_json'], db_connection


async def com_config_read_async(close_db=False, force_local=False,
                                loop=None, as_pool=False):
    """
    Read in the database connection and open unless specified not too
    """
    # open the database
    import database_async as database_base_async
    db_connection = database_base_async.MKServerDatabaseAsync()
    await db_connection.db_open(force_local=force_local, loop=loop, as_pool=as_pool)
    db_options_json = await db_connection.db_opt_status_read()
    if close_db:
        await db_connection.db_close()
        # since read is from coroutine
        return db_options_json['mm_options_json']
    # since read is from coroutine
    return db_options_json['mm_options_json'], db_connection
