#
# @blueprint.before_request
# async def before_request():
#     """
#     Executes before each request
#     """
#     await database_base_async = database_base.MKServerDatabase()
#     g.google_instance = common_google.CommonGoogle(await request.app.db_functions.db_opt_status_read(db_connection)[0])
#     g.twitch_api = common_network_twitchv5.CommonNetworkTwitchV5(
#         await request.app.db_functions.db_opt_status_read(db_connection)[0])
