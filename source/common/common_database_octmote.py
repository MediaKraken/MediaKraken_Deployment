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

import json
import os
import sqlite3
import uuid

from . import common_network_irdb


class CommonDatabaseOctmote:
    """
    Class for interfacing with database of Octmote
    """

    def __init__(self):
        self.sql3_conn = None
        self.db_cursor = None

    def com_db_open(self, db_file=None):
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
        self.db_cursor = self.sql3_conn.cursor()
        self.sql3_conn.text_factory = lambda x: str(x, "utf-8", "ignore")
        if create_db:
            # create the tables since they don't exist
            self.db_cursor.execute('CREATE TABLE octmote_server_settings (server_host text,'
                                   ' server_port integer)')
            self.db_cursor.execute('insert into octmote_server_settings (server_host,'
                                   ' server_port) values (\'localhost\',8097)')
            self.db_cursor.execute('CREATE TABLE octmote_anidb (anidb_aid numeric,'
                                   ' anidb_type numeric, anidb_language text, anidb_title text)')
            self.db_cursor.execute('CREATE TABLE octmote_layout (layout_guid text,'
                                   ' layout_name text, layout_json text)')
            self.db_cursor.execute('CREATE TABLE octmote_macro (macro_guid text,'
                                   ' macro_name text, macro_json text)')
            self.db_cursor.execute('CREATE TABLE octmote_item (item_guid text,'
                                   ' item_type text, item_manufacturer text, item_model_number text,'
                                   ' item_json text)')
            # grab brands and insert them into database
            self.db_cursor.execute('CREATE TABLE octmote_brand (brand_guid text,'
                                   ' brand_name text)')
            json_brand = common_network_irdb.com_irdb_brand_list()["objects"]
            for brand_name in json_brand:
                self.db_cursor.execute('insert into octmote_brand (brand_guid, brand_name)'
                                       ' values (?,?)', (str(uuid.uuid4()), brand_name["brand"]))
            # create device db and load with types
            self.db_cursor.execute('CREATE TABLE octmote_device (device_guid text,'
                                   ' device_name text, device_description text)')
            # TODO use the DEVICE_ITEM_TYPES from common_device_commands_base.py
            # add base devices to database
            self.db_cursor.execute('insert into octmote_device'
                                   ' (device_guid, device_name, device_description)'
                                   ' values (?,\'BluRay\', \'BluRay Player\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device'
                                   ' (device_guid, device_name, device_description)'
                                   ' values (?,\'DVD\', \'DVD Player\')', (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Laserdisc\','
                                   ' \'Laser Disc Player\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'VHS\', \'VHS VCR\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Beta\', \'Beta VCR\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'TV\', \'Television\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Projector\', \'DLP, LCD, LED Projector\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'CRT Projector\', \'CRT Analog Projector\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'3D BluRay\', \'3D Capable BluRay Player\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'3D Projector\', \'DLP, LCD, LED 3D Projector\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Phono\', \'Analog Phonograph Player\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'DAC\', \'Digital To Analog Converter\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Tape\', \'Tape Deck\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'CD\', \'Compact Disc Player\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'SACD\', \'Super Audio Compact Disc Player\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'SVHS\', \'Super VHS VCR\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'SBeta\', \'Super Beta VCR\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Receiver\', \'Audio/Video Receiver\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Amplifier\', \'Audio Amplifier\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Decoder\', \'Audio Decoder\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'DAT\', \'Digital Audio Tape\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Reel\', \'Reel To Reel Tape\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Cable\', \'Cable TV\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Satellite\', \'Satellite TV\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Net/USB\', \'Net/USB\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Vid Proc\', \'Video Processor\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Stream\', \'Audio/Video Streaming Device\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Game\', \'Game System\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'Preamp\', \'Audio/Video Preamplifier\')',
                                   (str(uuid.uuid4()),))
            self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                                   ' device_description) values (?,\'UPS\', \'Uninteruptable Power Supply\')',
                                   (str(uuid.uuid4()),))
            self.sql3_conn.commit()
        self.db_cursor.execute(
            'select server_host, server_port from octmote_server_settings')
        return self.db_cursor.fetchone()[0]

    def com_db_close(self):
        """
        Close sqlite3 database
        """
        self.sql3_conn.close()

    def com_db_layout_config_insert(self, layout_record_name, layout_record_json):
        """
        Insert new layout config into database
        """
        self.db_cursor.execute('insert into octmote_layout (layout_guid, layout_name,'
                               ' layout_json) values (?,?,?)', (uuid.uuid4(), layout_record_name,
                                                                layout_record_json))
        self.sql3_conn.commit()

    def com_db_layout_list(self):
        """
        Load list of layouts
        """
        self.db_cursor.execute('select layout_guid, layout_name from octmote_layout'
                               ' order by layout_name asc')
        return self.db_cursor

    def com_db_layout_detail(self, guid):
        """
        Layout detail
        """
        self.db_cursor.execute('select layout_json from octmote_layout where layout_guid = ?',
                               (guid,))
        return self.db_cursor

    def com_db_device_insert(self, device_record_name, device_record_description):
        """
        Insert new device type into database
        """
        self.db_cursor.execute('insert into octmote_device (device_guid, device_name,'
                               ' device_json) values (?,?,?)', (str(uuid.uuid4()),
                                                                device_record_name,
                                                                device_record_description))
        self.sql3_conn.commit()
        self.db_cursor.execute('select device_guid from octmote_device where rowid = ?',
                               (self.db_cursor.lastrowid,))
        return self.db_cursor

    def com_db_device_list(self):
        """
        list devices
        """
        self.db_cursor.execute('select device_guid, device_name from octmote_device'
                               ' order by device_name asc')
        return self.db_cursor

    def com_db_device_detail(self, guid):
        """
        device detail
        """
        self.db_cursor.execute('select device_description from octmote_device'
                               ' where device_guid = ?', (guid,))
        return self.db_cursor

    def com_db_item_insert(self, item_record_json):
        """
        Insert new item into database
        """
        json_data = json.loads(item_record_json)
        # find all the models and store a record for each
        for model_number in json_data["Model Support"]:
            self.db_cursor.execute('insert into octmote_item (item_guid, item_type,'
                                   ' item_manufacturer, item_model_number, item_json)'
                                   ' values (?,?,?,?,?)',
                                   (str(uuid.uuid4()), json_data["Item Type"],
                                    json_data["Manufacturer"],
                                    model_number, item_record_json))
        self.sql3_conn.commit()
        self.db_cursor.execute('select item_guid from octmote_item where rowid = ?',
                               (self.db_cursor.lastrowid,))
        return self.db_cursor

    def com_db_item_list(self):
        """
        item list
        """
        self.db_cursor.execute('select item_guid, item_type, item_manufacturer,'
                               ' item_model_number from octmote_item order by item_type,'
                               ' item_manufacturer, item_model_number asc')
        return self.db_cursor

    def com_db_item_detail(self, guid):
        """
        item detail
        """
        self.db_cursor.execute(
            'select item_type from octmote_item where item_guid = ?', (guid,))
        return self.db_cursor

    def com_db_general_query(self, sql_command):
        """
        Do general query
        """
        self.db_cursor.execute(sql_command)
        return self.db_cursor.fetchall()

    def com_db_general_insert(self, sql_command):
        """
        Do general insert
        """
        self.db_cursor.execute(sql_command)
        self.sql3_conn.commit()
