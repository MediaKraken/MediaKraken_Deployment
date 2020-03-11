def db_share(db_connection, offset=0, records=None):
    """
    # read the shares list
    """
    return db_connection.fetch('select mm_media_share_guid,'
                               ' mm_media_share_type,'
                               ' mm_media_share_user,'
                               ' mm_media_share_password,'
                               ' mm_media_share_server,'
                               ' mm_media_share_path'
                               ' from mm_media_share'
                               ' order by mm_media_share_type, mm_media_share_server,'
                               ' mm_media_share_path offset %s limit %s', (offset, records))
