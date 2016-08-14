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
import hashlib
import json
import requests


class CommonSchedulesDirect(object):
    """
    Class for interfacing with Schedules Direct
    """
    def __init__(self):
        self.headers = {'User-Agent': 'MediaKraken_0.1.6',
                        'Accept-Encoding': 'gzip, deflate'}
        self.BASE_API_URL = 'https://json.schedulesdirect.org/20141201'


    def com_schedules_direct_login(self, user_name, user_password):
        resp = requests.post(self.BASE_API_URL + "/token", headers=self.headers,\
            data=json.dumps({"password": hashlib.sha1(user_password.encode('utf-8')).hexdigest(),\
            "username": user_name})).json()
        if resp['code'] != 3000:
            logging.debug("SD login response: %s-%s", resp['code'], resp['token'])
            self.headers['token'] = resp['token']
        else:
            logging.error("SD Connection failed")


    def com_schedules_direct_status(self):
        resp = requests.get(self.BASE_API_URL + "/status", headers=self.headers)
        logging.debug("SD Status: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_schedules_direct_client_version(self):
        resp = requests.get(self.BASE_API_URL + "/version/MediaKraken")
        logging.debug("SD Version: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_schedules_direct_available(self, countries=None):
        if countries is None:
            resp = requests.get(self.BASE_API_URL + "/available")
        else:
            resp = requests.get(self.BASE_API_URL + "/available/countries")
        logging.debug("SD Available: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_schedules_direct_headends(self, country_code, postal_code):
        resp = requests.get(self.BASE_API_URL + "/headends?country=" + country_code
                + "&postalcode=" + postal_code, headers=self.headers)
        logging.debug("SD Headends: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_schedules_direct_lineup_add(self, lineup_id):
        resp = requests.put(self.BASE_API_URL + "/lineups/" + lineup_id, headers=self.headers)
        if resp.json()['response'] == 'INVALID_LINEUP':
            logging.error("SD Invalid lineup: %s", lineup_id)
        elif resp.json()['response'] == "DUPLICATE_LINEUP":
            logging.error("SD lineup duplicate: %s", lineup_id)
        else:
            logging.info("SD lineup added: %s", lineup_id)
        logging.debug("SD Lineup Add: %s-%s", resp.status_code, resp.json())  
        return resp.json()


    def com_schedules_direct_lineup_list(self):
        resp = requests.get(self.BASE_API_URL + "/lineups", headers=self.headers)
        logging.debug("SD Lineup: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_schedules_direct_lineup_delete(self, lineup_id):
        resp = requests.delete(self.BASE_API_URL + "/lineups/" + lineup_id, headers=self.headers)
        if resp.json()['response'] != 'OK':
            logging.error("SD Invalid lineup delete: %s", lineup_id)
        elif resp.json()['code'] == 2103:
            logging.erorr("SD lineup not in account: %s", lineup_id)
        else:
            logging.info("SD lineup deleted: %s", lineup_id)
        logging.debug("SD Lineup Delete: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_schedules_direct_lineup_channel_map(self, lineup_id):
        resp = requests.get(self.BASE_API_URL + "/lineups/" + lineup_id, headers=self.headers)
        logging.debug("SD Channel Map: %s-%s", resp.status_code, resp.json())
        return resp.json()

# TODO automap lineup


    def com_schedules_direct_program_info(self, program_ids):
        resp = requests.post(self.BASE_API_URL + "/programs", headers=self.headers,\
            data=program_ids)
        logging.debug("Header: %s", resp.headers)
        logging.debug("Text: %s", resp.text)
        logging.debug("SD Program Info: %s", resp.status_code)
        return resp.json()


    # this one is only for EP types, not MV
    def com_schedules_direct_program_desc(self, program_ids):
        resp = requests.post(self.BASE_API_URL + "/metadata/description",\
                headers=self.headers, data=program_ids)
        logging.debug("Header: %s", resp.headers)
        logging.debug("Text: %s", resp.text)
        logging.debug("SD Program Desc: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_schedules_direct_schedules_by_stationid(self, station_ids):
        resp = requests.post(self.BASE_API_URL + "/schedules", headers=self.headers,\
                data=station_ids)
        logging.debug("SD Station: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_schedules_direct_md5(self, station_ids):
        resp = requests.post(self.BASE_API_URL + "/schedules/mkd5", headers=self.headers,\
                data=program_ids)
        logging.debug("SD MD5: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_schedules_still_running(self, program_id):
        resp = requests.post(self.BASE_API_URL + ("/metadata/stillRunning/%s", program_id),\
                headers=self.headers)
        logging.debug("SD Running: %s-%s", resp.status_code, resp.json())
        return resp.json()


    def com_schedules_program_metadata(self, program_ids):
        resp = requests.post(self.BASE_API_URL + "/metadata/programs/", headers=self.headers,\
                data=program_ids)
        logging.debug("SD Program Meta: %s-%s", resp.status_code, resp.json())
        return resp.json()

# TODO retrieve image

# TODO retrieve celbrity image
