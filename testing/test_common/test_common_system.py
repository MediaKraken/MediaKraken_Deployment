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
from MK_Common_System import *


# def pprint_ntuple(nt, return_value=None):


# return virtual memory
# def MK_Common_System_Virtual_Memory(attribute_list=None):


# return swap memory
# def MK_Common_System_SWAP_Memory(attribute_list=None):


# return cpu count
def test_MK_Common_System_CPU_Count():
    assert MK_Common_System_CPU_Count() == 8


# return partitions
def test_MK_Common_System_Partitions():
    MK_Common_System_Partitions()


# get boot time
def test_MK_Common_System_Boot_Time():
    MK_Common_System_Boot_Time()


# get users 
def test_MK_Common_System_Users():
    MK_Common_System_Users()


# get cpu percentage
@pytest.mark.parametrize(("per_cpu"), [
    (True),
    (False)])
def test_MK_Common_System_CPU_Usage(per_cpu):
    MK_Common_System_CPU_Usage(per_cpu)


# get cpu times
def test_MK_Common_System_CPU_Times():
    MK_Common_System_CPU_Times()


# get disk usage
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    path = 'C:'
else:
    path = '/'
def test_MK_Common_System_Disk_Usage():
    MK_Common_System_Disk_Usage(path)


# get disk usage of all partitions
@pytest.mark.parametrize(("human_readable"), [
    (True),
    (False)])
def test_MK_Common_System_Disk_Usage_All(human_readable):
    MK_Common_System_Disk_Usage_All(human_readable)


# get disk IO
@pytest.mark.parametrize(("per_disk"), [
    (True),
    (False)])
def test_MK_Common_System_Disk_IO(per_disk):
    MK_Common_System_Disk_IO(per_disk)


# get system uptime
def test_MK_Common_System_Uptime():
    MK_Common_System_Uptime()


# get processes and optionally check for one
@pytest.mark.parametrize(("process_name"), [
    (None),
    ('init'),
    ('fakeprocessname')])
def test_MK_Common_Process_List(process_name):
    MK_Common_Process_List(process_name)
