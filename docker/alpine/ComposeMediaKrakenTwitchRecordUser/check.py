#This script checks if a user on twitch is currently streaming and then records the stream via streamlink
import datetime
import re
import subprocess
import sys
import os
import getopt
from requests import exceptions as reqexc
from threading import Timer
from twitch import TwitchClient

CLIENT_ID = 'PASTE YOUR CLIENT ID HERE AS A STRING'
# e.g. CLIENT_ID = '123456789ABCDEFG'

CLIENT_ID_FILE = os.getcwd()+os.path.sep+"client_id.txt"
# Location of client_id.txt config file.

VALID_BROADCAST = [ 'live' ]
# 'rerun' can be added through commandline flags/options

def get_client_id():
    print("Visit the following website to generate a client id for this script.")
    print("https://glass.twitch.tv/console/apps")
    print("Enter client id from website.")
    id=input("client id: ")
    client_file=open(CLIENT_ID_FILE,'w')
    client_file.write(id)
    client_file.close()
    #sys.exit(4)

def check_client_id():
    global CLIENT_ID
    try:
        client_file=open(CLIENT_ID_FILE,'r')
    except FileNotFoundError as ex:
        print(ex)
        print("Client id file doesn't exist.")
        get_client_id()
        sys.exit(4)
    CLIENT_ID=client_file.read()
    client_file.close()

def check_user(user):
    global CLIENT_ID
    global VALID_BROADCAST
    """ returns 0: online, 1: offline, 2: not found, 3: error """
    try:
        client = TwitchClient(client_id=CLIENT_ID)
        response = client.users.translate_usernames_to_ids(user)
    except reqexc.HTTPError as ex:
        print("Bad client id: '%s'" %(CLIENT_ID))
        print(ex)
        get_client_id()
        sys.exit(4)
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
            status = 1      # user offline
    else:
        status = 2          # user not found

    return status, stream_info

def loopcheck():
    status, stream_info = check_user(user)
    if status == 2:
        print("Username not found. Invalid username?")
        sys.exit(3)
    elif status == 3:
        print("Unexpected error. Maybe try again later")
    elif status == 1:
        t = Timer(time, loopcheck)
        print(user,"is currently offline, checking again in",time,"seconds")
        t.start()
    elif status == 0:
        print(user,"is online. Stop.")
        filename = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")+" - "+user+" - "+re.sub(r"[^a-zA-Z0-9]+", ' ', stream_info['channel']['status'])+".flv"
        dir = os.getcwd()+os.path.sep+user
        if not os.path.exists(dir):
            os.makedirs(dir)
        subprocess.call(["streamlink","https://twitch.tv/"+user,quality,"-o",filename], cwd=dir)
        print("Stream is done. Going back to checking..")
        t = Timer(time, loopcheck)
        t.start()

def usage():
    print("Usage: check.py [options] [user]")
    print("This script checks if a user on twitch is currently streaming and then records the stream via streamlink")
    print("    -h,--help               Display this message.")
    print("    -t,--time=TIME          Set the time interval in seconds between checks for user. Default is 30.")
    print("    -q,--quality=QUALITY    Set the quality of the stream. Default is 'best'. See streamlink documentation for more details.")
    print("    -c,--client-id=ID       Override the client id. The script will ask for an id if not given or stored in a configuration file.")
    print("    -r,--allow-rerun        Don't ignore reruns.")



def main():
    global time
    global user
    global quality
    global VALID_BROADCAST
    global CLIENT_ID

    # Defaults
    time=30.0
    quality="best"

    # Use getopts to process options and arguments.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:q:c:r", ["help", "time=","quality=","client-id=","allow-rerun"])
    except getopt.GetoptError as ex:
        print(ex)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):  # Display help message
            usage()
            sys.exit()
        elif opt in ('-t', '--time'): # Set time interval between checks for user
            try:
                time = int(arg)
            except ValueError as ex:
                print('"%s" cannot be converted to an int: %s' % (arg, ex))
                print("Using default: %ds" %(time))
                print("")
        elif opt in ("-q", "--quality"): # Set quality
            quality = arg
        elif opt in ("-r", "--allow-rerun"): # Allow recording of reruns
            VALID_BROADCAST.append('rerun')
        elif opt in ("-c", "--client-id"): # Override client id
            CLIENT_ID = arg

    # Checking if the remaining arguments are valid.
    if len(args) > 1:
        user = " ".join(args)
        print("'%s' is not a valid username" %(user))
        print("")
        usage()
        sys.exit(2)

    # Check if user is supplied.
    user = "".join(args)
    if user == "":
        print("User not supplied")
        usage()
        sys.exit(2)

    if(time<15):
        print("Time shouldn't be lower than 15 seconds")
        time=15


    if CLIENT_ID == 'PASTE YOUR CLIENT ID HERE AS A STRING':
        check_client_id()

    
#    t = Timer(time, loopcheck)
    print("Checking for",user,"every",time,"seconds. Record with",quality,"quality.")
    loopcheck()
#    t.start()


if __name__ == "__main__":
    # execute only if run as a script
    main()
