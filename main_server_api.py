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
import logging # pylint: disable=W0611
try:
    import cPickle as pickle
except:
    import pickle
from twisted.web.static import File
from klein import Klein
import json
import datetime
from common import common_config_ini
from common import common_logging
from common import common_signal
from common import common_version


class MediaKrakenAPI(object):
    app = Klein()


    def __init__(self):
        # open the database
        self.config_handle, self.option_config_json,\
            self.db_connection = common_config_ini.com_config_read()
        self.user_xref = []
        # start logging
        common_logging.com_logging_start('./log/MediaKraken_API')


    @app.route('/')
    def home(self, request):
        return common_version.APP_VERSION

    # shows and all the subroutes
    with app.subroute("/Artists") as app:
        @app.route("/")
        def artists(self, request):
            return None


    # channels and all the subroutes
    with app.subroute("/Channels") as app:
        @app.route("/")
        def channels(self, request):
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
            logging.info("req: %s", request.content.getvalue())
            # {"username": "quinn", "password": "da39a3ee5e6b4b0d3255bfef95601890afd80709"}
            return pickle.dumps(self.db_connection.db_user_login_kodi(request.content.getvalue()))


        @app.route("/FavoriteItems")
        def user_favorite(self, request):
            return None


        @app.route("/Items/<guid>")
        def user_items(self, request, guid):
            #json_data = db_connection.
            return None


        @app.route("/ItemsSync/<synctime>")
        def user_items_sync(self, request, synctime):
            logging.info("req: %s", request.content.getvalue())
            items_added = []
            for row_data in self.db_connection.db_kodi_user_sync_list_added(synctime):
                items_added.append(row_data[0])
            sync_json = {"ItemsAdded": items_added, "ItemsRemoved": [""], "ItemsUpdated": [""],
                "UserDataChanged": [{"Rating": 0, "PlayedPercentage": 0,
                "UnplayedItemCount": "int", "PlaybackPositionTicks": "long", "PlayCount": "int",
                "IsFavorite": False, "Likes": False, "LastPlayedDate": "Date", "Played": False,
                "Key": "", "ItemId": ""}]}
            return pickle.dumps(sync_json)


        @app.route("/PlayedItems")
        def user_played_items(self, request):
            return None


        @app.route("/Pref/<guid>")
        def user_pref(self, request, guid):
            logging.info("reqpref: %s %s", request.content.getvalue(), guid)
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
            for row_data in self.db_connection.db_user_list_name(None, None):
                user_data.append((row_data[0], row_data[1], None))
            logging.info("userdat: %s", user_data)
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
            options_json, status_json = self.db_connection.db_opt_status_read()
            logging.info("otions: %s", options_json)
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
    # set signal exit breaks
    common_signal.com_signal_set_break()
    option_config_json, db_connection = common_config_ini.com_config_read()
    run_api = MediaKrakenAPI()
    run_api.app.run("localhost", int(option_config_json['MediaKrakenServer']['APIPort']))
