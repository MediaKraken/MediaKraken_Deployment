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
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.srv_db_open('127.0.0.1', 5432, 'metamandb', 'metamanpg', 'metamanpg')


    @classmethod
    def teardown_class(self):
        self.db_connection.srv_db_close()


    # insert media into database
    # def srv_db_insert_media(self, media_uuid, media_path, media_class_uuid, media_metadata_uuid, media_ffprobe_json, media_json):
#        self.db_connection.srv_db_rollback()


    def test_srv_db_read_media(self):
        """
        # read in all media unless guid specified
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_read_media()


    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found
    def test_srv_db_read_media_guid(self, media_guid):
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_read_media(media_guid)


    def test_srv_db_known_media_count(self):
        """
        # count known media
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_known_media_count()


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_srv_db_known_media(self, offset, records):
        """
        # find all known media
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_known_media(offset, records)


    def test_srv_db_matched_media_count(self):
        """
        # count matched media
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_matched_media_count()


    def test_srv_db_known_media_all_unmatched_count(self):
        """
        # count all media that is NULL for meatadata match
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_known_media_all_unmatched_count()


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_srv_db_known_media_all_unmatched(self, offset, records):
        """
        # read all media that is NULL for metadata match
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_known_media_all_unmatched(offset, records)


    def test_srv_db_media_duplicate_count(self):
        """
        # count the duplicates for pagination
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_duplicate_count()


    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_srv_db_media_duplicate(self, offset, records):
        """
        # list duplicates
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_duplicate(offset, records)


    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found
    def test_srv_db_media_duplicate_detail_count(self, media_guid):
        """
        # duplicate detail count
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_duplicate_detail_count(media_guid)


    @pytest.mark.parametrize(("media_guid", "offset", "records"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', None, None),       # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 100, 100),         # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 100000000, 1000),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', None, None),       # not exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 100, 100),         # not exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 100000000, 1000)]) # not exists
    def test_srv_db_media_duplicate_detail(self, media_guid, offset, records):
        """
        # list duplicate detail
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_duplicate_detail(media_guid, offset, records)


    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found
    def test_srv_db_media_path_by_uuid(self, media_guid):
        """
        # find path for media by uuid
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_path_by_uuid(media_guid)


    @pytest.mark.parametrize(("media_guid", "user_id", "status_bool"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, False),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, False),  # not found
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, True),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, True)])  # not found
    def test_srv_db_media_watched_status_update(self, media_guid, user_id, status_bool):
        """
        # set watched/unwatched status for media
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_watched_status_update(media_guid, user_id, status_bool)


    @pytest.mark.parametrize(("media_guid", "user_id", "status_bool"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, False),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, False),  # not found
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, True),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, True)])  # not found    
    def test_srv_db_media_favorite_status_update(self, media_guid, user_id, status_bool):
        """
        # set favorite status for media
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_favorite_status_update(media_guid, user_id, status_bool)


    @pytest.mark.parametrize(("media_guid", "user_id", "status_bool"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, False),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, False),  # not found
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, True),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, True)])  # not found
    def test_srv_db_media_poo_status_update(self, media_guid, user_id, status_bool):
        """
        # set favorite status for media
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_poo_status_update(media_guid, user_id, status_bool)


    @pytest.mark.parametrize(("media_guid", "user_id", "status_bool"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, False),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, False),  # not found
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, True),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, True)])  # not found
    def test_srv_db_media_mismatch_status_update(self, media_guid, user_id, status_bool):
        """
        # set favorite status for media
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_mismatch_status_update(media_guid, user_id, status_bool)


    @pytest.mark.parametrize(("media_guid", "user_id", "ffmpeg_time"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, 100),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, 100),  # not found
        ('04442b10-3fb5-4d87-95a6-b50dbd072630', 1, 1000000000),   # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633', 1, 1000000000)])  # not found
    def test_srv_db_media_watched_checkpoint_update(self, media_guid, user_id, ffmpeg_time):
        """
        # set checkpoint for media (so can pick up where left off per user)
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_watched_checkpoint_update(media_guid, user_id, ffmpeg_time)


    # update the mediaid
    # def srv_db_update_media_id(self, media_guid, metadata_guid):
#        self.db_connection.srv_db_rollback()


    # update the mediajson
    # def srv_db_update_media_json(self, media_guid, mediajson):
#        self.db_connection.srv_db_rollback()


    def test_srv_db_known_media_chapter_scan(self):
        """
        # return all media which needs chapter images created
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_known_media_chapter_scan()


    @pytest.mark.parametrize(("metadata_guid"), [
        ('8d5ef41c-25b4-45e5-aada-b0ac9c7f6b4d'),  # exists
        ('8d5ef41c-25b4-45e5-aada-b0ac9c7f6b4e')])  # not found    
    def test_srv_db_media_by_metadata_guid(self, metadata_guid):
        """
        # fetch all media with METADATA match
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_by_metadata_guid(metadata_guid)


    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found
    def test_srv_db_media_image_path(self, media_guid):
        """
        # grab image path for media id NOT metadataid
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_media_image_path(media_guid)


    @pytest.mark.parametrize(("media_guid"), [
        ('04442b10-3fb5-4d87-95a6-b50dbd072630'),  # exists
        ('04442b10-3fb5-4d87-95a6-b50dbd072633')])  # not found    
    def test_srv_db_read_media_metadata_both(self, media_guid):
        """
        # read in metadata by id
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_read_media_metadata_both(media_guid)


    # do a like class path match for trailers and extras
    # def srv_db_read_media_path_like(self, media_path):
#        self.db_connection.srv_db_rollback()


    @pytest.mark.parametrize(("new_days"), [
        (7),
        (400)])
    def test_srv_db_read_media_new_count(self, new_days):
        """
        # new media count
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_read_media_new_count(new_days)


    @pytest.mark.parametrize(("new_days", "offset", "records"), [
        (7, None, None),
        (400, None, None),
        (400, 100, 100),
        (400, 10000000, 1000)])
    def test_srv_db_read_media_new(self, new_days, offset, records):
        """
        # new media
        """
        self.db_connection.srv_db_rollback()
        self.db_connection.srv_db_read_media_new(new_days, offset, records)
