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
import os
import uuid
import json
import xmltodict
import subprocess

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_MAME_XML')

# technically arcade games are "systems"....
# they just don't have @isdevice = 'yes' like mess hardware does

# create mame game list
mame_pid = subprocess.Popen('mame', '-listxml', '>', '/mediakraken/emulation/mame.xml')
mame_pid.wait()
update_game = 0
insert_game = 0
with open("/mediakraken/emulation/mame.xml", 'r') as xml_file:
    json_data = xmltodict.parse(xml_file.read())
    for child_of_root in json_data['mame']['machine']:
        logging.info("child: %s", child_of_root)
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

# load games from hash files
total_software = 0
total_software_update = 0
hash_path = "/mediakraken/emulation/hash"
for fname in os.listdir(hash_path):
    logging.info("fname: %s", fname)
    # find system id from mess
    file_name, ext = os.path.splitext(fname)
    if ext == ".xml":
        db_connection.execute('select gs_id from mm_metadata_game_systems_info'\
            ' where gs_game_system_json->\'@name\' ? %s', (file_name.replace(".xml", ""),))
        row_data = db_connection.fetchone()
        if row_data is not None:
            with open(os.path.join(hash_path, fname), 'r') as data_file:
                for json_game in xmltodict.parse(data_file.read())['softwarelist']['software']:
                    # TODO check to see if exists....if so, update
                    # build args and insert the record
                    db_connection.execute('insert into mm_metadata_game_software_info (gi_id,'\
                        ' gi_system_id, gi_game_info_json) values (%s,%s,%s)',
                        (str(uuid.uuid4()), row_data['gs_id'], json.dumps(json_game)))
                    total_software += 1
        else:
            logging.info("system not found: %s", file_name)
            # TODO add "new" system
    elif ext == ".hsi":
        db_connection.execute('select gs_id from mm_metadata_game_systems_info'\
            ' where gs_game_system_json->\'@name\' ? %s', (file_name.replace(".hsi", ""),))
        row_data = db_connection.fetchone()
        if row_data is not None:
            with open(os.path.join(hash_path, fname), 'r') as data_file:
                for json_game in xmltodict.parse(data_file.read())['hashfile']['hash']:
                    # TODO check to see if exists....if so, update
                    # build args and insert the record
                    db_connection.execute("insert into mm_metadata_game_software_info (gi_id,'\
                        ' gi_system_id, gi_game_info_json) values (%s,%s,%s)",
                        (str(uuid.uuid4()), row_data['gs_id'], json.dumps(json_game)))
                    total_software += 1
        else:
            logging.info("system not found: %s", file_name)
            # TODO add "new" system

    if total_software > 0:
        db_connection.db_notification_insert(
            common_internationalization.com_inter_number_format(total_software)
            + " games(s) metadata added from MAME hash", True)

    if total_software_update > 0:
        db_connection.db_notification_insert(
            common_internationalization.com_inter_number_format(total_software_update)
            + " games(s) metadata updated from MAME hash", True)


# update mame game descriptions from history dat
game_titles = []
game_desc = ""
add_to_desc = False
history_file = open("/mediakraken/emulation/history.dat", "rb")
while 1:
    line = history_file.readline()
    if not line:
        break
    if line.find("$info=") == 0:
        game_titles = line.split("=", 1)[1].split(",")
    elif line.find("$end") == 0:
        add_to_desc = False
        for game in game_titles:
            db_connection.execute('select gi_game_info_json from mm_game_info'
                                  ' where gi_game_info_name ? %s', (game,))
            json_data = json.loads(db_connection.fetchone()[0])
            json_data['overview'] = game_desc
            db_connection.execute("update mm_game_info set gi_game_info_json = %s"
                                  " where gi_game_info_name ? %s", (json.dumps(json_data), game))
            game_desc = ""
    if add_to_desc:
        game_desc += line
    if line.find("$bio") == 0:
        add_to_desc = True
history_file.close()


# commit all changes to db
db_connection.db_commit()


# close the database
db_connection.db_close()
