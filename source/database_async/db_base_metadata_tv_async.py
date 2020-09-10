from common import common_global


async def db_meta_tv_detail(self, guid):
    """
    # return metadata for tvshow
    """
    return await self.db_connection.fetchrow('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_metadata_tvshow_name,'
                                             ' mm_metadata_tvshow_json,'
                                             ' mm_metadata_tvshow_localimage_json,'
                                             ' COALESCE(mm_metadata_tvshow_localimage_json'
                                             '->\'Images\'->\'tvmaze\'->>\'Poster\','
                                             ' mm_metadata_tvshow_localimage_json'
                                             '->\'Images\'->\'thetvdb\'->>\'Poster\')'
                                             ' from mm_metadata_tvshow'
                                             ' where mm_metadata_tvshow_guid = $1) as json_data',
                                             guid)


async def db_meta_tv_episode(self, show_guid, season_number, episode_number):
    """
    # grab episode detail
    """
    common_global.es_inst.com_elastic_index('info', {"show guid": show_guid,
                                                     'season': season_number,
                                                     'eps': episode_number})
    return await self.db_connection.fetchrow(
        'SELECT row_to_json(json_data)'
        ' FROM (select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'EpisodeName\' as eps_name,'
        ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'FirstAired\' as eps_first_air,'
        ' mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Runtime\' as eps_runtime,'
        ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'Overview\' as eps_overview'
        ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = $1) as json_data',
        show_guid, str(season_number), str(episode_number))


async def db_meta_tv_epsisode_by_id(self, show_guid, show_episode_id):
    """
    # grab episode detail by eps id
    """
    # TODO tvmaze
    # TODO injection fix
    return await self.db_connection.fetchrow('SELECT row_to_json(json_data)'
                                             ' FROM (select eps_data->\'EpisodeName\' as eps_name,'
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
                                             + str(show_episode_id) + '" }\') as json_data',
                                             show_guid)


async def db_meta_tv_eps_season(self, show_guid):
    """
    # grab tvmaze ep data for eps per season
    """
    season_data = {}
    for row_data in await self.db_connection.fetch(
            'SELECT row_to_json(json_data)'
            ' FROM (select count(*) as ep_count, jsonb_array_elements_text(mm_metadata_tvshow_json'
            '->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Episode\')::jsonb->\'SeasonNumber\' as season_num'
            ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = $1'
            ' group by season_num) as json_data', show_guid):
        # if row_data[0] in season_data:
        #     if season_data[row_data[0]] < row_data[1]:
        #         season_data[row_data[0]] = row_data[1]
        # else:
        #     season_data[row_data[0]] = row_data[1]
        season_data[int(row_data['season_num'])] = row_data['ep_count']
    return season_data


async def db_meta_tv_list(self, offset=0, records=None, search_value=None):
    """
    # return list of tvshows
    """
    # TODO order by release date
    return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                          ' FROM (select mm_metadata_tvshow_guid,'
                                          ' mm_metadata_tvshow_name,'
                                          ' mm_metadata_tvshow_json->\'first_air_date\''
                                          ' as air_date,'
                                          ' mm_metadata_tvshow_localimage_json->\'Poster\''
                                          ' as image_json from mm_metadata_tvshow'
                                          ' order by LOWER(mm_metadata_tvshow_name),'
                                          ' mm_metadata_tvshow_json->\'first_air_date\''
                                          ' offset $1 limit $2) as json_data',
                                          offset, records)


async def db_meta_tv_list_count(self, search_value=None):
    """
    # tvshow count
    """
    if search_value is None:
        return await self.db_connection.fetchval('select count(*) from mm_metadata_tvshow '
                                                 'where mm_metadata_tvshow_name % $1',
                                                 search_value)
    else:
        return await self.db_connection.fetchval('select count(*) from mm_metadata_tvshow')


async def db_meta_tv_season_eps_list(self, show_guid, season_number):
    """
    # grab episodes within the season
    """
    episode_data = {}
    # TODO security check the seasonumber since from webpage addy - injection
    await self.db_connection.fetch(
        'SELECT row_to_json(json_data)'
        ' FROM (select eps_data->\'id\' as eps_id, eps_data->\'EpisodeNumber\' as eps_num,'
        ' eps_data->\'EpisodeName\' as eps_name,'
        ' eps_data->\'filename\' as eps_filename'
        ' from (select jsonb_array_elements_text('
        'mm_metadata_tvshow_json->\'Episode\')::jsonb as eps_data'
        ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = $1)'
        ' as select_eps_data where eps_data @> \'{ "SeasonNumber": "'
        + str(season_number) + '" }\') as json_data', show_guid)
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
