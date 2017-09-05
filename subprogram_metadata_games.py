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
from common import common_network
import zipfile
import os
import uuid
import json
import xmltodict

# open the database
option_config_json, db_connection = common_config_ini.com_config_read(True)

# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_MAME_XML')

# technically arcade games are "systems"....
# they just don't have @isdevice = 'yes' like mess hardware does

# create mame game list
if False:
    file_name = '/mediakraken/emulation/mame0189lx.zip'
    if not os.path.exists(file_name):
        common_network.mk_network_fetch_from_url(
            'https://github.com/mamedev/mame/releases/download/mame0189/mame0189lx.zip',
            file_name)
    zip_handle = zipfile.ZipFile(file_name, 'r')  # issues if u do RB
    for zippedfile in zip_handle.namelist():
        update_game = 0
        insert_game = 0
        json_data = xmltodict.parse(zip_handle.read(zippedfile))
        for child_of_root in json_data['mame']['machine']:
            logging.info("child: %s", child_of_root)
            logging.info("childname: %s", child_of_root['@name'])
            # see if exists then need to update
            if db_connection.db_meta_game_list_count(child_of_root['@name']) > 0:
                db_connection.db_meta_game_update(None, child_of_root['@name'], child_of_root)
                update_game += 1
            else:
                db_connection.db_meta_game_insert(None, child_of_root['@name'], child_of_root)
                insert_game += 1
    zip_handle.close()

    if update_game > 0:
        db_connection.db_notification_insert(
            common_internationalization.com_inter_number_format(update_game)
            + " games(s) metadata updated from MAME XML", True)

    if insert_game > 0:
        db_connection.db_notification_insert(
            common_internationalization.com_inter_number_format(insert_game)
            + " games(s) metadata added from MAME XML", True)

# load games from hash files
if True:
    file_name = '/mediakraken/emulation/mame0189s.zip'
    if not os.path.exists(file_name):
        common_network.mk_network_fetch_from_url(
            'https://github.com/mamedev/mame/releases/download/mame0189/mame0189s.zip',
            file_name)
    total_software = 0
    total_software_update = 0
    # do this all the time, since could be a new one
    with zipfile.ZipFile(file_name, 'r') as zf:
        zf.extract('mame.zip', '/mediakraken/emulation/')
    zip_handle = zipfile.ZipFile('/mediakraken/emulation/mame.zip', 'r')  # issues if u do RB
    for zippedfile in zip_handle.namelist():
        logging.info('zip: %s', zippedfile)
        if zippedfile[0:5] == 'hash/' and zippedfile != 'hash/':
            logging.info("fname: %s", zippedfile)
            json_data = xmltodict.parse(zip_handle.read(zippedfile))
            logging.info('after json')
            # find system id from mess
            file_name, ext = os.path.splitext(zippedfile)
            logging.info('fil,etx %s %s', (file_name, ext))
            game_short_name_guid \
                = db_connection.db_meta_games_system_guid_by_short_name(file_name.split('/', 1)[1])
            if game_short_name_guid is None:
                game_short_name_guid = db_connection.db_meta_games_system_insert(
                    None, file_name.split('/', 1)[1], None, None)
            if ext == ".xml":
                for json_game in json_data['softwarelist']['software']:
                    logging.info('xml: %s', json_game)
                    # TODO check to see if exists....if so, update
                    # build args and insert the record
                    db_connection.db_meta_game_insert(game_short_name_guid, json_game['@name'], json_game)
                    total_software += 1
            elif ext == ".hsi":
                for json_game in json_data['hashfile']['hash']:
                    logging.info('hsi: %s', json_game)
                    # TODO check to see if exists....if so, update
                    # build args and insert the record
                    db_connection.db_meta_game_insert(game_short_name_guid, json_game['name'], json_game)
                    total_software += 1

    if total_software > 0:
        db_connection.db_notification_insert(
            common_internationalization.com_inter_number_format(total_software)
            + " games(s) metadata added from MAME hash", True)

    if total_software_update > 0:
        db_connection.db_notification_insert(
            common_internationalization.com_inter_number_format(total_software_update)
            + " games(s) metadata updated from MAME hash", True)


# update mame game descriptions from history dat
file_name = '/mediakraken/emulation/history189.zip'
if not os.path.exists(file_name):
    common_network.mk_network_fetch_from_url(
        'https://www.arcade-history.com/dats/history189.zip', file_name)
if True:
    game_titles = []
    game_desc = ""
    add_to_desc = False
    zip_handle = zipfile.ZipFile(file_name, 'r')  # issues if u do RB
    for zippedfile in zip_handle.namelist():
        logging.info('zip: %s', zippedfile)
        history_file = zip_handle.read(zippedfile)
        while 1:
            line = history_file.readline()
            if not line:
                break
            if line.find("$info=") == 0:
                game_titles = line.split("=", 1)[1].split(",")
            elif line.find("$end") == 0:
                add_to_desc = False
                for game in game_titles:
                    game_data = json.loads(db_connection.db_meta_game_by_name_and_system(
                        game, None)[0])
                    # let it explode if not found....should always be found
                    game_data['gi_game_info_json']['overview'] = game_desc
                    db_connection.db_meta_game_update_by_guid(
                        json.dumps(game_data['gi_game_info_json']), game_data['gi_id'])
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
