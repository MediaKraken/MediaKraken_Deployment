# This script checks if a user on twitch is currently streaming and then records the stream via streamlink

# forked and heavily modified for MediaKraken project
import datetime
import getopt
import re
import subprocess
import sys
import time

from requests import exceptions as reqexc
from twitch import TwitchClient

# Defaults
CLIENT_ID = None
VALID_BROADCAST = ['live']


def check_user(user):
    """ returns 0: online, 1: offline, 2: not found, 3: error """
    try:
        client = TwitchClient(client_id=CLIENT_ID)
        response = client.users.translate_usernames_to_ids(user)
    except reqexc.HTTPError as ex:
        print("Bad client id: '%s'" % CLIENT_ID)
        print(ex)
        sys.exit(4)
    # so stream_info has something to return as it's used in main loop
    stream_info = 0
    if response.__len__() > 0:
        user_id = response[0].id
        stream_info = client.streams.get_stream_by_user(user_id)
        if stream_info is not None:
            if stream_info.broadcast_platform in VALID_BROADCAST:
                status = 0  # user is streaming
            else:
                status = 3  # unexpected error
        else:
            status = 1  # user offline
    else:
        # user not found
        sys.exit(3)
    return status, stream_info


def main():
    global VALID_BROADCAST
    global CLIENT_ID
    # Use getopts to process options and arguments.
    opts, args = getopt.getopt(sys.argv[1:], "c:r",
                               ["client-id=", "allow-rerun"])
    # check client and rerun
    for opt, arg in opts:
        if opt in ("-r", "--allow-rerun"):  # Allow recording of reruns
            VALID_BROADCAST.append('rerun')
        elif opt in ("-c", "--client-id"):  # Override client id
            CLIENT_ID = arg
    user = "".join(args)
    while True:
        status, stream_info = check_user(user)
        if status == 0:
            filename = datetime.datetime.now().strftime(
                "%Y-%m-%d %H.%M.%S") + " - " + user + " - " + re.sub(r"[^a-zA-Z0-9]+", ' ',
                                                                     stream_info['channel'][
                                                                         'status']) + ".flv"
            # call waits for subprocess to finish
            subprocess.call(["streamlink", "https://twitch.tv/" + user, "best", "-o", filename],
                            cwd='/mediakraken/downloads')
        time.sleep(30)


if __name__ == "__main__":
    # execute only if run as a script
    main()
