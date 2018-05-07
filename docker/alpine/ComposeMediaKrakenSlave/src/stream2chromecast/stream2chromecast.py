#!/usr/bin/env python
"""
stream2chromecast.py: Chromecast media streamer for Linux

author: Pat Carter - https://github.com/Pat-Carter/stream2chromecast

version: 0.6.3

"""

# Copyright (C) 2014-2016 Pat Carter
#
# This file is part of Stream2chromecast.
#
# Stream2chromecast is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Stream2chromecast is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Stream2chromecast.  If not, see <http://www.gnu.org/licenses/>.


VERSION = "0.6.3"

import BaseHTTPServer
import errno
import httplib
import mimetypes
import os
import re
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib
import urlparse
from threading import Thread

from cc_media_controller import CCMediaController
from common import common_docker
from common import common_global
from common import common_logging_elasticsearch

script_name = (sys.argv[0].split(os.sep))[-1]

PIDFILE = os.path.join(tempfile.gettempdir(), "stream2chromecast_%s.pid")

FFMPEG = 'ffmpeg %s -i "%s" -preset ultrafast -f mp4 -frag_duration 3000 -b:v 2000k -loglevel error %s -'


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    content_type = "video/mp4"

    """ Handle HTTP requests for files which do not need transcoding """

    def do_GET(self):

        query = self.path.split("?", 1)[-1]
        filepath = urllib.unquote_plus(query)

        self.suppress_socket_error_report = None

        self.send_headers(filepath)

        print "sending data"
        try:
            self.write_response(filepath)
        except socket.error, e:
            if isinstance(e.args, tuple):
                if e[0] in (errno.EPIPE, errno.ECONNRESET):
                    print "disconnected"
                    self.suppress_socket_error_report = True
                    return

            raise

    def handle_one_request(self):
        try:
            return BaseHTTPServer.BaseHTTPRequestHandler.handle_one_request(self)
        except socket.error:
            if not self.suppress_socket_error_report:
                raise

    def finish(self):
        try:
            return BaseHTTPServer.BaseHTTPRequestHandler.finish(self)
        except socket.error:
            if not self.suppress_socket_error_report:
                raise

    def send_headers(self, filepath):
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-type", self.content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Transfer-Encoding", "chunked")
        self.end_headers()

    def write_response(self, filepath):
        with open(filepath, "rb") as f:
            while True:
                line = f.read(1024)
                if len(line) == 0:
                    break

                chunk_size = "%0.2X" % len(line)
                self.wfile.write(chunk_size)
                self.wfile.write("\r\n")
                self.wfile.write(line)
                self.wfile.write("\r\n")

        self.wfile.write("0")
        self.wfile.write("\r\n\r\n")


class TranscodingRequestHandler(RequestHandler):
    """ Handle HTTP requests for files which require realtime transcoding with ffmpeg """
    transcoder_command = FFMPEG
    transcode_options = ""
    transcode_input_options = ""
    bufsize = 0

    def write_response(self, filepath):
        if self.bufsize != 0:
            print "transcode buffer size:", self.bufsize

        ffmpeg_command = self.transcoder_command % (
            self.transcode_input_options, filepath, self.transcode_options)

        ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, shell=True,
                                          bufsize=self.bufsize)

        for line in ffmpeg_process.stdout:
            chunk_size = "%0.2X" % len(line)
            self.wfile.write(chunk_size)
            self.wfile.write("\r\n")
            self.wfile.write(line)
            self.wfile.write("\r\n")

        self.wfile.write("0")
        self.wfile.write("\r\n\r\n")


class SubRequestHandler(RequestHandler):
    """ Handle HTTP requests for subtitles files """
    content_type = "text/vtt;charset=utf-8"


def kill_old_pid(device_ip):
    """ attempts to kill a previously running instance of this application casting to the specified device. """
    pid_file = PIDFILE % device_ip
    try:
        with open(pid_file, "r") as pidfile:
            pid = int(pidfile.read())
            os.killpg(pid, signal.SIGTERM)
    except:
        pass


def save_pid(device_ip):
    """ saves the process id of this application casting to the specified device in a pid file. """
    pid_file = PIDFILE % device_ip
    with open(pid_file, "w") as pidfile:
        pidfile.write("%d" % os.getpid())


