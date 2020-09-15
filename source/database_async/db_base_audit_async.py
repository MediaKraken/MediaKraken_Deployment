import datetime
import os
import uuid


async def db_audit_path_status(self):
    """
    # read scan status
    """
    return await self.db_connection.fetch('select mm_media_dir_path,'
                                          ' mm_media_dir_status'
                                          ' from mm_media_dir'
                                          ' where mm_media_dir_status IS NOT NULL'
                                          ' order by mm_media_dir_path')


async def db_audit_path_update_status(self, lib_guid, status_json):
    """
    # update status
    """
    await self.db_connection.execute('update mm_media_dir set mm_media_dir_status = $1'
                                     ' where mm_media_dir_share_guid = $2',
                                     status_json, lib_guid)


async def db_audit_path_update_by_uuid(self, lib_path, class_guid, lib_guid):
    """
    # update audit path
    """
    await self.db_connection.execute('update mm_media_dir set mm_media_dir_path = $1,'
                                     ' mm_media_dir_class_type = $2'
                                     ' where mm_media_dir_share_guid = $3',
                                     lib_path, class_guid, lib_guid)


async def db_audit_path_delete(self, lib_guid):
    """
    # remove media path
    """
    await self.db_connection.execute(
        'delete from mm_media_dir where mm_media_dir_share_guid = $1', lib_guid)


async def db_audit_path_add(self, dir_path, class_guid, share_guid):
    """
    # add media path
    """
    new_guid = str(uuid.uuid4())
    await self.db_connection.execute('insert into mm_media_dir (mm_media_dir_guid,'
                                     ' mm_media_dir_path,'
                                     ' mm_media_dir_class_type,'
                                     ' mm_media_dir_last_scanned,'
                                     ' mm_media_dir_share_guid)'
                                     ' values ($1,$2,$3,$4,$5)',
                                     (new_guid, dir_path, class_guid,
                                      psycopg2.Timestamp(1970, 1, 1, 0, 0, 1), share_guid))
    return new_guid


async def db_audit_path_check(self, dir_path):
    """
    # lib path check (dupes)
    """
    return await self.db_connection.fetchval('select count(*) from mm_media_dir'
                                             ' where mm_media_dir_path = $1',
                                             dir_path)


async def db_audit_dir_timestamp_update(self, dir_path):
    """
    # update the timestamp for directory scans
    """
    if dir_path[:1] != "\\":  # if not unc.....add the mnt
        dir_path = os.path.join('/mediakraken/mnt', dir_path)
    await self.db_connection.execute('update mm_media_dir set mm_media_dir_last_scanned = $1'
                                     ' where mm_media_dir_path = $2', datetime.datetime.now(),
                                     dir_path)


async def db_audit_paths(self, offset=0, records=None):
    """
    # read the paths to audit
    """
    return await self.db_connection.fetch('select mm_media_dir_path,'
                                          ' mm_media_dir_class_type,'
                                          ' mm_media_dir_last_scanned,'
                                          ' mm_media_dir_share_guid'
                                          ' from mm_media_dir'
                                          ' order by mm_media_dir_class_type, mm_media_dir_path'
                                          ' offset $1 limit $2', offset, records)


async def db_audit_path_by_uuid(self, dir_id):
    """
    # lib data per id
    """
    return await self.db_connection.fetchrow('select mm_media_dir_guid,'
                                             ' mm_media_dir_path,'
                                             ' mm_media_dir_class_type'
                                             ' from mm_media_dir'
                                             ' where mm_media_dir_share_guid = $1',
                                             dir_id)


async def db_audit_shares(self, offset=0, records=None):
    """
    # read the shares list
    """
    return await self.db_connection.fetch('select mm_media_share_guid,'
                                          ' mm_media_share_type,'
                                          ' mm_media_share_user,'
                                          ' mm_media_share_password,'
                                          ' mm_media_share_server,'
                                          ' mm_media_share_path'
                                          ' from mm_media_share'
                                          ' order by mm_media_share_type, mm_media_share_server,'
                                          ' mm_media_share_path offset $1 limit $2',
                                          offset,
                                          records)


async def db_audit_share_delete(self, share_guid):
    """
    # remove share
    """
    await self.db_connection.execute('delete from mm_media_share'
                                     ' where mm_media_share_guid = $1',
                                     share_guid)


async def db_audit_share_by_uuid(self, share_id):
    """
    # share per id
    """
    return await self.db_connection.fetchrow('select mm_media_share_guid,'
                                             ' mm_media_share_type,'
                                             ' mm_media_share_user,'
                                             ' mm_media_share_password,'
                                             ' mm_media_share_server,'
                                             ' mm_media_share_path,'
                                             ' from mm_media_share'
                                             ' where mm_media_share_guid = $1',
                                             share_id)


async def db_audit_share_update_by_uuid(self, share_type, share_user,
                                        share_password, share_server,
                                        share_path, share_id):
    """
    # update share
    """
    await self.db_connection.execute('update mm_media_share set mm_media_share_type = $1,'
                                     ' mm_media_share_user = $2,'
                                     ' mm_media_share_password = $3',
                                     ' mm_media_share_server = $4',
                                     ' where mm_media_share_path = $5',
                                     ' and mm_media_share_guid = $6',
                                     share_type, share_user,
                                     share_password, share_server,
                                     share_path, share_id)


async def db_audit_share_check(self, dir_path):
    """
    # share path check (dupes)
    """
    return await self.db_connection.fetchval('select count(*) from mm_media_share'
                                             ' where mm_media_share_path = $1',
                                             dir_path)


async def db_audit_share_add(self, share_type, share_user,
                             share_password, share_server, share_path):
    """
    # add share path
    """
    new_guid = str(uuid.uuid4())
    await self.db_connection.execute('insert into mm_media_share'
                                     ' (mm_media_share_guid,'
                                     ' mm_media_share_type,'
                                     ' mm_media_share_user,'
                                     ' mm_media_share_password,'
                                     ' mm_media_share_server,'
                                     ' mm_media_share_path)'
                                     ' values ($1,$2,$3,$4,$5,$6)',
                                     new_guid, share_type, share_user,
                                     share_password, share_server, share_path)
    return new_guid
