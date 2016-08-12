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


# metadata guid by name
def srv_db_MetadataTV_GUID_By_TVShow_Name(self, tvshow_name, tvshow_year=None):
    metadata_guid = None
    if tvshow_year is None:
        self.sql3_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow where LOWER(mm_metadata_tvshow_name) = %s', (tvshow_name.lower(),))
    else:
        self.sql3_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow where (LOWER(mm_metadata_tvshow_name) = %s) and (substring(mm_metadata_tvshow_json->\'Meta\'->\'theTVDB\'->\'Meta\'->>\'FirstAired\' from 0 for 5) in (%s,%s,%s) or substring(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->>\'premiered\' from 0 for 5) in (%s,%s,%s))', (tvshow_name.lower(), str(tvshow_year), str(int(tvshow_year) + 1), str(int(tvshow_year) - 1), str(tvshow_year), str(int(tvshow_year) + 1), str(int(tvshow_year) - 1)))
    for row_data in self.sql3_cursor.fetchall():
        metadata_guid = row_data['mm_metadata_tvshow_guid']
        logging.debug("db find metadata tv guid: %s", metadata_guid)
        break
    return metadata_guid



# metadata guid by imdb id
def srv_db_MetadataTV_GUID_By_IMDB(self, imdb_uuid):
    self.sql3_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow where mm_metadata_media_tvshow_id->\'IMDB\' ? %s', (imdb_uuid,))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


# metadata guid by tv id
def srv_db_MetadataTV_GUID_By_TVDB(self, thetvdb_uuid):
    self.sql3_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow where mm_metadata_media_tvshow_id->\'theTVDB\' ? %s', (thetvdb_uuid,))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


# metadata guid by tvmaze id
def srv_db_MetadataTV_GUID_By_TVMaze(self, tvmaze_uuid):
    self.sql3_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow where mm_metadata_media_tvshow_id->\'TVMaze\' ? %s', (tvmaze_uuid,))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


# metadata guid by tvrage id
def srv_db_MetadataTV_GUID_By_TVRage(self, tvrage_uuid):
    self.sql3_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow where mm_metadata_media_tvshow_id->\'TVRage\' ? %s', (tvrage_uuid,))
    try:
        return self.sql3_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


# tvshow count
def srv_db_Metadata_TVShow_List_Count(self):
    self.sql3_cursor.execute('select count(*) from mm_metadata_tvshow')
    return self.sql3_cursor.fetchone()[0]


# return list of tvshows
def srv_db_Metadata_TVShow_List(self, offset=None, records=None):
    # COALESCE - priority over one column
    if offset is None:
        self.sql3_cursor.execute('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name, COALESCE(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'premiered\', mm_metadata_tvshow_json->\'Meta\'->\'theTVDB\'->\'Meta\'->\'Series\'->\'FirstAired\'), COALESCE(mm_metadata_tvshow_localimage_json->\'Images\'->\'TVMaze\'->>\'Poster\', mm_metadata_tvshow_localimage_json->\'Images\'->\'theTVDB\'->>\'Poster\') from mm_metadata_tvshow order by LOWER(mm_metadata_tvshow_name)')
    else:
        self.sql3_cursor.execute('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name, COALESCE(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'premiered\', mm_metadata_tvshow_json->\'Meta\'->\'theTVDB\'->\'Meta\'->\'Series\'->\'FirstAired\'), COALESCE(mm_metadata_tvshow_localimage_json->\'Images\'->\'TVMaze\'->>\'Poster\', mm_metadata_tvshow_localimage_json->\'Images\'->\'theTVDB\'->>\'Poster\') from mm_metadata_tvshow where mm_metadata_tvshow_guid in (select mm_metadata_tvshow_guid from mm_metadata_tvshow order by LOWER(mm_metadata_tvshow_name) offset %s limit %s) order by LOWER(mm_metadata_tvshow_name)', (offset, records))
    return self.sql3_cursor.fetchall()


# update image json
def srv_db_Metadata_TVShow_Update_Image(self, image_json, metadata_uuid):
    self.sql3_cursor.execute('update mm_metadata_tvshow set mm_metadata_tvshow_localimage_json = %s where mm_metadata_tvshow_guid = %s', (image_json, metadata_uuid))


