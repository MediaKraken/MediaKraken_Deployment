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
import pytest
import sys
sys.path.append("./common")
sys.path.append("./server") # for db import
import database as database_base


class TestDatabaseMedia(object):


    @classmethod
    def setup_class(self):
        self.db = database_base.MK_Server_Database()
        self.db.MK_Server_Database_Open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db.MK_Server_Database_Close()


    # insert media into database
    # def MK_Server_Database_Insert_Media(self, media_uuid, media_path, media_class_uuid, media_metadata_uuid, media_ffprobe_json, media_json):
#        self.db.MK_Server_Database_Rollback()


    # read in all media unless guid specified
    def Test_MK_Server_Database_Read_Media(self):
        self.db.MK_Server_Database_Read_Media()
        self.db.MK_Server_Database_Rollback()


    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found
    def Test_MK_Server_Database_Read_Media_Guid(self, media_guid):
        self.db.MK_Server_Database_Read_Media(media_guid)
        self.db.MK_Server_Database_Rollback()


    # count known media
    def Test_MK_Server_Database_Known_Media_Count(self):
        self.db.MK_Server_Database_Known_Media_Count()
        self.db.MK_Server_Database_Rollback()


    # find all known media
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_MK_Server_Database_Known_Media(self, offset, records):
        self.db.MK_Server_Database_Known_Media(offset, records)
        self.db.MK_Server_Database_Rollback()


    # count matched media
    def Test_MK_Server_Database_Matched_Media_Count(self):
        self.db.MK_Server_Database_Matched_Media_Count()
        self.db.MK_Server_Database_Rollback()


    # count all media that is NULL for meatadata match
    def Test_MK_Server_Database_Known_Media_All_Unmatched_Count(self):
        self.db.MK_Server_Database_Known_Media_All_Unmatched_Count()
        self.db.MK_Server_Database_Rollback()


    # read all media that is NULL for metadata match
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_MK_Server_Database_Known_Media_All_Unmatched(self, offset, records):
        self.db.MK_Server_Database_Known_Media_All_Unmatched(offset, records)
        self.db.MK_Server_Database_Rollback()


    # count the duplicates for pagination
    def Test_MK_Server_Database_Media_Duplicate_Count(self):
        self.db.MK_Server_Database_Media_Duplicate_Count()
        self.db.MK_Server_Database_Rollback()


    # list duplicates
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def Test_MK_Server_Database_Media_Duplicate(self, offset, records):
        self.db.MK_Server_Database_Media_Duplicate(offset, records)
        self.db.MK_Server_Database_Rollback()


    # duplicate detail count
    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found
    def Test_MK_Server_Database_Media_Duplicate_Detail_Count(self, media_guid):
        self.db.MK_Server_Database_Media_Duplicate_Detail_Count(media_guid)
        self.db.MK_Server_Database_Rollback()


    # list duplicate detail
    @pytest.mark.parametrize(("media_guid", "offset", "records"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', None, None),       # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 100, 100),         # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 100000000, 1000),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', None, None),       # not exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 100, 100),         # not exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 100000000, 1000)]) # not exists
    def Test_MK_Server_Database_Media_Duplicate_Detail(self, media_guid, offset, records):
        self.db.MK_Server_Database_Media_Duplicate_Detail(media_guid, offset, records)
        self.db.MK_Server_Database_Rollback()


    # find path for media by uuid
    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found
    def Test_MK_Server_Database_Media_Path_By_UUID(self, media_guid):
        self.db.MK_Server_Database_Media_Path_By_UUID(media_guid)
        self.db.MK_Server_Database_Rollback()


    # set watched/unwatched status for media
    @pytest.mark.parametrize(("media_guid", "user_id", "status_bool"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, False),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, False),  # not found
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, True),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, True)])  # not found
    def Test_MK_Server_Database_Media_Watched_Status_Update(self, media_guid, user_id, status_bool):
        self.db.MK_Server_Database_Media_Watched_Status_Update(media_guid, user_id, status_bool)
        self.db.MK_Server_Database_Rollback()


    # set favorite status for media
    @pytest.mark.parametrize(("media_guid", "user_id", "status_bool"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, False),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, False),  # not found
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, True),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, True)])  # not found    
    def Test_MK_Server_Database_Media_Favorite_Status_Update(self, media_guid, user_id, status_bool):
        self.db.MK_Server_Database_Media_Favorite_Status_Update(media_guid, user_id, status_bool)
        self.db.MK_Server_Database_Rollback()


    # set favorite status for media
    @pytest.mark.parametrize(("media_guid", "user_id", "status_bool"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, False),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, False),  # not found
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, True),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, True)])  # not found
    def Test_MK_Server_Database_Media_Poo_Status_Update(self, media_guid, user_id, status_bool):
        self.db.MK_Server_Database_Media_Poo_Status_Update(media_guid, user_id, status_bool)
        self.db.MK_Server_Database_Rollback()


    ## set favorite status for media
    @pytest.mark.parametrize(("media_guid", "user_id", "status_bool"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, False),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, False),  # not found
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, True),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, True)])  # not found
    def Test_MK_Server_Database_Media_Mismatch_Status_Update(self, media_guid, user_id, status_bool):
        self.db.MK_Server_Database_Media_Mismatch_Status_Update(media_guid, user_id, status_bool)
        self.db.MK_Server_Database_Rollback()


    # set checkpoint for media (so can pick up where left off per user)
    @pytest.mark.parametrize(("media_guid", "user_id", "ffmpeg_time"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, 100),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, 100),  # not found
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, 1000000000),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, 1000000000)])  # not found
    def Test_MK_Server_Database_Media_Watched_Checkpoint_Update(self, media_guid, user_id, ffmpeg_time):
        self.db.MK_Server_Database_Media_Watched_Checkpoint_Update(media_guid, user_id, ffmpeg_time)
        self.db.MK_Server_Database_Rollback()


    # update the mediaid
    # def MK_Server_Database_Update_Media_ID(self, media_guid, metadata_guid):
