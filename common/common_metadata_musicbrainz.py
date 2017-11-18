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
import logging # pylint: disable=W0611
import musicbrainzngs
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


class CommonMetadataMusicbrainz(object):
    """
    Class for interfacing with musicbrainz
    """
    def __init__(self, option_config_json):
        # If you plan to submit data, authenticate
        #musicbrainzngs.auth(option_config_json.get('MediaBrainz','User').strip(),
        #option_config_json.get('MediaBrainz','Password').strip())
        musicbrainzngs.set_useragent("MediaKraken_Server", common_version.APP_VERSION,
            "spootdev@gmail.com http://www.mediakraken.org")
        # If you are connecting to a development server
        if option_config_json['MediaBrainz']['Host'] != 'None':
            if option_config_json['MediaBrainz']['Host'] != 'Docker':
                musicbrainzngs.set_hostname(option_config_json['MediaBrainz']['Host'] + ':'
                                            + option_config_json['MediaBrainz']['Port'])
            else:
                musicbrainzngs.set_hostname('mkbrainz:5000')


    def show_release_details(self, rel):
        """
        Get release details
        """
        # "artist-credit-phrase" is a flat string of the credited artists
        # joined with " + " or whatever is given by the server.
        # You can also work with the "artist-credit" list manually.
        #print "{}, by {}".format(rel['title'], rel["artist-credit-phrase"])
        if 'date' in rel:
            pass
        logging.info("musicbrainz ID: {}".format(rel['id']))


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
            logging.error("no release found")
            return None
        else:
            for (idx, release) in enumerate(result['release-list']):
                logging.info("match #{}:".format(idx+1))
                self.show_release_details(release)
            return release['id']


    def com_mediabrainz_get_recordings(self, artist_name=None, release_name=None,
            song_name=None, return_limit=5, strict_flag=False):
        """
        # search by artist and song name
        """
        result = musicbrainzngs.search_recordings(artist=artist_name, release=release_name,
            recording=song_name, limit=return_limit, strict=strict_flag)
        if not result['recording-list']:
            logging.error("no recording found")
            return None
        else:
            for (idx, release) in enumerate(result['recording-list']):
                logging.info("match #{}:".format(idx+1))
                self.show_release_details(release)
            return release['id']
