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
import logging
import sqlite3
import uuid
import os
import json
import common.common_network_IRDB


class CommonDatabaseOctmote(object):
    """
    Class for interfacing with database of Octmote
    """
    def __init__(self):
        pass


    def MK_Database_Sqlite3_Open(self, db_file = None):
        """
        Open database and pull in config from sqlite and create db if not exist
        """
        create_db = False
        if db_file is None:
            if not os.path.isfile("OctMote.db"):
                create_db = True
            self.sql3_conn = sqlite3.connect("OctMote.db")
        else:
            self.sql3_conn = sqlite3.connect(db_file)
        self.sql3_cursor = sql3_conn.cursor()
        self.sql3_conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
        if create_db:
            # create the tables since they don't exist
            self.sql3_cursor.execute("CREATE TABLE octmote_server_settings (server_host text, server_port integer)")
            self.sql3_cursor.execute("insert into octmote_server_settings (server_host, server_port) values ('localhost',8097)")
            self.sql3_cursor.execute("CREATE TABLE octmote_anidb (anidb_aid numeric, anidb_type numeric, anidb_language text, anidb_title text)")
            self.sql3_cursor.execute("CREATE TABLE octmote_layout (layout_guid text, layout_name text, layout_json text)")
            self.sql3_cursor.execute("CREATE TABLE octmote_macro (macro_guid text, macro_name text, macro_json text)")
            self.sql3_cursor.execute("CREATE TABLE octmote_item (item_guid text, item_type text, item_manufacturer text, item_model_number text, item_json text)")
            # grab brands and insert them into database
            self.sql3_cursor.execute("CREATE TABLE octmote_brand (brand_guid text, brand_name text)")
            json_brand = com_network_IRDB.com_IRDB_Brand_List()["objects"]
            for brand_name in json_brand:
                self.sql3_cursor.execute("insert into octmote_brand (brand_guid, brand_name) values (?,?)", (str(uuid.uuid4()), brand_name["brand"]))
            # create device db and load with types
            self.sql3_cursor.execute("CREATE TABLE octmote_device (device_guid text, device_name text, device_description text)")
            # add base devices to database
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'BluRay', 'BluRay Player')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'DVD', 'DVD Player')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Laserdisc', 'Laser Disc Player')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'VHS', 'VHS VCR')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Beta', 'Beta VCR')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'TV', 'Television')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Projector', 'DLP, LCD, LED Projector')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'CRT Projector', 'CRT Analog Projector')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'3D BluRay', '3D Capable BluRay Player')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'3D Projector', 'DLP, LCD, LED 3D Projector')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Phono', 'Analog Phonograph Player')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'DAC', 'Digital To Analog Converter')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Tape', 'Tape Deck')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'CD', 'Compact Disc Player')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'SACD', 'Super Audio Compact Disc Player')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'SVHS', 'Super VHS VCR')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'SBeta', 'Super Beta VCR')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Receiver', 'Audio/Video Receiver')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Amplifier', 'Audio Amplifier')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Decoder', '\"Description\":\"Audio Decoder\"')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'DAT', 'Digital Audio Tape')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Reel', 'Reel To Reel Tape')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Cable', 'Cable TV')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Satellite ', 'Satellite  TV')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Net/USB', 'Net/USB')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Vid Proc', 'Video Processor')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Stream', 'Audio/Video Streaming Device')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Game', 'Game System')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'Preamp', 'Audio/Video Preamplifier')", (str(uuid.uuid4()),))
            self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_description) values (?,'UPS', 'Uninteruptable Power Supply')", (str(uuid.uuid4()),))
            self.sql3_conn.commit()
        self.sql3_cursor.execute("select server_host, server_port from octmote_server_settings")
        try:
            return self.sql3_cursor.fetchone()[0]
        except:
            return None


    def MK_Database_Sqlite3_Close():
        """
        Close sqlite3 database
        """
        self.sql3_conn.close()


    def MK_Database_Sqlite3_Layout_Config_Insert(self, layout_record_name, layout_record_json):
        """
        Insert new layout config into database
        """
        self.sql3_cursor.execute("insert into octmote_layout (layout_guid, layout_name, layout_json) values (?,?,?)", (uuid.uuid4(), layout_record_name, layout_record_json))
        self.sql3_conn.commit()


    def MK_Database_Sqlite3_Layout_List(self):
        self.sql3_cursor.execute("select layout_guid, layout_name from octmote_layout order by layout_name asc")
        return self.sql3_cursor


    def MK_Database_Sqlite3_Layout_Detail(self, guid):
        self.sql3_cursor.execute("select layout_json from octmote_layout where layout_guid = ?",\
            (guid,))
        return self.sql3_cursor


    def MK_Database_Sqlite3_Device_Insert(self, device_record_name, device_record_description):
        """
        Insert new device type into database
        """
        self.sql3_cursor.execute("insert into octmote_device (device_guid, device_name, device_json) values (?,?,?)", (str(uuid.uuid4()), device_record_name, device_record_description))
        self.sql3_conn.commit()
        self.sql3_cursor.execute("select device_guid from octmote_device where rowid = ?",\
            (self.sql3_cursor.lastrowid,))
        return self.sql3_cursor


    def MK_Database_Sqlite3_Device_List(self):
        self.sql3_cursor.execute("select device_guid, device_name from octmote_device order by device_name asc")
        return self.sql3_cursor


    def MK_Database_Sqlite3_Device_Detail(self, guid):
        self.sql3_cursor.execute("select device_description from octmote_device where device_guid = ?", (guid,))
        return self.sql3_cursor


    def MK_Database_Sqlite3_Item_Insert(self, item_record_json):
        """
        Insert new item into database
        """
        json_data = json.loads(item_record_json)
        # find all the models and store a record for each
        for model_number in json_data["Model Support"]:
            self.sql3_cursor.execute("insert into octmote_item (item_guid, item_type, item_manufacturer, item_model_number, item_json) values (?,?,?,?,?)", (str(uuid.uuid4()), json_data["Item Type"], json_data["Manufacturer"], model_number, item_record_json))
        self.sql3_conn.commit()
        self.sql3_cursor.execute("select item_guid from octmote_item where rowid = ?",\
            (self.sql3_cursor.lastrowid,))
        return self.sql3_cursor


    def MK_Database_Sqlite3_Item_List(self):
        self.sql3_cursor.execute("select item_guid, item_type, item_manufacturer, item_model_number from octmote_item order by item_type, item_manufacturer, item_model_number asc")
        return self.sql3_cursor


    def MK_Database_Sqlite3_Item_Detail(self, guid):
        self.sql3_cursor.execute("select item_type from octmote_item where item_guid = ?", (guid,))
        return self.sql3_cursor


    def MK_Database_Sqlite3_General_Query(self, sql_command):
        """
        Do general query
        """
        self.sql3_cursor.execute(sql_command)
        return self.sql3_cursor.fetchall()


    def MK_Database_Sqlite3_General_Insert(self, sql_command):
        """
        Do general insert
        """
        self.sql3_cursor.execute(sql_command)
        self.sql3_conn.commit()


    def MK_Database_Sqlite3_anidb_Title_Insert(self, sql_params_list):
        """
        Insert new anidb entries into database
        """
        self.sql3_cursor.execute("delete from octmote_anidb")
        for sql_params in sql_params_list:
            self.sql3_cursor.execute("insert into octmote_anidb (anidb_aid, anidb_type, anidb_language, anidb_title) values (?,?,?,?)", sql_params)
        self.sql3_conn.commit()


    def MK_Database_Sqlite3_anidb_Title_Search(self, title_to_search):
        self.sql3_cursor.execute("select anidb_aid from octmote_anidb where anidb_title = ? limit 1", (title_to_search,))
        try:
            return self.sql3_cursor.fetchone()[0]
        except:
            return None