#        self.db.MK_Server_Database_Rollback()


    # update the mediajson
    # def MK_Server_Database_Update_Media_JSON(self, media_guid, mediajson):
#        self.db.MK_Server_Database_Rollback()


    # return all media which needs chapter images created
    def Test_MK_Server_Database_Known_Media_Chapter_Scan(self):
        self.db.MK_Server_Database_Known_Media_Chapter_Scan()
        self.db.MK_Server_Database_Rollback()


    # fetch all media with METADATA match
    @pytest.mark.parametrize(("metadata_guid"), [
        ('8d5ef41c-25b4-45e5-aada-b0ac9c7f6b4d'),  # exists
        ('8d5ef41c-25b4-45e5-aada-b0ac9c7f6b4e')])  # not found    
    def Test_MK_Server_Database_Media_By_Metadata_Guid(self, metadata_guid):
        self.db.MK_Server_Database_Media_By_Metadata_Guid(metadata_guid)
        self.db.MK_Server_Database_Rollback()


    # grab image path for media id NOT metadataid
    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found
    def Test_MK_Server_Database_Media_Image_Path(self, media_guid):
        self.db.MK_Server_Database_Media_Image_Path(media_guid)
        self.db.MK_Server_Database_Rollback()


    # read in metadata by id
    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found    
    def Test_MK_Server_Database_Read_Media_Metadata_Both(self, media_guid):
        self.db.MK_Server_Database_Read_Media_Metadata_Both(media_guid)
        self.db.MK_Server_Database_Rollback()


    # do a like class path match for trailers and extras
    # def MK_Server_Database_Read_Media_Path_Like(self, media_path):
#        self.db.MK_Server_Database_Rollback()


    # new media count
    @pytest.mark.parametrize(("new_days"), [
        (7),
        (400)])
    def Test_MK_Server_Database_Read_Media_New_Count(self, new_days):
        self.db.MK_Server_Database_Read_Media_New_Count(new_days)
        self.db.MK_Server_Database_Rollback()


    # new media
    @pytest.mark.parametrize(("new_days", "offset", "records"), [
        (7, None, None),
        (400, None, None),
        (400, 100, 100),
        (400, 10000000, 1000)])
    def Test_MK_Server_Database_Read_Media_New(self, new_days, offset, records):
        self.db.MK_Server_Database_Read_Media_New(new_days, offset, records)
        self.db.MK_Server_Database_Rollback()
