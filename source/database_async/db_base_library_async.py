import uuid


def db_library_path_add(db_connection, dir_path, class_guid, share_guid):
    """
    # add media path
    """
    new_guid = str(uuid.uuid4())
    db_connection.execute('insert into mm_media_dir (mm_media_dir_guid,'
                          ' mm_media_dir_path,'
                          ' mm_media_dir_class_type,'
                          ' mm_media_dir_last_scanned,'
                          ' mm_media_dir_share_guid)'
                          ' values (%s,%s,%s,%s,%s)',
                          (new_guid, dir_path, class_guid,
                           psycopg2.Timestamp(1970, 1, 1, 0, 0, 1), share_guid))
    return new_guid


def db_library_path_by_uuid(db_connection, self, dir_id):
    """
    # lib data per id
    """
    return db_connection.fetch('select mm_media_dir_guid,'
                               ' mm_media_dir_path,'
                               ' mm_media_dir_class_type'
                               ' from mm_media_dir'
                               ' where mm_media_dir_share_guid = %s', (dir_id,))


def db_libary_path_delete(db_connection, lib_guid):
    """
    # remove media path
    """
    db_connection.execute(
        'delete from mm_media_dir where mm_media_dir_share_guid = %s', (lib_guid,))


def db_library_path_update_by_uuid(db_connection, lib_path, class_guid, lib_guid):
    """
    # update audit path
    """
    db_connection.execute('update mm_media_dir set mm_media_dir_path = %s,'
                          ' mm_media_dir_class_type = %s'
                          ' where mm_media_dir_share_guid = %s',
                          (lib_path, class_guid, lib_guid))


def db_library_paths(db_connection, offset=0, records=None):
    """
    # read the paths to audit
    """
    return db_connection.fetch('select mm_media_dir_path,'
                               ' mm_media_dir_class_type,'
                               ' mm_media_dir_last_scanned,'
                               ' mm_media_dir_share_guid'
                               ' from mm_media_dir'
                               ' order by mm_media_dir_class_type, mm_media_dir_path'
                               ' offset %s limit %s', (offset, records))