def get_mimetype(filename, ffprobe_cmd=None):
    """ find the container format of the file """
    # default value
    mimetype = "video/mp4"

    # guess based on filename extension
    guess = mimetypes.guess_type(filename)[0]
    if guess is not None:
        if guess.lower().startswith("video/") or guess.lower().startswith("audio/"):
            mimetype = guess

    # use the OS file command...
    try:
        file_cmd = 'file --mime-type -b "%s"' % filename
        file_mimetype = subprocess.check_output(file_cmd, shell=True).strip().lower()

        if file_mimetype.startswith("video/") or file_mimetype.startswith("audio/"):
            mimetype = file_mimetype

            print "OS identifies the mimetype as :", mimetype
            return mimetype
    except:
        pass

    if ffprobe_cmd is None:
        return mimetype

    has_video = False
    format_name = None

    ffprobe_cmd = '%s -show_streams -show_format "%s"' % (ffprobe_cmd, filename)
    ffmpeg_process = subprocess.Popen(ffprobe_cmd, stdout=subprocess.PIPE, shell=True)

    for line in ffmpeg_process.stdout:
        if line.startswith("codec_type=audio"):
            pass
        elif line.startswith("codec_type=video"):
            has_video = True
        elif line.startswith("format_name="):
            name, value = line.split("=")
            format_name = value.strip().lower().split(",")

    # use the default if it isn't possible to identify the format type
    if format_name is None:
        return mimetype

    if has_video:
        mimetype = "video/"
    else:
        mimetype = "audio/"

    if "mp4" in format_name:
        mimetype += "mp4"
    elif "webm" in format_name:
        mimetype += "webm"
    elif "ogg" in format_name:
        mimetype += "ogg"
    elif "mp3" in format_name:
        mimetype = "audio/mpeg"
    elif "wav" in format_name:
        mimetype = "audio/wav"
    else:
        mimetype += "mp4"

    return mimetype


def play(filename, transcode=False, transcoder=None, transcode_options=None,
         transcode_input_options=None,
         transcode_bufsize=0, device_name=None, subtitles=None, subtitles_language=None):
    """ play a local file or transcode from a file or URL and stream to the chromecast """

    cast = CCMediaController(device_name=device_name)

    kill_old_pid(cast.host)
    save_pid(cast.host)

    if os.path.isfile(filename):
        filename = os.path.abspath(filename)
        print "source is file: %s" % filename
    else:
        if transcode and (filename.lower().startswith("http://")
                          or filename.lower().startswith("https://")
                          or filename.lower().startswith("rtsp://")):
            print "source is URL: %s" % filename
        else:
            sys.exit("media file %s not found" % filename)

    probe_cmd = "ffprobe"

    status = cast.get_status()
    webserver_ip = status['client'][0]
    print "local ip address:", webserver_ip
    common_global.es_inst.com_elastic_index('info',
                                            {'webserver_ip': webserver_ip})

    docker_inst = common_docker.CommonDocker()
    # it returns a dict, not a json
    webserver_ext_ip = docker_inst.com_docker_info()['Swarm']['NodeAddr']
    # port code pulls MAPPED ports.....so, -p
    webserver_ext_port = int(docker_inst.com_docker_port(container_id=None,
                                                         mapped_port='5050')[0]['HostPort'])
    print 'ip', webserver_ext_ip
    print 'port', webserver_ext_port
    common_global.es_inst.com_elastic_index('info',
                                            {'exip': webserver_ext_ip, 'exPort':
                                                webserver_ext_port})
    req_handler = RequestHandler

    if transcode:
        req_handler = TranscodingRequestHandler

        req_handler.transcoder_command = FFMPEG

        if transcode_options is not None:
            req_handler.transcode_options = transcode_options

        if transcode_input_options is not None:
            req_handler.transcode_input_options = transcode_input_options

        req_handler.bufsize = transcode_bufsize

    if req_handler == RequestHandler:
        req_handler.content_type = get_mimetype(filename, probe_cmd)

    # must start the webservers on the LOCAL docker ips
    # then let the external ones map to internal ports

    # create a webserver to handle a single request for the media file
    server = BaseHTTPServer.HTTPServer((webserver_ip, 5050), req_handler)

    thread = Thread(target=server.handle_request)
    thread.start()

    url = "http://%s:%s?%s" % (webserver_ext_ip, webserver_ext_port,
                               urllib.quote_plus(filename, "/"))
    print "URL & content-type: ", url, req_handler.content_type

    # create another webserver to handle a request for the subtitles file,
    # if specified in the subtitles parameter
    sub = None
    if subtitles:
        if os.path.isfile(subtitles):
            # convert srt to vtt
            if subtitles[-3:].lower() == 'srt':
                print "Converting subtitle to WebVTT"
                with open(subtitles, 'r') as srtfile:
                    content = srtfile.read()
                    content = re.sub(r'([\d]+)\,([\d]+)', r'\1.\2', content)
                    subtitles = subtitles[:-3] + '.vtt'
                    with open(subtitles, 'w') as vttfile:
                        vttfile.write("WEBVTT\n\n" + content)

            webserver_port_subtitle = int(docker_inst.com_docker_port(container_id=None,
                                                                      mapped_port='5060')[0][
                                              'HostPort'])
            print 'sub port', webserver_port_subtitle
            sub_server = BaseHTTPServer.HTTPServer((webserver_ip, 5060), SubRequestHandler)
            thread2 = Thread(target=sub_server.handle_request)
            thread2.start()

            sub = "http://%s:%s?%s" % (
                webserver_ext_ip, webserver_port_subtitle,
                urllib.quote_plus(subtitles, "/"))
            print "sub URL: ", sub
        else:
            print "Subtitles file %s not found" % subtitles

    load(cast, url, req_handler.content_type, sub, subtitles_language)


