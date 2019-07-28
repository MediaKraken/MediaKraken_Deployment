'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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

import datetime

from common import common_global


def db_media_sports_random(self):
    """
    Find random sports
    """
    self.db_cursor.execute('select mm_metadata_sports_guid,mm_media_guid from mm_media,'
                           'mm_metadata_sports'
                           ' where mm_media_metadata_guid = mm_metadata_sports_guid'
                           ' and random() < 0.01 limit 1')
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_media_sports_count_by_genre(self, class_guid):
    """
    # movie count by genre
    """
    self.db_cursor.execute('select jsonb_array_elements_text(mm_metadata_json->\'Meta\''
                           '->\'themoviedb\'->\'Meta\'->\'genres\')::jsonb as gen,'
                           ' count(mm_metadata_json->\'Meta\''
                           '->\'themoviedb\'->\'Meta\'->\'genres\')'
                           ' from ((select distinct on (mm_media_metadata_guid)'
                           ' mm_metadata_json from mm_media, mm_metadata_sports'
                           ' where mm_media_class_guid = %s'
                           ' and mm_media_metadata_guid = mm_metadata_sports_guid)'
                           ' union (select distinct'
                           ' on (mmr_media_metadata_guid) mm_metadata_json from mm_media_remote,'
                           ' mm_metadata_sports where mmr_media_class_guid = %s'
                           ' and mmr_media_metadata_guid = mm_metadata_sports_guid))'
                           ' as temp group by gen',
                           (class_guid, class_guid))
    return self.db_cursor.fetchall()


