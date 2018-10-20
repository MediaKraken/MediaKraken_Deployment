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

import uuid


def db_insert_remote_media(self, media_link_uuid, media_uuid, media_class_uuid,
                           media_metadata_uuid, media_ffprobe_json):
    """
    # insert media into database
    """
    new_guid = str(uuid.uuid4())
    self.db_cursor.execute('insert into mm_media_remote (mmr_media_guid, mmr_media_link_id,'
                           ' mmr_media_uuid, mmr_media_class_guid, mmr_media_metadata_guid,'
                           ' mmr_media_ffprobe_json)'
                           ' values (%s,%s,%s,%s,%s,%s)', (new_guid, media_link_uuid, media_uuid,
                                                           media_class_uuid, media_metadata_uuid,
                                                           media_ffprobe_json))
    self.db_commit()
    return new_guid


def db_read_remote_media(self, media_guid=None):
    """
    # read in all media unless guid specified
    """
    if media_guid is not None:
        self.db_cursor.execute('select * from mm_media_remote where mmr_media_guid = %s',
                               (media_guid,))
        try:
            return self.db_cursor.fetchone()
        except:
            return None
    else:
        self.db_cursor.execute('select * from mm_media_remote')
        return self.db_cursor.fetchall()


def db_known_remote_media_count(self):
    """
    # count known media
    """
    self.db_cursor.execute('select count(*) from mm_media_remote')
    return self.db_cursor.fetchone()[0]


# processed via main_link........
# process new records from network sync event from linked server
# def db_Media_Remote_New_Data(self, link_uuid, link_records):
#    # 0-media guid, 1-type, 2-ffrobe, 3-media id json
#    metadata_guid = None
#    for row_data in link_records:
#        if row_data[1] == 'Movie':
#            if 'themoviedb' in row_data[3]:
#                metadata_guid = db_meta_guid_by_tmdb(row_data[3]['themoviedb'])
#            if metadata_guid is None and 'imdb' in row_data[3]:
#                metadata_guid = db_meta_guid_by_imdb(row_data[3]['imdb'])
#            if metadata_guid is None and 'thetvdb' in row_data[3]:
#                metadata_guid = db_meta_guid_by_tvdb(row_data[3]['thetvdb'])
#        elif row_data[1] == 'TV Show':
#            if 'imdb' in row_data[3]
#                metadata_guid = db_metaTV_guid_by_imdb(row_data[3]['imdb'])
#            if metadata_guid is None and 'thetvdb' in row_data[3]:
#                metadata_guid = db_metatv_guid_by_tvdb(row_data[3]['thetvdb'])
#            if metadata_guid is None and 'tvmaze' in row_data[3]:
#                metadata_guid = db_metaTV_guid_by_tvmaze(row_data[3]['tvmaze'])
#            if metadata_guid is None and 'TVRage' in row_data[3]:
#                metadata_guid = db_metatv_guid_by_tvrage(row_data[3]['TVRage'])
#        elif row_data[1] == 'Sports':
#            pass
#        elif row_data[1] == 'Music':
#            pass
#        elif row_data[1] == 'Music Video':
#            pass
#        elif row_data[1] == 'Book':
#            pass
#        else:
#            common_global.es_inst.com_elastic_index('error', {'stuff':'Link bad data type: %s', row_data[1])
#            return None
#        if metadata_guid is not None:
#            self.db_insert_remote_media(link_uuid, row_data[0], \
# self.db_media_uuid_by_class(row_data[1]), metadata_guid[0], json.dumps(row_data[2]))


def db_media_remote_read_new(self, date_last_sync, sync_movie=None, sync_tv=None,
                             sync_sports=None, sync_music=None, sync_music_video=None,
                             sync_book=None):
    """
    # new media for link
    """
    # TODO add games to this
    first_query = True
    sync_query = ''
    if sync_movie is not None:
        sync_query += ('select mm_media_guid, \'Movie\', mm_media_ffprobe_json,'
                       ' mm_metadata_media_id from mm_media, mm_metadata_movie'
                       ' where mm_media_metadata_guid = mm_metadata_guid'
                       ' and mm_media_json->>\'DateAdded\' >= \'%s\'' % (date_last_sync,))
        first_query = False

    if sync_tv is not None:
        if not first_query:
            sync_query += ' union all '
        sync_query += ('select mm_media_guid, \'TV Show\', mm_media_ffprobe_json,'
                       ' mm_metadata_media_tvshow_id from mm_media, mm_metadata_tvshow'
                       ' where mm_metadata_tvshow_guid = mm_metadata_tvshow_guid'
                       ' and mm_media_json->>\'DateAdded\' >= \'%s\'' % (date_last_sync,))
        first_query = False

    if sync_sports is not None:
        if not first_query:
            sync_query += ' union all '
        sync_query += ('select mm_media_guid, \'Sports\', mm_media_ffprobe_json,'
                       ' mm_metadata_media_sports_id from mm_media, mm_metadata_sports'
                       ' where mm_metadata_sports_guid = mm_metadata_sports_guid'
                       ' and mm_media_json->>\'DateAdded\' >= \'%s\'' % (date_last_sync,))
        first_query = False

    if sync_music is not None:
        if not first_query:
            sync_query += ' union all '
        sync_query += ('select mm_media_guid, \'Music\', mm_media_ffprobe_json,'
                       ' mm_metadata_media_music_id from mm_media, mm_metadata_music'
                       ' where mm_metadata_music_guid = mm_metadata_music_guid'
                       ' and mm_media_json->>\'DateAdded\' >= \'%s\'' % (date_last_sync,))
        first_query = False

    if sync_music_video is not None:
        if not first_query:
            sync_query += ' union all '
        sync_query += ('select mm_media_guid, \'Music Video\', mm_media_ffprobe_json,'
                       ' mm_metadata_music_video_media_id from mm_media, mm_metadata_music_video'
                       ' where mm_metadata_music_video_guid = mm_metadata_music_video_guid'
                       ' and mm_media_json->>\'DateAdded\' >= \'%s\'' % (date_last_sync,))
        first_query = False

    if sync_book is not None:
        if not first_query:
            sync_query += ' union all '
        sync_query += ('select mm_media_guid, \'Book\', mm_media_ffprobe_json,'
                       ' mm_metadata_book_isbn from mm_media, mm_metadata_book'
                       ' where mm_metadata_book_guid = mm_metadata_book_guid'
                       ' and mm_media_json->>\'DateAdded\' >= \'%s\'' % (date_last_sync,))
        first_query = False
    if sync_query != '':
        self.db_cursor.execute(sync_query)
        return self.db_cursor.fetchall()
    else:
        return None
