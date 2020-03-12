def db_meta_tv_detail(self, db_connection, guid):
    """
    # return metadata for tv show
    """
    return db_connection.fetchrow('select mm_metadata_tvshow_name, mm_metadata_tvshow_json,'
                                  ' mm_metadata_tvshow_localimage_json,'
                                  ' COALESCE(mm_metadata_tvshow_localimage_json'
                                  '->\'Images\'->\'tvmaze\'->>\'Poster\','
                                  ' mm_metadata_tvshow_localimage_json'
                                  '->\'Images\'->\'thetvdb\'->>\'Poster\') from mm_metadata_tvshow'
                                  ' where mm_metadata_tvshow_guid = %s', (guid,))


def db_meta_tv_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    # return list of tvshows
    """
    # TODO order by release date
    # COALESCE - priority over one column
    return db_connection.fetch('select mm_metadata_tvshow_guid,mm_metadata_tvshow_name,'
                               ' COALESCE(mm_metadata_tvshow_json->\'Meta\'->\'tvmaze\'->\'premiered\','
                               ' mm_metadata_tvshow_json->\'Meta\'->\'thetvdb\'->\'Meta\'->\'Series\''
                               '->\'FirstAired\') as air_date, COALESCE(mm_metadata_tvshow_localimage_json->\'Images\''
                               '->\'tvmaze\'->>\'Poster\', mm_metadata_tvshow_localimage_json->\'Images\''
                               '->\'thetvdb\'->>\'Poster\') as image_json from mm_metadata_tvshow'
                               ' where mm_metadata_tvshow_guid in (select mm_metadata_tvshow_guid'
                               ' from mm_metadata_tvshow order by LOWER(mm_metadata_tvshow_name)'
                               ' offset %s limit %s) order by LOWER(mm_metadata_tvshow_name)',
                               (offset, records))


def db_meta_tv_list_count(self, db_connection, search_value=None):
    """
    # tvshow count
    """
    if search_value is None:
        return db_connection.fetchval('select count(*) from mm_metadata_tvshow')
    else:
        return db_connection.fetchval('select count(*) from mm_metadata_tvshow')


def db_meta_tv_detail(self, db_connection, guid):
    """
    # return metadata for tvshow
    """
    return db_connection.fetchrow('select mm_metadata_tvshow_name, mm_metadata_tvshow_json,'
                                  ' mm_metadata_tvshow_localimage_json,'
                                  ' COALESCE(mm_metadata_tvshow_localimage_json'
                                  '->\'Images\'->\'tvmaze\'->>\'Poster\','
                                  ' mm_metadata_tvshow_localimage_json'
                                  '->\'Images\'->\'thetvdb\'->>\'Poster\') from mm_metadata_tvshow'
                                  ' where mm_metadata_tvshow_guid = %s', (guid,))
