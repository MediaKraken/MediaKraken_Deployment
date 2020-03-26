import uuid


async def db_device_by_uuid(self, db_connection, guid):
    """
    Return details from database via uuid
    """
    return await db_connection.fetchrow('select mm_device_type,'
                                        ' mm_device_json'
                                        ' from mm_device'
                                        ' where mm_device_id = $1', (guid,))


async def db_device_check(self, db_connection, device_type, device_name, device_ip):
    """
    Check to see if device exists already on db
    """
    return await db_connection.fetchval(
        'select count(*) from mm_device'
        ' where mm_device_type = $1 mm_device_json->\'Name\' ? $2'
        ' and mm_device_json->\'IP\' ? $3', (device_type, device_name, device_ip))


async def db_device_delete(self, db_connection, guid):
    """
    Remove a device from the database via uuid
    """
    await db_connection.execute(
        'delete from mm_device'
        ' where mm_device_id = $1', (guid,))


async def db_device_list(self, db_connection, device_type=None, offset=0, records=None,
                         search_value=None):
    """
    Return list of devices in database
    """
    if device_type is None:
        return await db_connection.fetch('select mm_device_id,'
                                         ' mm_device_type,'
                                         ' mm_device_json'
                                         ' from mm_device'
                                         ' order by mm_device_type'
                                         ' offset $1 limit $2', (offset, records))
    else:
        return await db_connection.fetch('select mm_device_id,'
                                         ' mm_device_type,'
                                         ' mm_device_json'
                                         ' from mm_device'
                                         ' where mm_device_type = $1 offset $2 limit $3',
                                         (device_type, offset, records))


async def db_device_update_by_uuid(self, db_connection, guid, device_type, device_json):
    """
    Update the device in the database
    """
    await db_connection.execute('update mm_device set mm_device_type = $1,'
                                ' mm_device_json = $2'
                                ' where mm_device_id = $3', (device_type, device_json, guid))


async def db_device_upsert(self, db_connection, device_type, device_json):
    """
    Upsert a device into the database
    """
    new_guid = str(uuid.uuid4())
    await db_connection.execute('INSERT INTO mm_device (mm_device_id,'
                                ' mm_device_type,'
                                ' mm_device_json)'
                                ' VALUES ($1, $2, $3)'
                                ' ON CONFLICT ((mm_device_json->>"IP"))'
                                ' DO UPDATE SET mm_device_type = $4, mm_device_json = $5',
                                (new_guid, device_type, device_json, device_type, device_json))
    return new_guid
