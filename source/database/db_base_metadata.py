"""
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
"""

import json

from common import common_logging_elasticsearch_httpx


def db_read_media_metadata(self, media_guid):
    """
    # read in the media with corresponding metadata
    """
    self.db_cursor.execute('select mm_metadata_guid,'
                           ' mm_metadata_media_id,'
                           ' mm_media_name,'
                           ' mm_metadata_json,'
                           ' mm_metadata_localimage_json,'
                           ' mm_metadata_user_json'
                           ' from mm_metadata_movie'
                           ' where mm_metadata_guid = %s', (media_guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_update(self, series_id_json, result_json, image_json):
    """
    # update record by tmdb
    """
    self.db_cursor.execute('update mm_metadata_movie set mm_metadata_media_id = %s,'
                           ' mm_media_name = %s,'
                           ' mm_metadata_json = %s,'
                           ' mm_metadata_localimage_json = %s'
                           ' where mm_metadata_media_id = %s',
                           (series_id_json, result_json['title'],
                            json.dumps(result_json), json.dumps(image_json),
                            result_json['id']))
    self.db_commit()


def db_meta_genre_list_count(self):
    """
    # count all the generes
    """
    self.db_cursor.execute('select distinct jsonb_array_elements_text(mm_metadata_json'
                           '->\'genres\')b'
                           ' from mm_metadata_movie')
    return len(self.db_cursor.fetchall())


def db_meta_genre_list(self, offset=0, records=None):
    """
    # grab all the generes
    """
    self.db_cursor.execute('select distinct jsonb_array_elements_text(mm_metadata_json'
                           '->\'genres\')b from mm_metadata_movie'
                           ' order by jsonb_array_elements_text(mm_metadata_json->\'genres\')b offset %s limit %s',
                           (offset, records))
    return self.db_cursor.fetchall()


def db_meta_movie_count_genre(self):
    """
    # movie count by genre
    """
    self.db_cursor.execute(
        'select jsonb_array_elements_text(mm_metadata_json->\'genres\')b as gen,'
        ' count(mm_metadata_json->\'genres\') from mm_metadata_movie group by gen'
        ' order by jsonb_array_elements_text(mm_metadata_json->\'genres\')b ')
    return self.db_cursor.fetchall()


def db_meta_guid_by_imdb(self, imdb_uuid):
    """
    # metadata guid by imdb id
    """
    self.db_cursor.execute('select mm_metadata_guid'
                           ' from mm_metadata_movie'
                           ' where mm_metadata_media_id->\'imdb\' ? %s', (imdb_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_guid']
    except:
        return None


def db_meta_guid_by_tmdb(self, tmdb_uuid):
    """
    # see if metadata exists type and id
    """
    self.db_cursor.execute('select mm_metadata_guid'
                           ' from mm_metadata_movie'
                           ' where mm_metadata_media_id = %s',
                           (tmdb_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_guid']
    except:
        return None


def db_meta_insert_tmdb(self, uuid_id, series_id, data_title, data_json,
                        data_image_json):
    """
    # insert metadata from themoviedb
    """
    self.db_cursor.execute('insert into mm_metadata_movie (mm_metadata_guid,'
                           ' mm_metadata_media_id,'
                           ' mm_media_name,'
                           ' mm_metadata_json,'
                           ' mm_metadata_localimage_json)'
                           ' values (%s,%s,%s,%s,%s)', (uuid_id, series_id, data_title,
                                                        data_json, data_image_json))
    self.db_commit()


def db_meta_tmdb_count(self, tmdb_id):
    """
    # see if metadata exists via themovedbid
    """
    self.db_cursor.execute('select exists(select 1 from mm_metadata_movie'
                           ' where mm_metadata_media_id = %s limit 1) limit 1', (tmdb_id,))
    return self.db_cursor.fetchone()[0]


def db_meta_movie_count(self, search_value=None):
    if search_value is not None:
        self.db_cursor.execute('select count(*) from mm_metadata_movie '
                               ' where mm_media_name %% %s',
                               (search_value,))
    else:
        self.db_cursor.execute('select count(*) from mm_metadata_movie')
    return self.db_cursor.fetchone()[0]


def db_meta_movie_list(self, offset=0, records=None, search_value=None):
    """
    # return list of movies
    """
    if search_value is not None:
        self.db_cursor.execute('select mm_metadata_guid,mm_media_name,'
                               'mm_metadata_json->\'release_date\' as mm_date,'
                               'mm_metadata_localimage_json->\'Poster\' as mm_poster,'
                               'mm_metadata_user_json'
                               ' from mm_metadata_movie where mm_metadata_guid'
                               ' in (select mm_metadata_guid'
                               ' from mm_metadata_movie where mm_media_name %% %s'
                               ' order by mm_media_name offset %s limit %s)'
                               ' order by mm_media_name, mm_date',
                               (search_value, offset, records))
    else:
        self.db_cursor.execute('select mm_metadata_guid,mm_media_name,'
                               'mm_metadata_json->\'release_date\' as mm_date,'
                               'mm_metadata_localimage_json->\'Poster\' as mm_poster,'
                               'mm_metadata_user_json'
                               ' from mm_metadata_movie '
                               'where mm_metadata_guid in (select mm_metadata_guid'
                               ' from mm_metadata_movie order by mm_media_name offset %s limit %s)'
                               ' order by mm_media_name, mm_date', (offset, records))
    return self.db_cursor.fetchall()


def db_meta_fetch_media_id_json(self, media_id_id,
                                collection_media=False):
    """
    # grab the current metadata json id
    """
    if not collection_media:
        self.db_cursor.execute('select mm_metadata_guid,'
                               ' mm_metadata_media_id'
                               ' from mm_metadata_movie'
                               ' where mm_metadata_media_id = %s',
                               (media_id_id,))
    else:
        self.db_cursor.execute('select mm_metadata_collection_guid,'
                               ' mm_metadata_collection_media_ids'
                               ' from mm_metadata_collection'
                               ' where mm_metadata_collection_media_ids->>%s = %s',
                               (media_id_id,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_meta_fetch_series_media_id_json(self, media_id_id,
                                       collection_media=False):
    """
    Fetch series json by id
    """
    if not collection_media:
        self.db_cursor.execute('select mm_metadata_tvshow_guid,'
                               ' mm_metadata_media_tvshow_id'
                               ' from mm_metadata_tvshow'
                               ' where mm_metadata_media_tvshow_id = %s',
                               (media_id_id,))
        try:
            return self.db_cursor.fetchone()
        except:
            return None


def db_find_metadata_guid(self, media_name, media_release_year):
    """
    Lookup id by name/year
    """
    metadata_guid = None
    if media_release_year is not None:
        # for year and -3/+3 year as well
        self.db_cursor.execute('select mm_metadata_guid from mm_metadata_movie'
                               ' where (LOWER(mm_media_name) = %s'
                               ' or LOWER(mm_metadata_json->>\'original_title\') = %s)'
                               ' and substring(mm_metadata_json->>\'release_date\' from 0 for 5)'
                               ' in (%s,%s,%s,%s,%s,%s,%s)',
                               (media_name.lower(), media_name.lower(), str(media_release_year),
                                str(int(media_release_year) + 1),
                                str(int(media_release_year) + 2),
                                str(int(media_release_year) + 3),
                                str(int(media_release_year) - 1),
                                str(int(media_release_year) - 2),
                                str(int(media_release_year) - 3)))
    else:
        self.db_cursor.execute('select mm_metadata_guid from mm_metadata_movie'
                               ' where (LOWER(mm_media_name) = %s'
                               ' or LOWER(mm_metadata_json->>\'original_title\') = %s)',
                               (media_name.lower(), media_name.lower()))
    for row_data in self.db_cursor.fetchall():
        # TODO should probably handle multiple results better.   Perhaps a notification?
        metadata_guid = row_data['mm_metadata_guid']
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text={
            "db find metadata guid": metadata_guid})
        break
    return metadata_guid


def db_meta_update_media_id_from_scudlee(self, media_tvid, media_imdbid,
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
    row_data = self.db_meta_fetch_media_id_json(media_id, False)
    # do the update if a record is found
    if row_data is not None:
        # update json data
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={"id": media_tvid,
                                                                           'imdb': media_imdbid,
                                                                           'ani': media_aniid})
        json_data = json.loads(row_data['mm_metadata_media_id'])
        if media_imdbid is not None:
            json_data.update({'imdb': media_imdbid})
        if media_tvid is not None:
            json_data.update({'thetvdb': media_tvid})
        if media_aniid is not None:
            json_data.update({'anidb': media_aniid})
        self.db_cursor.execute('update mm_metadata_movie set mm_metadata_media_id = %s'
                               ' where mm_metadata_guid = %s',
                               (json.dumps(json_data), row_data['mm_metadata_guid']))
    # lookup id from series
    row_data = self.db_meta_fetch_series_media_id_json(media_type, media_id)
    # do the update if a record is found
    if row_data is not None:
        # update json data
        common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info',
                                                             message_text={"id2": media_tvid,
                                                                           'imdb': media_imdbid,
                                                                           'anidb': media_aniid})
        json_data = json.loads(row_data['mm_metadata_media_tvshow_id'])
        if media_imdbid is not None:
            json_data.update({'imdb': media_imdbid})
        if media_tvid is not None:
            json_data.update({'thetvdb': media_tvid})
        if media_aniid is not None:
            json_data.update({'anidb': media_aniid})
        self.db_cursor.execute('update mm_metadata_tvshow set mm_metadata_media_tvshow_id = %s'
                               ' where mm_metadata_tvshow_guid = %s', (json.dumps(json_data),
                                                                       row_data[
                                                                           'mm_metadata_tvshow_guid']))


def db_meta_queue_list(self, user_id, offset=0, records=None, search_value=None):
    # TODO sort by release date as well
    # TODO use the search value
    self.db_cursor.execute('(select mm_metadata_guid,'
                           ' mm_media_name'
                           ' from mm_metadata_movie '
                           ' where mm_metadata_user_json->\'UserStats\'->%s->>\'queue\' = '
                           '\'True\''
                           ' order by LOWER(mm_media_name))'
                           ' UNION ALL '
                           '(select mm_metadata_tvshow_guid,'
                           ' mm_metadata_tvshow_name'
                           ' from mm_metadata_tvshow '
                           ' where mm_metadata_tvshow_user_json->\'UserStats\'->%s->>\'queue\' '
                           '= \'True\''
                           ' order by LOWER(mm_metadata_tvshow_name))'
                           ' UNION ALL '
                           '(select mm_metadata_music_guid,'
                           ' mm_metadata_music_name'
                           ' from mm_metadata_music '
                           ' where mm_metadata_music_user_json->\'UserStats\'->%s->>\'queue\' '
                           '= \'True\''
                           ' order by LOWER(mm_metadata_music_name))'
                           ' UNION ALL '
                           '(select mm_metadata_music_video_guid,'
                           ' mm_media_music_video_band'
                           ' from mm_metadata_music_video '
                           ' where '
                           'mm_metadata_music_video_user_json->\'UserStats\'->%s->>\'queue\' '
                           '= \'True\''
                           ' order by LOWER(mm_media_music_video_band))'
                           ' offset %s limit %s',
                           (user_id, user_id, user_id, user_id, offset, records))
    return self.db_cursor.fetchall()
