import datetime
import uuid


async def db_library_path_add(self, dir_path, class_guid, share_guid):
    """
    # add media path
    """
    new_guid = str(uuid.uuid4())
    await self.db_connection.execute('insert into mm_media_dir (mm_media_dir_guid,'
                                     ' mm_media_dir_path,'
                                     ' mm_media_dir_class_type,'
                                     ' mm_media_dir_last_scanned,'
                                     ' mm_media_dir_share_guid)'
                                     ' values ($1, $2, $3, $4, $5)',
                                     new_guid, dir_path, class_guid,
                                     datetime.datetime(1970, 1, 1, 0, 0, 1), share_guid)
    return new_guid


async def db_library_path_by_uuid(self, dir_id):
    """
    # lib data per id
    """
    return await self.db_connection.fetchrow('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_media_dir_guid,'
                                             ' mm_media_dir_path,'
                                             ' mm_media_dir_class_type'
                                             ' from mm_media_dir'
                                             ' where mm_media_dir_share_guid = $1)'
                                             ' as json_data',
                                             dir_id)


async def db_library_path_check(self, dir_path):
    """
    # lib path check (dupes)
    """
    return await self.db_connection.fetchval(
        'select count(*) from mm_media_dir where mm_media_dir_path = $1',
        dir_path)


async def db_library_path_delete(self, lib_guid):
    """
    # remove media path
    """
    await self.db_connection.execute(
        'delete from mm_media_dir where mm_media_dir_share_guid = $1', lib_guid)


async def db_library_path_status(self):
    """
    # read scan status
    """
    return await self.db_connection.fetchrow('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_media_dir_path,'
                                             ' mm_media_dir_status'
                                             ' from mm_media_dir'
                                             ' where mm_media_dir_status IS NOT NULL'
                                             ' order by mm_media_dir_path) as json_data')


async def db_library_path_update_by_uuid(self, lib_path, class_guid, lib_guid):
    """
    # update audit path
    """
    await self.db_connection.execute('update mm_media_dir set mm_media_dir_path = $1,'
                                     ' mm_media_dir_class_type = $2'
                                     ' where mm_media_dir_share_guid = $3',
                                     lib_path, class_guid, lib_guid)


async def db_library_paths(self, offset=0, records=None):
    """
    # read the paths to audit
    """
    return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                          ' FROM (select mm_media_dir_path,'
                                          ' mm_media_dir_class_type,'
                                          ' mm_media_dir_last_scanned,'
                                          ' mm_media_dir_share_guid'
                                          ' from mm_media_dir'
                                          ' order by mm_media_dir_class_type, mm_media_dir_path'
                                          ' offset $1 limit $2) as json_data', offset, records)
