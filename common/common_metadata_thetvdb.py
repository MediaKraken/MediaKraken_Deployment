'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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
import os
import xmltodict
import zipfile
#import zlib
import StringIO
from . import common_file
from . import common_metadata
from . import common_network

'''
http://www.thetvdb.com/wiki/index.php/Programmers_API
'''


class CommonMetadataTheTVDB(object):
    """
    Class for interfacing with TheTVDB
    """
    def __init__(self):
        # pull in the ini file config
        import ConfigParser
        Config = ConfigParser.ConfigParser()
        if os.path.isfile("MediaKraken.ini"):
            Config.read("MediaKraken.ini")
        else:
            Config.read("../../MediaKraken_Server/MediaKraken.ini")
        self.thetvdb_API_Key = Config.get('API', 'theTVdb').strip()


    def com_meta_TheTVDB_Updates(self, frequency='day'):
        # http://www.thetvdb.com/wiki/index.php/API:Update_Records
        # frequency = all, day, month, week
        updates_xml_zip = zipfile.ZipFile(StringIO.StringIO(common_network\
            .mk_network_fetch_from_url('http://thetvdb.com/api/' + self.thetvdb_API_Key\
            + '/updates/updates_' + frequency + '.zip', None)))
        # for the data
        for zippedshowFile in updates_xml_zip.namelist():
            xml_show_data = xmltodict.parse(updates_xml_zip.read(zippedshowFile))
        return xml_show_data


    def com_meta_TheTVDB_Get_ZIP_by_ID(self, tv_show_id, lang_code='en'):
        xml_show_data = None
        xml_actor_data = None
        xml_banners_data = None
        logging.debug("zip: %s %s %s", self.thetvdb_API_Key, tv_show_id, lang_code)
        try:
            # TODO catch errors
            show_zip = zipfile.ZipFile(StringIO.StringIO(common_network.\
                mk_network_fetch_from_url('http://thetvdb.com/api/' + self.thetvdb_API_Key\
                + '/zip/' + lang_code + '/' + tv_show_id + '.zip', None)))
        except:
            return (None, None, None)
        # for the individual show data
        for zippedshowFile in show_zip.namelist():
            if zippedshowFile == 'en.xml':
                xml_show_data = xmltodict.parse(show_zip.read(zippedshowFile))
                logging.debug("xml show: %s", xml_show_data)
            elif zippedshowFile == 'actors.xml':
                xml_actor_data = xmltodict.parse(show_zip.read(zippedshowFile))
                logging.debug("xml actor: %s", xml_actor_data)
            elif zippedshowFile == 'banners.xml':
                xml_banners_data = xmltodict.parse(show_zip.read(zippedshowFile))
                logging.debug("xml banner: %s", xml_banners_data)
        return (xml_show_data, xml_actor_data['Actors'], xml_banners_data['Banners'])


#    # depreciated....they round-robin at their end
#    def com_meta_TheTVDB_Get_Mirrors():
#        mirror_list_xml = common_network.mk_network_fetch_from_url('http://thetvdb.com/api/'\
# + self.thetvdb_API_Key + '/mirrors.xml', None)
#        return mirror_list_xml


    def com_meta_TheTVDB_Get_Server_Epoc_Time(self):
        return common_network.mk_network_fetch_from_url(\
            'http://thetvdb.com/api/Updates.php?type=none', None)

    #'''
    #Following is the future database processing section
    #'''

    def com_meta_TheTVDB_Updates_by_Epoc(self, epoc_timestamp):
        return common_network.mk_network_fetch_from_url(\
            'http://thetvdb.com/api/Updates.php?type=all&time=' + str(epoc_timestamp), None)


    def com_meta_TheTVDB_Update_Series_Read(self, tv_show_id, lang_code='en'):
        return common_network.mk_network_fetch_from_url('http://thetvdb.com/api/'\
            + self.thetvdb_API_Key + '/series/' + tv_show_id + '/' + lang_code + '.xml', None)


    def com_meta_TheTVDB_Update_Episode_Read(self, tv_eps_id, lang_code='en'):
        return common_network.mk_network_fetch_from_url('http://thetvdb.com/api/'\
            + self.thetvdb_API_Key + '/episodes/' + tv_eps_id + '/' + lang_code + '.xml', None)

'''
xmltodict.parse(xml, False)
Record <previoustime> for next update
a. Using the XML from com_meta_TheTVDB_Updates_by_Epoc, store <Time> as <previoustime> and use for your next call to Updates.php
'''
