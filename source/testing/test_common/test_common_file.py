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

import datetime
import sys

sys.path.append('.')
from common import common_file
import pytest  # pylint: disable=W0611


# return file modfication date in datetime format
@pytest.mark.parametrize(("file_name", "expected_result"), [
    ("./testing/cache/cache.iso", True),
    ("./testing/cache/cache_fake.iso", None)])
def test_com_file_modification_timestamp(file_name, expected_result):
    """
    Test function
    """
    assert isinstance(common_file.com_file_modification_timestamp(file_name, expected_result),
                      datetime.datetime) == expected_result


# save data as file
@pytest.mark.parametrize(("file_name", "data_block", "as_pickle", "with_timestamp", "file_ext"), [
    ('./testing/cache/Test.txt', "Test", False, False, None),
    ('./testing/cache/Test2.txt', "Test2", False, False, ".dat"),
    ('./testing/cache/Test2_2.txt', "Test2", False, True, ".dat"),
    ('./testing/cache/Test3.txt', "Test3", False, True, None),
    ('./testing/cache/Test4_Pickle.txt', ("Test4", "Test5"), True, False, None),
    ('./testing/cache/Test6_Pickle.txt', ("Test4", "Test5"), True, True, None),
    ('./testing/cache/Test7_Pickle.txt', ("Test4", "Test5"), True, False, ".pickle"),
    ('./testing/cache/Test8_Pickle.txt', ("Test4", "Test5"), False, True, ".dat")])
def test_com_file_save_data(file_name, data_block, as_pickle, with_timestamp, file_ext):
    """
    Test function
    """
    common_file.com_file_save_data(
        file_name, data_block, as_pickle, with_timestamp, file_ext)


# load file as data
@pytest.mark.parametrize(("file_name", "as_pickle"), [
    ('./testing/cache/HashCalc.txt', False),
    ('./testing/cache/HashCalc.txt', True),
    ('./testing/cache/pickle.txt', True),
    ('./testing/cache/pickle.txt', False)])
def test_com_file_load_data(file_name, as_pickle):
    """
    Test function
    """
    common_file.com_file_load_data(file_name, as_pickle)


# find all filters files in directory
@pytest.mark.parametrize(("dir_name", "filter_text", "walk_dir", "skip_junk", "file_size",
                          "directory_only"), [
                             ('./testing/cachenotfound', None, False, False, False, False),
                             ('./testing/cache', None, False, False, False, False),
                             ('./cache', None, True, False, False, False),
                             ('./testing/cache', None, False, True, False, False),
                             ('./testing/cache', None, False, False, True, False),
                             ('./testing/cache', None, False, False, False, True),
                             ('./testing/cache', "waffle",
                              True, False, False, False),
                             ('./testing/cache', "waffle",
                              False, True, False, False),
                             ('./testing/cache', "waffle",
                              False, False, True, False),
                             ('./testing/cache', "waffle",
                              False, False, False, True),
                             ('./testing/cache', None, True, True, False, False),
                             ('./testing/cache', None, True, True, True, False),
                             ('./testing/cache', None, False, True, True, False),
                             ('./testing/cache', None, False, True, False, True),
                             ('./testing/cache', None, False, True, True, True),
                             ('./testing/cache', None, True, True, False, True),
                             ('./testing/cache', None, True, True, True, True),
                             ('./testing/cache', "waffle",
                              True, True, False, False),
                             ('./testing/cache', "waffle",
                              True, True, True, False),
                             ('./testing/cache', "waffle",
                              False, True, True, False),
                             ('./testing/cache', "waffle",
                              False, True, False, True),
                             ('./testing/cache', "waffle",
                              False, True, True, True),
                             ('./testing/cache', "waffle",
                              True, True, False, True),
                             ('./testing/cache', "waffle", True, True, True, True)])
def test_com_file_dir_list(dir_name, filter_text, walk_dir, skip_junk, file_size,
                           directory_only):
    """
    Test function
    """
    common_file.com_file_dir_list(dir_name, filter_text, walk_dir, skip_junk,
                                  file_size, directory_only)


# throw out junk entries in files list
def test_com_file_remove_junk():
    """
    Test function
    """
    assert common_file.com_file_remove_junk(
        ("ok", "blah full length")) == ("ok")


# see if file is junk
@pytest.mark.parametrize(("file_name", "expected_result"), [
    ('./testing/cache/HashCalc.txt', False),
    ('./testing/cache/HashCalcfull album.txt', True),
    ('./testing/cache/picklefull length.txt', True),
    ('./testing/cache/pickle.txt', False)])
def test_com_file_is_junk(file_name, expected_result):
    """
    Test function
    """
    assert common_file.com_file_is_junk(file_name) == expected_result
