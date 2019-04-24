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

import os
from pytvdbapi import api

# from xml.dom import minidom
from . import common_global


class CommonTheTVDB(object):
    """
    Class for interfacing with thetvdb
    """

    def __init__(self, option_config_json):
        os.remove('/tmp/pytvdbapi')
        self.tvdb_connection = api.TVDB(option_config_json['API']['thetvdb'], actors=True,
                                        ignore_case=True)

    def com_thetvdb_show_info(self, show_title, show_language='en'):
        """
        # get show information
        """
        return self.com_thetvdb_show_details(self.com_thetvdb_search(self.tvdb_connection,
                                                                     show_title, show_language))

    def com_thetvdb_search(self, show_title, show_year, show_language='en'):
        """
        # search for show
        """
        # TODO deal with year portion of match
        if show_year is not None:
            common_global.es_inst.com_elastic_index('info', {"bah2": show_title + ' ' + str(
                show_year)})
            # this generally fails if I include year....
            show_data = self.tvdb_connection.search(show_title, show_language)
        else:
            show_data = self.tvdb_connection.search(show_title, show_language)
        common_global.es_inst.com_elastic_index('info', {"tvdb search": show_data})
        if len(show_data) > 0:
            show = show_data[0]
            return show.SeriesID
        return None

    #     # save entire show info
    #     def com_thetvdb_show_db_save(self, show_data):
    #         """
    #         # save entire show info
    #         """
    #         show_data.update()
    #         # store the show data
    #         json_media_id = json.dumps({'imdb':show_data.imdb_ID, 'thetvdb':show_data.SeriesID,
    #             'zap2it':show_data.zap2it_id})
    #         # start saving pictures (if available)
    #         banner_path = None
    #         fanart_path = None
    #         poster_path = None
    #         json_media_json = json.dumps({'Overview':show_data.Overview,
    #             'AliasNames':show_data.AliasNames, 'Language':show_data.language,
    #             'FirstAired':show_data.FirstAired, 'Status':show_data.Status,
    #             'ContentRating':show_data.ContentRating, 'Rating':show_data.Rating,
    #             'RatingCount':show_data.RatingCount, 'Airs_DayOfWeek':show_data.Airs_DayOfWeek,
    #             'Airs_Time':show_data.Airs_Time, 'Runtime':show_data.Runtime,
    #             'LastUpdate':show_data.lastupdated, 'Network':show_data.Network,
    #             'Network_ID_thetvdb':show_data.NetworkID})
    #
    #     #    print "show:",show.seriesid,show.id
    #     #    print "genre", show.Genre
    #     #    print "act:", show.actor_objects
    #     #    print "banner:", show.banner_objects
    #     #    print "lang:", show.lang
    #
    #         # download the images if links exist
    #         update_json = False
    #         banner_path, fanart_path, poster_path = None
    #         if len(show_data.banner) > 0:
    #             banner_path = common_metadata.com_meta_image_path(show_data.SeriesName,
    #                 'banner', 'thetvdb', show_data.banner)
    #             update_json = True
    #         if len(show_data.fanart) > 0:
    #             fanart_path = common_metadata.com_meta_image_path(show_data.SeriesName,
    #                 'fanart', 'thetvdb', show_data.fanart)
    #             update_json = True
    #         if len(show_data.poster) > 0:
    #             poster_path = common_metadata.com_meta_image_path(show_data.SeriesName,
    #                 'poster', 'thetvdb', show_data.poster)
    #             update_json = True
    #         if update_json:
    #             json_media_json.update({'LocalImages':{'Banner':banner_path, 'Fanart':fanart_path,
    #                 'Poster':poster_path}})
    #         # save the show data
    #         com_database.db_meta_save_show(show_data.SeriesName,
    #             json_media_id, json_media_json)
    #
    #         # store the season data
    #     # atm not using season data anyways
    #     #    json_media_id = json.dumps({'imdb':'', 'thetvdb':'', 'themoviedb':'', 'anidb':'',\
    # # 'RT':'', 'OpenMovieDB':'', 'FanArt':'', 'ScreenGrabber':'', 'zap2it':''})
    #     #    db_meta_Save_Season(self,season_json):
    #     #    sql_params = str(uuid.uuid4()),season_json
    #     #    self.db_cursor.execute('insert into mm_media_seasons (mm_media_seasons_guid,\
    # # mm_media_season_json) values (%s,%s)',sql_params)
    #
    #         # store the episode data
    #         json_media_id = json.dumps({'imdb':'', 'thetvdb':'', 'themoviedb':'', 'anidb':'', 'rt':'',
    #             'omdb':'', 'fanart':'', 'screengrabber':'', 'zap2it':''})
    #     #    db_meta_Save_Episode(self,episode_id_json, episode_name, episode_json)
    #     #    sql_params = str(uuid.uuid4()),episode_id_json, episode_name, episode_json
    #     #    self.db_cursor.execute('insert into mm_metadata (mm_metadata_guid,\
    #         #mm_metadata_media_id, mm_media_name, mm_metadata_json) values (%s,%s,%s,%s)',sql_params)
    #         return metadata_uuid

    def com_thetvdb_episode_info(self, show_language, episode_id):
        """
        # get episode information
        """
        return self.tvdb_connection.get_episode(show_language, episodeid=episode_id)

    def com_thetvdb_season_episode_info(self, show_language, season_no, ep_no, show_id):
        """
        # get episode information by season and episode
        """
        return self.tvdb_connection.get_episode(show_language, season_no, ep_no, show_id)

    def com_thetvdb_show_details(self, show_data):
        """
        # show data from result
        """
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
                common_global.es_inst.com_elastic_index('info', {'stuff': episode.EpisodeNumber})
                common_global.es_inst.com_elastic_index('info', {'stuff': episode.EpisodeName})
        return show_dict