def db_media_sports_list_count(self, class_guid, list_type=None, list_genre='All',
                               group_collection=False, include_remote=False, search_text=None):
    """
    # web media count
    """
    common_global.es_inst.com_elastic_index('info', {"classuid counter":
                                                         class_guid, 'type': list_type,
                                                     'genre': list_genre})
    # messageWords[0]=="movie" or messageWords[0]=='in_progress' or messageWords[0]=='video':
    if list_genre == 'All':
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    self.db_cursor.execute('select count(*) from (select distinct'
                                           ' mm_metadata_sports_guid from mm_media,'
                                           ' mm_metadata_sports'
                                           ' where mm_media_class_guid = %s'
                                           ' and mm_media_metadata_guid'
                                           ' = mm_metadata_sports_guid'
                                           ' and mm_media_json->>\'DateAdded\' >= %s)'
                                           ' as temp', (class_guid, (datetime.datetime.now()
                                                                     - datetime.timedelta(
                                days=7)).strftime("%Y-%m-%d"),))
                else:
                    self.db_cursor.execute('select count(*) from ((select distinct'
                                           ' mm_metadata_sports_guid from mm_media,'
                                           ' mm_metadata_sports'
                                           ' where mm_media_class_guid = %s'
                                           ' and mm_media_metadata_guid'
                                           ' = mm_metadata_sports_guid'
                                           ' and mm_media_json->>\'DateAdded\' >= %s)'
                                           ' union (select distinct mmr_metadata_guid'
                                           ' from mm_media_remote,'
                                           ' mm_metadata_sports where mmr_media_class_guid = %s'
                                           ' and mmr_media_metadata_guid = mm_metadata_sports_guid'
                                           ' and mm_media_json->>\'DateAdded\' >= %s)) as temp',
                                           (class_guid, (datetime.datetime.now()
                                                         - datetime.timedelta(days=7)).strftime(
                                               "%Y-%m-%d"),
                                            class_guid, (datetime.datetime.now()
                                                         - datetime.timedelta(days=7)).strftime(
                                               "%Y-%m-%d")))
            else:
                self.db_cursor.execute('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    self.db_cursor.execute('select count(*) from (select distinct'
                                           ' mm_metadata_sports_guid from mm_media,'
                                           ' mm_metadata_sports'
                                           ' where mm_media_class_guid = %s'
                                           ' and mm_media_metadata_guid'
                                           ' = mm_metadata_sports_guid) as temp', (class_guid,))
                else:
                    self.db_cursor.execute('select count(*) from ((select distinct'
                                           ' mm_metadata_sports_guid from mm_media, mm_metadata_sports'
                                           ' where mm_media_class_guid = %s and mm_media_metadata_guid'
                                           ' = mm_metadata_sports_guid)'
                                           ' union (select distinct mm_metadata_sports_guid'
                                           ' from mm_media_remote, mm_metadata_sports'
                                           ' where mmr_media_class_guid = %s'
                                           ' and mmr_media_metadata_guid = mm_metadata_sports_guid)) as temp',
                                           (class_guid, class_guid))
            else:
                if not include_remote:
                    self.db_cursor.execute('select count(*) as row_count'
                                           ' from ((select distinct mm_metadata_sports_guid from mm_media,'
                                           ' mm_metadata_sports where mm_media_class_guid = %s'
                                           ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                           ' and (mm_metadata_json->>\'belongs_to_collection\') is null)'
                                           ' union (select count(*) from xxxx as row_count)) as temp',
                                           (class_guid, class_guid))
                else:
                    self.db_cursor.execute('select 1')
    else:
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    self.db_cursor.execute('select count(*) from (select distinct'
                                           ' mm_metadata_sports_guid from mm_media, mm_metadata_sports'
                                           ' where mm_media_class_guid = %s and mm_media_metadata_guid'
                                           ' = mm_metadata_sports_guid and mm_media_json->>\'DateAdded\' >= %s'
                                           ' and mm_metadata_json->\'Meta\''
                                           '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s) as temp',
                                           (class_guid, (datetime.datetime.now()
                                                         - datetime.timedelta(days=7)).strftime(
                                               "%Y-%m-%d"), list_genre))
                else:
                    self.db_cursor.execute('select count(*) from ((select distinct'
                                           ' mm_metadata_sports_guid from mm_media, mm_metadata_sports'
                                           ' where mm_media_class_guid = %s and mm_media_metadata_guid'
                                           ' = mm_metadata_sports_guid and mm_media_json->>\'DateAdded\' >= %s'
                                           ' and mm_metadata_json->\'Meta\''
                                           '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s)'
                                           ' union (select distinct mmr_metadata_guid from mm_media_remote,'
                                           ' mm_metadata_sports where mmr_media_class_guid = %s'
                                           ' and mmr_media_metadata_guid = mm_metadata_sports_guid'
                                           ' and mmr_media_json->>\'DateAdded\' >= %s'
                                           ' and mm_metadata_json->\'genres\'->0->\'name\' ? %s)) as temp',
                                           (class_guid, (datetime.datetime.now()
                                                         - datetime.timedelta(days=7)).strftime(
                                               "%Y-%m-%d"), list_genre,
                                            class_guid, (datetime.datetime.now()
                                                         - datetime.timedelta(days=7)).strftime(
                                               "%Y-%m-%d"), list_genre))
            else:
                self.db_cursor.execute('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    self.db_cursor.execute('select count(*) from (select distinct'
                                           ' mm_metadata_sports_guid from mm_media, mm_metadata_sports'
                                           ' where mm_media_class_guid = %s and mm_media_metadata_guid'
                                           ' = mm_metadata_sports_guid and mm_metadata_json->\'Meta\''
                                           '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s)'
                                           ' as temp', (class_guid, list_genre))
                else:
                    self.db_cursor.execute('select count(*) from ((select distinct'
                                           ' mm_metadata_sports_guid from mm_media, mm_metadata_sports'
                                           ' where mm_media_class_guid = %s and mm_media_metadata_guid'
                                           ' = mm_metadata_sports_guid and mm_metadata_json->\'Meta\''
                                           '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s)'
                                           ' union (select distinct mmr_media_metadata_guid'
                                           ' from mm_media_remote,'
                                           ' mm_metadata_sports where mmr_media_class_guid = %s'
                                           ' and mmr_media_metadata_guid = mm_metadata_sports_guid'
                                           ' and mm_metadata_json->\'genres\'->0->\'name\' ? %s)) as temp',
                                           (class_guid, list_genre, class_guid, list_genre))
            else:
                self.db_cursor.execute('select 1')
    return self.db_cursor.fetchone()[0]


def db_media_sports_list(self, class_guid, list_type=None, list_genre='All',
                         list_limit=0, group_collection=False, offset=None, include_remote=False,
                         search_text=None):
    """
    # web media return
    """
    common_global.es_inst.com_elastic_index('info', {"classuid": class_guid, 'type': list_type,
                                                     'genre':
                                                         list_genre})
    common_global.es_inst.com_elastic_index('info', {"group and remote": group_collection,
                                                     'remote': include_remote})
    common_global.es_inst.com_elastic_index('info', {"list, offset": list_limit, 'offset': offset})
    # messageWords[0]=="movie" or messageWords[0]=='in_progress' or messageWords[0]=='video':
    if list_genre == 'All':
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json,'
                                               ' mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_media_json->>\'DateAdded\' >= %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name) as temp'
                                               ' order by LOWER(mm_metadata_sports_name)',
                                               (class_guid, (datetime.datetime.now()
                                                             - datetime.timedelta(days=7)).strftime(
                                                   "%Y-%m-%d")))
                    else:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_media_json->>\'DateAdded\' >= %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name) as temp'
                                               ' order by LOWER(mm_metadata_sports_name) offset %s limit %s',
                                               (class_guid, (datetime.datetime.now()
                                                             - datetime.timedelta(days=7)).strftime(
                                                   "%Y-%m-%d"),
                                                offset, list_limit))
                else:
                    if offset is None:
                        self.db_cursor.execute('select * from ((select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_media_json->>\'DateAdded\' >= %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name)'
                                               ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                               ' mmr_media_guid, mmr_media_json,'
                                               ' mm_metadata_sports_image_json, NULL as '
                                               'mmr_media_path'
                                               ' from mm_media_remote, mm_metadata_sports'
                                               ' where mmr_media_class_guid = %s and mmr_media_metadata_guid'
                                               ' = mm_metadata_sports_guid and mmr_media_json->>\'DateAdded\' >= %s'
                                               ' order by mmr_media_metadata_guid, mm_metadata_sports_name) as temp'
                                               ' order by LOWER(mm_metadata_sports_name)',
                                               (class_guid, (datetime.datetime.now()
                                                             - datetime.timedelta(days=7)).strftime(
                                                   "%Y-%m-%d"),
                                                class_guid, (datetime.datetime.now()
                                                             - datetime.timedelta(days=7)).strftime(
                                                   "%Y-%m-%d")))
                    else:
                        self.db_cursor.execute('select * from ((select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_media_json->>\'DateAdded\' >= %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name)'
                                               ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                               ' mmr_media_guid, mmr_media_json, '
                                               'mm_metadata_sports_image_json, NULL as '
                                               'mmr_media_path'
                                               '  from mm_media_remote, mm_metadata_sports'
                                               ' where mmr_media_class_guid = %s and mmr_media_metadata_guid'
                                               ' = mm_metadata_sports_guid and mmr_media_json->>\'DateAdded\' >= %s'
                                               ' order by mmr_media_metadata_guid, mm_metadata_sports_name) as temp'
                                               ' order by LOWER(mm_metadata_sports_name) offset %s limit %s',
                                               (class_guid, (datetime.datetime.now()
                                                             - datetime.timedelta(days=7)).strftime(
                                                   "%Y-%m-%d"),
                                                class_guid, (datetime.datetime.now()
                                                             - datetime.timedelta(days=7)).strftime(
                                                   "%Y-%m-%d"),
                                                offset, list_limit))
            else:
                if offset is None:
                    self.db_cursor.execute('select 1')
                else:
                    self.db_cursor.execute('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name) as temp'
                                               ' order by LOWER(mm_metadata_sports_name)',
                                               (class_guid,))
                    else:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name) as temp'
                                               ' order by LOWER(mm_metadata_sports_name) offset %s limit %s',
                                               (class_guid, offset, list_limit))
                else:
                    if offset is None:
                        self.db_cursor.execute('select * from ((select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name)'
                                               ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                               ' mmr_media_guid, mmr_media_json, '
                                               'mm_metadata_sports_image_json, NULL as '
                                               'mmr_media_path'
                                               '  from mm_media_remote, mm_metadata_sports'
                                               ' where mmr_media_class_guid = %s and mmr_media_metadata_guid'
                                               ' = mm_metadata_sports_guid'
                                               ' order by mmr_media_metadata_guid, mm_metadata_sports_name)) as temp'
                                               ' order by LOWER(mm_metadata_sports_name)',
                                               (class_guid, class_guid))
                    else:
                        self.db_cursor.execute('select * from ((select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name)'
                                               ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                               ' mmr_media_guid, mmr_media_json, '
                                               'mm_metadata_sports_image_json, NULL as '
                                               'mmr_media_path'
                                               '  from mm_media_remote, mm_metadata_sports'
                                               ' where mmr_media_class_guid = %s and mmr_media_metadata_guid'
                                               ' = mm_metadata_sports_guid'
                                               ' order by mmr_media_metadata_guid, mm_metadata_sports_name)) as temp'
                                               ' order by LOWER(mm_metadata_sports_name) offset %s limit %s',
                                               (class_guid, class_guid, offset, list_limit))
            else:
                if not include_remote:
                    if offset is None:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name as name,'
                                               ' mm_media_guid as guid, mm_metadata_sports_user_json as mediajson,'
                                               ' mm_metadata_sports_image_json as metajson,'
                                               ' mm_media_path as mediapath from mm_media,'
                                               ' mm_metadata_sports where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and (mm_metadata_json->>\'belongs_to_collection\') is null'
                                               ' union select mm_metadata_collection_name as name,'
                                               ' mm_metadata_collection_guid as guid, null::jsonb as metajson,'
                                               ' mm_media_path as mediapath'
                                               ' from mm_metadata_collection'
                                               ' order by mm_media_metadata_guid, name) as temp'
                                               ' order by LOWER(name)',
                                               (class_guid,))
                    else:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name as name,'
                                               ' mm_media_guid as guid, mm_metadata_sports_user_json as mediajson,'
                                               ' mm_metadata_sports_image_json as metajson,'
                                               ' mm_media_path as mediapath from mm_media,'
                                               ' mm_metadata_sports where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and (mm_metadata_json->>\'belongs_to_collection\') is null'
                                               ' union select mm_metadata_collection_name as name,'
                                               ' mm_metadata_collection_guid as guid, null::jsonb as metajson,'
                                               ' mm_media_path as mediapath'
                                               ' from mm_metadata_collection'
                                               ' order by mm_media_metadata_guid, name) as temp'
                                               ' order by LOWER(name) offset %s limit %s',
                                               (class_guid, offset, list_limit))
                else:
                    if offset is None:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name as name,'
                                               ' mm_media_guid as guid, mm_metadata_sports_user_json as mediajson,'
                                               ' mm_metadata_sports_image_json as metaimagejson,'
                                               ' mm_media_path as mediapath'
                                               ' from mm_media, mm_metadata_sports where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and (mm_metadata_json->>\'belongs_to_collection\') is null'
                                               # TODO put back in
                                               #                        ' union select mm_metadata_collection_name as name,'
                                               #                        ' mm_metadata_collection_guid as guid,'
                                               #                        ' null::jsonb as mediajson, null::jsonb as metajson,'
                                               #                        ' null::jsonb as metaimagejson, mm_media_path as mediapath'
                                               #                        ' from mm_metadata_collection'
                                               ' order by mm_media_metadata_guid, name) as temp'
                                               ' order by LOWER(name)',
                                               (class_guid,))
                    else:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name as name,'
                                               ' mm_media_guid as guid, mm_metadata_sports_user_json as mediajson,'
                                               ' mm_metadata_sports_image_json as metaimagejson,'
                                               ' mm_media_path as mediapath'
                                               ' from mm_media, mm_metadata_sports where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and (mm_metadata_json->>\'belongs_to_collection\') is null'
                                               # TODO put back in
                                               #                        ' union select mm_metadata_collection_name as name,'
                                               #                        ' mm_metadata_collection_guid as guid,'
                                               #                        ' null::jsonb as mediajson, null::jsonb as metajson,'
                                               #                        ' null::jsonb as metaimagejson, mm_media_path as mediapath'
                                               #                        ' from mm_metadata_collection'
                                               ' order by mm_media_metadata_guid, name) as temp'
                                               ' order by LOWER(name) offset %s limit %s',
                                               (class_guid, offset, list_limit))
    else:
        if list_type == "recent_addition":
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_media_json->>\'DateAdded\' >= %s'
                                               ' and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name) as temp'
                                               ' order by LOWER(mm_metadata_sports_name)',
                                               (class_guid, (datetime.datetime.now()
                                                             - datetime.timedelta(days=7)).strftime(
                                                   "%Y-%m-%d"),
                                                list_genre))
                    else:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_media_json->>\'DateAdded\' >= %s'
                                               ' and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name) as temp'
                                               ' order by LOWER(mm_metadata_sports_name) offset %s limit %s',
                                               (class_guid, (datetime.datetime.now()
                                                             - datetime.timedelta(days=7)).strftime(
                                                   "%Y-%m-%d"),
                                                list_genre, offset, list_limit))
                else:
                    if offset is None:
                        self.db_cursor.execute('select * from ((select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_media_json->>\'DateAdded\' >= %s'
                                               ' and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name)'
                                               ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                               ' mmr_media_guid, mmr_media_json, '
                                               'mm_metadata_sports_image_json, NULL as '
                                               'mmr_media_path'
                                               '  from mm_media_remote, mm_metadata_sports'
                                               ' where mmr_media_class_guid = %s'
                                               ' and mmr_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mmr_media_json->>\'DateAdded\' >= %s'
                                               ' and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mmr_media_metadata_guid, mm_metadata_sports_name)) as temp'
                                               ' order by LOWER(mm_metadata_sports_name)',
                                               (class_guid, (datetime.datetime.now()
                                                             - datetime.timedelta(days=7)).strftime(
                                                   "%Y-%m-%d"),
                                                list_genre))
                    else:
                        self.db_cursor.execute('select * from ((select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_media_json->>\'DateAdded\' >= %s'
                                               ' and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name)'
                                               ' union (select distinct on (mmr_media_metadata_guid) mm_metadata_sports_name,'
                                               ' mmr_media_guid, mmr_media_json, '
                                               'mm_metadata_sports_image_json, NULL as '
                                               'mmr_media_path'
                                               '  from mm_media_remote, mm_metadata_sports'
                                               ' where mmr_media_class_guid = %s'
                                               ' and mmr_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mmr_media_json->>\'DateAdded\' >= %s'
                                               ' and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mmr_media_metadata_guid, mm_metadata_sports_name)) as temp'
                                               ' order by LOWER(mm_metadata_sports_name) offset %s limit %s',
                                               (class_guid, (datetime.datetime.now()
                                                             - datetime.timedelta(days=7)).strftime(
                                                   "%Y-%m-%d"),
                                                list_genre, offset, list_limit))

            else:
                self.db_cursor.execute('select 1')
        else:
            if not group_collection:
                if not include_remote:
                    if offset is None:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name) as temp'
                                               ' order by LOWER(mm_metadata_sports_name)',
                                               (class_guid, list_genre))
                    else:
                        self.db_cursor.execute('select * from (select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name) as temp'
                                               ' order by LOWER(mm_metadata_sports_name) offset %s limit %s',
                                               (class_guid, list_genre, offset, list_limit))

                else:
                    if offset is None:
                        self.db_cursor.execute('select * from ((select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name)'
                                               ' union (select distinct on (mmr_media_metadata_guid)'
                                               ' mm_metadata_sports_name, mmr_media_guid, mmr_media_json,'
                                               ' mm_metadata_sports_image_json, NULL as '
                                               'mmr_media_path'
                                               '  from mm_media_remote, mm_metadata_sports'
                                               ' where mmr_media_class_guid = %s and mmr_media_metadata_guid'
                                               ' = mm_metadata_sports_guid and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mmr_media_metadata_guid, mm_metadata_sports_name)) as temp'
                                               ' order by LOWER(mm_metadata_sports_name)',
                                               (class_guid, list_genre, class_guid, list_genre))
                    else:
                        self.db_cursor.execute('select * from ((select distinct'
                                               ' on (mm_media_metadata_guid) mm_metadata_sports_name, mm_media_guid,'
                                               ' mm_metadata_sports_user_json, mm_metadata_sports_image_json,'
                                               ' mm_media_path'
                                               ' from mm_media, mm_metadata_sports'
                                               ' where mm_media_class_guid = %s'
                                               ' and mm_media_metadata_guid = mm_metadata_sports_guid'
                                               ' and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mm_media_metadata_guid, mm_metadata_sports_name)'
                                               ' union (select distinct on (mmr_media_metadata_guid)'
                                               ' mm_metadata_sports_name, mmr_media_guid, mmr_media_json,'
                                               ' mm_metadata_sports_image_json, NULL as '
                                               'mmr_media_path'
                                               '  from mm_media_remote, mm_metadata_sports'
                                               ' where mmr_media_class_guid = %s and mmr_media_metadata_guid'
                                               ' = mm_metadata_sports_guid and mm_metadata_json->\'Meta\''
                                               '->\'themoviedb\'->\'Meta\'->\'genres\'->0->\'name\' ? %s'
                                               ' order by mmr_media_metadata_guid, mm_metadata_sports_name)) as temp'
                                               ' order by LOWER(mm_metadata_sports_name) offset %s limit %s',
                                               (class_guid, list_genre, class_guid, list_genre,
                                                offset, list_limit))
            else:
                if offset is None:
                    self.db_cursor.execute('select 1')
                else:
                    self.db_cursor.execute('select 1')
    return self.db_cursor.fetchall()


