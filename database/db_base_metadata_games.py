'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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


def db_meta_game_system_list_count(self):
    """
    Return game system count
    """
    self.db_cursor.execute('select count(*) from mm_metadata_game_systems_info'
        ' where gs_game_system_json->\'@isdevice\' ? \'yes\'')
    return self.db_cursor.fetchone()[0]


def db_meta_game_system_list(self, offset=None, records=None):
    """
    # return list of game systems
    """
    if offset is None:
        self.db_cursor.execute('select gs_id,gs_game_system_json->\'@name\','
            'gs_game_system_json->\'description\',gs_game_system_json->\'year\''
            ' from mm_metadata_game_systems_info where gs_game_system_json->\'@isdevice\''
            ' ? \'yes\' order by gs_game_system_json->\'description\'')
    else:
        self.db_cursor.execute('select gs_id,gs_game_system_json->\'@name\','
            'gs_game_system_json->\'description\',gs_game_system_json->\'year\''
            ' from mm_metadata_game_systems_info where gs_id in (select gs_id'
            ' from mm_metadata_game_systems_info where gs_game_system_json->\'@isdevice\''
            ' ? \'yes\' order by gs_game_system_json->\'description\' offset %s limit %s)'
            ' order by gs_game_system_json->\'description\'', (offset, records))
    return self.db_cursor.fetchall()


def db_meta_game_list_count(self):
    """
    # return list of games count
    """
    self.db_cursor.execute('select count(*) from mm_metadata_game_software_info')
    return self.db_cursor.fetchone()[0]


# TODO select subselect for speed
def db_meta_game_list(self, offset=None, records=None):
    """
    # return list of games
    """
    if offset is None:
        self.db_cursor.execute('select gi_id,gi_game_info_json->\'description\','
            'gi_game_info_json->\'year\',gs_game_system_json->\'description\''
            ' from mm_metadata_game_software_info,mm_metadata_game_systems_info'
            ' where gi_system_id = gs_id order by gi_game_info_json->\'description\'')
    else:
        self.db_cursor.execute('select gi_id,gi_game_info_json->\'description\','
            'gi_game_info_json->\'year\',gs_game_system_json->\'description\''
            ' from mm_metadata_game_software_info,mm_metadata_game_systems_info'
            ' where gi_system_id = gs_id order by gi_game_info_json->\'description\''
            ' offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def db_meta_game_by_guid(self, guid):
    """
    # return game data
    """
    self.db_cursor.execute('select gi_id, gi_system_id, gi_game_info_json'
        ' from mm_metadata_game_software_info where gi_id = %s', (guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_game_by_system_count(self, guid):
    """
    # game list by system count
    """
    self.db_cursor.execute('select count(*) from mm_metadata_game_software_info,'
        ' mm_metadata_game_systems_info where gi_system_id = gs_id and gs_id = %s', (guid,))
    return self.db_cursor.fetchone()[0]


def db_meta_game_by_system(self, guid, offset=None, records=None):
    """
    # game list by system count
    """
    self.db_cursor.execute('select * from mm_metadata_game_software_info,'
        ' mm_metadata_game_systems_info where gi_system_id = gs_id and gs_id = %s'
        ' offset %s, limit %s', (guid, offset, records))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_game_by_sha1(self, sha1_hash):
    """
    # game by sha1
    """
    self.db_cursor.execute('select gi_id from mm_metadata_game_software_info'
        ' where gi_game_info_json->\'@sha1\' ? %s', (sha1_hash,))
    try:
        return self.db_cursor.fetchone()['gi_id']
    except:
        return None


def db_meta_game_by_name_and_system(self, game_name, game_system_short_name):
    """
    # game by name and system short name
    """
    self.db_cursor.execute('select gi_id from mm_metadata_game_software_info'
        ' where gi_game_info_json->\'@name\' = %s and gi_system_id = %s',
        (game_name, game_system_short_name))
    return self.db_cursor.fetchall()


def db_meta_games_system_insert(self, platform_id, platform_name,
        platform_alias, platform_json=None):
    """
    # insert game system
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_metadata_game_systems_info(gs_id,'
        ' gs_game_system_id, gs_game_system_name, gs_game_system_alias,'
        ' gs_game_system_json) values (%s, %s, %s, %s, %s)',
        (new_guid, platform_id, platform_name, platform_alias, platform_json))
    return new_guid
