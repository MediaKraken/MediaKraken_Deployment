'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street,
  Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

import xmltodict

from common import common_config_ini
from common import common_global
from common import common_internationalization
from common import common_logging_elasticsearch
from common import common_network

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
    'subprogram_trailer_download')

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()

total_trailers_downloaded = 0

data = xmltodict.parse(common_network.mk_network_fetch_from_url(
    "http://feeds.hd-trailers.net/hd-trailers", None))
if data is not None:
    for item in data['item']:
        common_global.es_inst.com_elastic_index('info', {'item': item})
        download_link = None
        if ('(Trailer' in data['item']['title']
            and option_config_json['Trailer']['Trailer'] is True) \
                or ('(Behind' in data['item']['title']
                    and option_config_json['Trailer']['Behind'] is True) \
                or ('(Clip' in data['item']['title']
                    and option_config_json['Trailer']['Clip'] is True) \
                or ('(Featurette' in data['item']['title']
                    and option_config_json['Trailer']['Featurette'] is True) \
                or ('(Carpool' in data['item']['title']
                    and option_config_json['Trailer']['Carpool'] is True):
            for trailer_url in data['item']['enclosure url']:
                if '1080p' in trailer_url:
                    download_link = data['item']['enclosure url']
                    break
        if download_link is not None:
            # TODO let the metadata fetch program grab these
            # TODO verify this trailer has not been downloaded before
            # TODO so only insert db dl records
            common_network.mk_network_fetch_from_url(
                download_link, '/static/meta/trailer')

if total_trailers_downloaded > 0:
    db_connection.db_notification_insert(
        common_internationalization.com_inter_number_format(
            total_trailers_downloaded)
        + " trailers(s) flagged for download.", True)

# commit all changes to db
db_connection.db_commit()

# close the database
db_connection.db_close()