def db_read_media_metadata_sports_both(self, media_guid):
    """
    # read in metadata and ffprobe by id
    """
    self.db_cursor.execute('select mm_media_ffprobe_json,mm_metadata_json,'
                           'mm_metadata_sports_image_json from mm_media, mm_metadata_sports'
                           ' where mm_media_metadata_guid = mm_metadata_sports_guid'
                           ' and mm_media_guid = %s', (media_guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_read_media_sports_list_by_uuid(self, media_guid):
    self.db_cursor.execute('select mm_media_ffprobe_json from mm_media'
                           ' where mm_media_metadata_guid in (select mm_metadata_sports_guid from '
                           'mm_media where mm_media_guild = %s)', (media_guid,))
    video_data = []
    for file_data in self.db_cursor.fetchall():
        # go through streams
        audio_streams = []
        subtitle_streams = ['None']
        if 'streams' in file_data['FFprobe'] and file_data['FFprobe']['streams'] is not None:
            for stream_info in file_data['FFprobe']['streams']:
                common_global.es_inst.com_elastic_index('info', {"info": stream_info})
                stream_language = ''
                stream_title = ''
                stream_codec = ''
                try:
                    stream_language = stream_info['tags']['language'] + ' - '
                except:
                    pass
                try:
                    stream_title = stream_info['tags']['title'] + ' - '
                except:
                    pass
                try:
                    stream_codec \
                        = stream_info['codec_long_name'].rsplit('(', 1)[1].replace(')', '') \
                          + ' - '
                except:
                    pass
                if stream_info['codec_type'] == 'audio':
                    common_global.es_inst.com_elastic_index('info', {'stuff': 'audio'})
                    audio_streams.append((stream_codec + stream_language
                                          + stream_title)[:-3])
                elif stream_info['codec_type'] == 'subtitle':
                    subtitle_streams.append(stream_language)
                    common_global.es_inst.com_elastic_index('info', {'stuff': 'subtitle'})
    return video_data
