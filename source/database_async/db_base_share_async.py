import uuid


async def db_share_add(self, db_connection, share_type, share_user, share_password, share_server,
                       share_path):
    """
    # add share path
    """
    new_guid = str(uuid.uuid4())
    await db_connection.execute('insert into mm_media_share (mm_media_share_guid,'
                                ' mm_media_share_type,'
                                ' mm_media_share_user,'
                                ' mm_media_share_password,'
                                ' mm_media_share_server,'
                                ' mm_media_share_path)'
                                ' values (%s,%s,%s,%s,%s,%s)',
                                (new_guid, share_type, share_user,
                                 share_password, share_server, share_path))
    return new_guid


async def db_share_check(self, db_connection, dir_path):
    """
    # share path check (dupes)
    """
    return await db_connection.fetchval(
        'select count(*) from mm_media_share where mm_media_share_path = %s',
        (dir_path,))


async def db_share_delete(self, db_connection, share_guid):
    """
    # remove share
    """
    await db_connection.execute('delete from mm_media_share where mm_media_share_guid = %s',
                                (share_guid,))


async def db_share_list(self, db_connection, offset=0, records=None):
    """
    # read the shares list
    """
    return await db_connection.fetch('select mm_media_share_guid,'
                                     ' mm_media_share_type,'
                                     ' mm_media_share_user,'
                                     ' mm_media_share_password,'
                                     ' mm_media_share_server,'
                                     ' mm_media_share_path'
                                     ' from mm_media_share'
                                     ' order by mm_media_share_type, mm_media_share_server,'
                                     ' mm_media_share_path offset %s limit %s', (offset, records))


async def db_share_update_by_uuid(self, db_connection, share_type, share_user, share_password,
                                  share_server,
                                  share_path, share_id):
    """
    # update share
    """
    await db_connection.execute('update mm_media_share set mm_media_share_type = %s,'
                                ' mm_media_share_user = %s,'
                                ' mm_media_share_password = %s',
                                ' mm_media_share_server = %s',
                                ' where mm_media_share_path = %s',
                                ' and mm_media_share_guid = %s',
                                (share_type, share_user, share_password, share_server,
                                 share_path, share_id))
