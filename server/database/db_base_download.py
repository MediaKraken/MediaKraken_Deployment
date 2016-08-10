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

import uuid
import logging


# create/insert a download
def MK_Server_Database_Download_Insert(self, provider, down_json):
    self.sql3_cursor.execute(u'insert into mm_download_que (mdq_id,mdq_provider,mdq_download_json) values (%s,%s,%s)', (str(uuid.uuid4()), provider, down_json))
    self.MK_Server_Database_Commit()


## read the download
#def MK_Server_Database_Download_Read(self):
#    self.sql3_cursor.execute(u'select mdq_id,mdq_provider,mdq_download_json from mm_download_que')
#    return self.sql3_cursor.fetchall()


# read the downloads by provider
def MK_Server_Database_Download_Read_By_Provider(self, provider_name):
    self.sql3_cursor.execute(u'select mdq_id,mdq_download_json from mm_download_que where mdq_provider = %s', (provider_name,))
    return self.sql3_cursor.fetchall()


# remove download
def MK_Server_Database_Download_Delete(self, guid):
    self.sql3_cursor.execute(u'delete from mm_download_que where mdq_id = %s', (guid,))
    self.MK_Server_Database_Commit()


# update provdier
def MK_Server_Database_Download_Update_Provider(self, provider_name, guid):
    logging.debug('download update provider: %s %s', provider_name, guid)
    self.sql3_cursor.execute(u'update mm_download_que set mdq_provider = %s where mdq_id = %s', (provider_name, guid))
    self.MK_Server_Database_Commit()


def MK_Server_Database_Download_Update(self, update_json, guid):
    logging.debug('download update: %s %s', update_json, guid)
    self.sql3_cursor.execute(u'update mm_download_que set mdq_download_json = %s where mdq_id = %s', (update_json, guid))
    self.MK_Server_Database_Commit()
