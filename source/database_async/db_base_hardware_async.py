import uuid


async def db_hardware_device_count(self, hardware_manufacturer, model_name=None,
                                   db_connection=None):
    """
    Return json for machine/model
    """
    if model_name is None:
        return await self.db_connection.fetchval('select count(*) from mm_hardware'
                                                 ' where mm_hardware_manufacturer = $1',
                                                 hardware_manufacturer)
    else:
        return await self.db_connection.fetchval('select count(*) from mm_hardware'
                                                 ' where mm_hardware_manufacturer = $1'
                                                 ' and mm_hardware_model = $2',
                                                 hardware_manufacturer, model_name)


async def db_hardware_json_read(self, manufacturer, model_name, db_connection=None):
    """
    Return json for machine/model
    """
    return await self.db_connection.fetchval('select mm_hardware_json::json'
                                             ' from mm_hardware_json'
                                             ' where mm_hardware_manufacturer = $1'
                                             ' and mm_hardware_model = $2',
                                             manufacturer, model_name)


async def db_hardware_insert(self, manufacturer, model_name, json_data, db_connection=None):
    new_guid = str(uuid.uuid4())
    await self.db_connection.execute('insert into mm_hardware_json (mm_hardware_id,'
                                     ' mm_hardware_manufacturer,'
                                     ' mm_hardware_model,'
                                     ' mm_hardware_json::json)'
                                     ' values ($1, $2, $3, $4)',
                                     new_guid, manufacturer, model_name, json_data)
    await self.db_connection.execute('commit')
    return new_guid


async def db_hardware_delete(self, guid, db_connection=None):
    await self.db_connection.execute('delete from mm_hardware_json'
                                     ' where mm_hardware_id = $1', guid)
    await self.db_connection.execute('commit')
