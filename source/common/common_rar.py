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

# https://pypi.org/project/rarfile/

# needs unrar to be available

import rarfile


def com_rar_file_list(file_name):
    """
    f.filename
    f.file_size
    """
    rf = rarfile.RarFile(file_name)
    return rf.infolist()


def com_rar_file_read_file(file_name, file_single):
    with rarfile.RarFile(file_name) as rf:
        with rf.open(file_single) as f:
            return f
