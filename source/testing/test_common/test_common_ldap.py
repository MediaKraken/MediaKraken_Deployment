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
from common import common_ldap


class TestCommonLDAP:

    @classmethod
    def setup_class(self):
        self.db_connection = common_ldap.CommonLDAP()

    @classmethod
    def teardown_class(self):
        pass

    # class com_LDAP_API:
    #    def __init__(self, ldap_server, ou_name, dc_name):

    @pytest.mark.parametrize(("user_name", "user_password", "expected_result"), [
        ("metaman", "metaman", True),
        ("metaman", "metaman_fake", False),
        ("metaman_fake", "metaman_fake", False)])
    def test_com_ldap_logon(self, user_name, user_password, expected_result):
        """
        Test ldap login
        """
        self.db_connection.com_ldap_logon(user_name, user_password)

    def test_com_ldap_close(self):
        """
        Test ldap close
        """
        self.db_connection.com_ldap_close()
