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
import logging # pylint: disable=W0611
import json
import sys
import os
import signal
sys.path.append("./vault/lib")
import subprocess
try:
    import cPickle as pickle
except:
    import pickle
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet import reactor
import ip2country
from common import common_network


class NetworkEvents(Int32StringReceiver):
    """
    Process the network events for the server
    """
    # init is called on every connection
    def __init__(self, users, db_connection, genre_list, option_config_json):
        self.MAX_LENGTH = 32000000 # pylint: disable=C0103
        # server info
        self.db_connection = db_connection
        self.users = users
        self.user_host_name = None
        self.user_ip_addy = None
        self.user_user_name = None
        self.user_slave = False
        self.user_verified = 0
        self.user_country_code = None
        self.user_country_name = None
        self.user_cpu_usage = 0
        self.user_ffmpeg_data = [] # hold the info of running jobs on slave(s) along with chromecast
        self.proc_file_scan = None
        self.proc_media_match = None
        self.proc_chapter_create = None
        self.proc_anime_match = None
        self.proc_subtitle_media_match = None


    def connectionMade(self):
        """
        Network connection made from client so ask for ident
        """
        logging.info('Got Connection')
        self.sendString('IDENT'.encode("utf8"))


    def connectionLost(self, reason):
        """
        Network connection dropped so remove client
        """
        logging.info('Lost Connection')
        if self.users.has_key(self.user_user_name):
            del self.users[self.user_user_name]


    def stringReceived(self, data):
        """
        Message received from client
        """
        msg = None
        message_words = data.split(' ')
        logging.info('GOT Data: %s', data)
        logging.info('Message: %s', message_words[0])
        if message_words[0] == "VALIDATE":
            # have to create the self.player data so network knows how to send data back
            self.user_host_name = message_words[1]
            self.user_ip_addy = str(self.transport.getPeer()).split('\'')[1]
            self.user_user_name = message_words[1]
            # lookup the country
            country_data = ip2country.IP2Country(verbose=1).lookup(self.user_ip_addy)
            self.user_country_code = country_data[0]
            self.user_country_name = country_data[1]
            self.users[message_words[1]] = self
            logging.info("user: %s %s", self.user_host_name, self.user_ip_addy)
            if self.user_user_name == 'link':
                pass
        # user commands
        elif message_words[0] == "LOGIN":
            pass
