"""
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
"""

import os
import random
import re
import string  # pylint: disable=W0402

from . import common_global
from . import common_network


def com_meta_calc_trailer_weight(trailer_file_list, title_name, title_year):
    """
    Determine "weight" of file to download for trailer
    """
    old_weight = 0
    best_match = None
    weight = 0
    for file_name in trailer_file_list:
        # compute the weight
        weight = 0
        if file_name.lower().find('official trailer') != -1:
            weight += 3
        if file_name.lower().find(title_name.lower()) != -1:
            weight += 10
        if file_name.find('HD') != -1:
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


def com_meta_image_file_path(media_name, media_type):
    """
    Determine file path of images
    """
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {"filename": media_name})
    pattern = r'[^\.a-zA-Z]'
    # This is the SAVE path.  Do NOT shorten the path to static.
    # This is the SAVE path.  Do NOT shorten the path to static.
    # This is the SAVE path.  Do NOT shorten the path to static.
    # This is the SAVE path.  Do NOT shorten the path to static.
    # This is the SAVE path.  Do NOT shorten the path to static.
    try:
        # first char of filename
        if re.search(pattern, os.path.basename(media_name)[0]):
            file_path = os.path.join(common_global.static_data_directory, '/meta/images',
                                     media_type, random.choice(string.ascii_lowercase))
        else:
            file_path = os.path.join(common_global.static_data_directory + '/meta/images',
                                     media_type, os.path.basename(media_name)[0].lower())
    except:
        file_path = os.path.join(common_global.static_data_directory + '/meta/images',
                                 media_type, random.choice(string.ascii_lowercase))
    # This is the SAVE path.  Do NOT shorten the path to static.
    # This is the SAVE path.  Do NOT shorten the path to static.
    # This is the SAVE path.  Do NOT shorten the path to static.
    # os.path.join should be adding the terminating slash
    common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'file image path': file_path})
    return file_path


def com_meta_image_path(media_name, media_type, source_link, source_file):
    """
    determine image location
    media name - used to determine a-z dir
    media_type - banner, poster, etc
    source_link - the website/host to use
    source_file - the "file name" on the url
    """
    url = ''
    file_path = com_meta_image_file_path(media_name, media_type)
    # determine url and such
    if source_link == 'themoviedb':
        url = 'https://image.tmdb.org/t/p/original/'
    elif source_link == 'thetvdb':
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
    elif source_link == 'thelogodb':
        # simply a placeholder so I don't ponder about this one in the future
        pass
    elif source_link == 'tvmaze':
        # simply a placeholder so I don't ponder about this one in the future
        pass
    file_path += source_file
    # snag file if not downloaded before
    if not os.path.isfile(file_path):
        common_network.mk_network_fetch_from_url(url + source_file, file_path)
    return file_path
