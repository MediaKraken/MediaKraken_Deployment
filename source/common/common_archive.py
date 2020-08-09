"""
  Copyright (C) 2019 Quinn D Granfor <spootdev@gmail.com>

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
"""

import libarchive


def com_archive_unarchive(file_name):
    """
    Unarchives provided file name into PWD. Should autodetect the archive type.
    """
    libarchive.extract_file(file_name)


def com_archive_read(file_name):
    with libarchive.file_reader(file_name) as archive:
        for entry in archive:
            for block in entry.get_blocks():
                pass


def com_archive_create(file_name_out, format_type, file_name_list):
    # shows .tar.gz with libarchive.file_writer(file_name_out, 'ustar', 'gzip') as archive:
    with libarchive.file_writer(file_name_out, format_type) as archive:
        archive.add_files(file_name_list)
