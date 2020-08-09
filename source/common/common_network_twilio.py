"""
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
"""

from twilio.rest import Client


class CommonNetworkTwilio:
    """
    Class for interfacing with twilio
    """

    def __init__(self, account, token):
        self.twilio_inst = Client(account, token)

    def com_net_twilio_call(self, to_num, from_num):
        return self.twilio_inst.calls.create(to=to_num, from_=from_num,
                                             url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")

    def com_net_twilio_sms(self, to_num, from_num, sms_text):
        return self.twilio_inst.client.messages.create(to=to_num, from_=from_num, body=sms_text)

    def com_net_twilio_get_messages(self):
        return self.twilio_inst.messages.list()
