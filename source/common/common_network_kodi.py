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

import logging  # pylint: disable=W0611
import socket


# from kodipydent import Kodi
# https://github.com/haikuginger/kodipydent


def com_net_kodi_command(host_ip, host_port, kodi_command):
    """
    # send commands to kodi via raw tcp and json
    """
    kodi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    kodi_socket.connect((host_ip, host_port))
    kodi_socket.sendall(kodi_command.split('|', 1)[1])
    kodi_response = ''
    # if subscript 0 is true then a response is expected
    if kodi_command.split('|', 1)[0]:
        while 1:
            kodi_response += kodi_socket.recv(1024)
            logging.info("kodi response: %s", kodi_response)
            brackets_match = (kodi_response.count('{') - kodi_response.count('}'))
            # if proper termination then exit loop
            if brackets_match == 0:
                break
    kodi_socket.close()
    return kodi_response

# com_net_kodi_command('10.1.0.20', 9090, KODI_SHOW_INFO)


# def com_net_kodi_media_update(db_connection, movie_data=False, collections_data=False,
#                               tv_data=False, music_data=False, music_video_data=False):
#     """
#     return media to kodi plugin
#     """
#     movie_list = []
#     if movie_data:
#         for movie_row in db_connection.db_kodi_user_sync_movie():
#             # title, plot, shortplot, tagline, votecount, rating, writer, year, imdb, sorttitle,
#             # runtime, mpaa, genre, director, studio, trailer, country, movieid, date_added, cast
#             movie_list.append({'title': movie_row[0], 'plot': movie_row[1],
#                                'shortplot': movie_row[2], 'tagline': movie_row[3],
#                                'votecount': movie_row[4], 'rating': movie_row[5],
#                                'writer': movie_row[6], 'year': movie_row[7],
#                                'imdb': movie_row[8], 'sorttitle': movie_row[9],
#                                'runtime': movie_row[10], 'mpaa': movie_row[11],
#                                'genre': movie_row[12], 'director': movie_row[13],
#                                'studio': movie_row[14], 'trailer': movie_row[15],
#                                'country': movie_row[16], 'movieid': movie_row[17],
#                                'date_added': movie_row[18], 'cast': movie_row[19]})
#     collections_list = []
#     if collections_data:
#         for collection_row in db_connection.db_kodi_user_sync_collection():
#             collections_list.append({})
#     tv_list = []
#     if tv_data:
#         for tv_row in db_connection.db_kodi_user_sync_tv_shows():
#             tv_list.append({})
#     music_list = []
#     if music_data:
#         for music_row in db_connection.db_kodi_user_sync_music_songs():
#             music_list.append({})
#     music_video_list = []
#     if music_video_data:
#         for music_video_row in db_connection.db_kodi_user_sync_music_videos():
#             music_video_list.append({})
#
#
# def com_net_kodi_rpc(host_ip):
#     """
#     kodi rpc wrapper
#     """
#     mk_kodi = Kodi(host_ip)
#     # movies = mk_kodi.VideoLibrary.GetMovies()
#     logging.info(mk_kodi)
