'''
  Copyright (C) 2015 Quinn D Granfor <spootdev@gmail.com>

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
#import logging
import os
import time
import scandir
try:
    import cPickle as pickle
except:
    import pickle
from common import common_string

JUNK_FILES = [
            '(gameplay)',
            'official gameplay',
            'movie clip',
            'fan made',
            'review -',
            'full movie',
            'full album',
            'full length',
            'deleted scene',
            ]


def com_file_modification_timestamp(file_name):
    """
    Return file modfication date in datetime format
    """
    if os.path.exists(file_name):
        return os.path.getmtime(file_name)
    else:
        return None


def com_file_save_data(file_name, data_block, as_pickle=False, with_timestamp=False,\
        file_ext=None):
    """
    Save data as file
    """
    file_handle = None
    if with_timestamp:
        file_handle = open(file_name + '_' + time.strftime("%Y%m%d%H%M%S") + file_ext, 'w+')
    else:
        file_handle = open(file_name, 'w+')
    if as_pickle:
        #file_handle.write(pickle.dump(data_block))
        pickle.dump(data_block, file_handle)
    else:
        file_handle.write(data_block)
    file_handle.close()


def com_file_load_data(file_name, as_pickle=False):
    """
    Load data from file as ascii or pickle
    """
    file_handle = open(file_name, "r")
    if as_pickle:
        data_block = pickle.loads(file_handle.read())
    else:
        data_block = file_handle.read()
    file_handle.close()
    return data_block


def com_file_dir_list(dir_name, filter_text, walk_dir, skip_junk=True, file_size=False,\
        directory_only=False):
    """
    Find all filtered files in directory
    """
    if os.path.isdir(dir_name):
        match_list = []
        if not walk_dir:
            if filter_text is not None:
                for file_name in os.listdir(dir_name):
                    # filter text such as '.txt'
                    if file_name.rsplit('.', 1)[1] in filter_text:
                    #if file_name.endswith(filter_text):
                        match_list.append(os.path.join(dir_name, file_name))
            else:
                for file_name in os.listdir(dir_name):
                    if directory_only:
                        if os.path.isdir(os.path.join(dir_name, file_name)):
                            match_list.append(os.path.join(dir_name, file_name))
                    else:
                        match_list.append(os.path.join(dir_name, file_name))
        else:
            for root, dirs, files in scandir.walk(dir_name):
                for file_name in files:
                    if filter_text is not None:
                        if file_name.endswith(filter_text):
                            #logging.debug(os.path.join(root, file_name))
                            match_list.append(os.path.join(root, file_name))
                    else:
                        if directory_only:
                            if os.path.isdir(os.path.join(dir_name, file_name)):
                                match_list.append(os.path.join(dir_name, file_name))
                        else:
                            match_list.append(os.path.join(root, file_name))
        if skip_junk and len(match_list) > 0:
            match_list = com_file_remove_junk(match_list)
        if file_size:
            match_list_size = []
            for row_data in match_list:
                match_list_size.append((row_data,\
                    common_string.bytes2human(os.path.getsize(row_data))))
            return match_list_size
        return match_list
    else:
        return None


def com_file_remove_junk(file_list):
    """
    Throw out junk entries in files list
    """
    for file_name in file_list:
        for search_string in JUNK_FILES:
            try:
                if file_name.lower().find(search_string) != -1:
                    file_list.remove(file_name)
                    break
            except:
                pass
    return file_list


def com_file_is_junk(file_name):
    """
    See if file is junk
    """
    for search_string in JUNK_FILES:
        try:
            if file_name.lower().find(search_string) != -1:
                return True
        except:
            pass
    return False
