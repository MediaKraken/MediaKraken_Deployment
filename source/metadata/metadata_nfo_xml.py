"""
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
"""

import inspect
import os
import pathlib
import xml

import xmltodict
from common import common_file
from common import common_file_extentions
from common import common_logging_elasticsearch_httpx


async def nfo_xml_file(media_file_path):
    """
    Find and load nfo and xml file(s) if they exist
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    nfo_data = None
    xml_data = None
    # check for NFO or XML as no need to do lookup if ID found in it
    # pull the "real" extension
    ext_check = pathlib.Path(media_file_path).suffix.lower()
    if ext_check in common_file_extentions.SUBTITLE_EXTENSION:
        # need to chop off the lang too, the split works even with no .lang in name
        nfo_file_check = media_file_path.rsplit('.', 2)[0] + '.nfo'
        xml_file_name = media_file_path.rsplit('.', 2)[0] + '.xml'
    else:  # not a subtitle, should be a "normal" file
        nfo_file_check = media_file_path.rsplit('.', 1)[0] + '.nfo'
        xml_file_name = media_file_path.rsplit('.', 1)[0] + '.xml'
    if os.path.isfile(nfo_file_check):  # check for nfo
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'nfo file found': nfo_file_check})
        try:
            nfo_data = xmltodict.parse(common_file.com_file_load_data(nfo_file_check, False))
        except xml.parsers.expat.ExpatError:
            pass
        except UnicodeDecodeError:
            pass
    else:
        # only check for xml if nfo doesn't exist
        if os.path.isfile(xml_file_name):  # check for xml
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 'xml file found': xml_file_name})
            try:
                xml_data = xmltodict.parse(common_file.com_file_load_data(xml_file_name, False))
            except xml.parsers.expat.ExpatError:
                pass
            except UnicodeDecodeError:
                pass
        elif os.path.isfile(
                os.path.join(os.path.dirname(os.path.abspath(media_file_path)), 'movie.xml')):
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 'movie xml file found': xml_file_name})
            try:
                xml_data = xmltodict.parse(common_file.com_file_load_data(os.path.join(
                    os.path.dirname(os.path.abspath(media_file_path)), 'movie.xml'), False))
            except xml.parsers.expat.ExpatError:
                pass
            except UnicodeDecodeError:
                pass
    return nfo_data, xml_data


async def nfo_file_tv(media_file_path):
    """
    Find and load nfo and xml file(s) if they exist
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    nfo_data = None
    # check for NFO or XML as no need to do lookup if ID found in it
    # TODO should check for one dir back too I suppose
    nfo_file_check = media_file_path.rsplit('/', 1)[0] + 'tvinfo.nfo'
    if os.path.isfile(nfo_file_check):  # check for nfo
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                         message_text={
                                                                             'nfo tv file found': nfo_file_check})
        try:
            nfo_data = xmltodict.parse(common_file.com_file_load_data(nfo_file_check, False))
        except xml.parsers.expat.ExpatError:
            pass
        except UnicodeDecodeError:
            pass
    else:
        nfo_file_check = media_file_path.rsplit('/', 1)[0] + 'tvshow.nfo'
        if os.path.isfile(nfo_file_check):  # check for nfo
            await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                             message_text={
                                                                                 'nfo tv file found2': nfo_file_check})
            try:
                nfo_data = xmltodict.parse(common_file.com_file_load_data(nfo_file_check, False))
            except xml.parsers.expat.ExpatError:
                pass
            except UnicodeDecodeError:
                pass
    return nfo_data


async def nfo_xml_id_lookup(nfo_data, xml_data):
    """
    Lookup by id's in nfo/xml files
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    imdb_id = None
    tmdb_id = None
    # load both fields for more data in media_id_json on db
    if nfo_data is not None:
        try:  # not all will have imdb
            imdb_id = nfo_data['movie']['imdbid']
            if len(imdb_id) == 0:
                imdb_id = None
        except KeyError:
            pass
        try:  # not all nfo's have the movie/tmdb
            tmdb_id = nfo_data['movie']['tmdbid']
            if len(tmdb_id) == 0:
                tmdb_id = None
        except KeyError:
            pass
    if xml_data is not None:
        if 'movie' in xml_data:  # standard nfo/xml file
            if imdb_id is None:
                try:  # not all xmls's will have the imdb
                    imdb_id = xml_data['movie']['imdbid']
                    if len(imdb_id) == 0:
                        imdb_id = None
                except KeyError:
                    pass
            if tmdb_id is None:
                try:  # not all xml's have the movie/tmdb
                    tmdb_id = xml_data['movie']['tmdbid']
                    if len(tmdb_id) == 0:
                        tmdb_id = None
                except KeyError:
                    pass
        else:  # movie.xml
            if imdb_id is None:
                try:  # not all xmls's will have the imdb
                    imdb_id = xml_data['Title']['IMDB']
                    if len(imdb_id) == 0:
                        imdb_id = None
                except KeyError:
                    pass
            if tmdb_id is None:
                try:  # not all xml's have the movie/tmdb
                    tmdb_id = xml_data['Title']['TMDbId']
                    if len(tmdb_id) == 0:
                        tmdb_id = None
                except:
                    pass
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'nfo/xml imdb': imdb_id,
                                                                         'tmdb': tmdb_id})
    return imdb_id, tmdb_id


async def nfo_id_lookup_tv(nfo_data):
    """
    Look up id's in nfo/xml lookup for tv
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][3]})
    imdb_id = None
    tvdb_id = None
    tmdb_id = None
    # load both fields for more data in media_id_json on db
    if nfo_data is not None:
        try:
            tvdb_id = nfo_data['episodedetails']['tvdbid']
            if len(tvdb_id) == 0:
                tvdb_id = None
        except KeyError:
            pass
        try:
            tmdb_id = nfo_data['episodedetails']['tmdbid']
            if len(tmdb_id) == 0:
                tmdb_id = None
        except KeyError:
            pass
        try:
            imdb_id = nfo_data['episodedetails']['imdbid']
            if len(imdb_id) == 0:
                imdb_id = None
        except KeyError:
            pass
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'nfo tv imdb': imdb_id,
                                                                         'tvdb': tvdb_id,
                                                                         'tmdb': tmdb_id})
    return imdb_id, tvdb_id, tmdb_id
