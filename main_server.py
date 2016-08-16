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
import ConfigParser
config_handle = ConfigParser.ConfigParser()
config_handle.read("MediaKraken.ini")
import sys
import subprocess
import signal
import os
sys.path.append("./common")
sys.path.append("./server")
import common_logging
import common_watchdog
rmda_enabled_os = False
try:
    from common import common_rmda
    rmda_enabled_os = True
except:
    pass
import database as database_base


def signal_receive(signum, frame):
    logging.infol('CHILD Main: Received USR1')
    os.kill(proc.pid, signal.SIGTERM)
    os.kill(proc_image.pid, signal.SIGTERM)
    os.kill(proc_cron.pid, signal.SIGTERM)
    os.kill(proc_broadcast.pid, signal.SIGTERM)
    os.kill(proc_ffserver.pid, signal.SIGTERM)
    os.kill(proc_web_app.pid, signal.SIGTERM)
    os.kill(proc_trigger, signal.SIGTERM)
    os.kill(proc_api, signal.SIGTERM)
    for link_data in link_pid.keys():
        os.kill(link_pid[link_data], signal.SIGTERM)
    # stop watchdog
    watchdog.com_watchdog_stop()
    # cleanup db
    db.srv_db_rollback()
    # log stop
    db.srv_db_activity_insert('MediaKraken_Server Stop', None, 'System: Server Stop',\
        'ServerStop', None, None, 'System')
    # commit
    db.srv_db_commit()
    db.srv_db_close()
    sys.stdout.flush()
    sys.exit(0)


# start logging
common_logging.com_logging_start()

# store pid for initd
pid = os.getpid()
logging.info('MediaKraken_PID %s', pid)
try:
    op = open("/var/mm_server.pid", "w")
    op.write("%s" % pid)
    op.close()
except:
    #op = open("mm_server.pid", "w")
    pass


logging.info('Check Certs')
# check for and create ssl certs if needed
if not os.path.isfile('./key/cacert.pem'):
    proc_ssl = subprocess.Popen(['python', './subprogram_ssl_keygen.py'], shell=False)
    proc_ssl.wait()
    if not os.path.isfile('./key/cacert.pem'):
        logging.critical("Cannot generate SSL certificate. Exiting.....")
        sys.exit()


logging.info("Validate Paths")
# validate paths in ini file
# keep the checks split so user can be told which one is wrong
if not os.path.isdir(config_handle.get('MediaKrakenServer', 'MetadataImageLocal').strip()):
    logging.critical("MediaKrakenServer/MetadataImageLocal is not a valid directory!  Exiting...")
    logging.critical("Invalid Path: %s",\
        config_handle.get('MediaKrakenServer', 'MetadataImageLocal').strip())
    sys.exit()
if not os.path.isdir(config_handle.get('MediaKrakenServer', 'BackupLocal').strip()):
    logging.critical("MediaKrakenServer/BackupLocal is not a valid directory!  Exiting...")
    logging.critical("Invalid Path: %s",\
        config_handle.get('MediaKrakenServer', 'BackupLocal').strip())
    sys.exit()


logging.info("Open DB")
# open the database
db = database_base.MKServerDatabase()
try:
    db.srv_db_open(config_handle.get('DB Connections', 'PostDBHost').strip(),\
        config_handle.get('DB Connections', 'PostDBPort').strip(),\
        config_handle.get('DB Connections', 'PostDBName').strip(),\
        config_handle.get('DB Connections', 'PostDBUser').strip(),\
        config_handle.get('DB Connections', 'PostDBPass').strip())
except:
    logging.critical("Cannot open database. Exiting...")
    sys.exit()


db.srv_db_activity_insert('MediaKraken_Server Start', None, 'System: Server Start',\
        'ServerStart', None, None, 'System')


if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    signal.signal(signal.SIGBREAK, signal_receive)   # ctrl-c
else:
    signal.signal(signal.SIGTSTP, signal_receive)   # ctrl-z
    signal.signal(signal.SIGUSR1, signal_receive)   # ctrl-c


# look for infiniband rdma devices
if rmda_enabled_os:
    rmda_devices = com_RMDA.mk_rdma_get_devices()
    if rmda_devices is None:
        rmda_enabled_os = False


logging.info("Start Watchdog")
# startup watchdog
watchdog = common_watchdog.CommonWatchdog()
watchdog.com_watchdog_start(db.srv_db_audit_paths(None, None))


# startup the other reactor via popen as it's non-blocking
proc = subprocess.Popen(['python', './subprogram_reactor_string.py'], shell=False)
logging.info("Reactor PID: %s", proc.pid)


# fire up web image server
proc_image = subprocess.Popen(['python', './subprogram_reactor_web_images.py'],\
    shell=False)
logging.info("Reactor Web Image PID: %s", proc_image.pid)


# fire up broadcast server
proc_broadcast = subprocess.Popen(['python', './subprogram_broadcast.py'], shell=False)
logging.info("Broadcast PID: %s", proc_broadcast.pid)


# fire up cron service
proc_cron = subprocess.Popen(['python', './subprogram_cron_checker.py'], shell=False)
logging.info("Cron PID: %s", proc_cron.pid)


# fire up ffserver
if str.upper(sys.platform[0:3]) == 'WIN' or str.upper(sys.platform[0:3]) == 'CYG':
    pass
else:
    proc_ffserver = subprocess.Popen(['ffserver', '-f', './conf/ffserver.conf'], shell=False)
    logging.info("FFServer PID: %s", proc_ffserver.pid)


# fire up trigger procress
proc_trigger = subprocess.Popen(['python', 'main_trigger.py'], shell=False)
logging.info("Trigger PID: %s", proc_trigger.pid)


# fire up api server
proc_api = subprocess.Popen(['python', 'main_api.py'], shell=False)
logging.info("API PID: %s", proc_api.pid)


# fire up link servers
link_pid = {}
for link_data in db.srv_db_Link_List():
    proc_link = subprocess.Popen(['python', 'main_link.py', link_data[2]['IP'],\
        str(link_data[2]['Port'])], shell=False)
    logging.info("Link PID: %s", proc_link.pid)
    link_pid[link_data[0]] = proc_link.pid


# fire up uwsgi server
proc_web_app = subprocess.Popen(['uwsgi', '--socket', '0.0.0.0:8080', '--protocol', 'http',\
        '--chdir=./web_app', '--ini', './web_app/mediakraken_uwsgi.ini'], shell=False)


# hold here
proc_web_app.wait()


# stop watchdog
watchdog.com_watchdog_stop()


# log stop
db.srv_db_activity_insert('MediaKraken_Server Stop', None, 'System: Server Stop',\
         'ServerStop', None, None, 'System')

# commit
db.srv_db_commit()


# close the database
db.srv_db_close()


# stop children
os.kill(proc.pid, signal.SIGTERM)
os.kill(proc_image.pid, signal.SIGTERM)
os.kill(proc_broadcast.pid, signal.SIGTERM)
os.kill(proc_cron.pid, signal.SIGTERM)
os.kill(proc_ffserver.pid, signal.SIGTERM)
os.kill(proc_web_app.pid, signal.SIGTERM)
os.kill(proc_trigger, signal.SIGTERM)
os.kill(proc_api, signal.SIGTERM)
for link_data in link_pid.keys():
    os.kill(link_pid[link_data], signal.SIGTERM)
