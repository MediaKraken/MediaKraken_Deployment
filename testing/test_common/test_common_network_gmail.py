'''
  Copyright (C) 2018 Quinn D Granfor <spootdev@gmail.com>

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
import pytest  # pylint: disable=W0611
import sys

sys.path.append('.')
from common import common_network_gmail


# send email
@pytest.mark.parametrize(("email_receipient", "email_subject", "email_body"), [
    ('spootdevfake@gmail.com', "test1", "body"),
    ('spootdev@gmail.com', "test2", "body"),
    ('spootdev@fakegmail.com', "test3", "body")])
def test_com_net_send_email(email_receipient, email_subject, email_body):
    """
    Test function
    """
    common_network_gmail.com_net_send_email(email_receipient, email_subject, email_body)
