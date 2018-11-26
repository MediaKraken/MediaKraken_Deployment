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


def db_3d_list_count(self, search_value=None):
    # if search_value is not None:
    #     self.db_cursor.execute('select count(*)'
    #                            ' from mm_metadata_collection'
    #                            ' where mm_metadata_collection_name %% %s',
    #                            (search_value, ))
    # else:
    #     self.db_cursor.execute('select count(*)'
    #                            ' from mm_metadata_collection')
    # return self.db_cursor.fetchone()[0]
    return 0


def db_3d_list(self, offset=None, records=None, search_value=None):
    """
    Return collections list from the database
    """
    # if offset is None:
    #     if search_value is not None:
    #         self.db_cursor.execute('select mm_metadata_collection_guid,'
    #                                'mm_metadata_collection_name,'
    #                                'mm_metadata_collection_imagelocal_json'
    #                                ' from mm_metadata_collection'
    #                                ' where mm_metadata_collection_name %% %s'
    #                                ' order by mm_metadata_collection_name',
    #                                (search_value,))
    #     else:
    #         self.db_cursor.execute('select mm_metadata_collection_guid,'
    #                                'mm_metadata_collection_name,'
    #                                'mm_metadata_collection_imagelocal_json'
    #                                ' from mm_metadata_collection'
    #                                ' order by mm_metadata_collection_name')
    # else:
    #     if search_value is not None:
    #         self.db_cursor.execute('select mm_metadata_collection_guid,'
    #                                'mm_metadata_collection_name,'
    #                                'mm_metadata_collection_imagelocal_json'
    #                                ' from mm_metadata_collection'
    #                                ' where mm_metadata_collection_guid'
    #                                ' in (select mm_metadata_collection_guid'
    #                                ' from mm_metadata_collection'
    #                                ' where mm_metadata_collection_name %% %s'
    #                                ' order by mm_metadata_collection_name'
    #                                ' offset %s limit %s) order by mm_metadata_collection_name',
    #                                (search_value, offset, records))
    #     else:
    #         self.db_cursor.execute('select mm_metadata_collection_guid,'
    #                                'mm_metadata_collection_name,'
    #                                'mm_metadata_collection_imagelocal_json'
    #                                ' from mm_metadata_collection'
    #                                ' where mm_metadata_collection_guid'
    #                                ' in (select mm_metadata_collection_guid'
    #                                ' from mm_metadata_collection'
    #                                ' order by mm_metadata_collection_name'
    #                                ' offset %s limit %s) order by mm_metadata_collection_name',
    #                                (offset, records))
    # return self.db_cursor.fetchall()
    return None
