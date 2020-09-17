async def db_library_path_status(db_connection):
    """
    # read scan status
    """
    return await db_connection.fetchrow('select mm_media_dir_path,'
                                        ' mm_media_dir_status'
                                        ' from mm_media_dir'
                                        ' where mm_media_dir_status IS NOT NULL'
                                        ' order by mm_media_dir_path')
