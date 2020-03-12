def db_meta_movie_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    # return list of movies
    """
    if search_value is not None:
        return db_connection.fetch('select mm_metadata_guid,mm_media_name,'
                                   'mm_metadata_json->\'Meta\'->\'themoviedb\'->\'Meta\'->\'release_date\' as mm_date,'
                                   'mm_metadata_localimage_json->\'Images\'->\'themoviedb\'->\'Poster\' as mm_poster,'
                                   'mm_metadata_user_json'
                                   ' from mm_metadata_movie where mm_metadata_guid in (select mm_metadata_guid'
                                   ' from mm_metadata_movie where mm_media_name %% %s'
                                   ' order by mm_media_name offset %s limit %s)'
                                   ' order by mm_media_name, mm_date',
                                   (search_value, offset, records))
    else:
        return db_connection.fetch('select mm_metadata_guid,mm_media_name,'
                                   'mm_metadata_json->\'Meta\'->\'themoviedb\'->\'Meta\'->\'release_date\' as mm_date,'
                                   'mm_metadata_localimage_json->\'Images\'->\'themoviedb\'->\'Poster\' as mm_poster,'
                                   'mm_metadata_user_json'
                                   ' from mm_metadata_movie where mm_metadata_guid in (select mm_metadata_guid'
                                   ' from mm_metadata_movie order by mm_media_name offset %s limit %s)'
                                   ' order by mm_media_name, mm_date', (offset, records))


def db_meta_movie_count(self, db_connection, search_value=None):
    if search_value is not None:
        return db_connection.fetchval('select count(*) from mm_metadata_movie '
                                      ' where mm_media_name %% %s',
                                      (search_value,))
    else:
        return db_connection.fetchval('select count(*) from mm_metadata_movie')
