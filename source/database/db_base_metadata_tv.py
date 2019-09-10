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

from common import common_global


def db_metatv_insert_tmdb(self, uuid_id, series_id, data_title, data_json,
                          data_image_json):
    """
    # insert metadata from themoviedb
    """
    self.db_cursor.execute('insert into mm_metadata_tvshow (mm_metadata_tvshow_guid,'
                           ' mm_metadata_media_tvshow_id, mm_metadata_tvshow_name,'
                           ' mm_metadata_tvshow_json,'
                           ' mm_metadata_tvshow_localimage_json)'
                           ' values (%s,%s,%s,%s,%s)', (uuid_id, series_id, data_title,
                                                        data_json, data_image_json))
    self.db_commit()


def db_metatv_guid_by_tvshow_name(self, tvshow_name, tvshow_year=None):
    """
    # metadata guid by name
    """
    common_global.es_inst.com_elastic_index('info',
                                            {'db_metatv_guid_by_tvshow_name': str(tvshow_name),
                                             'year': tvshow_year})
    metadata_guid = None
    if tvshow_year is None:
        self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'
                               ' where LOWER(mm_metadata_tvshow_name) = %s',
                               (tvshow_name.lower(),))
    else:
        # TODO jin index firstaird and premiered
        # TODO check tvmaze as well
        self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'
                               ' where (LOWER(mm_metadata_tvshow_name) = %s)'
                               ' and (substring(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\''
                               '->>\'FirstAired\' from 0 for 5) in (%s,%s,%s,%s,%s,%s,%s)'
                               ' or substring(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->>\'premiered\''
                               ' from 0 for 5) in (%s,%s,%s,%s,%s,%s,%s))',
                               (tvshow_name.lower(), str(tvshow_year),
                                str(int(tvshow_year) + 1),
                                str(int(tvshow_year) + 2),
                                str(int(tvshow_year) + 3),
                                str(int(tvshow_year) - 1),
                                str(int(tvshow_year) - 2),
                                str(int(tvshow_year) - 3),
                                str(tvshow_year),
                                str(int(tvshow_year) + 1),
                                str(int(tvshow_year) + 2),
                                str(int(tvshow_year) + 3),
                                str(int(tvshow_year) - 1),
                                str(int(tvshow_year) - 2),
                                str(int(tvshow_year) - 3)))
    for row_data in self.db_cursor.fetchall():
        metadata_guid = row_data['mm_metadata_tvshow_guid']
        common_global.es_inst.com_elastic_index('info', {"db find metadata tv guid":
                                                             metadata_guid})
        break
    return metadata_guid


