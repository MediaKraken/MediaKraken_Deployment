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
from common import common_system


# def pprint_ntuple(nt, return_value=None):


# return virtual memory
# def common_system_Virtual_Memory(attribute_list=None):


# return swap memory
# def common_system_SWAP_Memory(attribute_list=None):


def test_com_system_cpu_count():
    """
    # return cpu count
    """
    assert common_system.com_system_cpu_count() == 16


def test_com_system_partitions():
    """
    # return partitions
    """
    common_system.com_system_partitions()


def test_com_system_boot_time():
    """
    # get boot time
    """
    common_system.com_system_boot_time()


def test_com_system_users():
    """
    # get users 
    """
    common_system.com_system_users()


@pytest.mark.parametrize(("per_cpu"), [
    (True),
    (False)])
def test_com_system_cpu_usage(per_cpu):
    """
    # get cpu percentage
    """
    common_system.com_system_cpu_usage(per_cpu)


def test_com_system_cpu_times():
    """
    # get cpu times
    """
    common_system.com_system_cpu_times()


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    path = 'C:'
else:
    path = '/'


def test_com_system_disk_usage():
    """
    # get disk usage
    """
    common_system.com_system_disk_usage(path)


@pytest.mark.parametrize(("human_readable"), [
    (True),
    (False)])
def test_com_system_disk_usage_all(human_readable):
    """
    # get disk usage of all partitions
    """
    common_system.com_system_disk_usage_all(human_readable)


@pytest.mark.parametrize(("per_disk"), [
    (True),
    (False)])
def test_com_system_disk_io(per_disk):
    """
    # get disk IO
    """
    common_system.com_system_disk_io(per_disk)


def test_com_system_uptime():
    """
    # get system uptime
    """
    common_system.com_system_uptime()


@pytest.mark.parametrize(("process_name"), [
    (None),
    ('init'),
    ('fakeprocessname')])
def test_com_process_list(process_name):
    """
    # get processes and optionally check for one
    """
    common_system.com_process_list(process_name)
