"""
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
"""

from enum import unique, IntFlag

# instance for elastisearch
es_inst = None

# clients connected to server available for playback
client_devices = []

# store pids of things running
pid_dict = {}


@unique
class DLMediaType(IntFlag):
    Movie = 1
    TV = 2
    Person = 3
    Sports = 4
    Game = 5
    Publication = 6
    Picture = 7
    Anime = 8
    Music = 9
    Adult = 10

    Adult_Image = 1000
    Adult_Movie = 1001
    Adult_Scene = 1002

    Game_CHD = 501
    Game_Cinematics = 502
    Game_Intro = 503
    Game_ISO = 504
    Game_ROM = 505
    Game_Speedrun = 506
    Game_Superplay = 507

    Movie_Home = 111
    Movie_Extras = 112
    Movie_Soundtrack = 113
    Movie_Subtitle = 114
    Movie_Theme = 115
    Movie_Trailer = 116

    Music_Album = 901
    Music_Lyrics = 902
    Music_Song = 903
    Music_Video = 904

    Publication_Book = 601
    Publication_Comic = 602
    Publication_Comic_Strip = 603
    Publication_Magazine = 604

    TV_Episode = 201
    TV_Extras = 202
    TV_Season = 203
    TV_Subtitle = 204
    TV_Theme = 205
    TV_Trailer = 206