def load(cast, url, mimetype, sub=None, sub_language=None):
    """ load a chromecast instance with a url and wait for idle state """
    try:
        print "loading media..."

        cast.load(url, mimetype, sub, sub_language)

        # wait for playback to complete before exiting
        print "waiting for player to finish - press ctrl-c to stop..."

        idle = False
        while not idle:
            time.sleep(1)
            idle = cast.is_idle()

    except KeyboardInterrupt:
        print
        print "stopping..."
        cast.stop()

    finally:
        print "done"


def playurl(url, device_name=None):
    """ play a remote HTTP resource on the chromecast """

    def get_resp(url):
        url_parsed = urlparse.urlparse(url)

        scheme = url_parsed.scheme
        host = url_parsed.netloc
        path = url.split(host, 1)[-1]

        conn = None
        if scheme == "https":
            conn = httplib.HTTPSConnection(host)
        else:
            conn = httplib.HTTPConnection(host)

        conn.request("HEAD", path)

        resp = conn.getresponse()
        return resp

    def get_full_url(url, location):
        url_parsed = urlparse.urlparse(url)

        scheme = url_parsed.scheme
        host = url_parsed.netloc

        if location.startswith("/") is False:
            path = url.split(host, 1)[-1]
            if path.endswith("/"):
                path = path.rsplit("/", 2)[0]
            else:
                path = path.rsplit("/", 1)[0] + "/"
            location = path + location

        full_url = scheme + "://" + host + location

        return full_url

    resp = get_resp(url)

    if resp.status != 200:
        redirect_codes = [301, 302, 303, 307, 308]
        if resp.status in redirect_codes:
            redirects = 0
            while resp.status in redirect_codes:
                redirects += 1
                if redirects > 9:
                    sys.exit("HTTP Error: Too many redirects")
                headers = resp.getheaders()
                for header in headers:
                    if len(header) > 1:
                        if header[0].lower() == "location":
                            redirect_location = header[1]
                if redirect_location.startswith("http") is False:
                    redirect_location = get_full_url(url, redirect_location)
                print "Redirecting to " + redirect_location
                resp = get_resp(redirect_location)
            if resp.status != 200:
                sys.exit("HTTP error:" + str(resp.status) + " - " + resp.reason)
        else:
            sys.exit("HTTP error:" + str(resp.status) + " - " + resp.reason)

    print "Found HTTP resource"

    headers = resp.getheaders()

    mimetype = None

    for header in headers:
        if len(header) > 1:
            if header[0].lower() == "content-type":
                mimetype = header[1]

    if mimetype != None:
        print "content-type:", mimetype
    else:
        mimetype = "video/mp4"
        print "resource does not specify mimetype - using default:", mimetype

    cast = CCMediaController(device_name=device_name)
    load(cast, url, mimetype)


