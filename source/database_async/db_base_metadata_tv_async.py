import inspect

from common import common_logging_elasticsearch_httpx


async def db_metatv_guid_by_tmdb(self, tmdb_uuid, db_connection=None):
    """
    # metadata guid by tmdb id
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchrow('select mm_metadata_tvshow_guid from mm_metadata_tvshow'
                                  ' where mm_metadata_media_tvshow_id->\'themoviedb\' ? $1',
                                  tmdb_uuid)['mm_metadata_tvshow_guid']


async def db_meta_tv_detail(self, guid, db_connection=None):
    """
    # return metadata for tvshow
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchrow('select mm_metadata_tvshow_name,'
                                  ' mm_metadata_tvshow_json::json,'
                                  ' mm_metadata_tvshow_localimage_json,'
                                  ' COALESCE(mm_metadata_tvshow_localimage_json'
                                  '->\'Images\'->\'tvmaze\'->>\'Poster\','
                                  ' mm_metadata_tvshow_localimage_json'
                                  '->\'Images\'->\'thetvdb\'->>\'Poster\')'
                                  ' from mm_metadata_tvshow'
                                  ' where mm_metadata_tvshow_guid = $1',
                                  guid)


async def db_meta_tv_episode(self, show_guid, season_number, episode_number, db_connection=None):
    """
    # grab episode detail
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchrow(
        'select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'EpisodeName\' as eps_name,'
        ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'FirstAired\' as eps_first_air,'
        ' mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Runtime\' as eps_runtime,'
        ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'Overview\' as eps_overview'
        ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = $1',
        show_guid, str(season_number), str(episode_number))


async def db_meta_tv_epsisode_by_id(self, show_guid, show_episode_id, db_connection=None):
    """
    # grab episode detail by eps id
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    # TODO tvmaze
    # TODO injection fix
    return await db_conn.fetchrow('select eps_data->\'EpisodeName\' as eps_name,'
                                  ' eps_data->\'FirstAired\' as eps_first_air,'
                                  ' eps_data->\'Runtime\' as eps_runtime,'
                                  ' eps_data->\'Overview\' as eps_overview,'
                                  ' eps_data->\'filename\' as eps_filename'
                                  ' from (select jsonb_array_elements_text('
                                  'mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
                                  '->\'Meta\'->\'Episode\')::jsonb as eps_data'
                                  ' from mm_metadata_tvshow'
                                  ' where mm_metadata_tvshow_guid = $1)'
                                  ' as select_eps_data where eps_data @> \'{ "id": "'
                                  + str(show_episode_id) + '" }\'',
                                  show_guid)


async def db_meta_tv_eps_season(self, show_guid, db_connection=None):
    """
    # grab tvmaze ep data for eps per season
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    season_data = {}
    for row_data in await db_conn.fetch(
            'select count(*) as ep_count, jsonb_array_elements_text(mm_metadata_tvshow_json'
            '->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Episode\')::jsonb->\'SeasonNumber\' as season_num'
            ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = $1'
            ' group by season_num', show_guid):
        # if row_data[0] in season_data:
        #     if season_data[row_data[0]] < row_data[1]:
        #         season_data[row_data[0]] = row_data[1]
        # else:
        #     season_data[row_data[0]] = row_data[1]
        season_data[int(row_data['season_num'])] = row_data['ep_count']
    return season_data


async def db_meta_tv_list(self, offset=0, records=None, search_value=None, db_connection=None):
    """
    # return list of tvshows
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    # TODO order by release date
    return await db_conn.fetch('select mm_metadata_tvshow_guid,'
                               ' mm_metadata_tvshow_name,'
                               ' mm_metadata_tvshow_json->\'first_air_date\''
                               ' as air_date,'
                               ' mm_metadata_tvshow_localimage_json->\'Poster\''
                               ' as image_json from mm_metadata_tvshow'
                               ' order by LOWER(mm_metadata_tvshow_name),'
                               ' mm_metadata_tvshow_json->\'first_air_date\''
                               ' offset $1 limit $2',
                               offset, records)


async def db_meta_tv_list_count(self, search_value=None, db_connection=None):
    """
    # tvshow count
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if search_value is None:
        return await db_conn.fetchval('select count(*) from mm_metadata_tvshow '
                                      'where mm_metadata_tvshow_name % $1',
                                      search_value)
    else:
        return await db_conn.fetchval('select count(*) from mm_metadata_tvshow')


async def db_meta_tv_season_eps_list(self, show_guid, season_number, db_connection=None):
    """
    # grab episodes within the season
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    episode_data = {}
    # TODO security check the seasonumber since from webpage addy - injection
    await db_conn.fetch(
        'select eps_data->\'id\' as eps_id, eps_data->\'EpisodeNumber\' as eps_num,'
        ' eps_data->\'EpisodeName\' as eps_name,'
        ' eps_data->\'filename\' as eps_filename'
        ' from (select jsonb_array_elements_text('
        'mm_metadata_tvshow_json->\'Episode\')::jsonb as eps_data'
        ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = $1)'
        ' as select_eps_data where eps_data @> \'{ "SeasonNumber": "'
        + str(season_number) + '" }\'', show_guid)
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


async def db_meta_tv_count_by_id(self, guid, db_connection=None):
    """
    # does movie exist already by provider id
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval('select count(*) from mm_metadata_tvshow'
                                  ' where mm_metadata_media_tvshow_id = $1', guid)
