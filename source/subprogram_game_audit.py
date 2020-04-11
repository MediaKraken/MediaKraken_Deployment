"""
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
"""

import copy
import hashlib
import multiprocessing
import os
import sys
import threading
import time
import zipfile
from threading import Thread

SHA1 = hashlib.sha1()
import os.path
from common import common_config_ini
from common import common_signal

lock = threading.Lock()

# store files, zippped and hash globally
files = {}
zippedFiles = {}
hashFileMap = {}

fileHASHList = []
fileHASHNameList = []
fileHASHListSingle = []
fileHASHNameListSingle = []


class HashGenerate(Thread):
    def __init__(self, file_name):
        Thread.__init__(self)
        self.file_name = file_name
        self.hash_result = None

    def get_generated_hash(self):
        return self.hash_result

    def run(self):
        if self.file_name[-3:] == 'zip':
            # Need to unpack the zip and check all files inside it
            try:
                lock.acquire()
                zip = zipfile.ZipFile(self.file_name, 'r')  # issues if u do RB
                hash_dict = {}
                for zippedFile in zip.namelist():
                    try:
                        # calculate sha1 hash
                        SHA1 = hashlib.sha1()  # "reset" the sha1 to blank
                        SHA1.update(zip.read(zippedFile))
                        sha1_hash_data = SHA1.hexdigest()
                        hash_dict[zippedFile] = sha1_hash_data
                    except:
                        lock.acquire()
                        Client_GlobalData.skipped_files.append(os.path.normpath(self.file_name)
                                                               + "|Error on SHA1 of file")
                        lock.release()
                zip.close()
                if len(hash_dict) > 0:
                    if len(hash_dict) == 1:
                        fileHASHListSingle.append(list(hash_dict.values())[0])
                        fileHASHNameListSingle.append(
                            os.path.normpath(self.file_name))
                    else:
                        fileHASHList.append(hash_dict)
                        fileHASHNameList.append(
                            os.path.normpath(self.file_name))
                lock.release()
            except:
                lock.acquire()
                Client_GlobalData.skipped_files.append(os.path.normpath(self.file_name)
                                                       + "|Error reading zip")
                lock.release()
        elif self.file_name[-2:] == '7z':
            # Need to unpack the 7z and check all files inside it
            try:
                lock.acquire()
                fp = open(self.file_name, 'rb')
                archive = Archive7z(fp)
                filenames = archive.getnames()
                hash_dict = {}
                for filename in filenames:
                    cf = archive.getmember(filename)
                    try:
                        # calculate sha1 hash
                        SHA1 = hashlib.sha1()  # "reset" the sha1 to blank
                        SHA1.update(cf.read())
                        sha1_hash_data = SHA1.hexdigest()
                        hash_dict[filename] = sha1_hash_data
                        # self.hash_result = self.file_name,fileHash,sha1_hash_data
                    except:
                        lock.acquire()
                        Client_GlobalData.skipped_files.append(os.path.normpath(self.file_name)
                                                               + "|Error on SHA1 of file")
                        lock.release()
                if len(hash_dict) > 0:
                    if len(hash_dict) == 1:
                        fileHASHListSingle.append(list(hash_dict.values())[0])
                        fileHASHNameListSingle.append(
                            os.path.normpath(self.file_name))
                    else:
                        fileHASHList.append(hash_dict)
                        fileHASHNameList.append(
                            os.path.normpath(self.file_name))
                fp.close()
                lock.release()
            except:
                lock.acquire()
                Client_GlobalData.skipped_files.append(os.path.normpath(self.file_name)
                                                       + "|Error reading 7z")
                lock.release()
        else:
            try:
                lock.acquire()
                file_pointer = open(self.file_name, 'rb')
                # calculate sha1 hash
                file_pointer.seek(0, 0)
                hash_dict = {}
                try:
                    SHA1 = hashlib.sha1()  # "reset" the sha1 to blank
                    for chunk in iter(lambda: file_pointer.read(128 * SHA1.block_size), ''):
                        SHA1.update(chunk)
                    sha1_hash_data = SHA1.hexdigest()
                    hash_dict[os.path.basename(
                        self.file_name)] = sha1_hash_data
                    print(("single: %s", self.file_name, sha1_hash_data), flush=True)
                except:
                    lock.acquire()
                    Client_GlobalData.skipped_files.append(os.path.normpath(self.file_name)
                                                           + "|Error on SHA1 of file")
                    lock.release()
                if len(hash_dict) > 0:
                    fileHASHListSingle.append(list(hash_dict.values())[0])
                    fileHASHNameListSingle.append(
                        os.path.normpath(self.file_name))
                file_pointer.close()
                lock.release()
            except:
                lock.acquire()
                Client_GlobalData.skipped_files.append(os.path.normpath(self.file_name)
                                                       + "|Error reading file")
                lock.release()


