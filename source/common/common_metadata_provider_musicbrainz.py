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

import json

import musicbrainzngs
from common import common_config_ini
from common import common_global
from common import common_version

'''
A musicbrainz release represents the unique release (i.e. issuing) of a product on a
specific date with specific release information such as the country, label, barcode,
packaging, etc. If you walk into a store and purchase an album or single, they're each
represented in musicbrainz as one release.

A recording is an entity in musicbrainz which can be linked to tracks on releases.
Each track must always be associated with a single recording, but a recording can
be linked to any number of tracks.

'''


class CommonMetadataMusicbrainz:
    """
    Class for interfacing with musicbrainz
    """

    def __init__(self, option_config_json):
        # If you plan to submit data, authenticate
        # musicbrainzngs.auth(option_config_json.get('MediaBrainz','User').strip(),
        # option_config_json.get('MediaBrainz','Password').strip())
        musicbrainzngs.set_useragent("MediaKraken_Server", common_version.APP_VERSION,
                                     "spootdev@gmail.com "
                                     "https://https://github.com/MediaKraken/MediaKraken_Deployment")
        # If you are connecting to a development server
        if option_config_json['MusicBrainz']['Host'] is not None:
            if option_config_json['MusicBrainz']['Host'] != 'Docker':
                musicbrainzngs.set_hostname(option_config_json['MusicBrainz']['Host'] + ':'
                                            + option_config_json['MusicBrainz']['Port'])
            else:
                musicbrainzngs.set_hostname('mkmusicbrainz:5000')

    def show_release_details(self, rel):
        """
        Get release details
        """
        # "artist-credit-phrase" is a flat string of the credited artists
        # joined with " + " or whatever is given by the server.
        # You can also work with the "artist-credit" list manually.
        # print "{}, by {}".format(rel['title'], rel["artist-credit-phrase"])
        if 'date' in rel:
            pass
        common_global.es_inst.com_elastic_index('info', {"musicbrainz ID": "{}".format(rel['id'])})

    def com_mediabrainz_get_releases(self, disc_id=None, artist_name=None,
                                     artist_recording=None, return_limit=5, strict_flag=False):
        """
        # search by artist and album name
        """
        if disc_id is not None:
            result = musicbrainzngs.get_releases_by_discid(disc_id,
                                                           includes=["artists", "recordings"])
        else:
            result = musicbrainzngs.search_releases(artist=artist_name, release=artist_recording,
                                                    limit=return_limit, strict=strict_flag)
        if not result['release-list']:
            common_global.es_inst.com_elastic_index('error', {'stuff': "no release found"})
            return None
        else:
            for (idx, release) in enumerate(result['release-list']):
                common_global.es_inst.com_elastic_index('info', {"match #{}:".format(idx + 1)})
                self.show_release_details(release)
            return release['id']

    def com_mediabrainz_get_recordings(self, artist_name=None, release_name=None,
                                       song_name=None, return_limit=5, strict_flag=False):
        """
        # search by artist and song name
        """
        result = musicbrainzngs.search_recordings(artist=artist_name, release=release_name,
                                                  recording=song_name, limit=return_limit,
                                                  strict=strict_flag)
        if not result['recording-list']:
            common_global.es_inst.com_elastic_index('error', {'stuff': "no recording found"})
            return None
        else:
            for (idx, release) in enumerate(result['recording-list']):
                common_global.es_inst.com_elastic_index('info', {"match #{}:".format(idx + 1)})
                self.show_release_details(release)
            return release['id']


option_config_json, db_connection = common_config_ini.com_config_read()
MBRAINZ_CONNECTION = CommonMetadataMusicbrainz(option_config_json)


def music_search_musicbrainz(db_connection, download_que_json, ffmpeg_data_json):
    try:
        common_global.es_inst.com_elastic_index('info',
                                                {"meta music search brainz": download_que_json})
    except:
        pass
    metadata_uuid = None
    # look at musicbrainz server
    music_data = MBRAINZ_CONNECTION.com_mediabrainz_get_recordings(
        ffmpeg_data_json['format']['tags']['ARTIST'],
        ffmpeg_data_json['format']['tags']['ALBUM'],
        ffmpeg_data_json['format']['tags']['TITLE'], return_limit=1)
    if music_data is not None:
        if metadata_uuid is None:
            metadata_uuid = db_connection.db_meta_song_add(
                ffmpeg_data_json['format']['tags']['TITLE'],
                music_data['fakealbun_id'], json.dumps(music_data))
    return metadata_uuid, music_data