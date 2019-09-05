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


# stuff in comments are the old class TEXT
@unique
class DLMediaType(IntFlag):
    Movie = 1  # "Movie"
    TV = 2  # "TV: Show"
    Person = 3

    Sports = 4  # "Sports"
    Game = 5  # "Video Game"
    Publication = 6
    Picture = 7  # "Picture"
    Anime = 8  # "Anime"
    Music = 9  # "Music"
    Adult = 10

    Adult_Image = 1000
    Adult_Movie = 1001  # "Movie: Adult"
    Adult_Scene = 1002

    Game_CHD = 501  # "Game CHD"
    Game_Cinematics = 502
    Game_Intro = 503  # "Video Game: Intro"
    Game_ISO = 504  # "Game ISO"
    Game_ROM = 505  # "Game ROM"
    Game_Speedrun = 506  # "Video Game: Speedrun"
    Game_Superplay = 507  # "Video Game: Superplay"

    Movie_Home = 111  # "Home Movie"
    Movie_Extras = 112  # "Movie: Extras"
    Movie_Soundtrack = 113
    Movie_Subtitle = 114  # "Movie: Subtitle"
    Movie_Theme = 115  # "Movie: Theme"
    Movie_Trailer = 116  # "Movie: Trailer"

    Music_Album = 901  # "Music Album"
    Music_Lyrics = 902  # "Music Lyric"
    Music_Song = 903
    Music_Video = 904  # "Music Video"

    Publication_Book = 601  # "Book"
    Publication_Comic = 602  # "Comic"
    Publication_Comic_Strip = 603  # "Comic Strip"
    Publication_Magazine = 604  # "Magazine"

    TV_Episode = 201  # "TV: Episode"
    TV_Extras = 202  # "TV: Extras"
    TV_Season = 203  # "TV: Season"
    TV_Subtitle = 204  # "TV: Subtitle"
    TV_Theme = 205  # "TV: Theme"
    TV_Trailer = 206  # "TV: Trailer"