def pause(device_name=None):
    """ pause playback """
    CCMediaController(device_name=device_name).pause()


def unpause(device_name=None):
    """ continue playback """
    CCMediaController(device_name=device_name).play()


def stop(device_name=None):
    """ stop playback and quit the media player app on the chromecast """
    CCMediaController(device_name=device_name).stop()


def get_status(device_name=None):
    """ print the status of the chromecast device """
    print CCMediaController(device_name=device_name).get_status()


def volume_up(device_name=None):
    """ raise the volume by 0.1 """
    CCMediaController(device_name=device_name).set_volume_up()


def volume_down(device_name=None):
    """ lower the volume by 0.1 """
    CCMediaController(device_name=device_name).set_volume_down()


def set_volume(v, device_name=None):
    """ set the volume to level between 0 and 1 """
    CCMediaController(device_name=device_name).set_volume(v)


def validate_args(args):
    """ validate that there are the correct number of arguments """
    if len(args) < 1:
        sys.exit()

    if args[0] == "-setvol" and len(args) < 2:
        sys.exit()


def get_named_arg_value(arg_name, args, integer=False):
    """ get a argument value by name """
    arg_val = None
    if arg_name in args:

        arg_pos = args.index(arg_name)
        arg_name = args.pop(arg_pos)

        if len(args) > (arg_pos + 1):
            arg_val = args.pop(arg_pos)

    if integer:
        int_arg_val = 0
        if arg_val is not None:
            try:
                int_arg_val = int(arg_val)
            except ValueError:
                print "Invalid integer parameter, defaulting to zero. Parameter name:", arg_name

        arg_val = int_arg_val

    return arg_val


def run():
    """ main execution """
    # start logging
    common_global.es_inst = common_logging_elasticsearch.CommonElasticsearch(
        'main_slave_stream2cromecast')

    args = sys.argv[1:]

    # optional device name parm. if not specified, device_name = None (the first device found will be used).
    device_name = get_named_arg_value("-devicename", args)

    # optional transcode options parm. if specified, these options will be passed to the transcoder to be applied to the output
    transcode_options = get_named_arg_value("-transcodeopts", args)

    # optional transcode options parm. if specified, these options will be passed to the transcoder to be applied to the input data
    transcode_input_options = get_named_arg_value("-transcodeinputopts", args)

    # optional transcode bufsize parm. if specified, the transcoder will buffer approximately this many bytes of output
    transcode_bufsize = get_named_arg_value("-transcodebufsize", args, integer=True)

    # optional subtitle parm. if specified, the specified subtitles will be played.
    subtitles = get_named_arg_value("-subtitles", args)

    # optional subtitle_language parm. if not specified en-US will be used.
    subtitles_language = get_named_arg_value("-subtitles_language", args)

    validate_args(args)

    if args[0] == "-stop":
        stop(device_name=device_name)

    elif args[0] == "-pause":
        pause(device_name=device_name)

    elif args[0] == "-continue":
        unpause(device_name=device_name)

    elif args[0] == "-status":
        get_status(device_name=device_name)

    elif args[0] == "-setvol":
        set_volume(float(args[1]), device_name=device_name)

    elif args[0] == "-volup":
        volume_up(device_name=device_name)

    elif args[0] == "-voldown":
        volume_down(device_name=device_name)

    elif args[0] == "-mute":
        set_volume(0, device_name=device_name)

    elif args[0] == "-transcode":
        arg2 = args[1]
        play(arg2, transcode=True, transcode_options=transcode_options,
             transcode_input_options=transcode_input_options, transcode_bufsize=transcode_bufsize,
             device_name=device_name, subtitles=subtitles, subtitles_language=subtitles_language)

    elif args[0] == "-playurl":
        arg2 = args[1]
        playurl(arg2, device_name=device_name)

    else:
        play(args[0], device_name=device_name, subtitles=subtitles,
             subtitles_language=subtitles_language)


if __name__ == "__main__":
    run()
