from __future__ import absolute_import, division, print_function, unicode_literals
import locale
locale.setlocale(locale.LC_ALL, '')
import logging # pylint: disable=W0611
import datetime
import uuid
import json
import subprocess
import os
import sys
sys.path.append('..')
sys.path.append('../..')
from common import common_string
import database as database_base
import natsort
import collections
import psycopg2

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)



db_connection = database_base.MKServerDatabase()
db_connection.db_open(True)

data_episode_count = db_connection.db_read_tvmeta_season_eps_list('a7ad882b-372a-4e46-bb77-26c09681ea01', 2)
print('dataeps: %s', data_episode_count)

key_list = natsort.natsorted(data_episode_count)

for key_data in key_list:
    print('key: %s', data_episode_count[key_data])

db_connection.db_close()
