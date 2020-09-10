async def db_metadata_guid_from_media_guid(self, guid):
    return await self.db_connection.fetchval('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_media_metadata_guid'
                                             ' from mm_media'
                                             ' where mm_media_guid = $1) as json_data', guid)
