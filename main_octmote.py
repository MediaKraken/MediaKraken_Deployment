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
__version__ = '0.1.6'
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
from common import common_ssdp
from common import common_telnet

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
        logging.debug("Connection Lost")

    def clientConnectionFailed(self, conn, reason):
        logging.debug("Connection Failed")


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
        self.OctMote_Server_Connection_Data = None
        self.server_list = None
        self.server_user_list = None
        self.global_selected_user_id = None
        self.emby_user_connection_json = None
        self.json_text = None
        self._notification_popup = None


    def exit_program(self):
        com_Database_Octmote.com_db_Close()


    def dismiss_popup(self):
        self._popup.dismiss()


    def build(self):
        self.base_device_guid_dict = {}
        self.base_item_guid_dict = {}
        self.base_layout_guid_dict = {}
        self.remote_mode_details_item = {}
        self.remote_mode_currrent_item = 'Default'
        # open database files
        self.OctMote_Server_Connection_Data = common_database_octmote.com_db_open()
        # fetch and import any item/layout files
        common_json.com_json_find()
        root = OctMote()
        self.connect_to_server()
        return root


    def connect_to_server(self):
        reactor.connectSSL(self.OctMote_Server_Connection_Data[0],\
            self.OctMote_Server_Connection_Data[1], EchoFactory(self), ssl.ClientContextFactory())


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
        self.server_list = com_MediaKraken.com_network_mediakraken_find_server()
        if self.server_list is not None:
            for found_server in self.server_list:
                btn1 = ToggleButton(text=self.server_list[found_server][1],\
                    group='mediakraken_server',)
                btn1.bind(on_press=partial(self.MediaKraken_Event_Button_Server_Select,\
                    found_server))
                self.root.ids.mediakraken_server_list_layout.add_widget(btn1)
        else:
            # go back to main menu
            self.root.ids._screen_manager.current = 'Main_Remote'


    def Emby_Find_Server_List(self):
        self.server_list = common_emby_network.com_network_emby_find_server()
        if self.server_list is not None:
            for found_server in self.server_list:
                btn1 = ToggleButton(text=self.server_list[found_server][1], group='emby_server',)
                btn1.bind(on_press=partial(self.Emby_Event_Button_Server_Select, found_server))
                self.root.ids.server_list_layout.add_widget(btn1)
        else:
            # go back to main menu
            self.root.ids._screen_manager.current = 'Main_Remote'


    def Emby_Event_Button_Server_Select(self, server_addr, *args):
        self.server_user_list = common_emby_network.com_network_emby_find_users(server_addr)
        self.root.ids.user_list_layout.clear_widgets()
        self.root.ids.user_list_layout.add_widget(Label(text='Emby Users(s)'))
        for found_user in self.server_user_list:
            btn1 = ToggleButton(text=found_user, group='emby_user',)
            btn1.bind(on_press=partial(self.Emby_Event_Button_User_Select, found_user))
            self.root.ids.user_list_layout.add_widget(btn1)
        self.global_selected_server_addr = server_addr


    def Emby_Event_Button_User_Select(self, server_user, *args):
        print("button server user %s", server_user)
        self.global_selected_user_id = server_user
        self.login_password = ''
        content = OctMoteLoginScreen(login_password=self.login_password, cancel=self.dismiss_popup)
        self._popup = Popup(title="Emby Login", content=content,\
            size_hint=(None, None), size=(425, 250))
        self._popup.open()


    def Emby_Event_Button_User_Select_Login(self, *args):
        self.dismiss_popup()
        self.emby_user_connection_json = common_emby_network.com_network_emby_user_login(\
            self.global_selected_server_addr, self.global_selected_user_id, self.login_password)
        # build header parameters to url
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.global_url_headers = {'User-Agent' : user_agent,
                                   'Authorization' : 'MediaBrowser',
                                   'UserId' : self.global_selected_user_id,
                                   'Client' : "Android",
                                   'Device' : "Samsung Galaxy SIII",
                                   'DeviceId' : uniqueid.id,
                                   'Version' : __version__}
        # go back to main menu
        self.root.ids._screen_manager.current = 'Main_Remote'


    # setup button has been clicked
    def main_OctMote_Setup_Screen(self, *args):
        # clear the children and reload to pick up new records
        if self.base_device_guid_dict:
            self.root.ids.setup_base_device_gridlayout.clear_widgets()
        self.root.ids.setup_base_device_gridlayout.bind(\
            minimum_height=self.root.ids.setup_base_device_gridlayout.setter('height'))
        # fetch base items for setup
        for base_device in common_database_octmote.com_db_device_list():
            btn1 = ToggleButton(text=base_device[1], size_hint_y=None, height=40,\
                group='setup_base_device_button',)
            btn1.bind(on_press=partial(self.main_OctMote_Setup_Base_Device_Selected,\
                base_device[0]))
            self.root.ids.setup_base_device_gridlayout.add_widget(btn1)
            self.base_device_guid_dict[base_device[0]] = base_device[1]
        # clear the children and reload to pick up new records
        if self.base_item_guid_dict:
            self.root.ids.setup_base_item_gridlayout.clear_widgets()
        self.root.ids.setup_base_item_gridlayout.bind(\
            minimum_height=self.root.ids.setup_base_item_gridlayout.setter('height'))
        # fetch items that users have added
        for item_device in common_database_octmote.com_db_item_list():
            btn1 = ToggleButton(text=item_device[1], size_hint_y=None, height=40,\
                group='setup_item_device_button',)
            btn1.bind(on_press=partial(self.main_OctMote_Setup_Base_Item_Selected, item_device[0]))
            self.root.ids.setup_base_item_gridlayout.add_widget(btn1)
            self.base_item_guid_dict[item_device[0]] = item_device[1]


    # from setup screen a base device has been selected
    def main_OctMote_Setup_Base_Device_Selected(self, *args):
        pass


    # from setup screen a device item has been selected
    def main_OctMote_Setup_Base_Item_Selected(self, *args):
        pass


    # load json file dialog
    def show_load(self):
        content = OctMoteLoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load Device Json File", content=content, size_hint=(0.9, 0.9))
        self._popup.open()


    def load(self, path, filename):
        try:
            with open(os.path.join(path, filename[0])) as stream:
                self.json_text = stream.read()
                self.root.ids.setup_item_json.text = self.json_text
        except:
            self.OctMote_Notification_Popup('Json Error', 'Not a text json file!')
        self.dismiss_popup()
        # pop up the finalize item import verification
        self.root.ids._screen_manager.current = 'Setup_Item_Import_Verify'


    # notification dialog
    def OctMote_Notification_Popup(self, header, message):
        content = OctMoteNotificationScreen(ok_button=self.dismiss_notification_popup)
        content.ids.message_text.text = message
        self._notification_popup = Popup(title=header, content=content, size_hint=(0.9, 0.9))
        self._notification_popup.open()


    def dismiss_notification_popup(self):
        self._notification_popup.dismiss()


    # from verify button, load json into the database
    def Setup_Import_Item_Json(self, *args):
        try:
            json_data = json.loads(self.root.ids.setup_item_json.text)
            item_guid = common_database_octmote.OctMote_Database_Sqlite3_Item_Insert(\
                self.root.ids.setup_item_name.text, json_data)
            # add guid to items in memory
            self.base_item_guid_dict[item_guid] = self.root.ids.setup_item_name.text
        except:
            # do popup for json error
            self.OctMote_Notification_Popup('Json Error', 'Unable to parse file!')


    # process remote control button
    def main_remote_control_event_process(self, action_type_list):
        try:
            json_data = json.loads(self.remote_mode_details_item[self.remote_mode_currrent_item])
            # check to see if rs232 device is already open
            if json_data["Protocol"]["Method"].lower() == "rs232":
                if not json_data["Protocol"]["Hardware Port"] in self.rs232_devices_dict:
                    self.rs232_devices_dict[json_data["Protocol"]["Host IP"]]\
                        = common_telnet.OctMote_Telnet_Open_Device(\
                        json_data["Protocol"]["Host IP"],\
                        json_data["Protocol"]["Host Port"], json_data["Protocol"]["User"],\
                        json_data["Protocol"]["Password"])
                common_telnet.OctMote_Telnet_Write_Device(self.rs232_devices_dict[\
                    json_data["Protocol"]["Host IP"]],\
                    self.OctMote_JSON_Fetch_Data_For_Command(json_data, action_type_list))
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
                        = common_telnet.MK_Telnet_Open_Device(json_data["Protocol"]["Host IP"],\
                        json_data["Protocol"]["Host Port"], json_data["Protocol"]["User"],\
                        json_data["Protocol"]["Password"])
                common_telnet.MK_Telnet_Write_Device(\
                    self.telnet_devices_dict[json_data["Protocol"]["Host IP"]],\
                    self.OctMote_JSON_Fetch_Data_For_Command(json_data, action_type_list))
            elif json_data["Protocol"]["Method"].lower() == "serial":
                # check to see if serial device already opened
                if not (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"])\
                        in self.serial_devices_dict:
                    self.serial_devices_dict[(json_data["Protocol"]["Host IP"],\
                        json_data["Protocol"]["Hardware Port"])]\
                        = common_serial.MK_Serial_Open_Device(json_data["Protocol"]["Hardware Port"],\
                        json_data["Protocol"]["Baud Rate"], json_data["Protocol"]["Parity Bit"],\
                        json_data["Protocol"]["Stop Bit"], json_data["Protocol"]["Data Length"])
                common_serial.MK_Serial_Write_Device(\
                    self.serial_devices_dict[json_data["Protocol"]["Hardware Port"]],\
                    self.OctMote_JSON_Fetch_Data_For_Command(json_data, action_type_list))
            elif json_data["Protocol"]["Method"].lower() == "eiscp":
                # check to see if eiscp device already open
                if not json_data["Protocol"]["Host IP"] in self.eiscp_devices_dict:
                    pass
            elif json_data["Protocol"]["Method"].lower() == "kivy":
                if not (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"])\
                        in self.kivy_lan_devices_dict:
                    self.kivy_lan_devices_dict[(json_data["Protocol"]["Host IP"],\
                        json_data["Protocol"]["Hardware Port"])]\
                        = (json_data["Protocol"]["Host IP"],\
                        json_data["Protocol"]["Hardware Port"])
                common_kodi.com_network_Kodi_Command(json_data["Protocol"]["Host IP"],\
                    json_data["Protocol"]["Hardware Port"],\
                    self.OctMote_JSON_Fetch_Data_For_Command(json_data, action_type_list))
            elif json_data["Protocol"]["Method"].lower() == "emby":
                pass
            else:
                print("Unhandled Protocol Method %s", json_data["Protocol"]["Method"])
        except:
            pass


    # grab data from json for command being issued
    def OctMote_JSON_Fetch_Data_For_Command(json_data, action_type_list):
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
    def main_evt_cal_black_level(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Black Level"))


    def main_evt_cal_brightness(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Brightness"))


    def main_evt_cal_brightness_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Brightness Up"))


    def main_evt_cal_brightness_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Brightness Down"))


    def main_evt_cal_color(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color"))


    def main_evt_cal_color_temp(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Temperature"))


    def main_evt_cal_color_temp_r(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Temp R"))


    def main_evt_cal_color_temp_g(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Temp G"))


    def main_evt_cal_color_temp_b(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Temp B"))


    def main_evt_cal_color_balance_r(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Balance R"))


    def main_evt_cal_color_balance_g(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Balance G"))


    def main_evt_cal_color_balance_b(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Balance B"))


    def main_evt_cal_color_density_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Density Up"))


    def main_evt_cal_color_density_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Color Density Down"))


    def main_evt_cal_contrast(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Contrast"))


    def main_evt_cal_constrast_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Contrast Up"))


    def main_evt_cal_constrast_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Contrast Down"))


    # calbration convergance
    def main_evt_cal_convergance_blanking(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Blanking"))


    def main_evt_cal_convergance_blanking_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Blanking On"))


    def main_evt_cal_convergance_blanking_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Blanking Off"))


    def main_evt_cal_convergance_bow(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Bow"))


    def main_evt_cal_convergance_dynamic(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Dynamic"))


    def main_evt_cal_convergance_edge_linearity(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Edge Linearity"))


    def main_evt_cal_convergance_keystone(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone"))


    def main_evt_cal_convergance_keystone_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Up"))


    def main_evt_cal_convergance_keystone_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Down"))


    def main_evt_cal_convergance_keystone_left(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Left"))


    def main_evt_cal_convergance_keystone_right(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Right"))


    def main_evt_cal_convergance_linearity(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Linearity"))


    def main_evt_cal_convergance_overscan_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Overscan On"))


    def main_evt_cal_convergance_overscan_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Overscan Off"))


    def main_evt_cal_convergance_phase(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Phase"))


    def main_evt_cal_convergance_pincushion(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Pincushion"))


    def main_evt_cal_convergance_shift(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Shift"))


    def main_evt_cal_convergance_size(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Size"))


    def main_evt_cal_convergance_skew(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Skew"))


    def main_evt_cal_convergance_static(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Static"))


    def main_evt_cal_convergance_quad_top_left(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Top Left"))


    def main_evt_cal_convergance_quad_top(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Top"))


    def main_evt_cal_convergance_quad_top_right(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance",\
            "Quandrant Top Right"))


    def main_evt_cal_convergance_quad_right(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Right"))


    def main_evt_cal_convergance_quad_left(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Left"))


    def main_evt_cal_convergance_quad_bottom_left(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance",\
            "Quandrant Bottom Left"))


    def main_evt_cal_convergance_quad_bottom_right(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance",\
            "Quandrant Bottom Right"))


    def main_evt_cal_convergance_quad_bottom(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Bottom"))


    def main_evt_cal_convergance_vertical_center(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Veritcal Center"))


    def main_evt_cal_convergance_vertical_size(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Convergance", "Vertical Size"))


    # calibration continued
    def main_evt_cal_detail(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Detail"))


    def main_evt_cal_detail_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Detail Up"))


    def main_evt_cal_detail_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Detail Down"))


    def main_evt_cal_gamma(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Gamma"))


    def main_evt_cal_gamma_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Gamma Up"))


    def main_evt_cal_gamma_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Gamma Down"))


    def main_evt_cal_hue(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Hue"))


    def main_evt_cal_hue_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Hue Up"))


    def main_evt_cal_hue_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Hue Down"))


    def main_evt_cal_tint(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Tint"))


    def main_evt_cal_tint_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Tint Up"))


    def main_evt_cal_tint_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Tint Down"))


    def main_evt_cal_sharpness(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Sharpness"))


    def main_evt_cal_sharpness_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Sharpness Up"))


    def main_evt_cal_sharpness_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Calibration", "Sharpness Down"))


#####################################################
    # main remote control events
    # application
    def main_evt_commands_application_amazon(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Amazon Instant Video"))


    def main_evt_commands_application_emby(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Emby"))


    def main_evt_commands_application_hbogo(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "HBO Go"))


    def main_evt_commands_application_hulu(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Hulu Plus"))


    def main_evt_commands_application_kodi(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Kodi"))


    def main_evt_commands_application_netflix(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Netflix"))


    def main_evt_commands_application_pandora(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Pandora"))


    def main_evt_commands_application_plex(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Plex"))


    def main_evt_commands_application_siriusxm(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "SiriusXM"))


    def main_evt_commands_application_slingtv(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "sling TV"))


    def main_evt_commands_application_vudu(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Application", "Vudu"))


    # aspect ratio
    def main_evt_commands_aspect_next(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Next Ratio"))


    def main_evt_commands_aspect_auto(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Auto"))


    def main_evt_commands_aspect_native(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Native"))


    def main_evt_commands_aspect_letterbox(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Letterbox"))


    def main_evt_commands_aspect_real(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Real"))


    def main_evt_commands_aspect_4x3(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "4:3"))


    def main_evt_commands_aspect_1x2(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "1:1"))


    def main_evt_commands_aspect_1x85(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "1.85"))


    def main_evt_commands_aspect_2x35(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "2.35"))


    def main_evt_commands_aspect_16x9(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "16:9"))


    def main_evt_commands_aspect_16x10(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "16:10"))


    # hardware
    def main_evt_commands_hardware_channel(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Channel"))


    def main_evt_commands_hardware_crt_b(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "CRT Blue"))


    def main_evt_commands_hardware_crt_g(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "CRT Green"))


    def main_evt_commands_hardware_crt_r(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "CRT Red"))


    def main_evt_commands_hardware_cut_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Cut-Off"))


    def main_evt_commands_hardware_lamp_hour_reset(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Lamp Hour Reset"))


    def main_evt_commands_hardware_luminance(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Luminance"))


    def main_evt_commands_hardware_optical_zoom_shift(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Optical Zoom Shift"))


    def main_evt_commands_hardware_optical_focus_shift(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Optical Focus Shift"))


    def main_evt_commands_hardware_projection_mode(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Projection Mode"))


    def main_evt_commands_hardware_reset(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Reset"))


    def main_evt_commands_hardware_shutter_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Shutter On"))


    def main_evt_commands_hardware_shutter_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Shutter Off"))


    def main_evt_commands_hardware_unit(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Unit"))


    def main_evt_commands_hardware_whisper_mode(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Hardware", "Whisper Mode"))


    # misc
    def main_evt_commands_misc_background(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Background"))


    def main_evt_commands_misc_cc_display(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Closed Caption Display"))


    def main_evt_commands_misc_film_mode(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Film Mode"))


    def main_evt_commands_misc_freeze(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Freeze"))


    def main_evt_commands_misc_freeze_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Freeze On"))


    def main_evt_commands_misc_freeze_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Freeze Off"))


    def main_evt_commands_misc_language(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Language"))


    def main_evt_commands_misc_osd(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "OSD"))


    def main_evt_commands_misc_osd_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "OSD On"))


    def main_evt_commands_misc_osd_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "OSD Off"))


    def main_evt_commands_misc_startup_image_yes(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Startup Image Yes"))


    def main_evt_commands_misc_startup_image_no(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Misc", "Startup Image No"))


    # navigation
    def main_evt_commands_left(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Direction", "Left"))


    def main_evt_commands_right(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Direction", "Right"))


    def main_evt_commands_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Direction", "Up"))


    def main_evt_commands_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Direction", "Down"))


    def main_evt_commands_one(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "One"))


    def main_evt_commands_two(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Two"))


    def main_evt_commands_three(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Three"))


    def main_evt_commands_four(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Four"))


    def main_evt_commands_five(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Five"))


    def main_evt_commands_six(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Six"))


    def main_evt_commands_seven(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Seven"))


    def main_evt_commands_eight(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Eight"))


    def main_evt_commands_nine(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Numeric", "Nine"))


    def main_evt_commands_fast_rewind(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Fast Rewind"))


    def main_evt_commands_chapter_rewind(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Chapter Rewind"))


    def main_evt_commands_fast_forward(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Fast Forward"))


    def main_evt_commands_chapter_forward(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Chapter Forward"))


    def main_evt_commands_play(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Play"))


    def main_evt_commands_pause(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Pause"))


    def main_evt_commands_stop(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Stop"))


    def main_evt_commands_info(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Info"))


    def main_evt_commands_record(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Navigation", "Record"))


    # power
    def main_evt_commands_power_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Power", "On"))


    def main_evt_commands_power_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Power", "Off"))


    def main_evt_commands_power_standy(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Power", "Standby"))


    # sound
    def main_evt_commands_sound_mute(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Sound", "Mute"))


    def main_evt_commands_sound_unmute(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Sound", "UnMute"))


    def main_evt_commands_sound_volume_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Sound", "Volume Up"))


    def main_evt_commands_sound_volume_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Sound", "Volume Down"))


    # zoom
    def main_evt_commands_zoom_zoom(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Zoom", "Zoom"))


    def main_evt_commands_zoom_up(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Zoom", "Zoom Up"))


    def main_evt_commands_zoom_down(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Commands", "Zoom", "Zoom Down"))


#####################################################
    # querys
    # library media
    def main_evt_query_library_media_albums(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "Albums"))


    def main_evt_query_library_media_artists(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "Artists"))


    def main_evt_query_library_media_movies(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "Movies"))


    def main_evt_query_library_media_music_videos(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "Music Videos"))


    def main_evt_query_library_media_songs(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "Songs"))


    def main_evt_query_library_media_tv_shows(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Media", "TV Shows"))


    # librrary playlist
    def main_evt_query_library_playlist_audio(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Playlist", "Audio"))


    def main_evt_query_library_playlist_video(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Library", "Playlist", "Video"))


    # more queries
    def main_evt_query_api_commands(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "API Commands"))


    def main_evt_query_aspect_ratio(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Aspect Ratio"))


    def main_evt_query_blank_status(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Blank Status"))


    def main_evt_query_brightness(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Brightness"))


    def main_evt_query_codec(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Codec (Playing Media)"))


    def main_evt_query_color_video(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Color (Video)"))


    def main_evt_query_color_mode(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Color Mode"))


    def main_evt_query_color_temp(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Color Temp"))


    def main_evt_query_company_name(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Company Name"))


    def main_evt_query_contrast(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Contrast"))


    def main_evt_query_density(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Density"))


    def main_evt_query_error_status(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Error Status"))


    def main_evt_query_filter_time(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Filter Time"))


    def main_evt_query_gain_green(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Gain Green"))


    def main_evt_query_gain_blue(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Gain Blue"))


    def main_evt_query_gain_red(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Gain Red"))


    def main_evt_query_input_selected(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Input Selected"))


    def main_evt_query_lamp_hours(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Lamp Hours"))


    def main_evt_query_lamp_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Lamp Off"))


    def main_evt_query_lamp_on(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Lamp On"))


    def main_evt_query_lamp_on_off(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Lamp On/Off"))


    def main_evt_query_model_name(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Model Name"))


    def main_evt_query_mute_status(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Mute Status"))


    def main_evt_query_native_resolution(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Native Resolution"))


    def main_evt_query_overscan_ratio(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Overscan Ratio"))


    def main_evt_query_power_state(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Power State"))


    def main_evt_query_projection_mode(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Projection Mode"))


    def main_evt_query_serial_number(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Serial Number"))


    def main_evt_query_sharpness(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Sharpness"))


    def main_evt_query_status(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Status"))


    def main_evt_query_tint_video(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Tint (Video)"))


    def main_evt_query_volume(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Query", "Volume"))


#####################################################
    # source
    def main_evt_source_aux1(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "AUX1"))


    def main_evt_source_aux2(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "AUX2"))


    def main_evt_source_bluray(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "BluRay"))


    def main_evt_source_cable_tv(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Cable/TV"))


    def main_evt_source_composite(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Composite"))


    def main_evt_source_component(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Component"))


    def main_evt_source_dvd(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "DVD"))


    def main_evt_source_game(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Game"))


    def main_evt_source_hdmi1(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI1"))


    def main_evt_source_hdmi2(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI2"))


    def main_evt_source_hdmi3(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI3"))


    def main_evt_source_hdmi4(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI4"))


    def main_evt_source_hdmi5(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI5"))


    def main_evt_source_hdmi6(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI6"))


    def main_evt_source_hdmi7(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI7"))


    def main_evt_source_hdmi8(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "HDMI8"))


    def main_evt_source_input(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Input"))


    def main_evt_source_laserdisc(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "LaserDisc"))


    def main_evt_source_net_usb(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Net/USB"))


    def main_evt_source_phono(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Phono"))


    def main_evt_source_rgb1(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "RGB1"))


    def main_evt_source_rgb2(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "RGB2"))


    def main_evt_source_satellite(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "Satellite"))


    def main_evt_source_svideo(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "S-Video"))


    def main_evt_source_usb(self):
        """
        Process button event
        """
        self.main_remote_control_event_process(("Source", "USB"))


if __name__ == '__main__':
    # load the kivy's here so all the classes have been defined
    Builder.load_file('kivy_layouts/main.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Load_Dialog.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Login.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Notification.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Slider.kv')
    OctMoteApp().run()
