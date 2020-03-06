



@blueprint.before_request
async def before_request(request):
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.option_config_json = g.db_connection.db_opt_status_read()[0]
    g.db_connection.db_open()

