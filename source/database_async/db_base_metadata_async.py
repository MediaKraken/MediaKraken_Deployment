async def db_metadata_guid_from_media_guid(self, guid, db_connection=None):
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval('select mm_media_metadata_guid'
                                  ' from mm_media'
                                  ' where mm_media_guid = $1', guid)


async def db_meta_insert_tmdb(self, uuid_id, series_id, data_title, data_json,
                              data_image_json, db_connection=None):
    """
    # insert metadata from themoviedb
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await db_conn.execute('insert into mm_metadata_movie (mm_metadata_guid,'
                          ' mm_metadata_media_id,'
                          ' mm_media_name,'
                          ' mm_metadata_json::json,'
                          ' mm_metadata_localimage_json::json)'
                          ' values ($1,$2,$3,$4,$5)',
                          uuid_id, series_id, data_title,
                          data_json, data_image_json)
    await db_conn.execute('commit')


async def db_meta_guid_by_imdb(self, imdb_uuid, db_connection=None):
    """
    # metadata guid by imdb id
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval('select mm_metadata_guid'
                                  ' from mm_metadata_movie'
                                  ' where mm_metadata_media_id->\'imdb\' ? $1',
                                  imdb_uuid)


async def db_meta_guid_by_tmdb(self, tmdb_uuid, db_connection=None):
    """
    # see if metadata exists type and id
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval('select mm_metadata_guid'
                                  ' from mm_metadata_movie'
                                  ' where mm_metadata_media_id = $1',
                                  tmdb_uuid)
