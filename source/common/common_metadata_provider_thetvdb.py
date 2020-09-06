"""
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
"""

import io
import zipfile

import requests
import xmltodict

from . import common_global
from . import common_network

'''
http://www.thetvdb.com/wiki/index.php/Programmers_API
'''


class CommonMetadataTheTVDB:
    """
    Class for interfacing with TheTVDB
    """

    def __init__(self, option_config_json):
        self.thetvdb_connection = option_config_json['API']['thetvdb']

    def com_meta_thetvdb_updates(self, frequency='day'):
        """
        # http://www.thetvdb.com/wiki/index.php/API:Update_Records
        # frequency = all, day, month, week
        """
        updates_xml_zip = zipfile.ZipFile(io.StringIO(common_network
            .mk_network_fetch_from_url(
            'http://thetvdb.com/api/' + self.thetvdb_connection
            + '/updates/updates_' + frequency + '.zip', None)))
        # for the data
        xml_show_data = None
        for zippedshowFile in updates_xml_zip.namelist():
            xml_show_data = xmltodict.parse(
                updates_xml_zip.read(zippedshowFile))
        return xml_show_data

    def com_meta_thetvdb_get_zip_by_id(self, tv_show_id, lang_code='en'):
        """
        Fetch zip by id
        """
        xml_show_data = None
        xml_actor_data = None
        xml_banners_data = None
        common_global.es_inst.com_elastic_index('info', {"zip": self.thetvdb_connection,
                                                         'showid': tv_show_id, 'lang': lang_code})

        show_data = requests.get('http://thetvdb.com/api/' + self.thetvdb_connection
                                 + '/zip/' + lang_code + '/' + tv_show_id + '.zip', timeout=5)
        if show_data.status_code == 200:
            show_zip = zipfile.ZipFile(io.StringIO(show_data.content))
        else:
            return (None, None, None)
        #        try:
        #            # TODO catch errors
        #            show_zip = zipfile.ZipFile(StringIO.StringIO(common_network.\
        #                mk_network_fetch_from_url('http://thetvdb.com/api/' + self.thetvdb_connection\
        #                + '/zip/' + lang_code + '/' + tv_show_id + '.zip', None)))
        #        except:
        #            return (None, None, None)

        # for the individual show data
        for zippedshowFile in show_zip.namelist():
            if zippedshowFile == 'en.xml':
                xml_show_data = xmltodict.parse(show_zip.read(zippedshowFile))
                common_global.es_inst.com_elastic_index('info', {"xml show": xml_show_data})
            elif zippedshowFile == 'actors.xml':
                xml_actor_data = xmltodict.parse(show_zip.read(zippedshowFile))
                common_global.es_inst.com_elastic_index('info', {"xml actor": xml_actor_data})
            elif zippedshowFile == 'banners.xml':
                xml_banners_data = xmltodict.parse(
                    show_zip.read(zippedshowFile))
                common_global.es_inst.com_elastic_index('info', {"xml banner": xml_banners_data})
        return (xml_show_data, xml_actor_data['Actors'], xml_banners_data['Banners'])

    #    # depreciated....they round-robin at their end
    #    def com_meta_TheTVDB_Get_Mirrors():
    #        mirror_list_xml = common_network.mk_network_fetch_from_url('http://thetvdb.com/api/'
    # + self.thetvdb_connection + '/mirrors.xml', None)
    #        return mirror_list_xml

    def com_meta_thetvdb_get_server_epoc_time(self):
        """
        Get epoc time from api server
        """
        return common_network.mk_network_fetch_from_url(
            'http://thetvdb.com/api/Updates.php?type=none', None)

    def com_meta_thetvdb_updates_by_epoc(self, epoc_timestamp):
        """
        Get updates by epoc
        """
        return common_network.mk_network_fetch_from_url(
            'http://thetvdb.com/api/Updates.php?type=all&time=' + str(epoc_timestamp), None)

    def com_meta_thetvdb_update_series_read(self, tv_show_id, lang_code='en'):
        """
        Update series
        """
        return common_network.mk_network_fetch_from_url('http://thetvdb.com/api/'
                                                        + self.thetvdb_connection
                                                        + '/series/' + tv_show_id
                                                        + '/' + lang_code + '.xml',
                                                        None)

    def com_meta_thetvdb_update_episode_read(self, tv_eps_id, lang_code='en'):
        """
        Update episode
        """
        return common_network.mk_network_fetch_from_url('http://thetvdb.com/api/'
                                                        + self.thetvdb_connection
                                                        + '/episodes/' + tv_eps_id
                                                        + '/' + lang_code + '.xml',
                                                        None)


'''
xmltodict.parse(xml, False)
Record <previoustime> for next update
a. Using the XML from com_meta_TheTVDB_Updates_by_Epoc, store <Time>
 as <previoustime> and use for your next call to Updates.php
'''
