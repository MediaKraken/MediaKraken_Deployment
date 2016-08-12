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
import logging
import json
from xml.dom import minidom
import common.common_file
import common.common_Metadata
import common.common_network
from pytvdbapi import api


class CommonTheTVDB(object):
    """
    Class for interfacing with theTVDB
    """
    def __init__(self):
        # pull in the ini file config
        import ConfigParser
        Config = ConfigParser.ConfigParser()
        Config.read("MediaKraken.ini")
        # setup connection
        self.tvdb_connection = api.TVDB(Config.get('API', 'theTVdb').strip(), actors=True,\
            ignore_case=True)


    # get show information
    def com_thetvdb_show_info(self, show_title, show_language):
        return com_thetvdb_Show_Details(com_thetvdb_Search(self.tvdb_connection,\
            show_title, show_language))


    # search for show
    def com_thetvdb_Search(self, show_title, show_year, show_id, show_language, save_db=True):
        if show_id is not None:
            show_data = self.tvdb_connection.get_series(show_id, show_language)
        else:
            if show_year is not None:
                logging.debug("bah2 %s", show_title + ' ' + str(show_year))
                # this generally fails if I include year....
                show_data = self.tvdb_connection.search(show_title, show_language)
            else:
                show_data = self.tvdb_connection.search(show_title, show_language)
        logging.debug("tvdb search: %s", show_data)
        if len(show_data) > 0:
            show = show_data[0]
            return show.SeriesID
            #show.update()
#            # save to local cache for future reference
#            if save_db:
#                metadata_uuid = com_thetvdb_Show_DB_Save(show)
#                return metadata_uuid
#            else:
#                show_dict = com_thetvdb_Show_Details(show_data)
#                com_file.com_file_Save_Data('./cache/' + show_title + '.dat', show_dict, True)
#                return show_dict
        return None


    # save entire show info
    def com_thetvdb_show_db_save(self, show_data):
        show_data.update()
        # store the show data
        json_media_id = json.dumps({'IMDB':show_data.IMDB_ID, 'theTVDB':show_data.SeriesID,
            'zap2it':show_data.zap2it_id})
        # start saving pictures (if available)
        banner_path = None
        fanart_path = None
        poster_path = None
        json_media_json = json.dumps({'Overview':show_data.Overview,\
            'AliasNames':show_data.AliasNames, 'Language':show_data.language,\
            'FirstAired':show_data.FirstAired, 'Status':show_data.Status,\
            'ContentRating':show_data.ContentRating, 'Rating':show_data.Rating,\
            'RatingCount':show_data.RatingCount, 'Airs_DayOfWeek':show_data.Airs_DayOfWeek,\
            'Airs_Time':show_data.Airs_Time, 'Runtime':show_data.Runtime,\
            'LastUpdate':show_data.lastupdated, 'Network':show_data.Network,\
            'Network_ID_thetvdb':show_data.NetworkID})

    #    print "show:",show.seriesid,show.id
    #    print "genre", show.Genre
    #    print "act:", show.actor_objects
    #    print "banner:", show.banner_objects
    #    print "lang:", show.lang

        # download the images if links exist
        update_json = False
        banner_path, fanart_path, poster_path = None
        if len(show_data.banner) > 0:
            banner_path = com_Metadata.com_MetaData_Image_Path(show_data.SeriesName,\
                'banner', 'thetvdb', show_data.banner)
            update_json = True
        if len(show_data.fanart) > 0:
            fanart_path = com_Metadata.com_MetaData_Image_Path(show_data.SeriesName,\
                'fanart', 'thetvdb', show_data.fanart)
            update_json = True
        if len(show_data.poster) > 0:
            poster_path = com_Metadata.com_MetaData_Image_Path(show_data.SeriesName,\
                'poster', 'thetvdb', show_data.poster)
            update_json = True
        if update_json:
            json_media_json.update({'LocalImages':{'Banner':banner_path, 'Fanart':fanart_path,\
                'Poster':poster_path}})
        # save the show data
        com_Database.srv_db_Metadata_Save_Show(show_data.SeriesName,
            json_media_id, json_media_json)

        # store the season data
    # atm not using season data anyways
    #    json_media_id = json.dumps({'IMDB':'', 'theTVDB':'', 'TMDB':'', 'AniDB':'', 'RT':'', 'OpenMovieDB':'', 'FanArt':'', 'ScreenGrabber':'', 'zap2it':''})
    #    srv_db_Metadata_Save_Season(self,season_json):
    #    sql_params = str(uuid.uuid4()),season_json
    #    self.sql3_cursor.execute('insert into mm_media_seasons (mm_media_seasons_guid, mm_media_season_json) values (%s,%s)',sql_params)

        # store the episode data
        json_media_id = json.dumps({'IMDB':'', 'theTVDB':'', 'TMDB':'', 'AniDB':'', 'RT':'',\
            'OpenMovieDB':'', 'FanArt':'', 'ScreenGrabber':'', 'zap2it':''})
    #    srv_db_Metadata_Save_Episode(self,episode_id_json, episode_name, episode_json)
    #    sql_params = str(uuid.uuid4()),episode_id_json, episode_name, episode_json
    #    self.sql3_cursor.execute('insert into mm_metadata (mm_metadata_guid, mm_metadata_media_id, mm_media_name, mm_metadata_json) values (%s,%s,%s,%s)',sql_params)
        return metadata_uuid



    # get episode information
    def com_thetvdb_episode_info(self, show_language, episode_id):
        return self.tvdb_connection.get_episode(show_language, episodeid=episode_id)


    # get episode information by season and episode
    def com_thetvdb_season_episode_info(self, show_language, season_no, ep_no, show_id):
        return self.tvdb_connection.get_episode(show_language, season_no, ep_no, show_id)


    # show data from result
    def com_thetvdb_show_details(self, show_data):
        show_dict = {}
        show = show_data[0]
        show_number_seasons = len(show)
        # loop through the season
        for show_ndx in range(0, show_number_seasons):
            season = show[show_ndx]
            show_number_episodes = len(season)
            # loop through the episodes
            for ep_ndx in range(0, show_number_episodes):
                episode = season[ep_ndx]
                logging.debug(episode.EpisodeNumber)
                logging.debug(episode.EpisodeName)
        return show_dict
