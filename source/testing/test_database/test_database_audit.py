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

import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
import database as database_base


class TestDatabaseAudit:

    @classmethod
    def setup_class(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.db_open(True)
        self.new_guid = None

    @classmethod
    def teardown_class(self):
        self.db_connection.db_close()

    def test_db_audit_path_status(self):
        """
        # read scan status
        """
        self.db_connection.db_rollback()
        self.db_connection.db_audit_path_status()

    # update status
    # def db_audit_path_update_status(self, lib_guid, status_json):
    #        self.db_connection.db_rollback()

    # update audit path
    # def db_audit_path_update_by_uuid(self, lib_path, class_guid, lib_guid):
    #        self.db_connection.db_rollback()

    @pytest.mark.parametrize(("dir_path", "class_guid", "share_guid"), [
        ('/home/spoot/fakedirzz', 'b3420d91-999b-4d10-a582-3cddef2ce278', None),
        ('/home/spoot', '18479e1a-68a4-4137-8c96-b7d7dab5c66f', None)])
    def test_db_audit_path_add(self, dir_path, class_guid, share_guid):
        """
        ## add media path
        """
        self.db_connection.db_rollback()
        self.new_guid = self.db_connection.db_audit_path_add(
            dir_path, class_guid, share_guid)

    @pytest.mark.parametrize(("dir_path"), [
        ('/home/spoot'),
        ('/home/spoot/fakedirzz')])
    def test_db_audit_path_check(self, dir_path):
        """
        ## lib path check (dupes)
        """
        self.db_connection.db_rollback()
        self.db_connection.db_audit_path_check(dir_path)

    @pytest.mark.parametrize(("dir_path"), [
        ('/home/spoot'),
        ('/home/spoot/fakedirzz')])
    def test_db_audit_dir_timestamp_update(self, dir_path):
        """
        ## update the timestamp for directory scans
        """
        self.db_connection.db_rollback()
        self.db_connection.db_audit_dir_timestamp_update(dir_path)

    # read the paths to audit
    @pytest.mark.parametrize(("offset", "records"), [
        (None, None),
        (100, 100),
        (100000000, 1000)])
    def test_db_audit_paths(self, offset, records):
        """
        Test function
        """
        self.db_connection.db_rollback()
        self.db_connection.db_audit_paths(offset, records)

    def test_db_audit_path_by_uuid(self):
        """
        ## lib data per id
        """
        self.db_connection.db_rollback()
        self.db_connection.db_audit_path_by_uuid(self.new_guid)

    def test_db_audit_path_delete(self):
        """
        ## remove media path
        """
        self.db_connection.db_rollback()
        self.db_connection.db_audit_path_delete(self.new_guid)
