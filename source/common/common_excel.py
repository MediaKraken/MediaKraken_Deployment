"""
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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

import pyexcel


class CommandExcel:
    """
    Class for interfacing with excel
    """

    def __init__(self):
        pass

    def com_excel_save(self, dataset, file_name):
        pyexcel.save_as(records=dataset, dest_file_name=file_name)

    def com_excel_load(self, file_name):
        return pyexcel.iget_records(file_name=file_name)

    def com_excel_free(self):
        pyexcel.free_resources()
