def db_image_count(self, db_connection, class_guid, search_value=None):
    """
    Image list count
    """
    return db_connection.fetchval('select count(*) from mm_media,'
                                  'mm_media_class'
                                  ' where mm_media.mm_media_class_guid'
                                  ' = mm_media_class.mm_media_class_guid'
                                  ' and mm_media_class_guid = %s', (class_guid,))


def db_image_list(self, db_connection, class_guid, offset=0, records=None, search_value=None):
    """
    Image list
    """
    return db_connection.fetch('select mm_media_path from mm_media,'
                               'mm_media_class'
                               ' where mm_media.mm_media_class_guid'
                               ' = mm_media_class.mm_media_class_guid'
                               ' and mm_media_class_guid = %s offset %s limit %s',
                               (class_guid, offset, records))
