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

import json
import os
import zipfile

import xmltodict
from common import common_config_ini
from common import common_global
from common import common_internationalization
from common import common_logging_elasticsearch
from common import common_network
from common import common_version

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
    'subprogram_metadata_games')

# technically arcade games are "systems"....
# they just don't have @isdevice = 'yes' like mess hardware does

# However, mame games are still being put as "games" and not systems
# to ease search and other filters by game/system

# create mame game list
file_name = ('/mediakraken/emulation/mame0%slx.zip' %
             common_version.MAME_VERSION)
# only do the parse/import if not processed before
if not os.path.exists(file_name):
    common_network.mk_network_fetch_from_url(
        ('https://github.com/mamedev/mame/releases/download/mame0%s/mame0%slx.zip'
         % (common_version.MAME_VERSION, common_version.MAME_VERSION)),
        file_name)
    zip_handle = zipfile.ZipFile(file_name, 'r')  # issues if u do RB
    update_game = 0
    insert_game = 0
    for zippedfile in zip_handle.namelist():
        json_data = xmltodict.parse(zip_handle.read(zippedfile))
        for child_of_root in json_data['mame']['machine']:
            common_global.es_inst.com_elastic_index('info', {'child': child_of_root,
                                                             'childname': child_of_root['@name']})
            # see if exists then need to update
            if db_connection.db_meta_game_list_count(child_of_root['@name']) > 0:
                # TODO handle shortname properly
                db_connection.db_meta_game_update(
                    None, child_of_root['@name'], child_of_root['description'], child_of_root)
                update_game += 1
            else:
                # TODO handle shortname properly
                db_connection.db_meta_game_insert(
                    None, child_of_root['@name'], child_of_root['description'], child_of_root)
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
file_name = ('/mediakraken/emulation/mame0%ss.zip' %
             common_version.MAME_VERSION)
# only do the parse/import if not processed before
if not os.path.exists(file_name):
    common_network.mk_network_fetch_from_url(
        ('https://github.com/mamedev/mame/releases/download/mame0%s/mame0%ss.zip'
         % (common_version.MAME_VERSION, common_version.MAME_VERSION)),
        file_name)
    total_software = 0
    total_software_update = 0
    # do this all the time, since could be a new one
    with zipfile.ZipFile(file_name, 'rb') as zf:
        zf.extract('mame.zip', '/mediakraken/emulation/')
    zip_handle = zipfile.ZipFile(
        '/mediakraken/emulation/mame.zip', 'r')  # issues if u do RB
    for zippedfile in zip_handle.namelist():
        print(('zip: %s', zippedfile))
        if zippedfile[0:5] == 'hash/' and zippedfile != 'hash/':
            print(("fname: %s", zippedfile))
            # find system id from mess
            file_name, ext = os.path.splitext(zippedfile)
            print(('fil,etx %s %s' % (file_name, ext)))
            if ext == ".xml" or ext == ".hsi":
                json_data = xmltodict.parse(zip_handle.read(zippedfile))
                print(('sys: %s', file_name.split('/', 1)[1]))
                game_short_name_guid \
                    = db_connection.db_meta_games_system_guid_by_short_name(
                    file_name.split('/', 1)[1])
                print(('wh %s', game_short_name_guid))
                if game_short_name_guid is None:
                    game_short_name_guid = db_connection.db_meta_games_system_insert(
                        None, file_name.split('/', 1)[1], None, None)
                if ext == ".xml":
                    # could be no games in list
                    if 'software' in json_data['softwarelist']:
                        print((json_data['softwarelist']['software']))
                        # TODO this fails if only one game
                        print((len(json_data['softwarelist']['software'])))
                        if '@name' in json_data['softwarelist']['software']:
                            # TODO check to see if exists....if so, update
                            db_connection.db_meta_game_insert(game_short_name_guid,
                                                              json_data['softwarelist']['software'][
                                                                  '@name'],
                                                              json_data['softwarelist']['software'][
                                                                  '@name'],
                                                              json_data['softwarelist']['software'])
                        else:
                            for json_game in json_data['softwarelist']['software']:
                                print(('xml: %s', json_game))
                                # json_game = json.loads(json_game)
                                # TODO check to see if exists....if so, update
                                # build args and insert the record
                                db_connection.db_meta_game_insert(game_short_name_guid,
                                                                  json_game['@name'],
                                                                  json_game['@name'], json_game)
                        total_software += 1
                elif ext == ".hsi":
                    # could be no games in list
                    if 'hash' in json_data['hashfile']:
                        if '@name' in json_data['hashfile']['hash']:
                            # TODO check to see if exists....if so, update
                            db_connection.db_meta_game_insert(game_short_name_guid,
                                                              json_data['hashfile']['hash'][
                                                                  '@name'],
                                                              json_data['hashfile']['hash'][
                                                                  '@name'],
                                                              json_data['hashfile']['hash'])
                        else:
                            for json_game in json_data['hashfile']['hash']:
                                print(('hsi: %s', json_game))
                                # TODO check to see if exists....if so, update
                                # build args and insert the record
                                db_connection.db_meta_game_insert(game_short_name_guid,
                                                                  json_game['@name'],
                                                                  json_game['@name'], json_game)
                        total_software += 1
    if total_software > 0:
        db_connection.db_notification_insert(
            common_internationalization.com_inter_number_format(total_software)
            + " games(s) metadata added from MAME hash", True)
    if total_software_update > 0:
        db_connection.db_notification_insert(
            common_internationalization.com_inter_number_format(
                total_software_update)
            + " games(s) metadata updated from MAME hash", True)

