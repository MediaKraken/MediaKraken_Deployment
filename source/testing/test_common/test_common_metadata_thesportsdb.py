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

import sys

import pytest  # pylint: disable=W0611

sys.path.append('.')
from common import common_config_ini
from common import common_metadata_thesportsdb


class TestCommonMetadatathesportsdb:

    @classmethod
    def setup_class(self):
        # open the database
        option_config_json, db_connection = common_config_ini.com_config_read(db_prod=False)
        self.db_connection = common_metadata_thesportsdb.CommonMetadataTheSportsDB(
            option_config_json)

    @classmethod
    def teardown_class(self):
        pass

    # team and player looksup
    @pytest.mark.parametrize(("team_name"), [
        ('Pacers'),
        ('Dallas Cowboys'),
        ('fakename')])
    def test_com_meta_thesportsdb_search_team_by_name(self, team_name):
        """
        Test function
        """
        self.db_connection.com_meta_thesportsdb_search_team_by_name(team_name)

    @pytest.mark.parametrize(("team_name"), [
        ('Pacers'),
        ('Dallas Cowboys'),
        ('fakename')])
    def test_com_meta_thesportsdb_search_players_by_team(self, team_name):
        """
        Test function
        """
        self.db_connection.com_meta_thesportsdb_search_players_by_team(
            team_name)

# def com_meta_thesportsdb_Search_Players_by_Name(self, player_name):


# def com_meta_thesportsdb_Search_Players_by_Team_And_Player_Name(self, team_name, player_name):


# event lookups
# def com_meta_thesportsdb_Search_Event_by_Name(self, event_name):


# Search for event by event file name
# thesportsdb.com/api/v1/json/{APIKEY}/searchfilename.php?e={league}{date}{hometeam} vs {awayteam}
# http://www.thesportsdb.com/api/v1/json/1/searchfilename.php?e=English_Premier_League_2015-04-26_Arsenal_vs_Chelsea

# Search for event by event name and season
# thesportsdb.com/api/v1/json/{APIKEY}/searchevents.php?e={eventname}&s={seasonstring}
# http://www.thesportsdb.com/api/v1/json/1/searchevents.php?e=Arsenal_vs_Chelsea&s=1415
#
#
# thesportsdb.com/api/v1/json/{APIKEY}/eventspastleague.php?d={YYYY-MM-DD}&s={sport_string}&l={league_string}
#
# http://www.thesportsdb.com/api/v1/json/1/eventsday.php?d=2014-10-10
# http://www.thesportsdb.com/api/v1/json/1/eventsday.php?d=2014-10-10&s=Soccer
# http://www.thesportsdb.com/api/v1/json/1/eventsday.php?d=2014-10-10&l=Australian_A-League
#
# Events in specific round by season
# thesportsdb.com/api/v1/json/1/eventsround.php?id={leagueid}8&r={round}&s={season}
#
# http://www.thesportsdb.com/api/v1/json/1/eventsround.php?id=4328&r=38&s=1415
#
# All events in specific league by season
# thesportsdb.com/api/v1/json/1/eventsseason.php?id={leagueid}8s={season}


# league lookups

# Search for all Leagues in a country
# thesportsdb.com/api/v1/json/{APIKEY}/search_all_leagues.php?c={countryname}
#
# http://www.thesportsdb.com/api/v1/json/1/search_all_leagues.php?c=England
#
# Search for all Leagues in a country and by sport
# thesportsdb.com/api/v1/json/{APIKEY}/search_all_leagues.php?c={countryname}&s={sportname}
#
# http://www.thesportsdb.com/api/v1/json/1/search_all_leagues.php?c=England&s=Soccer
#
# Search for all Leagues by sport
# thesportsdb.com/api/v1/json/{APIKEY}/search_all_leagues.php?s={sportname}
#
# http://www.thesportsdb.com/api/v1/json/1/search_all_leagues.php?s=soccer
#
# Search for all Teams in a League
# thesportsdb.com/api/v1/json/{APIKEY}/search_all_teams.php?l={leaguename}
#
# http://www.thesportsdb.com/api/v1/json/1/search_all_teams.php?l=English%20Premier%20League
#
# Search for all Teams in a sport by country
# thesportsdb.com/api/v1/json/{APIKEY}/search_all_teams.php?s={sportname}&c={countryname}
#
# http://www.thesportsdb.com/api/v1/json/1/search_all_teams.php?s=Soccer&c=Spain
#
# Search for all the users loved items
# thesportsdb.com/api/v1/json/{APIKEY}/searchloves.php?u={username}
#
# http://www.thesportsdb.com/api/v1/json/1/searchloves.php?u=zag
#
# Search for all Seasons in a League
# thesportsdb.com/api/v1/json/{APIKEY}/search_all_seasons.php?id={leagueid}
#
# http://www.thesportsdb.com/api/v1/json/1/search_all_seasons.php?id=4328


