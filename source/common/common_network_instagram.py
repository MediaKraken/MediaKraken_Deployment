'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

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

from InstagramAPI import InstagramAPI


class CommonNetworkInstragram(object):
    """
    Class for interfacing with instagram
    """

    def __init__(self, user, password):
        self.instagram_inst = InstagramAPI(user, password)
        self.instagram_inst.login()

    def com_net_instagram_upload(self, file_name, caption_text):
        self.instagram_inst.uploadPhoto(
            file_name, caption=caption_text, upload_id=None)

    def com_net_instagram_vid_upload(self, file_name, thumb_path, caption_text):
        self.instagram_inst.uploadVideo(
            file_name, thumb_path, caption=caption_text)

    def com_net_instagram_album_upload(self, media, caption_text):
        self.instagram_inst.uploadAlbum(media, caption=caption_text)


'''
    tagFeed(TODO);

    like;

    comment;

    deleteComment;

    expose;

    logout;

    editMedia;

    removeSelftag;

    mediaInfo;

    deleteMedia;

    getv2Inbox(TODO);

    getRecentActivity(TODO);

    megaphoneLog;

    timelineFeed;

    autoCompleteUserList;

    syncFeatures;

    removeProfilePicture;

    setPrivateAccount;

    setPublicAccount;

    getProfileData;

    editProfile;

    getUsernameInfo;

    getSelfUsernameInfo;

    getFollowingRecentActivity(TODO);

    getUserTags(TODO);

    getSelfUserTags;

    getMediaLikers(TODO);

    getGeoMedia(TODO);

    getSelfGeoMedia;

    fbUserSearch(TODO);

    searchUsers(TODO);

    searchUsername(TODO);

    syncFromAdressBook;

    searchTags(TODO);

    getTimeline(TODO);

    searchLocation(TODO);

    getSelfUserFeed;

    getPopularFeed(TODO);

    getUserFollowings;

    getUserFollowers;

    getSelfUserFollowers;

    getSelfUsersFollowing;

    unlike;

    getMediaComments;

    setNameAndPhone;

    getDirectShare;

    follow;

    unfollow;

    block;

    unblock;

    userFriendship;

    getLikedMedia;

'''