class HashScanner:
    def __init__(self):
        self.percentComplete = 0

    def calc_hash(self, audit_q, files):
        for file in files:
            thread = HashGenerate(file)
            thread.start()
            audit_q.put(thread, True)

    def get_hash_result(self, audit_q, total_files):
        onFile = 0
        lastPercent = 0
        Client_GlobalData.audit_on_file = 0
        self.percentComplete = 0
        while Client_GlobalData.audit_on_file < total_files:
            thread = audit_q.get(True)
            thread.join()
            # update percentage
            onFile += 1
            if onFile * 100 / total_files != lastPercent:
                lastPercent = onFile * 100 / total_files
                self.percentComplete = lastPercent
            Client_GlobalData.audit_on_file += 1

    def scan(self, paths):
        # find/count files to scan
        Client_GlobalData.skipped_files = []
        files_to_hash = []
        Client_GlobalData.audit_files_to_audit = 0
        for path in paths:
            try:
                for file_name in os.listdir(path):
                    if not os.path.isfile(os.path.join(path, file_name)):
                        continue
                    Client_GlobalData.audit_files_to_audit += 1
                    # not using join as it does the \\ in windows on the join between path and file
                    files_to_hash.append(
                        os.path.normpath(path + "/" + file_name))
            except:
                pass
        # calculate crc32 and sha1 on all files selected
        files = {}
        zippedFiles = {}
        hashFileMap = {}
        # Client_GlobalData.audit_files_to_audit = len(files_to_hash)
        # start the audit threads
        audit_q = Queue(multiprocessing.cpu_count() * 1)
        prod_thread = threading.Thread(
            target=self.calc_hash, args=(audit_q, files_to_hash))
        cons_thread = threading.Thread(target=self.get_hash_result,
                                       args=(audit_q, len(files_to_hash)))
        prod_thread.start()
        cons_thread.start()
        prod_thread.join()
        cons_thread.join()
        # verify all thread/ques are complete
        while not audit_q.empty():
            time.sleep(0.05)


