def db_hardware_device_count(db_connection, hardware_manufacturer, model_name=None):
    """
    Return json for machine/model
    """
    if model_name is None:
        return db_connection.fetchval('select count(*) from mm_hardware_json'
                                      ' where mm_hardware_manufacturer %% %s',
                                      (hardware_manufacturer,))
    else:
        return db_connection.fetchval('select count(*) from mm_hardware_json'
                                      ' where mm_hardware_manufacturer %% %s'
                                      ' and mm_hardware_model %% %s',
                                      (hardware_manufacturer, model_name))
