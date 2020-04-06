async def db_image_count(self, db_connection, class_guid, search_value=None):
    """
    Image list count
    """
    return await db_connection.fetchval('select count(*) from mm_media,'
                                        'mm_media_class_guid'
                                        ' where mm_media.mm_media_class_guid'
                                        ' = mm_media_class.mm_media_class_guid'
                                        ' and mm_media_class_guid = $1', class_guid)


async def db_image_list(self, db_connection, class_guid, offset=0, records=None, search_value=None):
    """
    Image list
    """
    return await db_connection.fetch('select mm_media_path from mm_media,'
                                     'mm_media_class_guid'
                                     ' where mm_media.mm_media_class_guid'
                                     ' = mm_media_class.mm_media_class_guid'
                                     ' and mm_media_class_guid = $1 offset $2 limit $3',
                                     class_guid, offset, records)
