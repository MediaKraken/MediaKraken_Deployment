import json


async def db_meta_movie_by_media_uuid(self, media_guid):
    """
    # read in metadata via media id
    """
    return await self.db_connection.fetchrow('select mm_metadata_json::json,'
                                             ' mm_metadata_localimage_json::json'
                                             ' from mm_media, mm_metadata_movie'
                                             ' where mm_media_metadata_guid = mm_metadata_guid'
                                             ' and mm_media_guid = $1', media_guid)


async def db_meta_movie_detail(self, media_guid):
    """
    # read in the media with corresponding metadata
    """
    return await self.db_connection.fetchrow('select mm_metadata_guid,'
                                             ' mm_metadata_media_id,'
                                             ' mm_media_name,'
                                             ' mm_metadata_json::json,'
                                             ' mm_metadata_localimage_json::json,'
                                             ' mm_metadata_user_json::json'
                                             ' from mm_metadata_movie'
                                             ' where mm_metadata_guid = $1',
                                             media_guid)


async def db_meta_movie_list(self, offset=0, records=None, search_value=None):
    """
    # return list of movies
    """
    if search_value is not None:
        return await self.db_connection.fetch('select mm_metadata_guid, mm_media_name,'
                                              ' mm_metadata_json->\'release_date\' as mm_date,'
                                              ' mm_metadata_localimage_json->\'Poster\''
                                              ' as mm_poster,'
                                              ' mm_metadata_user_json::json'
                                              ' from mm_metadata_movie where mm_metadata_guid'
                                              ' in (select mm_metadata_guid'
                                              ' from mm_metadata_movie where mm_media_name % $1'
                                              ' order by mm_media_name offset $2 limit $3)'
                                              ' order by mm_media_name, mm_date',
                                              search_value, offset, records)
    else:
        return await self.db_connection.fetch('select mm_metadata_guid, mm_media_name,'
                                              ' mm_metadata_json->\'release_date\' as mm_date,'
                                              ' mm_metadata_localimage_json->\'Poster\''
                                              ' as mm_poster,'
                                              ' mm_metadata_user_json::json'
                                              ' from mm_metadata_movie where mm_metadata_guid'
                                              ' in (select mm_metadata_guid'
                                              ' from mm_metadata_movie'
                                              ' order by mm_media_name offset'
                                              ' $1 limit $2)'
                                              ' order by mm_media_name, mm_date',
                                              offset, records)


async def db_meta_movie_count(self, search_value=None):
    if search_value is not None:
        return await self.db_connection.fetchval('select count(*) from mm_metadata_movie '
                                                 ' where mm_media_name % $1',
                                                 search_value)
    else:
        return await self.db_connection.fetchval('select count(*) from mm_metadata_movie')


async def db_meta_movie_status_update(self, metadata_guid, user_id, status_text):
    """
    # set status's for metadata
    """
    # do before the select to save db lock time
    if status_text == 'watched' or status_text == 'requested':
        status_setting = True
    else:
        status_setting = status_text
        status_text = 'Rating'
    # grab the user json for the metadata
    json_data = await self.db_connection.fetchrow('SELECT mm_metadata_user_json::json'
                                                  ' from mm_metadata_movie'
                                                  ' where mm_metadata_guid = $1 FOR UPDATE',
                                                  metadata_guid)
    # split this off so coroutine doesn't get mad
    try:
        json_data = json_data['mm_metadata_user_json']
    except:
        json_data = {'UserStats': {}}
    if str(user_id) in json_data['UserStats']:
        json_data['UserStats'][str(user_id)][status_text] = status_setting
    else:
        json_data['UserStats'][str(user_id)] = {status_text: status_setting}
    await self.db_meta_movie_json_update(metadata_guid,
                                         json.dumps(json_data))


async def db_meta_movie_json_update(self, media_guid, metadata_json):
    """
    # update the metadata json
    """
    await self.db_connection.execute('update mm_metadata_movie'
                                     ' set mm_metadata_user_json::json = $1'
                                     ' where mm_metadata_guid = $2',
                                     metadata_json, media_guid)
    await self.db_connection.execute('commit')


async def db_meta_movie_guid_count(self, guid):
    """
    # does movie exist already by metadata id
    """
    return await self.db_connection.fetchval('select count(*) from mm_metadata_movie'
                                             ' where mm_metadata_guid = $1', guid)