# fetch tvmaze rows to update
def srv_db_Metadata_TVShow_Images_To_Update(self, image_type):
    if image_type == 'TVMaze':
        self.sql3_cursor.execute("select mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\',mm_metadata_tvshow_guid from mm_metadata_tvshow where mm_metadata_tvshow_localimage_json->'Images'->'TVMaze'->'Redo' = 'true'")
    elif image_type == 'theTVDB':
        self.sql3_cursor.execute("select mm_metadata_tvshow_json->\'Meta\'->\'theTVDB\',mm_metadata_tvshow_guid from mm_metadata_tvshow where mm_metadata_tvshow_localimage_json->'Images'->'theTVDB'->'Redo' = 'true'")
    return self.sql3_cursor.fetchall()


# return metadata for tvshow
def srv_db_Metadata_TVShow_Detail(self, guid):
    self.sql3_cursor.execute('select mm_metadata_tvshow_name, mm_metadata_tvshow_json, mm_metadata_tvshow_localimage_json, COALESCE(mm_metadata_tvshow_localimage_json->\'Images\'->\'TVMaze\'->>\'Poster\', mm_metadata_tvshow_localimage_json->\'Images\'->\'theTVDB\'->>\'Poster\') from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s', (guid,))
    try:
        return self.sql3_cursor.fetchone()
    except:
        return None


# read in the tv episodes metadata by guid
def srv_db_Read_TVMetadata_Episodes(self, show_guid):
    sql_params = show_guid,
    return self.sql3_cursor.fetchall()


# grab tvmaze ep data for eps per season
def srv_db_Read_TVMetadata_Eps_Season(self, show_guid):
    # todo union will be bad later when both data sources are populated
    season_data = {}
    self.sql3_cursor.execute('(select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'season\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'number\' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s) union (select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'theTVDB\'->\'Meta\'->\'Episode\')::jsonb->\'SeasonNumber\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'theTVDB\'->\'Meta\'->\'Episode\')::jsonb->\'EpisodeNumber\' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s)', (show_guid, show_guid))    
    for row_data in self.sql3_cursor.fetchall():
        if row_data[0] in season_data:
            if season_data[row_data[0]] < row_data[1]:
                season_data[row_data[0]] = row_data[1]
        else:
            season_data[row_data[0]] = row_data[1]
    return season_data


# grab episodes within the season
def srv_db_Read_TVMetadata_Season_Eps_List(self, show_guid, season_number):
    episode_data = {}
    self.sql3_cursor.execute('(select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'season\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'number\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'name\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'id\', mm_metadata_tvshow_localimage_json->\'Images\'->\'TVMaze\'->\'Episodes\' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s)', (show_guid,))
    for row_data in self.sql3_cursor.fetchall():
        if row_data[0] == season_number:
            try:
                episode_data[row_data[1]] = (row_data[2], row_data[4][str(row_data[3])])
            except:
                episode_data[row_data[1]] = (row_data[2], 'Missing_Icon.png')
    return episode_data


# grab episode detail
def srv_db_Read_TVMetadata_Episode(self, show_guid, season_number, episode_number):
    logging.debug("huh: %s %s %s", show_guid, season_number, episode_number)
    self.sql3_cursor.execute('(select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'season\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'number\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'name\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'airstamp\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'runtime\', jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'TVMaze\'->\'_embedded\'->\'episodes\')::jsonb->\'summary\' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s)', (show_guid,))
    for row_data in self.sql3_cursor.fetchall():
        if str(row_data[0]) == season_number and str(row_data[1]) == episode_number:
            # 2 - name
            # 3 - airstamp
            # 4 - runtime
            # 5 - summary
            return row_data
            break
    return None


# total episdoes in metadata from tvmaze
# jsonb_array_length(mm_metadata_tvshow_json->'Meta'->'TVMaze'->'_embedded'->'episodes')

# "last" episode season number from tvmaze
# mm_metadata_tvshow_json->'Meta'->'TVMaze'->'_embedded'->'episodes'->(jsonb_array_length(mm_metadata_tvshow_json->'Meta'->'TVMaze'->'_embedded'->'episodes') - 1)->'season'
