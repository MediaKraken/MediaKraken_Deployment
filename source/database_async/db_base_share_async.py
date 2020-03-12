import uuid


def db_share_add(db_connection, share_type, share_user, share_password, share_server, share_path):
    """
    # add share path
    """
    new_guid = str(uuid.uuid4())
    db_connection.execute('insert into mm_media_share (mm_media_share_guid,'
                          ' mm_media_share_type,'
                          ' mm_media_share_user,'
                          ' mm_media_share_password,'
                          ' mm_media_share_server,'
                          ' mm_media_share_path)'
                          ' values (%s,%s,%s,%s,%s,%s)',
                          (new_guid, share_type, share_user,
                           share_password, share_server, share_path))
    return new_guid


def db_share_list(db_connection, offset=0, records=None):
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


def db_share_update_by_uuid(db_connection, share_type, share_user, share_password, share_server,
                            share_path, share_id):
    """
    # update share
    """
    db_connection.execute('update mm_media_share set mm_media_share_type = %s,'
                          ' mm_media_share_user = %s,'
                          ' mm_media_share_password = %s',
                          ' mm_media_share_server = %s',
                          ' where mm_media_share_path = %s',
                          ' and mm_media_share_guid = %s',
                          (share_type, share_user, share_password, share_server,
                           share_path, share_id))