class ROMFileParser:
    def __init__(self, files, zippedFiles, hashFileMap):
        self.files = files
        self.zippedFiles = zippedFiles
        self.hashFileMap = hashFileMap
        self.game_rom_id = []
        Client_GlobalData.matching_files_to_audit = len(
            fileHASHList) + len(fileHASHListSingle)
        # load the audit data from db
        db_full_hash_dict = []
        temp_dict = {}
        old_gir_gi_id = None
        conn_player = connect('db/hubcade_gui.db')
        curs_player = conn_player.cursor()
        conn_game = connect('db/game_database.db')
        curs_game = conn_game.cursor()
        conn_game.text_factory = lambda x: str(x, "utf-8", "ignore")
        # parse for multi roms archives and files
        curs_game.execute('select gir_gi_id,gir_rom_name,gir_sha1,gir_merged_rom_name from'
                          ' game_info,game_info_roms where gi_id = gir_gi_id and gi_id'
                          ' IN (select gir_gi_id from game_info_roms group by gir_gi_id having count(*) > 1)')
        first_rec = True
        for sql_row in curs_game:
            if first_rec:
                old_gir_gi_id = sql_row[0]
                first_rec = False
            if old_gir_gi_id != sql_row[0]:
                temp_dat = old_gir_gi_id, temp_dict
                db_full_hash_dict.append(temp_dat)
                temp_dict = {}
                old_gir_gi_id = sql_row[0]
            # don't put the rom file in the list if it's a merged one
            if len(sql_row[3]) < 2:
                temp_dict[sql_row[1]] = sql_row[2]
        # catch last data from db
        if old_gir_gi_id is None:
            temp_dat = old_gir_gi_id, temp_dict
            db_full_hash_dict.append(temp_dat)
        # loop through the rom hashs and do lookup against the db dict
        Client_GlobalData.found_rom_ids = []
        Client_GlobalData.found_rom_paths = []
        item_ndx = 0
        for rom_hash_data in fileHASHList:
            Client_GlobalData.matching_on_file += 1
            # below print is correct as it shows the crc32 and the filename
            rom_hash_length = len(rom_hash_data)
            for db_hash_dict in db_full_hash_dict:
                # in theory all crc32 and sha1 should match here for mame roms
                if rom_hash_length == len(db_hash_dict[1]) \
                        and cmp(rom_hash_data, db_hash_dict[1]) == 0:
                    Client_GlobalData.found_rom_ids.append(db_hash_dict[0])
                    Client_GlobalData.found_rom_paths.append(
                        fileHASHNameList[item_ndx])
                    db_full_hash_dict.remove(db_hash_dict)
                    break
            item_ndx += 1
        # do parse for single rom archives and files
        db_full_hash_dict = []
        temp_list = []
        curs_game.execute('select gir_gi_id,gir_sha1 from game_info,game_info_roms'
                          ' where gi_id = gir_gi_id and gi_id IN (select gir_gi_id from game_info_roms'
                          ' group by gir_gi_id having count(*) = 1)')
        for sql_row in curs_game:
            temp_list.append(sql_row[0])
            temp_list.append(sql_row[1])
            # temp_list.append(sql_row[2])
            db_full_hash_dict.append(temp_list)
            temp_list = []
        item_ndx = 0
        for rom_hash_data in fileHASHListSingle:
            Client_GlobalData.matching_on_file += 1
            for db_hash_dict in db_full_hash_dict:
                # check sha1 value
                if rom_hash_data == db_hash_dict[1]:
                    Client_GlobalData.found_rom_ids.append(db_hash_dict[0])
                    Client_GlobalData.found_rom_paths.append(
                        fileHASHNameListSingle[item_ndx])
                    # if sha1 there is almost no chance of dupe
                    # so remove hash to speed up rest of checks
                    db_full_hash_dict.remove(db_hash_dict)
                    break
            item_ndx += 1
        curs_player.close()
        conn_player.close()
        curs_game.close()
        conn_game.close()

    def rom_diff(self, first, second):
        # Check all keys in first dict
        for key in list(first.keys()):
            if key not in second:
                return False
            elif first[key] != second[key]:
                return False
        # Check all keys in second dict to find missing
        for key in list(second.keys()):
            if key not in first:
                return False
        return True


