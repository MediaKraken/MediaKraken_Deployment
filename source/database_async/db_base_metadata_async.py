async def db_metadata_guid_from_media_guid(self, guid):
    return await self.db_connection.fetchval('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_media_metadata_guid'
                                             ' from mm_media'
                                             ' where mm_media_guid = $1) as json_data', guid)


async def db_meta_insert_tmdb(self, uuid_id, series_id, data_title, data_json,
                              data_image_json):
    """
    # insert metadata from themoviedb
    """
    await self.db_connection.execute('insert into mm_metadata_movie (mm_metadata_guid,'
                                     ' mm_metadata_media_id,'
                                     ' mm_media_name,'
                                     ' mm_metadata_json,'
                                     ' mm_metadata_localimage_json)'
                                     ' values ($1,$2,$3,$4,$5)',
                                     uuid_id, series_id, data_title,
                                     data_json, data_image_json)
    await self.db_connection.db_commit()


async def db_meta_guid_by_imdb(self, imdb_uuid):
    """
    # metadata guid by imdb id
    """
    return await self.db_connection.fetchval('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_metadata_guid'
                                             ' from mm_metadata_movie'
                                             ' where mm_metadata_media_id->\'imdb\' ? $1)'
                                             ' as json_data',
                                             imdb_uuid)


async def db_meta_guid_by_tmdb(self, tmdb_uuid):
    """
    # see if metadata exists type and id
    """
    return await self.db_connection.fetchval('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_metadata_guid'
                                             ' from mm_metadata_movie'
                                             ' where mm_metadata_media_id = $1) as json_data',
                                             tmdb_uuid)
