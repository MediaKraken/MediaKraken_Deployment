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
import logging
import uuid


def srv_db_metatv_guid_by_tvshow_name(self, tvshow_name, tvshow_year=None):
    """
    # metadata guid by name
    """
    metadata_guid = None
    if tvshow_year is None:
        self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'\
            ' where LOWER(mm_metadata_tvshow_name) = %s', (tvshow_name.lower(),))
    else:
        self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'\
            ' where (LOWER(mm_metadata_tvshow_name) = %s) and (substring(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->>\'FirstAired\' from 0 for 5) in (%s,%s,%s) or substring(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->>\'premiered\' from 0 for 5) in (%s,%s,%s))', (tvshow_name.lower(), str(tvshow_year), str(int(tvshow_year) + 1), str(int(tvshow_year) - 1), str(tvshow_year), str(int(tvshow_year) + 1), str(int(tvshow_year) - 1)))
    for row_data in self.db_cursor.fetchall():
        metadata_guid = row_data['mm_metadata_tvshow_guid']
        logging.debug("db find metadata tv guid: %s", metadata_guid)
        break
    return metadata_guid



def srv_db_metatv_guid_by_imdb(self, imdb_uuid):
    """
    # metadata guid by imdb id
    """
    self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'\
        ' where mm_metadata_media_tvshow_id->\'imdb\' ? %s', (imdb_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


def srv_db_metatv_guid_by_tvdb(self, thetvdb_uuid):
    """
    # metadata guid by tv id
    """
    self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'\
        ' where mm_metadata_media_tvshow_id->\'thetvdb\' ? %s', (thetvdb_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


def srv_db_metatv_guid_by_tvmaze(self, tvmaze_uuid):
    """
    # metadata guid by tvmaze id
    """
    self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'\
        ' where mm_metadata_media_tvshow_id->\'tvmaze\' ? %s', (tvmaze_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


def srv_db_metatv_guid_by_tvrage(self, tvrage_uuid):
    """
    # metadata guid by tvrage id
    """
    self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'\
        ' where mm_metadata_media_tvshow_id->\'TVRage\' ? %s', (tvrage_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


def srv_db_meta_tvshow_list_count(self):
    """
    # tvshow count
    """
    self.db_cursor.execute('select count(*) from mm_metadata_tvshow')
    return self.db_cursor.fetchone()[0]


def srv_db_meta_tvshow_list(self, offset=None, records=None):
    """
    # return list of tvshows
    """
    # COALESCE - priority over one column
    if offset is None:
        self.db_cursor.execute('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name,'\
            ' COALESCE(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'premiered\','\
            ' mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Series\'->\'FirstAired\'), COALESCE(mm_metadata_tvshow_localimage_json->\'Images\'->\'tvmaze\'->>\'Poster\', mm_metadata_tvshow_localimage_json->\'Images\'->\'thetvdb\'->>\'Poster\') from mm_metadata_tvshow order by LOWER(mm_metadata_tvshow_name)')
    else:
        self.db_cursor.execute('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name,'\
            ' COALESCE(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'premiered\','\
            ' mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Series\'->\'FirstAired\'), COALESCE(mm_metadata_tvshow_localimage_json->\'Images\'->\'tvmaze\'->>\'Poster\', mm_metadata_tvshow_localimage_json->\'Images\'->\'thetvdb\'->>\'Poster\') from mm_metadata_tvshow where mm_metadata_tvshow_guid in (select mm_metadata_tvshow_guid from mm_metadata_tvshow order by LOWER(mm_metadata_tvshow_name) offset %s limit %s) order by LOWER(mm_metadata_tvshow_name)', (offset, records))
    return self.db_cursor.fetchall()


def srv_db_meta_tvshow_update_image(self, image_json, metadata_uuid):
    """
    # update image json
    """
    self.db_cursor.execute('update mm_metadata_tvshow set mm_metadata_tvshow_localimage_json = %s where mm_metadata_tvshow_guid = %s', (image_json, metadata_uuid))


def srv_db_meta_tvshow_images_to_update(self, image_type):
    """
    # fetch tvmaze rows to update
    """
    if image_type == 'tvmaze':
        self.db_cursor.execute("select mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\','\
            'mm_metadata_tvshow_guid from mm_metadata_tvshow'\
            ' where mm_metadata_tvshow_localimage_json->'Images'->'tvmaze'->'Redo' = 'true'")
    elif image_type == 'thetvdb':
        self.db_cursor.execute("select mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\','\
            'mm_metadata_tvshow_guid from mm_metadata_tvshow'\
            ' where mm_metadata_tvshow_localimage_json->'Images'->'thetvdb'->'Redo' = 'true'")
    return self.db_cursor.fetchall()


def srv_db_meta_tvshow_detail(self, guid):
    """
    # return metadata for tvshow
    """
    self.db_cursor.execute('select mm_metadata_tvshow_name, mm_metadata_tvshow_json,'\
        ' mm_metadata_tvshow_localimage_json, COALESCE(mm_metadata_tvshow_localimage_json->\'Images\'->\'tvmaze\'->>\'Poster\', mm_metadata_tvshow_localimage_json->\'Images\'->\'thetvdb\'->>\'Poster\') from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s', (guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def srv_db_read_tvmetadata_episodes(self, show_guid):
    """
    # read in the tv episodes metadata by guid
    """
    sql_params = show_guid,
    return self.db_cursor.fetchall()


def srv_db_read_tvmetadata_eps_season(self, show_guid):
    """
    # grab tvmaze ep data for eps per season
    """
    # todo union will be bad later when both data sources are populated
    season_data = {}
    self.db_cursor.execute('(select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'season\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'number\' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s) union (select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Episode\')::jsonb->\'SeasonNumber\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Episode\')::jsonb->\'EpisodeNumber\' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s)', (show_guid, show_guid))    
    for row_data in self.db_cursor.fetchall():
        if row_data[0] in season_data:
            if season_data[row_data[0]] < row_data[1]:
                season_data[row_data[0]] = row_data[1]
        else:
            season_data[row_data[0]] = row_data[1]
    return season_data


def srv_db_read_tvmetadata_season_eps_list(self, show_guid, season_number):
    """
    # grab episodes within the season
    """
    episode_data = {}
    self.db_cursor.execute('(select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'season\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'number\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'name\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'id\', mm_metadata_tvshow_localimage_json->\'Images\'->\'tvmaze\'->\'Episodes\' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s)', (show_guid,))
    for row_data in self.db_cursor.fetchall():
        if row_data[0] == season_number:
            try:
                episode_data[row_data[1]] = (row_data[2], row_data[4][str(row_data[3])])
            except:
                episode_data[row_data[1]] = (row_data[2], 'Missing_Icon.png')
    return episode_data


def srv_db_read_tvmetadata_episode(self, show_guid, season_number, episode_number):
    """
    # grab episode detail
    """
    logging.debug("huh: %s %s %s", show_guid, season_number, episode_number)
    self.db_cursor.execute('(select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'season\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'number\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'name\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'airstamp\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'runtime\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'summary\' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s)', (show_guid,))
    for row_data in self.db_cursor.fetchall():
        if str(row_data[0]) == season_number and str(row_data[1]) == episode_number:
            # 2 - name
            # 3 - airstamp
            # 4 - runtime
            # 5 - summary
            return row_data
    return None


# total episdoes in metadata from tvmaze
# jsonb_array_length(mm_metadata_tvshow_json->'Meta'->'tvmaze'->'_embedded'->'episodes')

# "last" episode season number from tvmaze
# mm_metadata_tvshow_json->'Meta'->'tvmaze'->'_embedded'->'episodes'->(jsonb_array_length(mm_metadata_tvshow_json->'Meta'->'tvmaze'->'_embedded'->'episodes') - 1)->'season'