def db_metatv_guid_by_imdb(self, imdb_uuid):
    """
    # metadata guid by imdb id
    """
    self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'
                           ' where mm_metadata_media_tvshow_id->\'imdb\' ? %s', (imdb_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


def db_metatv_guid_by_tvmaze(self, tvmaze_uuid):
    """
    # metadata guid by tvmaze id
    """
    self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'
                           ' where mm_metadata_media_tvshow_id->\'tvmaze\' ? %s', (tvmaze_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


def db_metatv_guid_by_tmdb(self, tmdb_uuid):
    """
    # metadata guid by tmdb id
    """
    self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'
                           ' where mm_metadata_media_tvshow_id->\'themoviedb\' ? %s',
                           (tmdb_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


def db_metatv_guid_by_rt(self, rt_uuid):
    """
    # metadata guid by rt id
    """
    self.db_cursor.execute('select mm_metadata_tvshow_guid from mm_metadata_tvshow'
                           ' where mm_metadata_media_tvshow_id->\'rottentomatoes\' ? %s',
                           (rt_uuid,))
    try:
        return self.db_cursor.fetchone()['mm_metadata_tvshow_guid']
    except:
        return None


def db_meta_tvshow_list_count(self, search_value=None):
    """
    # tvshow count
    """
    self.db_cursor.execute('select count(*) from mm_metadata_tvshow')
    return self.db_cursor.fetchone()[0]


def db_meta_tvshow_list(self, offset=0, records=None, search_value=None):
    """
    # return list of tvshows
    """
    # TODO order by release date
    # COALESCE - priority over one column
    self.db_cursor.execute('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name,'
                           ' COALESCE(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'premiered\','
                           ' mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Series\''
                           '->\'FirstAired\') as air_date, COALESCE(mm_metadata_tvshow_localimage_json->\'Images\''
                           '->\'tvmaze\'->>\'Poster\', mm_metadata_tvshow_localimage_json->\'Images\''
                           '->\'thetvdb\'->>\'Poster\') as image_json from mm_metadata_tvshow'
                           ' where mm_metadata_tvshow_guid in (select mm_metadata_tvshow_guid'
                           ' from mm_metadata_tvshow order by LOWER(mm_metadata_tvshow_name)'
                           ' offset %s limit %s) order by LOWER(mm_metadata_tvshow_name)',
                           (offset, records))
    return self.db_cursor.fetchall()


def db_meta_tvshow_update_image(self, image_json, metadata_uuid):
    """
    # update image json
    """
    self.db_cursor.execute('update mm_metadata_tvshow'
                           ' set mm_metadata_tvshow_localimage_json = %s'
                           ' where mm_metadata_tvshow_guid = %s',
                           (image_json, metadata_uuid))
    self.db_commit()


def db_meta_tvshow_images_to_update(self, image_type):
    """
    # fetch tv rows to update
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


def db_meta_tvshow_detail(self, guid):
    """
    # return metadata for tvshow
    """
    self.db_cursor.execute('select mm_metadata_tvshow_name, mm_metadata_tvshow_json,'
                           ' mm_metadata_tvshow_localimage_json,'
                           ' COALESCE(mm_metadata_tvshow_localimage_json'
                           '->\'Images\'->\'tvmaze\'->>\'Poster\','
                           ' mm_metadata_tvshow_localimage_json'
                           '->\'Images\'->\'thetvdb\'->>\'Poster\') from mm_metadata_tvshow'
                           ' where mm_metadata_tvshow_guid = %s', (guid,))
    try:
        return self.db_cursor.fetchone()
    except:
        return None


def db_read_tvmeta_episodes(self, show_guid):
    """
    # read in the tv episodes metadata by guid
    """
    return self.db_cursor.fetchall()


def db_read_tvmeta_eps_season(self, show_guid):
    """
    # grab tvmaze ep data for eps per season
    """
    season_data = {}
    # self.db_cursor.execute('select jsonb_array_elements_text(COALESCE((mm_metadata_tvshow_json'
    #                        '->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'season\', '
    #                         '(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Episode\')'
    #                         '::jsonb->\'SeasonNumber\')),'
    #                         'jsonb_array_elements_text(COALESCE((mm_metadata_tvshow_json'
    #                         '->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'number\','
    #                         '(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Episode\')'
    #                         '::jsonb->\'EpisodeNumber\'))'
    #                         'from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s', (show_guid,))

    self.db_cursor.execute(
        'select count(*) as ep_count, jsonb_array_elements_text(mm_metadata_tvshow_json'
        '->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Episode\')::jsonb->\'SeasonNumber\' as season_num'
        ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s'
        ' group by season_num', (show_guid,))
    for row_data in self.db_cursor.fetchall():
        # if row_data[0] in season_data:
        #     if season_data[row_data[0]] < row_data[1]:
        #         season_data[row_data[0]] = row_data[1]
        # else:
        #     season_data[row_data[0]] = row_data[1]
        season_data[int(row_data['season_num'])] = row_data['ep_count']
    return season_data


def db_read_tvmeta_season_eps_list(self, show_guid, season_number):
    """
    # grab episodes within the season
    """
    episode_data = {}
    # self.db_cursor.execute('select jsonb_array_elements_text(mm_metadata_tvshow_json'
    #     '->\'Meta\'->\'tvmaze\'->\'_embedded\'->\'episodes\')::jsonb->\'season\','
    #     ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\''
    #     '->\'_embedded\'->\'episodes\')::jsonb->\'number\','
    #     ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\''
    #     '->\'_embedded\'->\'episodes\')::jsonb->\'name\','
    #     ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\''
    #     '->\'_embedded\'->\'episodes\')::jsonb->\'id\', mm_metadata_tvshow_localimage_json'
    #     '->\'Images\'->\'tvmaze\'->\'Episodes\','

    # TODO security check the seasonumber since from webpage addy - injection
    self.db_cursor.execute(
        'select eps_data->\'id\' as eps_id, eps_data->\'EpisodeNumber\' as eps_num,'
        ' eps_data->\'EpisodeName\' as eps_name,'
        ' eps_data->\'filename\' as eps_filename'
        ' from (select jsonb_array_elements_text('
        'mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Episode\')::jsonb as eps_data'
        ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s)'
        ' as select_eps_data where eps_data @> \'{ "SeasonNumber": "'
        + str(season_number) + '" }\'', (show_guid,))
    # id, episode_number, episode_name, filename
    for row_data in self.db_cursor.fetchall():
        if row_data['eps_filename'] is None:
            episode_data[row_data['eps_num']] \
                = (row_data['eps_name'], 'missing_icon.jpg', row_data['eps_id'],
                   str(season_number))
        else:
            episode_data[row_data['eps_num']] \
                = (
                row_data['eps_name'], row_data['eps_filename'], row_data['eps_id'],
                str(season_number))
    return episode_data


def db_read_tvmeta_epsisode_by_id(self, show_guid, show_episode_id):
    """
    # grab episode detail by eps id
    """
    # TODO tvmaze
    # TODO injection fix
    self.db_cursor.execute('select eps_data->\'EpisodeName\' as eps_name,'
                           ' eps_data->\'FirstAired\' as eps_first_air,'
                           ' eps_data->\'Runtime\' as eps_runtime,'
                           ' eps_data->\'Overview\' as eps_overview,'
                           ' eps_data->\'filename\' as eps_filename'
                           ' from (select jsonb_array_elements_text('
                           'mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Episode\')::jsonb as eps_data'
                           ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s)'
                           ' as select_eps_data where eps_data @> \'{ "id": "'
                           + str(show_episode_id) + '" }\'', (show_guid,))
    return self.db_cursor.fetchone()


def db_read_tvmeta_episode(self, show_guid, season_number, episode_number):
    """
    # grab episode detail
    """
    common_global.es_inst.com_elastic_index('info', {"show guid": show_guid,
                                                     'season': season_number,
                                                     'eps': episode_number})
    # self.db_cursor.execute('(select
    #     ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\''
    #     '->\'_embedded\'->\'episodes\')::jsonb->\'name\','
    #     ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\''
    #     '->\'_embedded\'->\'episodes\')::jsonb->\'airstamp\','
    #     ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\''
    #     '->\'_embedded\'->\'episodes\')::jsonb->\'runtime\','
    #     ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\''
    #     '->\'_embedded\'->\'episodes\')::jsonb->\'summary\','

    self.db_cursor.execute(
        'select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'EpisodeName\' as eps_name,'
        ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'FirstAired\' as eps_first_air,'
        ' mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Runtime\' as eps_runtime,'
        ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'Overview\' as eps_overview'
        ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = %s',
        (show_guid, str(season_number), str(episode_number)))
    return self.db_cursor.fetchone()


# total episdoes in metadata from tvmaze
# jsonb_array_length(mm_metadata_tvshow_json->'Meta'->'tvmaze'->'_embedded'->'episodes')

# "last" episode season number from tvmaze
# mm_metadata_tvshow_json->'Meta'->'tvmaze'->'_embedded'->'episodes'->(jsonb_array_length(
# mm_metadata_tvshow_json->'Meta'->'tvmaze'->'_embedded'->'episodes')
# - 1)->'season'

# poster, backdrop, etc
def db_meta_tvshow_image_random(self, return_image_type='Poster'):
    """
    Find random tv show image
    """
    # TODO little bobby tables
    self.db_cursor.execute(
        'select mm_metadata_tvshow_localimage_json->\'Images\'->\'thetvdb\'->>\''
        + return_image_type + '\' as image_json,mm_metadata_guid from mm_media,mm_metadata_tvshow'
                              ' where mm_media_metadata_guid = mm_metadata_guid'
                              ' and (mm_metadata_tvshow_localimage_json->\'Images\'->\'thetvdb\'->>\''
        + return_image_type + '\'' + ')::text != \'null\' order by random() limit 1')
    try:
        # then if no results.....a None will except which will then pass None, None
        image_json, metadata_id = self.db_cursor.fetchone()
        return image_json, metadata_id
    except:
        return None, None