# update mame game descriptions from history dat
file_name = ('/mediakraken/emulation/history%s.zip' %
             common_version.MAME_VERSION)
# only do the parse/import if not processed before
if not os.path.exists(file_name):
    common_network.mk_network_fetch_from_url(
        ('https://www.arcade-history.com/dats/history%s.zip' %
         common_version.MAME_VERSION),
        file_name)
    game_titles = []
    game_desc = ""
    add_to_desc = False
    new_title = None
    total_software = 0
    total_software_update = 0
    system_name = None
    # do this all the time, since could be a new one
    with zipfile.ZipFile(file_name, 'r') as zf:
        zf.extract('history.dat', '/mediakraken/emulation/')
    history_file = open("/mediakraken/emulation/history.dat", "rb")
    while 1:
        line = history_file.readline().decode("utf-8")
        # print('line: %s' % line)
        if not line:
            break
        if line[0] == '$' and line[-1:] == ',':  # this could be a new system/game item
            # MAME "system"....generally a PCB game
            if line.find("$info=") == 0:  # goes by position if found
                system_name = None
                game_titles = line.split("=", 1)[1].split(",")
            # end of info block for game
            elif line.find("$end") == 0:  # goes by position if found
                add_to_desc = False
                for game in game_titles:
                    print(('game: %s' % game))
                    game_data = db_connection.db_meta_game_by_name_and_system(game, system_name)[
                        0]
                    print(('data: %s', game_data))
                    if game_data is None:
                        db_connection.db_meta_game_insert(
                            db_connection.db_meta_games_system_guid_by_short_name(
                                system_name),
                            new_title, game, json.dumps({'overview': game_desc}))
                        total_software += 1
                    else:
                        game_data['gi_game_info_json']['overview'] = game_desc
                        print((game_data['gi_id']))
                        db_connection.db_meta_game_update_by_guid(game_data['gi_id'],
                                                                  json.dumps(game_data[
                                                                                 'gi_game_info_json']))
                        total_software_update += 1
                game_desc = ''
            # this line can be skipped and is basically the "start" of game info
            elif line.find("$bio") == 0:  # goes by position if found
                line = history_file.readline().decode("utf-8")  # skip blank line
                new_title = history_file.readline().decode(
                    "utf-8").strip()  # grab the "real" game name
                add_to_desc = True
            else:
                # should be a system/game
                system_name = line[1:].split('=', 1)[0]
                game_titles = line.split("=", 1)[1].split(",")
        else:
            if add_to_desc:
                game_desc += line
    history_file.close()
    if total_software > 0:
        db_connection.db_notification_insert(
            common_internationalization.com_inter_number_format(total_software)
            + " games(s) metadata added from MAME hash", True)
    if total_software_update > 0:
        db_connection.db_notification_insert(
            common_internationalization.com_inter_number_format(
                total_software_update)
            + " games(s) metadata updated from MAME hash", True)

# read the category file and create dict/list for it
cat_file = open("Category.ini", "rb")
cat_dictionary = {}
category = ""
while 1:
    line = cat_file.readline()
    if not line:
        break
    if line.find("[") == 0:
        category = line.replace("[", "").replace("]", "").replace(" ", "").rstrip('\n').rstrip(
            '\r')  # wipe out space to make the category table
    elif len(line) > 1:
        result_value = db_connection.db_meta_game_category_by_name(category)
        if result_value is None:
            result_value = db_connection.db_meta_game_category_add(category)
        cat_dictionary[line.strip()] = result_value

# grab all system null in db as those are mame
for sql_row in db_connection.db_media_mame_game_list():
    db_connection.db_media_game_category_update(cat_dictionary[sql_row['gi_short_name']],
                                                sql_row['gi_id'])

# grab all the non parent roms that aren't set
for sql_row in db_connection.db_media_game_clone_list():
    for sql_cat_row in db_connection.db_media_game_category_by_name(sql_row['gi_cloneof']):
        db_connection.db_media_game_category_update(sql_cat_row['gi_gc_category'], sql_row['gi_id'])

# commit all changes to db
db_connection.db_commit()

# close the database
db_connection.db_close()
