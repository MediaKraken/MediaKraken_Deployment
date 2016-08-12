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

# code based on:
# https://developers.google.com/youtube/v3/code_samples/python#upload_a_video
# https://github.com/youtube/api-samples/tree/master/python

from __future__ import absolute_import, division, print_function, unicode_literals
import logging
import sys
# pull in the ini file config
import ConfigParser
Config = ConfigParser.ConfigParser()
Config.read("MediaKraken.ini")
import common.common_network
import requests
import json


# import google api modules
from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
#from oauth2client.tools import argparser


class CommonGoogle(object):
    """
    Class for interfacing with google api
    """
    def __init__(self):
        self.DEVELOPER_KEY = Config.get('API', 'Google').strip()
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,\
            developerKey=DEVELOPER_KEY)


    def com_google_youtube_search(search_term, max_results):
        """
        # query youtube via search
        """
        search_response = self.youtube.search().list(q=search_term, part="id,snippet",\
            maxResults=max_results).execute()
        videos = []
        channels = []
        playlists = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
              videos.append("%s (%s)" % (search_result["snippet"]["title"],\
                  search_result["id"]["videoId"]))
            elif search_result["id"]["kind"] == "youtube#channel":
              channels.append("%s (%s)" % (search_result["snippet"]["title"],\
                  search_result["id"]["channelId"]))
            elif search_result["id"]["kind"] == "youtube#playlist":
              playlists.append("%s (%s)" % (search_result["snippet"]["title"],\
                  search_result["id"]["playlistId"]))
        return (videos, channels, playlists)


    def com_google_youtube_info(video_url):
        """
        # info of particular video
        """
        return com_network.MK_Network_Fetch_From_URL('https://www.googleapis.com/'\
            + YOUTUBE_API_SERVICE_NAME + '/' + YOUTUBE_API_VERSION + '/videos?id=' + video_url\
            + '&key=' + DEVELOPER_KEY + '&part=snippet,contentDetails,statistics,status', None)


    def com_google_youtube_add_subscription(channel_id):
        """
        # add a subscription to the specified channel.
        """
        add_subscription_response = self.youtube.subscriptions().insert(
        part='snippet',
        body=dict(
          snippet=dict(
            resourceId=dict(
              channelId=channel_id
            )
          )
        )).execute()
        return add_subscription_response["snippet"]["title"]


    def com_google_youtube_rate_video(video_id, like_dislike='like'): # or dislike
        """
        # rate a yt video
        """
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        youtube.videos().rate(
          id=video_id,
          rating=like_dislike
        ).execute()


    def com_google_youtube_get_comments(video_id, channel_id):
        """
        Get yt comments for specified video
        """
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        results = youtube.commentThreads().list(
          part="snippet",
          videoId=video_id,
          channelId=channel_id,
          textFormat="plainText"
        ).execute()
        for item in results["items"]:
          comment = item["snippet"]["topLevelComment"]
          author = comment["snippet"]["authorDisplayName"]
          text = comment["snippet"]["textDisplay"]
          logging.info("Comment by %s: %s" % (author, text))
        return results["items"]


    def com_google_youtube_insert_comment(channel_id, video_id, text):
        insert_result = self.youtube.commentThreads().insert(
          part="snippet",
          body=dict(
            snippet=dict(
              channelId=channel_id,
              videoId=video_id,
              topLevelComment=dict(
                snippet=dict(
                  textOriginal=text
                )
              )
            )
          )
        ).execute()


    def com_google_youtube_update_comment(comment):
        comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"] = 'updated'
        update_result = self.youtube.commentThreads().update(
          part="snippet",
          body=comment
        ).execute()


    def com_google_youtube_add_subscription(channel_id):
        add_subscription_response = self.youtube.subscriptions().insert(
          part='snippet',
          body=dict(
            snippet=dict(
              resourceId=dict(
                channelId=channel_id
              )
            )
          )).execute()
        return add_subscription_response["snippet"]["title"]


# v2 is retired
## following ones don't need to be within class
#''' feed types
#most_recent
#most_viewed
#top_rated
#most_discussed
#top_favorites
#most_linked
#recently_featured
#most_responded
#'''
#
#def com_Google_Youtube_Feed_List(feed_type):
#    return json.loads(requests.get("http://gdata.youtube.com/feeds/api/standardfeeds/top_rated?v=2&alt=jsonc").text)
#    #for item in data['data']['items']:
