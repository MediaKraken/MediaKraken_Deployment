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

import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp3 import MP3


def com_meta_mutagen_file_type(file_name):
    return mutagen.FileType(file_name)


def com_meta_mutagen_file_detail(file_name):
    return mutagen.File(file_name)


def com_meta_mutagen_update(file_name, attr_name, attr_desc):
    audio = FLAC(file_name)
    audio[attr_name] = attr_desc
    audio.save()


def com_meta_mutagen_lenbit(file_name):
    audio = MP3(file_name)
    print((audio.info.length))
    print((audio.info.bitrate))
    return audio


def com_meta_mutagen_remove_id(file_name):
    audio = ID3(file_name)
    audio.delete()


def com_meta_mutagen_update_easy(file_name, attr_name, attr_desc):
    audio = EasyID3(file_name)
    if type(attr_name) == dict:
        for dict_item in list(attr_desc.keys()):
            audio[dict_item] = attr_desc[dict_item]
    else:
        audio[attr_name] = attr_desc
    audio.save()

# print(EasyID3.valid_keys.keys())
# print(com_meta_mutagen_file_type('/home/spoot/test.flac'))
