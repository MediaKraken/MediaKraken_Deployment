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
import json


def srv_db_read_media_metadata(self, media_guid):
    """
    # read in the media with corresponding metadata
    """
    self.db_cursor.execute("select mm_metadata_guid, mm_metadata_media_id, mm_media_name,'\
        ' mm_metadata_json, mm_metadata_localimage_json, mm_metadata_user_json'\
        ' from mm_metadata_movie where mm_metadata_guid = %s", (media_guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def srv_db_meta_update(self, series_id_json, result_json, image_json):
    """
    # update record by tmdb
    """
    self.db_cursor.execute('update mm_metadata_movie set mm_metadata_media_id = %s,'\
        ' mm_media_name = %s, mm_metadata_json = %s, mm_metadata_localimage_json = %s'\
        ' where mm_metadata_media_id->\'TMDB\' ? %s', (series_id_json, result_json['title'],\
        json.dumps(result_json), json.dumps(image_json), str(result_json['id'])))


def srv_db_meta_genre_list_count(self):
    """
    # count all the generes
    """
    self.db_cursor.execute('select distinct jsonb_array_elements_text(mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'genres\')::json from mm_metadata_movie')
    return len(self.db_cursor.fetchall())


def srv_db_meta_genre_list(self, offset=None, records=None):
    """
    # grab all the generes
    """
    if offset is None:
        self.db_cursor.execute('select distinct jsonb_array_elements_text(mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'genres\')::jsonb from mm_metadata_movie order by jsonb_array_elements_text(mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'genres\')::jsonb')
    else:
        self.db_cursor.execute('select distinct jsonb_array_elements_text(mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'genres\')::jsonb from mm_metadata_movie order by jsonb_array_elements_text(mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'genres\')::jsonb offset %s limit %s', (offset, records))
    return self.db_cursor.fetchall()


def srv_db_meta_movie_count_by_genre(self):
    """
    # movie count by genre
    """
    self.db_cursor.execute('select jsonb_array_elements_text(mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'genres\')::jsonb as gen, count(mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'genres\') from mm_metadata_movie group by gen order by jsonb_array_elements_text(mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'genres\')::jsonb ')
    return self.db_cursor.fetchall()

    
def srv_db_meta_guid_by_imdb(self, imdb_uuid):
    """
    # metadata guid by imdb id
    """
    self.db_cursor.execute('select mm_metadata_guid from mm_metadata_movie'\
        ' where mm_metadata_media_id->\'imdb\' ? %s', (imdb_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_guid']
    except:
        return None


def srv_db_meta_guid_by_tvdb(self, thetvdb_uuid):
    """
    # metadata guid by tv id
    """
    self.db_cursor.execute('select mm_metadata_guid from mm_metadata_movie'\
        ' where mm_metadata_media_id->\'thetvdb\' ? %s', (thetvdb_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_guid']
    except:
        return None


def srv_db_meta_guid_by_tmdb(self, tmdb_uuid):
    """
    # see if metadata exists type and id
    """
    self.db_cursor.execute('select mm_metadata_guid from mm_metadata_movie'\
        ' where mm_metadata_media_id->\'TMDB\' ? %s', (str(tmdb_uuid),))
    try:
        return self.db_cursor.fetchone()['mm_metadata_guid']
    except:
        return None


def srv_db_meta_guid_by_rt(self, rt_uuid):
    """
    # see if metadata exists type and id
    """
    self.db_cursor.execute('select mm_metadata_guid from mm_metadata_movie'\
        ' where mm_metadata_media_id->\'RT\' ? %s', (str(tmdb_uuid),))
    try:
        return self.db_cursor.fetchone()['mm_metadata_guid']
    except:
        return None


def srv_db_meta_insert_tmdb(self, uuid_id, series_id, data_title, data_json,\
        data_image_json):
    """
    # insert metadata from themoviedb
    """
    self.db_cursor.execute('insert into mm_metadata_movie (mm_metadata_guid,'\
        ' mm_metadata_media_id, mm_media_name, mm_metadata_json, mm_metadata_localimage_json)'\
        ' values (%s,%s,%s,%s,%s)', (uuid_id, series_id, data_title, data_json, data_image_json))
    self.srv_db_commit()


def srv_db_meta_tmdb_count(self, tmdb_id):
    """
    # see if metadata exists via themovedbid
    """
    self.db_cursor.execute('select count(*) from mm_metadata_movie'\
        ' where mm_metadata_media_id->\'TMDB\' ? %s', (str(tmdb_id),))
    return self.db_cursor.fetchone()[0]


def srv_db_meta_movie_list(self, offset=None, records=None):
    """
    # return list of movies
    """
    if offset is None:
        self.db_cursor.execute('select mm_metadata_guid,mm_media_name,'\
            'mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'release_date\','\
            ' mm_metadata_localimage_json->\'Images\'->\'TMDB\'->\'Poster\''\
            ' from mm_metadata_movie order by LOWER(mm_media_name)')
    else:
#        self.db_cursor.execute('select mm_metadata_guid,mm_media_name,mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'release_date\', mm_metadata_localimage_json->\'Images\'->\'TMDB\'->\'Poster\' from mm_metadata_movie where mm_metadata_guid in (select mm_metadata_guid from mm_metadata_movie order by LOWER(mm_media_name) offset %s limit %s) order by LOWER(mm_media_name)', (offset, records))
        self.db_cursor.execute('select mm_metadata_guid,mm_media_name,'\
            'mm_metadata_json->\'Meta\'->\'TMDB\'->\'Meta\'->\'release_date\','\
            ' mm_metadata_localimage_json->\'Images\'->\'TMDB\'->\'Poster\''\
            ' from mm_metadata_movie where mm_metadata_guid in (select mm_metadata_guid'\
            ' from mm_metadata_movie order by mm_media_name offset %s limit %s)'\
            ' order by mm_media_name', (offset, records))
    return self.db_cursor.fetchall()


def srv_db_meta_fetch_media_id_json(self, media_id_type, media_id_id,\
        collection_media=False):
    """
    # grab the current metadata json id
    """
    if not collection_media:
        self.db_cursor.execute('select mm_metadata_guid, mm_metadata_media_id'\
            ' from mm_metadata_movie where mm_metadata_media_id->>%s = %s',\
            (media_id_type, media_id_id))
    else:
        self.db_cursor.execute('select mm_metadata_collection_guid,'\
            ' mm_metadata_collection_media_ids from mm_metadata_collection'\
            ' where mm_metadata_collection_media_ids->>%s = %s', (media_id_type, media_id_id))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def srv_db_meta_fetch_series_media_id_json(self, media_id_type, media_id_id,\
        collection_media=False):
    if not collection_media:
        self.db_cursor.execute('select mm_metadata_tvshow_guid, mm_metadata_media_tvshow_id'\
            ' from mm_metadata_tvshow where mm_metadata_media_tvshow_id->>%s = %s',\
            (media_id_type, media_id_id))
        try:
            return self.db_cursor.fetchone()
        except:
            return None


def srv_db_find_metadata_guid(self, media_name, media_release_year):
    metadata_guid = None
    if media_release_year is not None:
        # for year and -1/+1 year as well
        self.db_cursor.execute('select mm_metadata_guid from mm_metadata_movie'\
            ' where (LOWER(mm_media_name) = %s'\
            ' or LOWER(mm_metadata_json->>\'original_title\') = %s)'\
            ' and substring(mm_metadata_json->>\'release_date\' from 0 for 5) in (%s,%s,%s)',\
            (media_name.lower(), media_name.lower(), str(media_release_year),\
            str(int(media_release_year) + 1), str(int(media_release_year) - 1)))
    else:
        self.db_cursor.execute('select mm_metadata_guid from mm_metadata_movie'\
            ' where (LOWER(mm_media_name) = %s'\
            ' or LOWER(mm_metadata_json->>\'original_title\') = %s)',\
            (media_name.lower(), media_name.lower()))
    for row_data in self.db_cursor.fetchall():
        metadata_guid = row_data['mm_metadata_guid']
        logging.debug("db find metadata guid: %s", metadata_guid)
        break
    return metadata_guid


def srv_db_meta_update_media_id_from_scudlee(self, media_tvid, media_imdbid,\
        media_aniid):
    """
    # update the mediaid in metadata
    """
    # do tvdb first due to datadump
    if media_tvid is not None:
        media_type = 'thetvdb'
        media_id = media_tvid
    elif media_imdbid is not None:
        media_type = 'imdb'
        media_id = media_imdbid
    elif media_aniid is not None:
        media_type = 'anidb'
        media_id = media_aniid
    # lookup id from metadata json or collections
    row_data = self.srv_db_meta_fetch_media_id_json(media_type, media_id, False)
    # do the update if a record is found
    if row_data is not None:
        # update json data
        logging.debug("id: %s %s %s", media_tvid, media_imdbid, media_aniid)
        json_data = json.loads(row_data['mm_metadata_media_id'])
        if media_imdbid is not None:
            json_data.update({'imdb':media_imdbid})
        if media_tvid is not None:
            json_data.update({'thetvdb':media_tvid})
        if media_aniid is not None:
            json_data.update({'anidb':media_aniid})
        self.db_cursor.execute('update mm_metadata_movie set mm_metadata_media_id = %s'\
            ' where mm_metadata_guid = %s', (json.dumps(json_data), row_data['mm_metadata_guid']))
    # lookup id from series
    row_data = self.srv_db_meta_fetch_series_media_id_json(media_type, media_id)
    # do the update if a record is found
    if row_data is not None:
        # update json data
        logging.debug("id2: %s %s %s", media_tvid, media_imdbid, media_aniid)
        json_data = json.loads(row_data['mm_metadata_media_tvshow_id'])
        if media_imdbid is not None:
            json_data.update({'imdb':media_imdbid})
        if media_tvid is not None:
            json_data.update({'thetvdb':media_tvid})
        if media_aniid is not None:
            json_data.update({'anidb':media_aniid})
        self.db_cursor.execute('update mm_metadata_tvshow set mm_metadata_media_tvshow_id = %s'\
            ' where mm_metadata_tvshow_guid = %s', (json.dumps(json_data),\
            row_data['mm_metadata_tvshow_guid']))
