async def db_hardware_device_count(self, db_connection, hardware_manufacturer, model_name=None):
    """
    Return json for machine/model
    """
    if model_name is None:
        return await db_connection.fetchval('select count(*) from mm_hardware'
                                            ' where mm_hardware_manufacturer % $1',
                                            hardware_manufacturer)
    else:
        return await db_connection.fetchval('select count(*) from mm_hardware'
                                            ' where mm_hardware_manufacturer % $1'
                                            ' and mm_hardware_model = $2',
                                            hardware_manufacturer, model_name)
