async def db_metadata_guid_from_media_guid(self, db_connection, guid):
    return await db_connection.fetchval(
        'select mm_media_metadata_guid'
        ' from mm_media'
        ' where mm_media_guid = %s', guid)
