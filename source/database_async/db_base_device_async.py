import uuid


async def db_device_by_uuid(self, guid, db_connection=None):
    """
    Return details from database via uuid
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchrow('select mm_device_type,'
                                  ' mm_device_json::json'
                                  ' from mm_device'
                                  ' where mm_device_id = $1', guid)


async def db_device_check(self, device_type, device_name, device_ip, db_connection=None):
    """
    Check to see if device exists already on db
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    return await db_conn.fetchval(
        'select count(*) from mm_device'
        ' where mm_device_type = $1 mm_device_json->\'Name\' ? $2'
        ' and mm_device_json->\'IP\' ? $3', device_type, device_name, device_ip)


async def db_device_delete(self, guid, db_connection=None):
    """
    Remove a device from the database via uuid
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await db_conn.execute(
        'delete from mm_device'
        ' where mm_device_id = $1', guid)


async def db_device_list(self, device_type=None, offset=0, records=None,
                         search_value=None, db_connection=None):
    """
    Return list of devices in database
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    if device_type is None:
        return await db_conn.fetch('select mm_device_id,'
                                   ' mm_device_type,'
                                   ' mm_device_json::json'
                                   ' from mm_device'
                                   ' order by mm_device_type'
                                   ' offset $1 limit $2',
                                   offset, records)
    else:
        return await db_conn.fetch('select mm_device_id,'
                                   ' mm_device_type,'
                                   ' mm_device_json::json'
                                   ' from mm_device'
                                   ' where mm_device_type = $1 offset $2 limit $3',
                                   device_type, offset, records)


async def db_device_update_by_uuid(self, guid, device_type, device_json, db_connection=None):
    """
    Update the device in the database
    """
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await db_conn.execute('update mm_device set mm_device_type = $1,'
                          ' mm_device_json = $2'
                          ' where mm_device_id = $3', device_type, device_json, guid)


async def db_device_upsert(self, device_type, device_json, db_connection=None):
    """
    Upsert a device into the database
    """
    new_guid = str(uuid.uuid4())
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    await db_conn.execute('INSERT INTO mm_device (mm_device_id,'
                          ' mm_device_type,'
                          ' mm_device_json)'
                          ' VALUES ($1, $2, $3)'
                          ' ON CONFLICT ((mm_device_json->>"IP"))'
                          ' DO UPDATE SET mm_device_type = $4, mm_device_json = $5',
                          new_guid, device_type, device_json, device_type, device_json)
    return new_guid
