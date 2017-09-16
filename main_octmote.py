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
import logging  # pylint: disable=W0611
import json
import os
# import plyer to fetch UID of devices
from plyer import uniqueid
from common import common_database_octmote
from common import common_iscp
from common import common_lirc
from common import common_emby
from common import common_emby_network
from common import common_json
from common import common_kodi
from common import common_mediakraken
from common import common_network
from common import common_roku_network
from common import common_serial
from common import common_signal
from common import common_ssdp
from common import common_network_telnet
from common import common_version

#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
from kivy.lang import Builder
install_twisted_reactor()
from twisted.internet import ssl, reactor, protocol


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)


    def dataReceived(self, data):
        self.factory.app.print_message(data)


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        logging.info("Connection Lost")

    def clientConnectionFailed(self, conn, reason):
        logging.info("Connection Failed")


import kivy
kivy.require('1.9.1')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.properties import NumericProperty, BooleanProperty, ListProperty,\
     StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from functools import partial


class OctMote(FloatLayout):
    pass


class OctMoteLoginScreen(BoxLayout):
    password = ObjectProperty(None)
    cancel = ObjectProperty(None)


class OctMoteLoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class OctMoteNotificationScreen(BoxLayout):
    message_text = ObjectProperty(None)
    ok_button = ObjectProperty(None)


