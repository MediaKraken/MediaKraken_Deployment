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

from common import common_config_ini
from common import common_global
from common import common_logging_elasticsearch
from common import common_metadata_scudlee
from common import common_signal

# start logging
common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch('subprogram_anime_scudlee')

# set signal exit breaks
common_signal.com_signal_set_break()

# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


# same code in subprograb update create collections
def store_update_record(db_connection, collection_name, guid_list):
    """
    # store/update the record
    """
    collection_guid = db_connection.db_collection_by_name(collection_name)
    if collection_guid is None:
        # insert
        db_connection.db_collection_insert(collection_name, guid_list)
    else:
        # update
        db_connection.db_collection_update(collection_guid, guid_list)


# check for new scudlee download
common_metadata_scudlee.mk_scudlee_fetch_xml()
# begin the media match on NULL matches
for row_data in common_metadata_scudlee.mk_scudlee_anime_list_parse():
    common_global.es_inst.com_elastic_index('info', {'row': 'row_data'})
    if row_data is not None:
        # skip media with "no" match...rowdata2 is imdbid
        # just check for non int then it's a non tvdb id
        if type(row_data[1]) != int and row_data[2] is None:
            pass
        else:
            # should be valid data, do the update
            db_connection.db_meta_update_media_id_from_scudlee(row_data[1],
                                                               row_data[2], row_data[0])

# begin the collections match/create/update
for row_data in common_metadata_scudlee.mk_scudlee_anime_set_parse():
    # db_connection.db_meta_update_Collection_Media_ID_From_Scudlee(row_data[0],row_data[1])
    if row_data[1] == "music video":
        pass
    else:
        store_update_record(db_connection, row_data[0], row_data[1])

# commit all changes to db
db_connection.db_commit()

# close the database
db_connection.db_close()
