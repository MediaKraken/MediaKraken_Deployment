# code based on:
# https://developers.google.com/youtube/v3/code_samples/python#upload_a_video
# https://github.com/youtube/api-samples/tree/master/python


# import google api modules
import httplib2
from googleapiclient.discovery import build

from . import common_global
from . import common_network


# from googleapiclient.errors import HttpError
# from oauth2client.tools import argparser


class CommonGoogle:
    """
    Class for interfacing with google api
    """

    def __init__(self, option_config_json):
        self.DEVELOPER_KEY = option_config_json['API']['google']
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        self.youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                             developerKey=self.DEVELOPER_KEY,
                             http=httplib2.Http(".cache",
                                                disable_ssl_certificate_validation=True))

    def com_google_youtube_search(self, search_term, max_results=25):
        """
        # query youtube via search
        """
        search_response = self.youtube.search().list(q=search_term,
                                                     part="id,snippet",
                                                     maxResults=max_results).execute()
        videos = []
        channels = []
        playlists = []
        for search_result in search_response.get("items", []):
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {'ytsearch': search_result})
            if search_result["id"]["kind"] == "youtube#video":
                videos.append(search_result["id"]["videoId"])
            elif search_result["id"]["kind"] == "youtube#channel":
                channels.append(search_result["id"]["channelId"])
            elif search_result["id"]["kind"] == "youtube#playlist":
                playlists.append(search_result["id"]["playlistId"])
        return (videos, channels, playlists)

    def com_google_youtube_info(self, video_url,
                                video_data='snippet,contentDetails,statistics,status'):
        """
        # info of particular video
        """
        return common_network.mk_network_fetch_from_url(('https://www.googleapis.com/'
                                                         + self.YOUTUBE_API_SERVICE_NAME + '/'
                                                         + self.YOUTUBE_API_VERSION
                                                         + '/videos?id='
                                                         + video_url.replace(
                    'www.youtube.com/watch?v=',
                    '') + '&key='
                                                         + self.DEVELOPER_KEY
                                                         + '&part=' + video_data), None)

    def com_google_youtube_add_subscription(self, channel_id):
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

    # or dislike
    def com_google_youtube_rate_video(self, video_id, like_dislike='like'):
        """
        # rate a yt video
        """
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                        developerKey=self.DEVELOPER_KEY)
        youtube.videos().rate(
            id=video_id,
            rating=like_dislike
        ).execute()

    def com_google_youtube_get_comments(self, video_id, channel_id):
        """
        Get yt comments for specified video
        """
        youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                        developerKey=self.DEVELOPER_KEY)
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
            common_logging_elasticsearch_httpx.com_es_httpx_post(message_type='info', message_text= {"Comment by": (
                author, text)})
        return results["items"]

    def com_google_youtube_insert_comment(self, channel_id, video_id, text):
        """
        Add youtube comment on video
        """
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

    def com_google_youtube_update_comment(self, comment):
        """
        Update comment on youtube video
        """
        comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"] = 'updated'
        update_result = self.youtube.commentThreads().update(
            part="snippet",
            body=comment
        ).execute()