# League Details by Id
# thesportsdb.com/api/v1/json/{APIKEY}/lookupleague.php?id={leagueid}
#
# http://www.thesportsdb.com/api/v1/json/1/lookupleague.php?id=4346
#
# League seasons by league Id
# thesportsdb.com/api/v1/json/{APIKEY}/lookupleague.php?id={leagueid}&s=all
#
# http://www.thesportsdb.com/api/v1/json/1/lookupleague.php?id=4346&s=all
#
# Team Details by Id
# thesportsdb.com/api/v1/json/{APIKEY}/lookupteam.php?id={teamid}
#
# http://www.thesportsdb.com/api/v1/json/1/lookupteam.php?id=133604
#
# Player Details by Id
# thesportsdb.com/api/v1/json/{APIKEY}/lookuplayer.php?id={playerid}
#
# http://www.thesportsdb.com/api/v1/json/1/lookupplayer.php?id=34145937
#
# Event Details by Id
# thesportsdb.com/api/v1/json/{APIKEY}/lookuevent.php?id={eventid}
#
# http://www.thesportsdb.com/api/v1/json/1/lookupevent.php?id=441613
#
# All teams in a league by League Id
# thesportsdb.com/api/v1/json/{APIKEY}/lookup_all_teams.php?id={leagueid}
#
# http://www.thesportsdb.com/api/v1/json/1/lookup_all_teams.php?id=4328
#
# All players in a team by Team Id
# thesportsdb.com/api/v1/json/{APIKEY}/lookup_all_players.php?id={teamid}

# http://www.thesportsdb.com/api/v1/json/1/lookup_all_players.php?id=133604
#
# Lookup Table by League ID and Season
# thesportsdb.com/api/v1/json/{APIKEY}/lookuptable.php?l={leagueid}&s={season}
#
#
# Schedules lookups
#
# Next 5 Events by Team Id
# thesportsdb.com/api/v1/json/{APIKEY}/eventsnext.php?id={teamid}
#
# http://www.thesportsdb.com/api/v1/json/1/eventsnext.php?id=133602
#
# Next 15 Events by League Id
# thesportsdb.com/api/v1/json/{APIKEY}/eventsnextleague.php?id={leagueid}
#
# http://www.thesportsdb.com/api/v1/json/1/eventsnextleague.php?id=4328
#
# Next 15 Events by League Id and Round
# thesportsdb.com/api/v1/json/{APIKEY}/eventsnextleague.php?id={leagueid}&r={round}
#
# http://www.thesportsdb.com/api/v1/json/1/eventsnextleague.php?id=4328&r=38
#
# Last 5 Events by Team Id
# thesportsdb.com/api/v1/json/{APIKEY}/eventslast.php?id={teamid}
#
# http://www.thesportsdb.com/api/v1/json/1/eventslast.php?id=133602
#
# Last 15 Events by League Id
# thesportsdb.com/api/v1/json/{APIKEY}/eventspastleague.php?id={leagueid}

# http://www.thesportsdb.com/api/v1/json/1/eventspastleague.php?id=4328


# Images

# Preview Images
# Most of the time you won't want to download the original large image, just get a small preview. This is possible simple by adding "/preview" onto the end URL. This will give you a small 200px version. This will work with JPG images only.
#
# Original Image - http://www.thesportsdb.com/images/media/league/fanart/xpwsrw1421853005.jpg
# Small Image - http://www.thesportsdb.com/images/media/league/fanart/xpwsrw1421853005.jpg/preview
#
#    # Livescores
#
# Soccer Livescores
# thesportsdb.com/api/v1/json/{APIKEY}/latestsoccer.php
# http://www.thesportsdb.com/api/v1/json/1/latestsoccer.php
# NOTE: Updated every 5mins
