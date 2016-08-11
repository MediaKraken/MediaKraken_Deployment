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
import urllib2
import urllib
import httplib
import socket
import json
import os
import sys
import hashlib
import traceback
import time
# include code
import MK_Common_Network


# create dictionary containing
# Address = Id, Name
# https://github.com/MediaBrowser/Emby/wiki/Locating-the-Server
def MK_Common_Network_Emby_Find_Server():
    """
    Search for servers for one second
    """
    t_end = time.time() + 1
    # create upd socket
    try:
        search_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # allow broadcast otherwise you'll get permission denied 10013 error
        search_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    except socket.error:
        logging.critical('Network_Find_Server: Failed to create socket')
        sys.exit()
    server_hosts_found = {}
    while time.time() < t_end:
        try:
            search_socket.sendto("who is EmbyServer?", ('<broadcast>', 7359))
            data_buff = search_socket.recvfrom(1024)
            server_reply = data_buff[0]
            logging.info('Server reply: ' + server_reply)
            data_block = json.loads(server_reply)
            if data_block["Address"] in server_hosts_found.keys():
                pass
            else:
                logging.debug("addr:" + data_block["Address"] + " : " + data_block["Id"] + " : " + data_block["Name"])
                server_hosts_found[data_block["Address"]] = (data_block["Id"], data_block["Name"])
        except socket.error, msg:
            logging.critical('Network_Find_Server Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()
    logging.info("hosts found: %s", server_hosts_found)
    return server_hosts_found


# create dictionary containing
# Name = Id, PrimaryImageTag (or NULL)
# https://github.com/MediaBrowser/Emby/wiki/Authentication
def MK_Common_Network_Emby_Find_Users(host_server):
    """
    Return user list from specified server
    """
    found_users = {}
    for user_data in json.loads(urllib2.urlopen(host_server + '/Users/Public?format=json').read()):
        user_image_id = None
        try:
            user_image_id = user_data['PrimaryImageTag']
        except:
            pass
        found_users[user_data['Name']] = (user_data['Id'], user_image_id)
        if user_image_id is not None:
            MK_Common_Network.Network_Fetch_Image_From_URL(host_server + '/Users/' + user_data['Id'] + '/Images/Primary', None)
    return found_users


# https://github.com/MediaBrowser/Emby/wiki/Authentication
def MK_Common_Network_Emby_User_Login(host_server, user_name, user_password):
    """
    Login with specified user/name/pass
    """
    json_response = None
    # sha1 hash the password
    password_hash_object = hashlib.sha1(user_password)
    password_hash = password_hash_object.hexdigest()
    # build parameters to url
    values = {'Username' : user_name, 'Password' : password_hash}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    try:
        response = urllib2.urlopen(urllib2.Request(host_server + '/Users/AuthenticateByName?format=json', json.dumps(values), headers=headers))
        json_response = response.read()
    except urllib2.HTTPError, e:
        logging.error('HTTPError = ' + str(e.code))
        if int(e.code) == httplib.UNAUTHORIZED:
            json_response = int(e.code)
    except urllib2.URLError, e:
        logging.error('URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        logging.error('HTTPException')
    return json_response


def MK_Common_Network_Emby_User(host_server, user_id, headers):
    return urllib2.urlopen(urllib2.Request(host_server + '/Users/' + user_id, headers=headers)).read()


# fetch list of open sessions for user
def MK_Common_Network_Emby_Sessions_List_Open(host_server, user_id):
    """
    If the user id is passed only return sessions it can control otherwise return all sessions
    """
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if user_id is not None:
        req = urllib2.Request(host_server + '/Sessions?format=json', headers)
    else:
        req = urllib2.Request(host_server + '/Sessions?format=json', json.dumps({'ControllableByUserId' : user_id}), headers=headers)
    response = urllib2.urlopen(req)
    return response.read()


# send command to specified session
# https://github.com/MediaBrowser/Emby/wiki/Remote-control
def MK_Common_Network_Emby_Sessions_Send_Command(host_server, session_id, playstate_command, session_command):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if playstate_command:
        url_location = '/Playing/'
    else:
        url_location = '/Command/'
    return urllib2.urlopen(urllib2.Request(host_server + '/Sessions/' + session_id + url_location + session_command, headers=headers)).read()


def MK_Common_Network_Emby_User_View_List(host_server, user_id, headers):
    return urllib2.urlopen(urllib2.Request(host_server + '/Users/' + user_id + "/Views", headers=headers)).read()


# https://github.com/MediaBrowser/Emby/wiki/Channels
def MK_Common_Network_Emby_User_Channel_List(host_server, user_id, headers):
    return urllib2.urlopen(urllib2.Request(host_server + '/Channels?userId=' + user_id, headers=headers)).read()


# https://github.com/MediaBrowser/Emby/wiki/Channels
def MK_Common_Network_Emby_User_Channel_Feature_List(host_server, channel_id, headers):
    return urllib2.urlopen(urllib2.Request(host_server + '/Channels/' + channel_id + '/Features', headers=headers)).read()
''' REQUEST TYPE
        StartIndex
        Limit
        Fields
        ParentId
        IsPlayed
        IncludeItemTypes
'''


# https://github.com/MediaBrowser/Emby/wiki/Channels
def MK_Common_Network_Emby_User_Channel_Items(host_server, channel_id, user_id, headers):
    return urllib2.urlopen(urllib2.Request(host_server + '/Channels/' + channel_id + '/Items?userId=' + user_id, headers=headers)).read()


# https://github.com/MediaBrowser/Emby/wiki/Latest-Items
# TODO grouping and such
# TODO episodes
def MK_Common_Network_Emby_User_Latest_Items_List(host_server, request_type, request_subtype, request_limit, request_grouping, user_id, headers):
    return urllib2.urlopen(urllib2.Request(host_server + '/Users/' + user_id + "/Items/Latest", headers=headers)).read()


# add new sync job
# https://github.com/MediaBrowser/Emby/wiki/Sync
def MK_Common_Network_Emby_Sync_Add():
    pass


# download images
# https://github.com/MediaBrowser/Emby/wiki/Images
def MK_Common_Network_Emby_Image_Download():
    #for users, the url's are /Users/{Id}/Images/{Type} and /Users/{Id}/Images/{Type}/{Index}. For media items, it's /Items/{Id}/Images/{Type}, as well as /Items/{Id}/Images/{Type}/{Index}
# TODO types
# TODO percentage complete
# TODO played or not image
    pass


# https://github.com/MediaBrowser/Emby/wiki/Items-by-name
def MK_Common_Network_Emby_Item_Info_By_Name():
    pass


# https://github.com/MediaBrowser/Emby/wiki/Playlists
# TODO create play
# TODO retrieve play
# TODO playlist items
# TODO add item to play
# TODO remove item from play

# https://github.com/MediaBrowser/Emby/wiki/Http-Live-Streaming
# TODO http stream

# https://github.com/MediaBrowser/Emby/wiki/Subtitles
# TODO grab subtitles

# https://github.com/MediaBrowser/Emby/wiki/Audio-Streaming
# TODO audio stream

# https://github.com/MediaBrowser/Emby/wiki/Video-Streaming
# TODO video stream
