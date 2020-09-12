import uuid


async def db_hardware_device_count(self, hardware_manufacturer, model_name=None):
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


async def db_hardware_json_read(self, manufacturer, model_name):
    """
    Return json for machine/model
    """
    return await self.db_connection.fetchval('SELECT row_to_json(json_data)'
                                             ' FROM (select mm_hardware_json'
                                             ' from mm_hardware_json'
                                             ' where mm_hardware_manufacturer = $1'
                                             ' and mm_hardware_model = $2) as json_data',
                                             manufacturer, model_name)


async def db_hardware_insert(self, manufacturer, model_name, json_data):
    new_guid = str(uuid.uuid4())
    await self.db_connection.execute('insert into mm_hardware_json (mm_hardware_id,'
                                     ' mm_hardware_manufacturer,'
                                     ' mm_hardware_model,'
                                     ' mm_hardware_json)'
                                     ' values ($1, $2, $3, $4)',
                                     new_guid, manufacturer, model_name, json_data)
    await self.db_connection.execute('commit')
    return new_guid


async def db_hardware_delete(self, guid):
    await self.db_connection.execute('delete from mm_hardware_json'
                                     ' where mm_hardware_id = $1', guid)
    await self.db_connection.execute('commit')
