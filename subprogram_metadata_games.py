'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
from common import common_config_ini
from common import common_internationalization
from common import common_logging
import uuid
import json
import xmltodict

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_MAME_XML')

# technically arcade games are "systems"....
# they just don't have @isdevice = 'yes' like mess hardware does

# create mame game list
update_game = 0
insert_game = 0
with open("/mediakraken/emulation/mame.xml", 'r') as xml_file:
    json_data = xmltodict.parse(xml_file.read())
    for child_of_root in json_data['mame']['machine']:
        print("child: %s", child_of_root)
        # see if exists then need to update
        db_connection.execute('select count(*) from mm_metadata_game_systems_info'
                              ' where gs_game_system_json->\'@name\' ? %s',
                              (child_of_root['@name'],))
        if db_connection.fetchone()[0] > 0:
            db_connection.execute('update mm_metadata_game_systems_info set gs_game_system_json = %s'
                                  ' where gs_game_system_json->\'@name\' ? %s',
                                  (json.dumps(child_of_root), child_of_root['@name']))
            update_game += 1
        else:
            db_connection.execute('insert into mm_metadata_game_systems_info'
                                  ' (gs_id, gs_game_system_json) values (%s,%s)',
                                  (str(uuid.uuid4()), json.dumps(child_of_root)))
            insert_game += 1

if update_game > 0:
    db_connection.db_notification_insert(
        common_internationalization.com_inter_number_format(update_game)
        + " games(s) metadata updated from MAME XML", True)

if insert_game > 0:
    db_connection.db_notification_insert(
        common_internationalization.com_inter_number_format(insert_game)
        + " games(s) metadata added from MAME XML", True)

# commit all changes to db
db_connection.db_commit()


# close the database
db_connection.db_close()
