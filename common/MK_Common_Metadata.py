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

from __future__ import unicode_literals
import logging
import os
import re
import random
import string
import MK_Common_Network


# pull in the ini file config
import ConfigParser
Config = ConfigParser.ConfigParser()
if os.path.exists("MediaKraken.ini"):
    Config.read("MediaKraken.ini")
else:
    Config.read("../../MediaKraken_Server/MediaKraken.ini")
base_image_path = Config.get('MediaKrakenServer', 'MetadataImageLocal').strip()
if base_image_path.endswith('/'):
    pass
else:
    base_image_path += '/'


# determine "weight" of file to download for trailer
def MK_Common_Metadata_Calc_Trailer_Weight(trailer_file_list, title_name, title_year):
    old_weight = 0
    best_match = None
    weight = 0
    for file_name in trailer_file_list:
        # compute the weight
        weight = 0
        if file_name.lower().find(u'official trailer') != -1:
            weight += 3
        if file_name.lower().find(title_name.lower()) != -1:
            weight += 10
        if file_name.find(u'HD') != -1:
            weight += 1
        if file_name.find(title_year) != -1:
            weight += 5
        if weight > old_weight:
            best_match = file_name
            old_weight = weight
        # if "max" find, then stop processing list
        if weight == 19:
            break
    return best_match, old_weight


# determine file path of images
def MK_Common_Metadata_Image_File_Path(media_name, media_type):
    logging.debug("filename: %s", media_name)
    pattern = r'[^\.a-zA-Z]'
    try:
        if re.search(pattern, os.path.basename(media_name)[0]): # first char of filename
            file_path = os.path.join(base_image_path, media_type, random.choice(string.ascii_lowercase))
        else:
            file_path = os.path.join(base_image_path, media_type, os.path.basename(media_name)[0].lower())
    except:
        file_path = os.path.join(base_image_path, media_type, random.choice(string.ascii_lowercase))       
    return file_path


# determine image location
# media name - used to determine a-z dir
# media_type - banner, poster, etc
# source_link - the website/host to use
# source_file - the "file name" on the url
def MK_Common_MetaData_Image_Path(media_name, media_type, source_link, source_file):
    file_path = MK_Common_Metadata_Image_File_Path(media_name, media_type)
    # determine url and such
    if source_link == "tmdb":
        url = 'https://image.tmdb.org/'
        if media_type == "poster":
            url += '/t/p/original'
        else:
            url += '/t/p/original'
    elif source_link == "thetvdb":
        url = 'https://thetvdb.com/banners/'
        # the following is part of the json data so no need for this
#        if media_type == 'banner':
#            url += 'graphical/'
#        elif media_type == 'fanart':
#            url += 'fanart/original/'
#        elif media_type == 'poster':
#            url += 'posters/'
#        elif media_type == 'actor':
#           url += 'actors/'
    elif source_link == "thelogodb":
        # simply a placeholder so I don't ponder about this one in the future
        url = ''
    elif source_link == "tvmaze":
        # simply a placeholder so I don't ponder about this one in the future
        url = ''
    file_path += source_file
    # snag file if not downloaded before
    if not os.path.isfile(file_path):
        MK_Common_Network.MK_Network_Fetch_From_URL(url + source_file, file_path)
    return file_path
