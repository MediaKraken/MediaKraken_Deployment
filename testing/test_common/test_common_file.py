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
import datetime
import sys
sys.path.append('.')
from common import common_file


# return file modfication date in datetime format
@pytest.mark.parametrize(("file_name", "expected_result"), [
    ("./cache/cache.iso", True),
    ("./cache/cache_fake.iso", None)])
def test_common_file_modification_timestamp(file_name, expected_result):
    """
    Test function
    """
    assert isinstance(common_file.com_file_modification_timestamp(file_name, expected_result),\
        datetime.datetime) == expected_result


# save data as file
@pytest.mark.parametrize(("file_name", "data_block", "as_pickle", "with_timestamp", "file_ext"), [
    ('./cache/Test.txt', "Test", False, False, None),
    ('./cache/Test2.txt', "Test2", False, False, ".dat"),
    ('./cache/Test2_2.txt', "Test2", False, True, ".dat"),
    ('./cache/Test3.txt', "Test3", False, True, None),
    ('./cache/Test4_Pickle.txt', ("Test4", "Test5"), True, False, None),
    ('./cache/Test6_Pickle.txt', ("Test4", "Test5"), True, True, None),
    ('./cache/Test7_Pickle.txt', ("Test4", "Test5"), True, False, ".pickle"),
    ('./cache/Test8_Pickle.txt', ("Test4", "Test5"), False, True, ".dat")])
def test_com_file_save_data(file_name, data_block, as_pickle, with_timestamp, file_ext):
    """
    Test function
    """
    common_file.com_file_save_data(file_name, data_block, as_pickle, with_timestamp, file_ext)


# load file as data
@pytest.mark.parametrize(("file_name", "as_pickle"), [
    ('./cache/HashCalc.txt', False),
    ('./cache/HashCalc.txt', True),
    ('./cache/pickle.txt', True),
    ('./cache/pickle.txt', False)])
def test_common_file_load_data(file_name, as_pickle):
    """
    Test function
    """
    common_file.com_file_load_data(file_name, as_pickle)


# find all filters files in directory
@pytest.mark.parametrize(("dir_name", "filter_text", "walk_dir", "skip_junk", "file_size",\
        "directory_only"), [
    ('./cachenotfound', None, False, False, False, False),
    ('./cache', None, False, False, False, False),
    ('./cache', None, True, False, False, False),
    ('./cache', None, False, True, False, False),
    ('./cache', None, False, False, True, False),
    ('./cache', None, False, False, False, True),
    ('./cache', "waffle", True, False, False, False),
    ('./cache', "waffle", False, True, False, False),
    ('./cache', "waffle", False, False, True, False),
    ('./cache', "waffle", False, False, False, True),
    ('./cache', None, True, True, False, False),
    ('./cache', None, True, True, True, False),
    ('./cache', None, False, True, True, False),
    ('./cache', None, False, True, False, True),
    ('./cache', None, False, True, True, True),
    ('./cache', None, True, True, False, True),
    ('./cache', None, True, True, True, True),
    ('./cache', "waffle", True, True, False, False),
    ('./cache', "waffle", True, True, True, False),
    ('./cache', "waffle", False, True, True, False),
    ('./cache', "waffle", False, True, False, True),
    ('./cache', "waffle", False, True, True, True),
    ('./cache', "waffle", True, True, False, True),
    ('./cache', "waffle", True, True, True, True)])
def test_common_file_dir_list(dir_name, filter_text, walk_dir, skip_junk, file_size,\
        directory_only):
    """
    Test function
    """
    common_file.com_file_dir_list(dir_name, filter_text, walk_dir, skip_junk,\
        file_size, directory_only)


# throw out junk entries in files list
def test_common_file_remove_junk():
    """
    Test function
    """
    assert common_file.com_file_remove_junk(("ok", "blah full length")) == ("ok")


# see if file is junk
@pytest.mark.parametrize(("file_name", "expected_result"), [
    ('./cache/HashCalc.txt', False),
    ('./cache/HashCalcfull album.txt', True),
    ('./cache/picklefull length.txt', True),
    ('./cache/pickle.txt', False)])
def test_common_file_is_junk(file_name, expected_result):
    """
    Test function
    """
    assert common_file.com_file_is_junk(file_name) == expected_result
