async def db_media_known_count(db_connection):
    """
    # count known media
    """
    return await db_connection.fetchval('select count(*) from mm_media')


async def db_media_matched_count(db_connection):
    """
    # count matched media
    """
    return await db_connection.fetchval('select count(*) from mm_media'
                                        ' where mm_media_metadata_guid is not NULL')
