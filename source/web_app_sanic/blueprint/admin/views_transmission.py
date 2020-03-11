@blueprint.before_request
async def before_request(request):
    """
    Executes before each request
    """
    await database_base_async = database_base.MKServerDatabase()
    g.option_config_json = await database_base_async.db_opt_status_read(db_connection)[0]
    await database_base_async.db_open()
