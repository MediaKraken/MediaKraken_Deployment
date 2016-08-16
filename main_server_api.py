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

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
try:
    import cPickle as pickle
except:
    import pickle
from twisted.web.static import File
from klein import Klein
import json
import datetime
import signal
import sys
sys.path.append("./common")
sys.path.append("./server")
from common import common_logging
import database as database_base


__version__ = json.dumps({"Version": "0.1.6"})


def signal_receive(signum, frame):
    print('CHILD Main API: Received USR1')
    sys.stdout.flush()
    sys.exit(0)


class MediaKrakenAPI(object):
    app = Klein()


    def __init__(self):
        self.db_connection = database_base.MKServerDatabase()
        self.db_connection.srv_db_open(Config.get('DB Connections', 'PostDBHost').strip(),\
            Config.get('DB Connections', 'PostDBPort').strip(),\
            Config.get('DB Connections', 'PostDBName').strip(),\
            Config.get('DB Connections', 'PostDBUser').strip(),\
            Config.get('DB Connections', 'PostDBPass').strip())
        self.user_xref = []
        # start logging
        common_logging.com_logging_start('./log/MediaKraken_API')


    @app.route('/')
    def home(self, request):
        return __version__

    # shows and all the subroutes
    with app.subroute("/Artists") as app:
        @app.route("/")
        def artists(self, request):
            return None


    # channels and all the subroutes
    with app.subroute("/Channels") as app:
        @app.route("/")
        def artists(self, request):
            return None


    # items and all the subroutes
    with app.subroute("/Items") as app:
        @app.route("/ThemeVideos")
        def items_themevideos(self, request):
            return None


        @app.route("/ThemeSongs")
        def items_themesongs(self, request):
            return None


    # livetv and all the subroutes
    with app.subroute("/LiveTv") as app:
        @app.route("/Channels")
        def livetv_channels(self, request):
            return None


        @app.route("/Recordings")
        def livetv_recordings(self, request):
            return None


    # Users and all the subroutes
    with app.subroute("/Users") as app:
        @app.route("/AuthenticateByName")
        def user_authenticate(self, request):
            logging.debug("req: %s", request.content.getvalue())
            # {"username": "quinn", "password": "da39a3ee5e6b4b0d3255bfef95601890afd80709"}
            return pickle.dumps(self.db_connection.srv_db_User_Login_Kodi(request.content.getvalue()))


        @app.route("/FavoriteItems")
        def user_favorite(self, request):
            return None


        @app.route("/Items/<guid>")
        def user_items(self, request, guid):
            #json_data = db.
            return None


        @app.route("/ItemsSync/<synctime>")
        def user_items_sync(self, request, synctime):
            logggin.debug("req: %s", request.content.getvalue())
            items_added = []
            for row_data in self.db_connection.srv_db_Kodi_User_Sync_List_Added(synctime):
                items_added.append(row_data[0])
            sync_json = {"ItemsAdded": items_added, "ItemsRemoved": [""], "ItemsUpdated": [""],\
                "UserDataChanged": [{"Rating": 0, "PlayedPercentage": 0,\
                "UnplayedItemCount": "int", "PlaybackPositionTicks": "long", "PlayCount": "int",\
                "IsFavorite": False, "Likes": False, "LastPlayedDate": "Date", "Played": False,\
                "Key": "", "ItemId": ""}]}
            return pickle.dumps(sync_json)


        @app.route("/PlayedItems")
        def user_played_items(self, request):
            return None


        @app.route("/Pref/<guid>")
        def user_pref(self, request, guid):
            logging.debug("reqpref:", request.content.getvalue(), guid)
            json_data = {
                  "Name": "",
                  "ServerId": "",
                  "ServerName": "",
#                  "ConnectUserName": "",
#                  "ConnectUserId": "",
#                  "ConnectLinkType": "",
                  "Id": "",
                  "OfflinePassword": "",
                  "OfflinePasswordSalt": "",
                  "PrimaryImageTag": "",
                  "HasPassword": False,
                  "HasConfiguredPassword": False,
                  "HasConfiguredEasyPassword": False,
                  "LastLoginDate": "Date",
                  "LastActivityDate": "Date",
                  "Configuration": {
                    "AudioLanguagePreference": "",
                    "PlayDefaultAudioTrack": False,
                    "SubtitleLanguagePreference": "",
                    "DisplayMissingEpisodes": False,
                    "DisplayUnairedEpisodes": False,
                    "GroupMoviesIntoBoxSets": False,
                    "ExcludeFoldersFromGrouping": [
                      ""
                    ],
                    "GroupedFolders": [
                      ""
                    ],
                    "SubtitleMode": "",
                    "DisplayCollectionsView": False,
                    "DisplayFoldersView": False,
                    "EnableLocalPassword": False,
                    "OrderedViews": [
                      ""
                    ],
                    "IncludeTrailersInSuggestions": False,
                    "EnableCinemaMode": False,
                    "LatestItemsExcludes": [
                      ""
                    ],
                    "PlainFolderViews": [
                      ""
                    ],
                    "HidePlayedInLatest": False,
                    "DisplayChannelsInline": False
                  },
                  "Policy": {
                    "IsAdministrator": False,
                    "IsHidden": False,
                    "IsDisabled": False,
                    "MaxParentalRating": "int",
                    "BlockedTags": [
                      ""
                    ],
                    "EnableUserPreferenceAccess": False,
                    "AccessSchedules": [
                      {
                        "DayOfWeek": "",
                        "StartHour": 0,
                        "EndHour": 0
                      }
                    ],
                    "BlockUnratedItems": [
                      "POST_UnratedItem/emby/emby/Users/{Id}"
                    ],
                    "EnableRemoteControlOfOtherUsers": False,
                    "EnableSharedDeviceControl": False,
                    "EnableLiveTvManagement": False,
                    "EnableLiveTvAccess": False,
                    "EnableMediaPlayback": False,
                    "EnableAudioPlaybackTranscoding": False,
                    "EnableVideoPlaybackTranscoding": False,
                    "EnableContentDeletion": False,
                    "EnableContentDownloading": False,
                    "EnableSync": False,
                    "EnableSyncTranscoding": False,
                    "EnabledDevices": [
                      ""
                    ],
                    "EnableAllDevices": False,
                    "EnabledChannels": [
                      ""
                    ],
                    "EnableAllChannels": False,
                    "EnabledFolders": [
                      ""
                    ],
                    "EnableAllFolders": False,
                    "InvalidLoginAttemptCount": 0,
                    "EnablePublicSharing": False,
                    "BlockedMediaFolders": [
                      ""
                    ],
                    "BlockedChannels": [
                      ""
                    ]
                  },
                  "PrimaryImageAspectRatio": 0,
                  "HasPrimaryImage": False
                }
            return pickle.dumps(json.dumps(json_data))


        @app.route("/Public")
        def user_public(self, request):
            user_data = []
            for row_data in self.db_connection.srv_db_User_List_Name(None, None):
                user_data.append((row_data[0], row_data[1], None))
            logging.debug("userdat: %s", user_data)
            return pickle.dumps(user_data)


        @app.route("/Views/<guid>")
        def user_favorite(self, request, guid):
            json_data = {'Items': {}}
            return pickle.dumps(json.dumps(json_data))


    # session and all the subroutes
    with app.subroute("/Sessions") as app:
        @app.route("/User")
        def session_users(self, request):
            return None


        @app.route("/Capabilities/Full")
        def session_capabilities(self, request):
            return None


    # shows and all the subroutes
    with app.subroute("/Shows") as app:
        @app.route("/Seasons")
        def show_seasons(self, request):
            return None


    # system and all the subroutes
    with app.subroute("/System") as app:
        @app.route("/Configuration")
        def system_configuration(self, request):
            options_json, status_json = self.db_connection.srv_db_Option_Status_Read()
            loggin.debug("otions: %s", options_json)
            return str(options_json['MaxResumePct'])


        @app.route("/GetServerDateTime")
        def system_datetime(self, request):
            return pickle.dumps(datetime.utcnow())


    # video and all the subroutes
    with app.subroute("/Videos") as app:
        @app.route("/AdditionalParts")
        def video_additional_parts(self, request):
            return None


    ## would show static dir list
    #@app.route('/', branch=True)
    #def pg_index(request):
    #    return File('./')


if __name__ == '__main__':
    if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
        signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
    else:
        signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
        signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c
    run_api = MediaKrakenAPI()
    run_api.app.run("localhost", int(Config.get('MediaKrakenServer', 'APIPort').strip()))
