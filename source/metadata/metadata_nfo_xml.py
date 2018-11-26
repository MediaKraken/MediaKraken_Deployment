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

import os

import xmltodict
from common import common_file
from common import common_file_extentions
from common import common_global


def nfo_xml_file(media_file_path):
    """
    Find and load nfo and xml file(s) if they exist
    """
    xml_data = None
    # check for NFO or XML as no need to do lookup if ID found in it
    try:  # pull the "real" extension
        ext_check = media_file_path[-4:].lower().split(".")[-1]
    except:
        ext_check = None
    if ext_check in common_file_extentions.SUBTITLE_EXTENSION:
        # need to chop off the lang too, the split works even with no .lang in name
        nfo_file_check = media_file_path.rsplit('.', 2)[0] + '.nfo'
        xml_file_name = media_file_path.rsplit('.', 2)[0] + '.xml'
    else:  # not a subtitle, should be a "normal" file
        nfo_file_check = media_file_path.rsplit('.', 1)[0] + '.nfo'
        xml_file_name = media_file_path.rsplit('.', 1)[0] + '.xml'
    if os.path.isfile(nfo_file_check):  # check for nfo
        common_global.es_inst.com_elastic_index('info', {'nfo file found': nfo_file_check})
        nfo_data = xmltodict.parse(common_file.com_file_load_data(nfo_file_check, False))
    else:
        nfo_data = None
        # only check for xml if nfo doesn't exist
        if os.path.isfile(xml_file_name):  # check for xml
            common_global.es_inst.com_elastic_index('info', {'xml file found': xml_file_name})
            xml_data = xmltodict.parse(common_file.com_file_load_data(xml_file_name, False))
        elif os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(media_file_path)), 'movie.xml')):
            common_global.es_inst.com_elastic_index('info', {'movie xml file found': xml_file_name})
            xml_data = xmltodict.parse(common_file.com_file_load_data(os.path.join(
                os.path.dirname(os.path.abspath(media_file_path)), 'movie.xml'), False))
    return nfo_data, xml_data


def nfo_xml_file_tv(media_file_path):
    """
    Find and load nfo and xml file(s) if they exist
    """
    xml_data = None
    # check for NFO or XML as no need to do lookup if ID found in it
    # TODO should check for one dir back too I spose
    if media_file_path.find('/') != -1:
        nfo_file_check = media_file_path.rsplit('/', 1)[0] + 'tvinfo.nfo'
    else:
        nfo_file_check = media_file_path.rsplit('\\', 1)[0] + 'tvinfo.nfo'
    if os.path.isfile(nfo_file_check):  # check for nfo
        common_global.es_inst.com_elastic_index('info', {'nfo tv file found': nfo_file_check})
        nfo_data = xmltodict.parse(
            common_file.com_file_load_data(nfo_file_check, False))
    else:
        nfo_data = None
    return nfo_data, xml_data


def nfo_xml_id_lookup(nfo_data, xml_data):
    """
    Lookup by id's in nfo/xml files
    """
    imdb_id = None
    tmdb_id = None
    rt_id = None
    # load both fields for more data in media_id_json on db
    if nfo_data is not None:
        try:  # not all will have imdb
            imdb_id = nfo_data['movie']['imdbid']
            if len(imdb_id) == 0:
                imdb_id = None
        except:
            pass
        try:  # not all nfo's have the movie/tmdb
            tmdb_id = nfo_data['movie']['tmdbid']
            if len(tmdb_id) == 0:
                tmdb_id = None
        except:
            pass
        # TODO RT
        try:  # not all nfo's have the rt
            rt_id = nfo_data['movie']['fakert']
            if len(rt_id) == 0:
                rt_id = None
        except:
            pass
    if xml_data is not None:
        if 'movie' in xml_data:  # standard nfo/xml file
            if imdb_id is None:
                try:  # not all xmls's will have the imdb
                    imdb_id = xml_data['movie']['imdbid']
                    if len(imdb_id) == 0:
                        imdb_id = None
                except:
                    pass
            if tmdb_id is None:
                try:  # not all xml's have the movie/tmdb
                    tmdb_id = xml_data['movie']['tmdbid']
                    if len(tmdb_id) == 0:
                        tmdb_id = None
                except:
                    pass
            # TODO RT
            if rt_id is None:
                try:  # not all xml's have the rt
                    rt_id = xml_data['movie']['fakert']
                    if len(rt_id) == 0:
                        rt_id = None
                except:
                    pass
        else:  # movie.xml
            if imdb_id is None:
                try:  # not all xmls's will have the imdb
                    imdb_id = xml_data['Title']['IMDB']
                    if len(imdb_id) == 0:
                        imdb_id = None
                except:
                    pass
            if tmdb_id is None:
                try:  # not all xml's have the movie/tmdb
                    tmdb_id = xml_data['Title']['TMDbId']
                    if len(tmdb_id) == 0:
                        tmdb_id = None
                except:
                    pass
            # TODO RT
            if rt_id is None:
                try:  # not all xml's have the rt
                    rt_id = xml_data['Title']['RottenTomatoesId']
                    if len(rt_id) == 0:
                        rt_id = None
                except:
                    pass
    common_global.es_inst.com_elastic_index('info', {'nfo/xml imdb': imdb_id, 'tmdb': tmdb_id,
                                                     'rt': rt_id})
    return (imdb_id, tmdb_id, rt_id)


def nfo_xml_id_lookup_tv(nfo_data, xml_data):
    """
    Look up id's in nfo/xml lookup for tv
    """
    imdb_id = None
    tvdb_id = None
    rt_id = None
    # load both fields for more data in media_id_json on db
    if nfo_data is not None:
        try:
            tvdb_id = nfo_data['episodedetails']['tvdbid']
            if len(tvdb_id) == 0:
                tvdb_id = None
        except:
            pass
        try:
            imdb_id = nfo_data['episodedetails']['imdbid']
            if len(imdb_id) == 0:
                imdb_id = None
        except:
            pass
        # TODO RT
        try:
            rt_id = nfo_data['episodedetails']['fakert']
            if len(rt_id) == 0:
                rt_id = None
        except:
            pass
    if xml_data is not None:
        try:
            tvdb_id = xml_data['episodedetails']['tvdbid']
            if len(tvdb_id) == 0:
                tvdb_id = None
        except:
            pass
        try:
            imdb_id = xml_data['episodedetails']['imdbid']
            if len(imdb_id) == 0:
                imdb_id = None
        except:
            pass
        # TODO RT
        try:
            rt_id = xml_data['episodedetails']['fakert']
            if len(rt_id) == 0:
                rt_id = None
        except:
            pass
    common_global.es_inst.com_elastic_index('info', {'nfo/xml tv imdb': imdb_id, 'tvdb': tvdb_id,
                                                     'rt': rt_id})
    return (imdb_id, tvdb_id, rt_id)