# actually processed in "main_link" program!!!!
#        elif message_words[0] == "RECEIVENEWMEDIA":
#            self.db_connection.db_Media_Link_New_Data(pickle.loads(message_words[1])
        elif message_words[0] == "REQUESTNEWMEDIA":
            msg = "RECEIVENEWMEDIA " + pickle.dumps(
                self.db_connection.db_Media_Link_Read_New(pickle.loads(message_words[1]),
                message_words[2], message_words[3], message_words[4], message_words[5],
                message_words[6], message_words[7]))
        elif message_words[0] == "PlayUUID" or message_words[0] == "demo":
            media_path = self.db_connection.db_media_path_by_uuid(message_words[1])[0]
            if media_path is not None:
                if True:
                    # launch and attach to local running ffserver
                    http_link = 'http://localhost:' + self.server_port_ffmpeg + '/stream.ffm'
                    self.proc_ffmpeg_stream = subprocess.Popen(['ffmpeg', '-i',
                        media_path, http_link], shell=False)
                    http_link = 'http://' + common_network.mk_network_get_default_ip() + ':'\
                        + self.server_port_ffmpeg + '/stream.ffm'
                else:
                    # tell slave to fire up the media
                    http_link = None
            msg = 'VIDPLAY ' + http_link
        elif message_words[0] == "FlagMismatchUUID":
            pass
        elif message_words[0] == "MediaIDUpdateUUID":
            # media id, metadata id
            self.db_connection.db_update_media_id(message_words[1], message_words[2])
        # metadata commands
        elif message_words[0] == "IMAGE":
            lookup_id = None
            # message_words[1] is returned to show client which one is being refreshed
            media_id = None
            if message_words[3] == 'None': # random movie selection
                if message_words[2] == "MOVIE":
                    try:
                        lookup_id, media_id\
                            = self.db_connection.db_media_random(message_words[5])
                    except:
                        pass
            else:
                # fetch specific id
                try:
                    lookup_id\
                        = json.loads(self.db_connection.db_media_image_path(message_words[3])\
                        [0])[message_words[4]] # use this to grab file path
                except:
                    pass
            if lookup_id is not None:
                msg = "IMAGE " + pickle.dumps((message_words[1], 'https://'\
                    + self.server_ip.strip() + ':' + self.server_port_image.strip() + '/'\
                    + lookup_id.replace('../images/', ''), media_id))
        # general data
        elif message_words[0] == "GENRELIST":
            msg = "GENRELIST " + pickle.dumps(self.genre_list)
        # theater data
        elif message_words[0] == "VIDEODETAIL":
            msg = "VIDEODETAIL " + pickle.dumps(
                self.db_connection.db_read_media_Metadata_Both(message_words[1]))
        elif message_words[0] == "VIDEOGENRELIST":
            msg = "VIDEOLIST " + pickle.dumps(self.db_connection.db_web_media_list(
                self.db_connection.db_media_uuid_by_class("Movie"),
                    message_words[0], message_words[1]))
        elif message_words[0] == "movie" or message_words[0] == "recent_addition"\
                or message_words[0] == 'in_progress' or message_words[0] == 'video':
            msg = "VIDEOLIST " + pickle.dumps(self.db_connection.db_web_media_list(
                self.db_connection.db_media_uuid_by_class("Movie"), message_words[0]))
        # admin commands
        elif message_words[0] == "ScanMedia":
            # popen expects a list
            self.proc_file_scan = subprocess.Popen([
                'subprogram_file_scan'], shell=False)
        elif message_words[0] == "ScanMediaStop":
            os.killpg(self.proc_file_scan.pid, signal.SIGUSR1)
        elif message_words[0] == "MatchMedia":
            # popen expects a list
            self.proc_media_match = subprocess.Popen([
                'subprogram_match_known_media'], shell=False)
        elif message_words[0] == "MatchMediaStop":
            os.killpg(self.proc_media_match.pid, signal.SIGUSR1)
        elif message_words[0] == "CreateChapterImage":
            # popen expects a list
            self.proc_chapter_create = subprocess.Popen([
                'subprogram_create_chapter_images'], shell=False)
        elif message_words[0] == "CreateChapterImageStop":
            os.killpg(self.proc_chapter_create.pid, signal.SIGUSR1)
        elif message_words[0] == "ScudLeeAnimeMatch":
            # popen expects a list
            self.proc_anime_match = subprocess.Popen([
                'subprogram_match_anime_id_scudlee'], shell=False)
        elif message_words[0] == "ScudLeeAnimeMatchStop":
            os.killpg(self.proc_anime_match.pid, signal.SIGUSR1)
        elif message_words[0] == "SubtitleMedia":
            # popen expects a list
            self.proc_subtitle_media_match = subprocess.Popen([
                'subprogram_subtitle_downloader'], shell=False)
        elif message_words[0] == "SubtitleMediaStop":
            os.killpg(self.proc_subtitle_media_match.pid, signal.SIGUSR1)
        elif message_words[0] == "CPUUSAGE":
            self.user_cpu_usage[self.user_ip_addy] = message_words[1]
        else:
            logging.error("UNKNOWN TYPE: %s", message_words[0])
            msg = "UNKNOWN_TYPE"
        if msg is not None:
            logging.info("should be sending data")
            self.send_single_user(msg.encode("utf8"))


    def send_single_user(self, message):
        """
        Send message to single user
        """
        for user_host_name, protocol in self.users.iteritems(): # pylint: disable=W0612
            if protocol == self:
                logging.info('send single: %s', message)
                protocol.sendString(message.encode("utf8"))
                break


    def send_all_users(self, message):
        """
        Send message to all users
        """
        for user_host_name, protocol in self.users.iteritems():
            if self.users[user_host_name].user_verified == 1:
                logging.info('send all: %s', message)
                protocol.sendString(message.encode("utf8"))


    def send_all_slaves(self, message):
        """
        Send to all slave servers
        """
        for user_host_name, protocol in self.users.iteritems():
            if self.users[user_host_name].user_slave:
                logging.info('send all slave: %s', message)
                protocol.sendString(message.encode("utf8"))


    def send_all_links(self, message):
        """
        Send to all linked servers
        """
        for user_host_name, protocol in self.users.iteritems():
            if self.users[user_host_name].user_link:
                logging.info('send all link: %s', message)
                protocol.sendString(message.encode("utf8"))


    @classmethod
    def broadcast_celery_message(self, message):
        """
        This is used only from the webapp and chromecast celery
        """
        logging.info('celery message received: %s', message)
        low_cpu_host = None
        low_cpu_host_percent = 100
        low_cpu_protocol = None
        for user_host_name, protocol in self.users.iteritems():
            if self.users[user_host_name].user_slave:
                if self.users[user_host_name].user_cpu_usage < low_cpu_host_percent:
                    low_cpu_host = user_host_name
                    low_cpu_protocol = protocol
                    low_cpu_host_percent = self.users[user_host_name].user_cpu_usage
        if low_cpu_host is not None:
            logging.info('send celery: %s', message)
            low_cpu_protocol.sendString(message.encode("utf8"))
        else:
            logging.error('no slave found for playback')
