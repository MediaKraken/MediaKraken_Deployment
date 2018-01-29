# stuff = 'where mm_media_name %% %s order by mm_media_name offset %s limit %s)' % ('table', 1, 3)
#
# print(stuff)
#
#
# stuff = 'hash/jfslhtr/jhytr'
#
# print stuff[0:5]
#
# print stuff.split('/',1)[1]
#
# print stuff[-1:]
import time
from metadata import metadata_game
# from common import common_lirc
from common import common_config_ini
from common import common_metadata_openweathermap

# metadata_game.game_system_update()

# lirc = common_lirc.CommonLIRC(None)
#
# lirc.com_lirc_init()
#
#
# code = ""
# while(code != "quit"):
#     print(lirc.com_lirc_nextcode())
#     # Delay...
#     time.sleep(1)
#
#
# lirc.com_lirc_close()
# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

weather = common_metadata_openweathermap.CommonMetadataOpenweatherMap(option_config_json)
weather.com_openweathermap_fetch_city()
weather.com_openweathermap_add_city()
