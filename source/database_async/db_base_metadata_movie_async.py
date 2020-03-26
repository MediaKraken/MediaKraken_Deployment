import json


async def db_meta_movie_by_media_uuid(self, db_connection, media_guid):
    """
    # read in metadata via media id
    """
    return await db_connection.fetchrow('select mm_metadata_json,'
                                        'mm_metadata_localimage_json '
                                        'from mm_media, mm_metadata_movie'
                                        ' where mm_media_metadata_guid = mm_metadata_guid'
                                        ' and mm_media_guid = %s', (media_guid,))


async def db_meta_movie_detail(self, db_connection, media_guid):
    """
    # read in the media with corresponding metadata
    """
    return await db_connection.fetchrow('select mm_metadata_guid,'
                                        ' mm_metadata_media_id,'
                                        ' mm_media_name,'
                                        ' mm_metadata_json,'
                                        ' mm_metadata_localimage_json,'
                                        ' mm_metadata_user_json'
                                        ' from mm_metadata_movie'
                                        ' where mm_metadata_guid = %s', (media_guid,))


async def db_meta_movie_list(self, db_connection, offset=0, records=None, search_value=None):
    """
    # return list of movies
    """
    if search_value is not None:
        return await db_connection.fetch('select mm_metadata_guid,mm_media_name,'
                                         'mm_metadata_json->\'Meta\'->\'themoviedb\'->\'Meta\'->\'release_date\' as mm_date,'
                                         'mm_metadata_localimage_json->\'Images\'->\'themoviedb\'->\'Poster\' as mm_poster,'
                                         'mm_metadata_user_json'
                                         ' from mm_metadata_movie where mm_metadata_guid in (select mm_metadata_guid'
                                         ' from mm_metadata_movie where mm_media_name %% %s'
                                         ' order by mm_media_name offset %s limit %s)'
                                         ' order by mm_media_name, mm_date',
                                         (search_value, offset, records))
    else:
        return await db_connection.fetch('select mm_metadata_guid,mm_media_name,'
                                         'mm_metadata_json->\'Meta\'->\'themoviedb\'->\'Meta\'->\'release_date\' as mm_date,'
                                         'mm_metadata_localimage_json->\'Images\'->\'themoviedb\'->\'Poster\' as mm_poster,'
                                         'mm_metadata_user_json'
                                         ' from mm_metadata_movie where mm_metadata_guid in (select mm_metadata_guid'
                                         ' from mm_metadata_movie order by mm_media_name offset %s limit %s)'
                                         ' order by mm_media_name, mm_date', (offset, records))


async def db_meta_movie_count(self, db_connection, search_value=None):
    if search_value is not None:
        return await db_connection.fetchval('select count(*) from mm_metadata_movie '
                                            ' where mm_media_name %% %s',
                                            (search_value,))
    else:
        return await db_connection.fetchval('select count(*) from mm_metadata_movie')


async def db_meta_movie_status_update(self, db_connection, metadata_guid, user_id, status_text):
    """
    # set status's for metadata
    """
    json_data = await db_connection.fetchrow('SELECT mm_metadata_user_json'
                                             ' from mm_metadata_movie'
                                             ' where mm_metadata_guid = %s FOR UPDATE',
                                             (metadata_guid,))['mm_metadata_user_json']
    if status_text == 'watched' or status_text == 'requested':
        status_setting = True
    else:
        status_setting = status_text
        status_text = 'Rating'
    try:
        if json_data is None or 'UserStats' not in json_data:
            json_data = {'UserStats': {}}
        if user_id in json_data['UserStats']:
            json_data['UserStats'][user_id][status_text] = status_setting
        else:
            json_data['UserStats'][user_id] = {status_text: status_setting}
        self.db_meta_movie_json_update(db_connection, metadata_guid, json.dumps(json_data))
    except:
        # TODO
        self.db_rollback()
        return None
