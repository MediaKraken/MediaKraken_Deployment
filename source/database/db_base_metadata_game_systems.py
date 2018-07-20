'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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

import uuid


def db_meta_game_system_by_guid(self, guid):
    """
    # return game system data
    """
    self.db_cursor.execute('select * from mm_metadata_game_systems_info where gs_id = %s',
                           (guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_game_system_list_count(self, search_value=None):
    """
    Return game system count
    """
    if search_value is not None:
        self.db_cursor.execute('select count(*) from mm_metadata_game_systems_info'
                               ' where gs_game_system_json->\'@isdevice\' ? \'yes\''
                               ' and gs_game_system_name %% %s', (search_value,))
    else:
        self.db_cursor.execute('select count(*) from mm_metadata_game_systems_info'
                               ' where gs_game_system_json->\'@isdevice\' ? \'yes\'')
    return self.db_cursor.fetchone()[0]


def db_meta_game_system_list(self, offset=None, records=None, search_value=None):
    """
    # return list of game systems
    """
    if offset is None:
        if search_value is not None:
            self.db_cursor.execute('select gs_id,gs_game_system_name,'
                                   'gs_game_system_json->\'description\','
                                   'gs_game_system_json->\'year\''
                                   ' from mm_metadata_game_systems_info'
                                   ' where gs_game_system_json->\'@isdevice\''
                                   ' ? \'yes\' and gs_game_system_name %% %s '
                                   'order by gs_game_system_json->\'description\'',
                                   (search_value,))
        else:
            self.db_cursor.execute('select gs_id,gs_game_system_json->\'@name\','
                                   'gs_game_system_json->\'description\','
                                   'gs_game_system_json->\'year\''
                                   ' from mm_metadata_game_systems_info'
                                   ' where gs_game_system_json->\'@isdevice\''
                                   ' ? \'yes\' order by gs_game_system_json->\'description\'')
    else:
        if search_value is not None:
            self.db_cursor.execute('select gs_id,gs_game_system_name,'
                                   'gs_game_system_json->\'description\','
                                   'gs_game_system_json->\'year\''
                                   ' from mm_metadata_game_systems_info'
                                   ' where gs_id in (select gs_id'
                                   ' from mm_metadata_game_systems_info'
                                   ' where gs_game_system_json->\'@isdevice\''
                                   ' ? \'yes\' and gs_game_system_name %% %s '
                                   'order by gs_game_system_json->\'description\''
                                   ' offset %s limit %s)'
                                   ' order by gs_game_system_json->\'description\'',
                                   (search_value, offset, records))
        else:
            self.db_cursor.execute('select gs_id,gs_game_system_name,'
                                   'gs_game_system_json->\'description\','
                                   'gs_game_system_json->\'year\''
                                   ' from mm_metadata_game_systems_info'
                                   ' where gs_id in (select gs_id'
                                   ' from mm_metadata_game_systems_info'
                                   ' where gs_game_system_json->\'@isdevice\''
                                   ' ? \'yes\' order by gs_game_system_json->\'description\''
                                   ' offset %s limit %s)'
                                   ' order by gs_game_system_json->\'description\'',
                                   (offset, records))
    return self.db_cursor.fetchall()


def db_meta_games_system_insert(self, platform_name,
                                platform_alias, platform_json=None):
    """
    # insert game system
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_metadata_game_systems_info(gs_id,'
                           ' gs_game_system_name, gs_game_system_alias,'
                           ' gs_game_system_json) values (%s, %s, %s, %s, %s)',
                           (new_guid, platform_name, platform_alias, platform_json))
    self.db_commit()
    return new_guid


def db_meta_games_system_guid_by_short_name(self, short_name):
    self.db_cursor.execute('select gs_id from mm_metadata_game_systems_info'
                           ' where gs_game_system_name = %s', (short_name,))
    try:
        return self.db_cursor.fetchone()['gs_id']
    except:
        return None


def db_meta_games_system_game_count(self, short_name):
    self.db_cursor.execute('select gs_id from mm_metadata_game_systems_info'
                           ' where gs_game_system_name = %s', (short_name,))
    try:
        return self.db_cursor.fetchone()['gs_id']
    except:
        return None


def db_meta_game_system_upsert(self, system_name, system_alias=None, system_json=None):
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('INSERT INTO mm_metadata_game_systems_info'
                           ' (gs_id, gs_game_system_name,'
                           ' gs_game_system_alias, gs_game_system_json)'
                           ' VALUES (%s, %s, %s, %s)'
                           ' ON CONFLICT (gs_game_system_name)'
                           ' DO UPDATE SET gs_game_system_alias = %s, gs_game_system_json = %s',
                           (new_guid, system_name, system_alias, system_json,
                            system_alias, system_json))
    self.db_cursor.commit()
    return new_guid
