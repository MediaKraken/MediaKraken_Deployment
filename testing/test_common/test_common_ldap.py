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


import pytest
import sys
sys.path.append("../MediaKraken_Common")
from MK_Common_LDAP import *


class Test_MK_Common_LDAP_API:


    @classmethod
    def setup_class(self):
        self.db = MK_Common_LDAP.MK_Common_LDAP_API()


    @classmethod
    def teardown_class(self):
        pass


#class MK_Common_LDAP_API:
#    def __init__(self, ldap_server, ou_name, dc_name):


    @pytest.mark.parametrize(("user_name", "user_password", "expected_result"), [
        ("metaman", "metaman", True),
        ("metaman", "metaman_fake", False),
        ("metaman_fake", "metaman_fake", False)])
    def test_MK_Common_LDAP_Logon(self, user_name, user_password, expected_result):
        MK_Common_LDAP_Logon(user_name, user_password, expected_result)


    def test_MK_Common_LDAP_Close(self):
        MK_Common_LDAP_Close()

