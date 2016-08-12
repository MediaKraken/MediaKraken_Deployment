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
sys.path.append("../common")
from common_system import *


# def pprint_ntuple(nt, return_value=None):


# return virtual memory
# def common_system_Virtual_Memory(attribute_list=None):


# return swap memory
# def common_system_SWAP_Memory(attribute_list=None):


# return cpu count
def Test_common_system_CPU_Count():
    assert common_system_CPU_Count() == 8


# return partitions
def Test_common_system_Partitions():
    common_system_Partitions()


# get boot time
def Test_common_system_Boot_Time():
    common_system_Boot_Time()


# get users 
def Test_common_system_Users():
    common_system_Users()


# get cpu percentage
@pytest.mark.parametrize(("per_cpu"), [
    (True),
    (False)])
def Test_common_system_CPU_Usage(per_cpu):
    common_system_CPU_Usage(per_cpu)


# get cpu times
def Test_common_system_CPU_Times():
    common_system_CPU_Times()


# get disk usage
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    path = 'C:'
else:
    path = '/'
def Test_common_system_Disk_Usage():
    common_system_Disk_Usage(path)


# get disk usage of all partitions
@pytest.mark.parametrize(("human_readable"), [
    (True),
    (False)])
def Test_common_system_Disk_Usage_All(human_readable):
    common_system_Disk_Usage_All(human_readable)


# get disk IO
@pytest.mark.parametrize(("per_disk"), [
    (True),
    (False)])
def Test_common_system_Disk_IO(per_disk):
    common_system_Disk_IO(per_disk)


# get system uptime
def Test_common_system_Uptime():
    common_system_Uptime()


# get processes and optionally check for one
@pytest.mark.parametrize(("process_name"), [
    (None),
    ('init'),
    ('fakeprocessname')])
def Test_com_Process_List(process_name):
    com_Process_List(process_name)