class OctMoteApp(App):
    connection = None
    def __init__(self, app):
        self.base_device_guid_dict = None
        self.base_item_guid_dict = None
        self.base_layout_guid_dict = None
        self.remote_mode_details_item = None
        self.remote_mode_currrent_item = None
        self.octmote_server_connection_data = None
        self.server_list = None
        self.server_user_list = None
        self.global_selected_user_id = None
        self.emby_user_connection_json = None
        self.json_text = None
        self._notification_popup = None
        self.global_selected_server_addr = None
        self.login_password = None
        self._popup = None
        self.global_url_headers = None


    def exit_program(self):
        common_database_octmote.com_db_close()


    def dismiss_popup(self):
        self._popup.dismiss()


    def build(self):
        self.base_device_guid_dict = {}
        self.base_item_guid_dict = {}
        self.base_layout_guid_dict = {}
        self.remote_mode_details_item = {}
        self.remote_mode_currrent_item = 'Default'
        # open database files
        self.octmote_server_connection_data = common_database_octmote.com_db_open()
        # fetch and import any item/layout files
        common_json.com_json_find()
        root = OctMote()
        self.connect_to_server()
        return root


    def connect_to_server(self):
        reactor.connectSSL(self.octmote_server_connection_data[0],
            self.octmote_server_connection_data[1], EchoFactory(self), ssl.ClientContextFactory())


    def on_connection(self, connection):
        print("Connected succesfully to OctMote server!")
        self.connection = connection
        # load control layout


    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.textbox.text))
            self.textbox.text = ""


    def mediakraken_find_server_list(self):
        self.server_list = common_mediakraken.com_network_mediakraken_find_server()
        if self.server_list is not None:
            for found_server in self.server_list:
                btn1 = ToggleButton(text=self.server_list[found_server][1],
                    group='mediakraken_server',)
                btn1.bind(on_press=partial(self.MediaKraken_Event_Button_Server_Select,
                    found_server))
                self.root.ids.mediakraken_server_list_layout.add_widget(btn1)
        else:
            # go back to main menu
            self.root.ids._screen_manager.current = 'Main_Remote'


    def emby_find_server_list(self):
        self.server_list = common_emby_network.com_network_emby_find_server()
        if self.server_list is not None:
            for found_server in self.server_list:
                btn1 = ToggleButton(text=self.server_list[found_server][1], group='emby_server',)
                btn1.bind(on_press=partial(self.emby_event_button_server_select, found_server))
                self.root.ids.server_list_layout.add_widget(btn1)
        else:
            # go back to main menu
            self.root.ids._screen_manager.current = 'Main_Remote'


    def emby_event_button_server_select(self, server_addr, *args):
        self.server_user_list = common_emby_network.com_network_emby_find_users(server_addr)
        self.root.ids.user_list_layout.clear_widgets()
        self.root.ids.user_list_layout.add_widget(Label(text='Emby Users(s)'))
        for found_user in self.server_user_list:
            btn1 = ToggleButton(text=found_user, group='emby_user',)
            btn1.bind(on_press=partial(self.emby_event_button_user_select, found_user))
            self.root.ids.user_list_layout.add_widget(btn1)
        self.global_selected_server_addr = server_addr


    def emby_event_button_user_select(self, server_user, *args):
        print("button server user %s", server_user)
        self.global_selected_user_id = server_user
        self.login_password = ''
        content = OctMoteLoginScreen(login_password=self.login_password,
                                     cancel=self.dismiss_popup)
        self._popup = Popup(title="Emby Login", content=content,
            size_hint=(None, None), size=(425, 250))
        self._popup.open()


    def emby_event_button_user_select_login(self, *args):
        self.dismiss_popup()
        self.emby_user_connection_json = common_emby_network.com_network_emby_user_login(
            self.global_selected_server_addr, self.global_selected_user_id, self.login_password)
        # build header parameters to url
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.global_url_headers = {'User-Agent' : user_agent,
                                   'Authorization' : 'MediaBrowser',
                                   'UserId' : self.global_selected_user_id,
                                   'Client' : "Android",
                                   'Device' : "Samsung Galaxy SIII",
                                   'DeviceId' : uniqueid.id,
                                   'Version' : common_version.APP_VERSION}
        # go back to main menu
        self.root.ids._screen_manager.current = 'Main_Remote'


    def main_setup_screen(self, *args):
        """
        # setup button has been clicked
        """
        # clear the children and reload to pick up new records
        if self.base_device_guid_dict:
            self.root.ids.setup_base_device_gridlayout.clear_widgets()
        self.root.ids.setup_base_device_gridlayout.bind(
            minimum_height=self.root.ids.setup_base_device_gridlayout.setter('height'))
        # fetch base items for setup
        for base_device in common_database_octmote.com_db_device_list():
            btn1 = ToggleButton(text=base_device[1], size_hint_y=None, height=40,
                group='setup_base_device_button',)
            btn1.bind(on_press=partial(self.main_setup_base_device_selected,
                base_device[0]))
            self.root.ids.setup_base_device_gridlayout.add_widget(btn1)
            self.base_device_guid_dict[base_device[0]] = base_device[1]
        # clear the children and reload to pick up new records
        if self.base_item_guid_dict:
            self.root.ids.setup_base_item_gridlayout.clear_widgets()
        self.root.ids.setup_base_item_gridlayout.bind(
            minimum_height=self.root.ids.setup_base_item_gridlayout.setter('height'))
        # fetch items that users have added
        for item_device in common_database_octmote.com_db_item_list():
            btn1 = ToggleButton(text=item_device[1], size_hint_y=None, height=40,
                group='setup_item_device_button',)
            btn1.bind(on_press=partial(self.main_setup_base_item_selected, item_device[0]))
            self.root.ids.setup_base_item_gridlayout.add_widget(btn1)
            self.base_item_guid_dict[item_device[0]] = item_device[1]


    def main_setup_base_device_selected(self, *args):
        """
        # from setup screen a base device has been selected
        """
        pass


    def main_setup_base_item_selected(self, *args):
        """
        # from setup screen a device item has been selected
        """
        pass


    def show_load(self):
        """
        # load json file dialog
        """
        content = OctMoteLoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load Device Json File", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):
        try:
            with open(os.path.join(path, filename[0])) as stream:
                self.json_text = stream.read()
                self.root.ids.setup_item_json.text = self.json_text
        except:
            self.octmote_notification_popup('Json Error', 'Not a text json file!')
        self.dismiss_popup()
        # pop up the finalize item import verification
        self.root.ids._screen_manager.current = 'Setup_Item_Import_Verify'


    def octmote_notification_popup(self, header, message):
        """
        # notification dialog
        """
        content = OctMoteNotificationScreen(ok_button=self.dismiss_notification_popup)
        content.ids.message_text.text = message
        self._notification_popup = Popup(title=header, content=content, size_hint=(0.9, 0.9))
        self._notification_popup.open()


    def dismiss_notification_popup(self):
        self._notification_popup.dismiss()


    def setup_import_item_json(self, *args):
        """
        # from verify button, load json into the database
        """
        try:
            json_data = json.loads(self.root.ids.setup_item_json.text)
            item_guid = common_database_octmote.OctMote_Database_Sqlite3_Item_Insert(
                self.root.ids.setup_item_name.text, json_data)
            # add guid to items in memory
            self.base_item_guid_dict[item_guid] = self.root.ids.setup_item_name.text
        except:
            # do popup for json error
            self.octmote_notification_popup('Json Error', 'Unable to parse file!')


    def main_remote_control_event_process(self, action_type_list):
        """
        # process remote control button
        """
        try:
            json_data = json.loads(self.remote_mode_details_item[self.remote_mode_currrent_item])
            # check to see if rs232 device is already open
            if json_data["Protocol"]["Method"].lower() == "rs232":
                if not json_data["Protocol"]["Hardware Port"] in self.rs232_devices_dict:
                    self.rs232_devices_dict[json_data["Protocol"]["Host IP"]]\
                        = common_network_telnet.OctMote_Telnet_Open_Device(
                        json_data["Protocol"]["Host IP"],
                        json_data["Protocol"]["Host Port"], json_data["Protocol"]["User"],
                        json_data["Protocol"]["Password"])
                common__network_telnet.OctMote_Telnet_Write_Device(self.rs232_devices_dict[\
                    json_data["Protocol"]["Host IP"]],
                    self.octmote_json_fetch_data_for_command(json_data, action_type_list))
                pass
            # check to see if IR device is already open
            elif json_data["Protocol"]["Method"].lower() == "ir":
                if not json_data["fake"] in self.ir_devices_dict:
                    pass
            # check to see if lan device already open
            elif json_data["Protocol"]["Method"].lower() == "lan":
                if not (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"])\
                        in self.lan_devices_dict:
                    pass
            elif json_data["Protocol"]["Method"].lower() == "telnet":
                # check to see if telnet device already opened
                if not json_data["Protocol"]["Host IP"] in self.telnet_devices_dict:
                    self.telnet_devices_dict[json_data["Protocol"]["Host IP"]]\
                        = common_network_telnet.MK_Telnet_Open_Device(
                        json_data["Protocol"]["Host IP"],
                        json_data["Protocol"]["Host Port"], json_data["Protocol"]["User"],
                        json_data["Protocol"]["Password"])
                common_network_telnet.MK_Telnet_Write_Device(
                    self.telnet_devices_dict[json_data["Protocol"]["Host IP"]],
                    self.octmote_json_fetch_data_for_command(json_data, action_type_list))
            elif json_data["Protocol"]["Method"].lower() == "serial":
                # check to see if serial device already opened
                if not (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"])\
                        in self.serial_devices_dict:
                    self.serial_devices_dict[(json_data["Protocol"]["Host IP"],
                        json_data["Protocol"]["Hardware Port"])]\
                        = common_serial.MK_Serial_Open_Device(
                        json_data["Protocol"]["Hardware Port"],
                        json_data["Protocol"]["Baud Rate"], json_data["Protocol"]["Parity Bit"],
                        json_data["Protocol"]["Stop Bit"], json_data["Protocol"]["Data Length"])
                common_serial.MK_Serial_Write_Device(
                    self.serial_devices_dict[json_data["Protocol"]["Hardware Port"]],
                    self.octmote_json_fetch_data_for_command(json_data, action_type_list))
            elif json_data["Protocol"]["Method"].lower() == "eiscp":
                # check to see if eiscp device already open
                if not json_data["Protocol"]["Host IP"] in self.eiscp_devices_dict:
                    pass
            elif json_data["Protocol"]["Method"].lower() == "kivy":
                if not (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"])\
                        in self.kivy_lan_devices_dict:
                    self.kivy_lan_devices_dict[(json_data["Protocol"]["Host IP"],
                        json_data["Protocol"]["Hardware Port"])]\
                        = (json_data["Protocol"]["Host IP"],
                        json_data["Protocol"]["Hardware Port"])
                common_kodi.com_network_kodi_command(json_data["Protocol"]["Host IP"],
                    json_data["Protocol"]["Hardware Port"],
                    self.octmote_json_fetch_data_for_command(json_data, action_type_list))
            elif json_data["Protocol"]["Method"].lower() == "emby":
                pass
            else:
                print("Unhandled Protocol Method %s", json_data["Protocol"]["Method"])
        except:
            pass


    def octmote_json_fetch_data_for_command(json_data, action_type_list):
        """
        # grab data from json for command being issued
        """
        first_time = True
        for commands in action_type_list:
            if first_time:
                data_block = json_data[commands]
            else:
                data_block = data_block[commands]
            first_time = False
        return data_block

#####################################################
    # main calibration events
    def evt_cal_black_level(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Black Level"))


    def evt_cal_brightness(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Brightness"))


    def evt_cal_brightness_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Brightness Up"))


    def evt_cal_brightness_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Brightness Down"))


    def evt_cal_color(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color"))


    def evt_cal_color_temp(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Temperature"))


    def evt_cal_color_temp_r(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Temp R"))


    def evt_cal_color_temp_g(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Temp G"))


    def evt_cal_color_temp_b(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Temp B"))


    def evt_cal_color_balance_r(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Balance R"))


    def evt_cal_color_balance_g(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Balance G"))


    def evt_cal_color_balance_b(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Balance B"))


    def evt_cal_color_density_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Density Up"))


    def evt_cal_color_density_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Density Down"))


    def evt_cal_contrast(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Contrast"))


    def evt_cal_constrast_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Contrast Up"))


    def evt_cal_constrast_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Contrast Down"))


    # calbration convergance
    def evt_cal_conv_blanking(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Blanking"))


    def evt_cal_conv_blanking_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Blanking On"))


    def evt_cal_conv_blanking_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Blanking Off"))


    def evt_cal_conv_bow(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Bow"))


    def evt_cal_conv_dynamic(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Dynamic"))


    def evt_cal_conv_edge_linearity(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Edge Linearity"))


    def evt_cal_conv_keystone(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone"))


    def evt_cal_conv_keystone_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Up"))


    def evt_cal_conv_keystone_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Down"))


    def evt_cal_conv_keystone_left(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Left"))


    def evt_cal_conv_keystone_right(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Right"))


    def evt_cal_conv_linearity(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Linearity"))


    def evt_cal_conv_overscan_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Overscan On"))


    def evt_cal_conv_overscan_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Overscan Off"))


    def evt_cal_conv_phase(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Phase"))


    def evt_cal_conv_pincushion(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Pincushion"))


    def evt_cal_conv_shift(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Shift"))


    def evt_cal_conv_size(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Size"))


    def evt_cal_conv_skew(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Skew"))


    def evt_cal_conv_static(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Static"))


    def evt_cal_conv_quad_top_left(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Top Left"))


    def evt_cal_conv_quad_top(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Top"))


    def evt_cal_conv_quad_top_right(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance",
            "Quandrant Top Right"))


    def evt_cal_conv_quad_right(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Right"))


    def evt_cal_conv_quad_left(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Left"))


    def evt_cal_conv_quad_bottom_left(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance",
            "Quandrant Bottom Left"))


    def evt_cal_conv_quad_bottom_right(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance",
            "Quandrant Bottom Right"))


    def evt_cal_conv_quad_bottom(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Bottom"))


    def evt_cal_conv_vertical_center(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Veritcal Center"))


    def evt_cal_conv_vertical_size(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Vertical Size"))


    # calibration continued
    def evt_cal_detail(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Detail"))


    def evt_cal_detail_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Detail Up"))


    def evt_cal_detail_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Detail Down"))


    def evt_cal_gamma(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Gamma"))


    def evt_cal_gamma_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Gamma Up"))


    def evt_cal_gamma_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Gamma Down"))


    def evt_cal_hue(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Hue"))


    def evt_cal_hue_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Hue Up"))


    def evt_cal_hue_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Hue Down"))


    def evt_cal_tint(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Tint"))


    def evt_cal_tint_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Tint Up"))


    def evt_cal_tint_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Tint Down"))


    def evt_cal_sharpness(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Sharpness"))


    def evt_cal_sharpness_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Sharpness Up"))


    def evt_cal_sharpness_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Sharpness Down"))


#####################################################
    # main remote control events
    # application
    def evt_cmd_application_amazon(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Amazon Instant Video"))


    def evt_cmd_application_emby(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Emby"))


    def evt_cmd_application_hbogo(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "HBO Go"))


    def evt_cmd_application_hulu(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Hulu Plus"))


    def evt_cmd_application_kodi(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Kodi"))


    def evt_cmd_application_netflix(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Netflix"))


    def evt_cmd_application_pandora(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Pandora"))


    def evt_cmd_application_plex(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Plex"))


    def evt_cmd_application_siriusxm(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "SiriusXM"))


    def evt_cmd_application_slingtv(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "sling TV"))


    def evt_cmd_application_vudu(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Vudu"))


    # aspect ratio
    def evt_cmd_aspect_next(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Next Ratio"))


    def evt_cmd_aspect_auto(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Auto"))


    def evt_cmd_aspect_native(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Native"))


    def evt_cmd_aspect_letterbox(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Letterbox"))


    def evt_cmd_aspect_real(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Real"))


    def evt_cmd_aspect_4x3(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "4:3"))


    def evt_cmd_aspect_1x2(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "1:1"))


    def evt_cmd_aspect_1x85(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "1.85"))


    def evt_cmd_aspect_2x35(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "2.35"))


    def evt_cmd_aspect_16x9(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "16:9"))


    def evt_cmd_aspect_16x10(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "16:10"))


    # hardware
    def evt_cmd_hardware_channel(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Channel"))


    def evt_cmd_hardware_crt_b(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "CRT Blue"))


    def evt_cmd_hardware_crt_g(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "CRT Green"))


    def evt_cmd_hardware_crt_r(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "CRT Red"))


    def evt_cmd_hardware_cut_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Cut-Off"))


    def evt_cmd_hardware_lamp_hour_reset(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Lamp Hour Reset"))


    def evt_cmd_hardware_luminance(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Luminance"))


    def evt_cmd_hardware_optical_zoom_shift(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Optical Zoom Shift"))


    def evt_cmd_hardware_optical_focus_shift(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Optical Focus Shift"))


    def evt_cmd_hardware_projection_mode(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Projection Mode"))


    def evt_cmd_hardware_reset(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Reset"))


    def evt_cmd_hardware_shutter_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Shutter On"))


    def evt_cmd_hardware_shutter_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Shutter Off"))


    def evt_cmd_hardware_unit(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Unit"))


    def evt_cmd_hardware_whisper_mode(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Whisper Mode"))


    # misc
    def evt_cmd_misc_background(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Background"))


    def evt_cmd_misc_cc_display(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Closed Caption Display"))


    def evt_cmd_misc_film_mode(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Film Mode"))


    def evt_cmd_misc_freeze(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Freeze"))


    def evt_cmd_misc_freeze_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Freeze On"))


    def evt_cmd_misc_freeze_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Freeze Off"))


    def evt_cmd_misc_language(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Language"))


    def evt_cmd_misc_osd(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "OSD"))


    def evt_cmd_misc_osd_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "OSD On"))


    def evt_cmd_misc_osd_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "OSD Off"))


    def evt_cmd_misc_startup_image_yes(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Startup Image Yes"))


    def evt_cmd_misc_startup_image_no(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Startup Image No"))


    # navigation
    def evt_cmd_left(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Direction", "Left"))


    def evt_cmd_right(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Direction", "Right"))


    def evt_cmd_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Direction", "Up"))


    def evt_cmd_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Direction", "Down"))


    def evt_cmd_one(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "One"))


    def evt_cmd_two(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Two"))


    def evt_cmd_three(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Three"))


    def evt_cmd_four(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Four"))


    def evt_cmd_five(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Five"))


    def evt_cmd_six(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Six"))


    def evt_cmd_seven(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Seven"))


    def evt_cmd_eight(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Eight"))


    def evt_cmd_nine(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Nine"))


    def evt_cmd_fast_rewind(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Fast Rewind"))


    def evt_cmd_chapter_rewind(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Chapter Rewind"))


    def evt_cmd_fast_forward(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Fast Forward"))


    def evt_cmd_chapter_forward(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Chapter Forward"))


    def evt_cmd_play(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Play"))


    def evt_cmd_pause(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Pause"))


    def evt_cmd_stop(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Stop"))


    def evt_cmd_info(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Info"))


    def evt_cmd_record(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Record"))


    # power
    def evt_cmd_power_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Power", "On"))


    def evt_cmd_power_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Power", "Off"))


    def evt_cmd_power_standy(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Power", "Standby"))


    # sound
    def evt_cmd_sound_mute(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Sound", "Mute"))


    def evt_cmd_sound_unmute(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Sound", "UnMute"))


    def evt_cmd_sound_volume_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Sound", "Volume Up"))


    def evt_cmd_sound_volume_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Sound", "Volume Down"))


    # zoom
    def evt_cmd_zoom_zoom(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Zoom", "Zoom"))


    def evt_cmd_zoom_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Zoom", "Zoom Up"))


    def evt_cmd_zoom_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Zoom", "Zoom Down"))


#####################################################
    # querys
    # library media
    def evt_query_library_media_albums(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "Albums"))


    def evt_query_library_media_artists(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "Artists"))


    def evt_query_library_media_movies(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "Movies"))


    def evt_query_library_media_music_videos(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "Music Videos"))


    def evt_query_library_media_songs(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "Songs"))


    def evt_query_library_media_tv_shows(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "TV Shows"))


    # librrary playlist
    def evt_query_library_playlist_audio(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Playlist", "Audio"))


    def evt_query_library_playlist_video(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Playlist", "Video"))


    # more queries
    def evt_query_api_commands(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "API Commands"))


    def evt_query_aspect_ratio(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Aspect Ratio"))


    def evt_query_blank_status(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Blank Status"))


    def evt_query_brightness(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Brightness"))


    def evt_query_codec(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Codec (Playing Media)"))


    def evt_query_color_video(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Color (Video)"))


    def evt_query_color_mode(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Color Mode"))


    def evt_query_color_temp(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Color Temp"))


    def evt_query_company_name(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Company Name"))


    def evt_query_contrast(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Contrast"))


    def evt_query_density(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Density"))


    def evt_query_error_status(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Error Status"))


    def evt_query_filter_time(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Filter Time"))


    def evt_query_gain_green(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Gain Green"))


    def evt_query_gain_blue(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Gain Blue"))


    def evt_query_gain_red(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Gain Red"))


    def evt_query_input_selected(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Input Selected"))


    def evt_query_lamp_hours(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Lamp Hours"))


    def evt_query_lamp_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Lamp Off"))


    def evt_query_lamp_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Lamp On"))


    def evt_query_lamp_on_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Lamp On/Off"))


    def evt_query_model_name(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Model Name"))


    def evt_query_mute_status(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Mute Status"))


    def evt_query_native_resolution(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Native Resolution"))


    def evt_query_overscan_ratio(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Overscan Ratio"))


    def evt_query_power_state(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Power State"))


    def evt_query_projection_mode(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Projection Mode"))


    def evt_query_serial_number(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Serial Number"))


    def evt_query_sharpness(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Sharpness"))


    def evt_query_status(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Status"))


    def evt_query_tint_video(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Tint (Video)"))


    def evt_query_volume(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Volume"))


#####################################################
    # source
    def evt_source_aux1(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "AUX1"))


    def evt_source_aux2(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "AUX2"))


    def evt_source_bluray(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "BluRay"))


    def evt_source_cable_tv(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Cable/TV"))


    def evt_source_composite(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Composite"))


    def evt_source_component(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Component"))


    def evt_source_dvd(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "DVD"))


    def evt_source_game(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Game"))


    def evt_source_hdmi1(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI1"))


    def evt_source_hdmi2(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI2"))


    def evt_source_hdmi3(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI3"))


    def evt_source_hdmi4(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI4"))


    def evt_source_hdmi5(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI5"))


    def evt_source_hdmi6(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI6"))


    def evt_source_hdmi7(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI7"))


    def evt_source_hdmi8(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI8"))


    def evt_source_input(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Input"))


    def evt_source_laserdisc(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "LaserDisc"))


    def evt_source_net_usb(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Net/USB"))


    def evt_source_phono(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Phono"))


    def evt_source_rgb1(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "RGB1"))


    def evt_source_rgb2(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "RGB2"))


    def evt_source_satellite(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Satellite"))


    def evt_source_svideo(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "S-Video"))


    def evt_source_usb(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "USB"))


if __name__ == '__main__':
    # set signal exit breaks
    common_signal.com_signal_set_break()
    # load the kivy's here so all the classes have been defined
    Builder.load_file('kivy_layouts/main.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Load_Dialog.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Login.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Notification.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Slider.kv')
    OctMoteApp().run()
