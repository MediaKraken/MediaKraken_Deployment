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
from common import common_hardware_roku
from common import common_logging
from common import common_signal


# set signal exit breaks
common_signal.com_signal_set_break()


# start logging
common_logging.com_logging_start('./log/MediaKraken_Subprogram_Roku_Thumbnail')


# open the database
option_config_json, db_connection = common_config_ini.com_config_read()


# log start
db_connection.db_activity_insert('MediaKraken_Server Roku Thumbnail Generate Start', None,
    'System: Server Roku Thumbnail Generate Start', 'ServerRokuThumbStart', None, None, 'System')

# go through ALL known media files
thumbnails_generated = 0
for row_data in db_connection.db_known_media():

#TODO  actually, this should probably be the metadata
# TODO the common roku code has the bif/thumb gen

    logging.info(row_data)


# send notications
if thumbnails_generated > 0:
    db_connection.db_notification_insert(
        common_internationalization.com_inter_number_format(thumbnails_generated)\
        + " Roku thumbnail(s) generated.", True)


# log end
db_connection.db_activity_insert('MediaKraken_Server Roku Thumbnail Generate Stop', None,
    'System: Server Roku Thumbnail Generate Stop', 'ServerRokuThumbStop', None, None, 'System')


# commit all changes
db_connection.db_commit()


# close DB
db_connection.db_close()
