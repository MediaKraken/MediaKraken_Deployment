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