class GameAuditer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.baseDirectories = ''
        self.hashScanner = None

    def run(self):
        self.game_audit()
        self.load_hash_map_from_database()

    def game_audit(self):
        self.hashScanner = HashScanner()
        self.hashScanner.scan(self.baseDirectories)
        fileHASHList = []
        fileHASHNameList = []
        fileHASHListSingle = []
        fileHASHNameListSingle = []
        Client_GlobalData.audit_files_to_audit = 0
        Client_GlobalData.audit_on_file = 0
        Client_GlobalData.matching_files_to_audit = 0
        Client_GlobalData.matching_on_file = 0
        Client_GlobalData.skipped_files = []
        romParser = ROMFileParser(files, zippedFiles, hashFileMap)

    def load_hash_map_from_database(self):
        if '-nolist' in sys.argv:
            return True
        common_global.es_inst.com_elastic_index('info', {'stuff': "loading roms from db"})
        # open the database
        option_config_json, db_connection = common_config_ini.com_config_read()
        # read all the audited games
        conn_game = connect('db/game_database.db')
        curs_game = conn_game.cursor()
        conn_game.text_factory = lambda x: str(x, "utf-8", "ignore")
        curs_game.execute("attach database 'db/hubcade_gui.db' as gui_db")
        curs_game.execute('select gs_system_long_name,gi_short_name,gi_long_name,gi_id,'
                          '(select gm_rotate from game_monitor where gm_id = gi_monitor_id),gi_players,'
                          'gc_category from game_info,gui_db.game_audit,game_systems,game_category'
                          ' where gi_id = gui_db.game_audit.ga_game_id and gs_id = gi_system_id'
                          ' and gi_gc_category = gc_id union all select \'Arcade\',gi_short_name,gi_long_name,'
                          'gi_id,(select gm_rotate from game_monitor where gm_id = gi_monitor_id),gi_players,'
                          'gc_category from game_info,gui_db.game_audit,game_category where gi_system_id = 0'
                          ' and gi_id = gui_db.game_audit.ga_game_id and gi_gc_category = gc_id')
        # for the times/time played
        conn_game_info = connect('db/hubcade_gui.db')
        curs_game_info = conn_game_info.cursor()
        conn_game_info.text_factory = lambda x: str(x, "utf-8", "ignore")
        # begin parse of data
        Client_GlobalData.audited_games = 0
        Client_GlobalData.audit_gameList = {}
        old_system_long_name = None
        first_record = True
        game_info = {}
        for sql_row in curs_game:
            Client_GlobalData.audited_games += 1
            game_times_played = 0
            game_time_played = 0
            game_monitor = "NA"
            game_players = 0
            game_category = "NA"
            sql_args = str(sql_row[3]),
            curs_game_info.execute('select game_times_played,game_time_played from game_info'
                                   ' where game_rom_id = ?', sql_args)
            row = curs_game_info.fetchone()
            if row is None:
                pass
            else:
                game_times_played = row[0]
                game_time_played = row[1]
            if sql_row[4] is not None:
                if int(sql_row[4]) == 0 or int(sql_row[4]) == 180:
                    game_monitor = "Horizontal"
                else:
                    game_monitor = "Vertical"
            if sql_row[5] is not None:
                game_players = sql_row[5]
            if sql_row[6] is not None:
                game_category = sql_row[6]
            if first_record:
                old_system_long_name = sql_row[0]
                first_record = False
            game_name = sql_row[1]
            if sql_row[2] is not None:
                game_name = sql_row[2]
            if old_system_long_name != sql_row[0]:
                if len(game_info) > 0:
                    Client_GlobalData.audit_gameList[old_system_long_name] \
                        = copy.deepcopy(list(game_info.items()))
                    Client_GlobalData.audit_gameList[old_system_long_name].sort(
                    )
                old_system_long_name = sql_row[0]
                game_info = {}
            game_info[game_name] = game_times_played, game_time_played, game_monitor, \
                                   game_players, str(sql_row[3]), game_category
        # catch last data from db
        if old_system_long_name is not None and len(game_info) > 0:
            Client_GlobalData.audit_gameList[old_system_long_name] \
                = copy.deepcopy(list(game_info.items()))
            Client_GlobalData.audit_gameList[old_system_long_name].sort()
        curs_game_info.close()
        conn_game_info.close()
        curs_game.close()
        conn_game.close()
        # close the database
        db_connection.db_close()
        return True

    def getnamesdictdb(self, subString):
        if len(subString) == 0:
            # no need to do scan if filter is blank
            return Client_GlobalData.audit_gameList
        subString = subString.lower()
        game_info = {}
        gameList = {}
        old_system_long_name = None
        first_record = True
        for gameSystem in list(Client_GlobalData.audit_gameList.items()):
            # need to break down gameSystem as technically it's
            # all the systems and data underneath it
            for gameData in gameSystem[1]:
                if (Client_GlobalData.app.mainFrame.monitor_type_combo.GetValue() == "Horizontal"
                    and gameData[1][2] != "Horizontal") \
                        or (
                        Client_GlobalData.app.mainFrame.monitor_type_combo.GetValue() == "Vertical"
                        and gameData[1][2] != "Vertical") \
                        or (int(gameData[1][
                                    3]) < Client_GlobalData.app.mainFrame.filter_player_count_spinner.GetValue()) or (
                        Client_GlobalData.app.mainFrame.filterjoincategorychoice.GetStringSelection() != "All" and Client_GlobalData.app.mainFrame.filterjoincategorychoice.GetStringSelection() !=
                        gameData[1][5]):
                    pass
                else:
                    if first_record:
                        old_system_long_name = gameSystem[0]
                        first_record = False
                    if subString in gameData[0].lower():
                        if gameSystem[0] not in gameList:
                            gameList[gameSystem[0]] = []
                        game_info[gameData[0]] = gameData[1][0], gameData[1][1], \
                                                 gameData[1][2], gameData[1][3], gameData[1][4], \
                                                 gameData[1][5]
                    if old_system_long_name != gameSystem[0]:
                        if len(game_info) > 0:
                            gameList[old_system_long_name] = copy.deepcopy(
                                list(game_info.items()))
                            gameList[old_system_long_name].sort()
                        old_system_long_name = gameSystem[0]
                        game_info = {}
        # catch last data from db
        if old_system_long_name is not None and len(game_info) > 0:
            gameList[old_system_long_name] = copy.deepcopy(list(game_info.items()))
            gameList[old_system_long_name].sort()
        return gameList


if __name__ == '__main__':
    # set signal exit breaks
    common_signal.com_signal_set_break()
    gameAuditer = GameAuditer()
    gameAuditer.baseDirectories = ['../roms']
    gameAuditer.audit()
