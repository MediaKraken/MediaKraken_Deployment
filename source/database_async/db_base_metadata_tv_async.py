from common import common_global


async def db_meta_tv_detail(self, db_connection, guid):
    """
    # return metadata for tvshow
    """
    return await db_connection.fetchrow('select mm_metadata_tvshow_name, mm_metadata_tvshow_json,'
                                        ' mm_metadata_tvshow_localimage_json,'
                                        ' COALESCE(mm_metadata_tvshow_localimage_json'
                                        '->\'Images\'->\'tvmaze\'->>\'Poster\','
                                        ' mm_metadata_tvshow_localimage_json'
                                        '->\'Images\'->\'thetvdb\'->>\'Poster\') from mm_metadata_tvshow'
                                        ' where mm_metadata_tvshow_guid = $1', guid)


async def db_meta_tv_episode(self, db_connection, show_guid, season_number, episode_number):
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
    return await db_connection.fetchrow(
        'select jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'EpisodeName\' as eps_name,'
        ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'FirstAired\' as eps_first_air,'
        ' mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Runtime\' as eps_runtime,'
        ' jsonb_array_elements_text(mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\''
        '->\'Episode\')::jsonb->\'Overview\' as eps_overview'
        ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = $1',
        show_guid, str(season_number), str(episode_number))


async def db_meta_tv_epsisode_by_id(self, db_connection, show_guid, show_episode_id):
    """
    # grab episode detail by eps id
    """
    # TODO tvmaze
    # TODO injection fix
    return await db_connection.fetchrow('select eps_data->\'EpisodeName\' as eps_name,'
                                        ' eps_data->\'FirstAired\' as eps_first_air,'
                                        ' eps_data->\'Runtime\' as eps_runtime,'
                                        ' eps_data->\'Overview\' as eps_overview,'
                                        ' eps_data->\'filename\' as eps_filename'
                                        ' from (select jsonb_array_elements_text('
                                        'mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Episode\')::jsonb as eps_data'
                                        ' from mm_metadata_tvshow where mm_metadata_tvshow_guid = $1)'
                                        ' as select_eps_data where eps_data @> \'{ "id": "'
                                        + str(show_episode_id) + '" }\'', show_guid)


async def db_meta_tv_eps_season(self, db_connection, show_guid):
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
    #                         'from mm_metadata_tvshow where mm_metadata_tvshow_guid = $1', (show_guid,))
    for row_data in await db_connection.fetch(
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


async def db_meta_tv_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    # return list of tvshows
    """
    # TODO order by release date
    # COALESCE - priority over one column
    return await db_connection.fetch('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name,'
                                     ' COALESCE(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'premiered\','
                                     ' mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Series\''
                                     '->\'FirstAired\') as air_date, COALESCE(mm_metadata_tvshow_localimage_json->\'Images\''
                                     '->\'tvmaze\'->>\'Poster\', mm_metadata_tvshow_localimage_json->\'Images\''
                                     '->\'thetvdb\'->>\'Poster\') as image_json from mm_metadata_tvshow'
                                     ' where mm_metadata_tvshow_guid in (select mm_metadata_tvshow_guid'
                                     ' from mm_metadata_tvshow order by LOWER(mm_metadata_tvshow_name)'
                                     ' offset $1 limit $2) order by LOWER(mm_metadata_tvshow_name)',
                                     offset, records)


async def db_meta_tv_list_count(self, db_connection, search_value=None):
    """
    # tvshow count
    """
    if search_value is None:
        return await db_connection.fetchval('select count(*) from mm_metadata_tvshow '
                                            'where mm_metadata_tvshow_name % $1', search_value)
    else:
        return await db_connection.fetchval('select count(*) from mm_metadata_tvshow')


async def db_meta_tv_season_eps_list(self, db_connection, show_guid, season_number):
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
    await db_connection.fetch(
        'select eps_data->\'id\' as eps_id, eps_data->\'EpisodeNumber\' as eps_num,'
        ' eps_data->\'EpisodeName\' as eps_name,'
        ' eps_data->\'filename\' as eps_filename'
        ' from (select jsonb_array_elements_text('
        'mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Episode\')::jsonb as eps_data'
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
