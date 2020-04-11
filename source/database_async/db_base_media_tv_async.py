async def db_media_tv_list(self, db_connection, genre_type=None, list_limit=None,
                           group_collection=False, offset=0, search_value=None):
    """
    # grab tv data
    """
    if search_value is not None:
        return await db_connection.fetch('select mm_metadata_tvshow_name,'
                                         ' mm_metadata_tvshow_guid,'
                                         ' count(*) as mm_count,'
                                         ' COALESCE(mm_metadata_tvshow_localimage_json'
                                         '->\'Images\'->\'tvmaze\'->>\'Poster\','
                                         ' mm_metadata_tvshow_localimage_json'
                                         '->\'Images\'->\'thetvdb\'->>\'Poster\')'
                                         ' from mm_metadata_tvshow,'
                                         ' mm_media where mm_media_metadata_guid = mm_metadata_tvshow_guid'
                                         ' and mm_metadata_tvshow_name % $1'
                                         ' group by mm_metadata_tvshow_guid'
                                         ' order by LOWER(mm_metadata_tvshow_name)'
                                         ' offset $2 limit $3', search_value, offset, list_limit)
    else:
        return await db_connection.fetch('select mm_metadata_tvshow_name,'
                                         ' mm_metadata_tvshow_guid,'
                                         ' count(*) as mm_count,'
                                         ' COALESCE(mm_metadata_tvshow_localimage_json'
                                         '->\'Images\'->\'tvmaze\'->>\'Poster\','
                                         ' mm_metadata_tvshow_localimage_json'
                                         '->\'Images\'->\'thetvdb\'->>\'Poster\')'
                                         ' from mm_metadata_tvshow,'
                                         ' mm_media where mm_media_metadata_guid = mm_metadata_tvshow_guid'
                                         ' group by mm_metadata_tvshow_guid'
                                         ' order by LOWER(mm_metadata_tvshow_name)'
                                         ' offset $1 limit $2', offset, list_limit)


async def db_media_tv_list_count(self, db_connection, genre_type=None, group_collection=False,
                                 search_value=None):
    """
    # grab tv data count
    """
    sql_data = await db_connection.fetch('select count(*) from mm_metadata_tvshow, mm_media'
                                         ' where mm_media_metadata_guid = mm_metadata_tvshow_guid'
                                         ' group by mm_metadata_tvshow_guid')
    if sql_data is None:
        return 0
    return len(sql_data)
