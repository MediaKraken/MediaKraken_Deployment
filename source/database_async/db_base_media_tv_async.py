async def db_media_tv_list(self, genre_type=None, list_limit=None,
                           group_collection=False, offset=0, search_value=None,
                           db_connection=None):
    """
    # grab tv data
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if search_value is not None:
        return await db_conn.fetch('select mm_metadata_tvshow_name,'
                                   ' mm_metadata_tvshow_guid,'
                                   ' count(*) as mm_count,'
                                   ' COALESCE(mm_metadata_tvshow_localimage_json'
                                   '->\'Images\'->\'tvmaze\'->>\'Poster\','
                                   ' mm_metadata_tvshow_localimage_json'
                                   '->\'Images\'->\'thetvdb\'->>\'Poster\')'
                                   ' from mm_metadata_tvshow,'
                                   ' mm_media where mm_media_metadata_guid'
                                   ' = mm_metadata_tvshow_guid'
                                   ' and mm_metadata_tvshow_name % $1'
                                   ' group by mm_metadata_tvshow_guid'
                                   ' order by LOWER(mm_metadata_tvshow_name)'
                                   ' offset $2 limit $3', search_value,
                                   offset, list_limit)
    else:
        return await db_conn.fetch('select mm_metadata_tvshow_name,'
                                   ' mm_metadata_tvshow_guid,'
                                   ' count(*) as mm_count,'
                                   ' COALESCE(mm_metadata_tvshow_localimage_json'
                                   '->\'Images\'->\'tvmaze\'->>\'Poster\','
                                   ' mm_metadata_tvshow_localimage_json'
                                   '->\'Images\'->\'thetvdb\'->>\'Poster\')'
                                   ' from mm_metadata_tvshow,'
                                   ' mm_media where mm_media_metadata_guid'
                                   ' = mm_metadata_tvshow_guid'
                                   ' group by mm_metadata_tvshow_guid'
                                   ' order by LOWER(mm_metadata_tvshow_name)'
                                   ' offset $1 limit $2',
                                   offset, list_limit)


async def db_media_tv_list_count(self, genre_type=None, group_collection=False,
                                 search_value=None, db_connection=None):
    """
    # grab tv data count
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    sql_data = await db_conn.fetch('select count(*) from mm_metadata_tvshow, mm_media'
                                   ' where mm_media_metadata_guid'
                                   ' = mm_metadata_tvshow_guid')
    if sql_data is None:
        return 0
    return len(sql_data)
