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

__version__ = '0.1.6'
from __future__ import absolute_import, division, print_function, unicode_literals
# import plyer to fetch UID of devices
from plyer import uniqueid
import json
import sys
import os
sys.path.append("../common")
import MK_Common_Database_Octmote
import MK_Common_ISCP
import MK_Common_LIRC
import MK_Common_Emby_Network
import common_network
import MK_Common_Roku_Network
import MK_Common_Serial
import MK_Common_SSDP
import MK_Common_Telnet
import MK_Common_JSON
import MK_Common_Kodi

#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
from kivy.lang import Builder
install_twisted_reactor()
from twisted.internet import ssl, reactor, protocol
import MK_Common_Emby
import MK_Common_MediaKraken


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
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty
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

    def exit_program(self):
        MK_Common_Database_Octmote.MK_Database_Sqlite3_Close()


    def dismiss_popup(self):
        self._popup.dismiss()


    def build(self):
        self.base_device_guid_dict = {}
        self.base_item_guid_dict = {}
        self.base_layout_guid_dict = {}
        self.remote_mode_details_item = {}
        self.remote_mode_currrent_item = 'Default'
        # open database files
        self.OctMote_Server_Connection_Data = MK_Common_Database_Octmote.MK_Database_Sqlite3_Open()
        # fetch and import any item/layout files
        MK_Common_JSON.MK_Json_Find()
        root = OctMote()
        self.connect_to_server()
        return root


    def connect_to_server(self):
        reactor.connectSSL(self.OctMote_Server_Connection_Data[0], self.OctMote_Server_Connection_Data[1], EchoFactory(self), ssl.ClientContextFactory())


    def on_connection(self, connection):
        print("Connected succesfully to OctMote server!")
        self.connection = connection
        # load control layout


    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.textbox.text))
            self.textbox.text = ""


    def MediaKraken_Find_Server_List(self):
        self.server_list = MK_Common_MediaKraken.common_network_MediaKraken_Find_Server()
        if self.server_list is not None:
            for found_server in self.server_list:
                btn1 = ToggleButton(text=self.server_list[found_server][1], group='mediakraken_server',)
                btn1.bind(on_press=partial(self.MediaKraken_Event_Button_Server_Select, found_server))
                self.root.ids.mediakraken_server_list_layout.add_widget(btn1)
        else:
            # go back to main menu
            self.root.ids._screen_manager.current = 'Main_Remote'


    def Emby_Find_Server_List(self):
        self.server_list = MK_Common_Emby_Network.common_network_Emby_Find_Server()
        if self.server_list is not None:
            for found_server in self.server_list:
                btn1 = ToggleButton(text=self.server_list[found_server][1], group='emby_server',)
                btn1.bind(on_press=partial(self.Emby_Event_Button_Server_Select, found_server))
                self.root.ids.server_list_layout.add_widget(btn1)
        else:
            # go back to main menu
            self.root.ids._screen_manager.current = 'Main_Remote'


    def Emby_Event_Button_Server_Select(self, server_addr, *args):
        self.server_user_list = MK_Common_Emby_Network.common_network_Emby_Find_Users(server_addr)
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
        self._popup = Popup(title="Emby Login", content=content, size_hint=(None, None), size=(425, 250))
        self._popup.open()


    def Emby_Event_Button_User_Select_Login(self, *args):
        self.dismiss_popup()
        self.emby_user_connection_json = MK_Common_Emby_Network.common_network_Emby_User_Login(self.global_selected_server_addr, self.global_selected_user_id, self.login_password)
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
        self.root.ids.setup_base_device_gridlayout.bind(minimum_height=self.root.ids.setup_base_device_gridlayout.setter('height'))
        # fetch base items for setup
        for base_device in MK_Common_Database_Octmote.MK_Database_Sqlite3_Device_List():
            btn1 = ToggleButton(text=base_device[1], size_hint_y=None, height=40, group='setup_base_device_button',)
            btn1.bind(on_press=partial(self.main_OctMote_Setup_Base_Device_Selected, base_device[0]))
            self.root.ids.setup_base_device_gridlayout.add_widget(btn1)
            self.base_device_guid_dict[base_device[0]] = base_device[1]
        # clear the children and reload to pick up new records
        if self.base_item_guid_dict:
            self.root.ids.setup_base_item_gridlayout.clear_widgets()
        self.root.ids.setup_base_item_gridlayout.bind(minimum_height=self.root.ids.setup_base_item_gridlayout.setter('height'))
        # fetch items that users have added
        for item_device in MK_Common_Database_Octmote.MK_Database_Sqlite3_Item_List():
            btn1 = ToggleButton(text=item_device[1], size_hint_y=None, height=40, group='setup_item_device_button',)
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
            item_guid = MK_Common_Database_Octmote.OctMote_Database_Sqlite3_Item_Insert(self.root.ids.setup_item_name.text, json_data)
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
                    self.rs232_devices_dict[json_data["Protocol"]["Host IP"]] = MK_Common_Telnet.OctMote_Telnet_Open_Device(json_data["Protocol"]["Host IP"], json_data["Protocol"]["Host Port"], json_data["Protocol"]["User"], json_data["Protocol"]["Password"])
                MK_Common_Telnet.OctMote_Telnet_Write_Device(self.rs232_devices_dict[json_data["Protocol"]["Host IP"]], self.OctMote_JSON_Fetch_Data_For_Command(json_data, action_type_list))
                pass
            # check to see if IR device is already open
            elif json_data["Protocol"]["Method"].lower() == "ir":
                if not json_data["fake"] in self.ir_devices_dict:
                    pass
                pass
            # check to see if lan device already open
            elif json_data["Protocol"]["Method"].lower() == "lan":
                if not (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"]) in self.lan_devices_dict:
                   pass
                pass
            elif json_data["Protocol"]["Method"].lower() == "telnet":
                # check to see if telnet device already opened
                if not json_data["Protocol"]["Host IP"] in self.telnet_devices_dict:
                    self.telnet_devices_dict[json_data["Protocol"]["Host IP"]] = MK_Common_Telnet.MK_Telnet_Open_Device(json_data["Protocol"]["Host IP"], json_data["Protocol"]["Host Port"], json_data["Protocol"]["User"], json_data["Protocol"]["Password"])
                MK_Common_Telnet.MK_Telnet_Write_Device(self.telnet_devices_dict[json_data["Protocol"]["Host IP"]], self.OctMote_JSON_Fetch_Data_For_Command(json_data, action_type_list))
            elif json_data["Protocol"]["Method"].lower() == "serial":
                # check to see if serial device already opened
                if not (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"]) in self.serial_devices_dict:
                    self.serial_devices_dict[(json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"])] = MK_Common_Serial.MK_Serial_Open_Device(json_data["Protocol"]["Hardware Port"], json_data["Protocol"]["Baud Rate"], json_data["Protocol"]["Parity Bit"], json_data["Protocol"]["Stop Bit"], json_data["Protocol"]["Data Length"])
                MK_Common_Serial.MK_Serial_Write_Device(self.serial_devices_dict[json_data["Protocol"]["Hardware Port"]], self.OctMote_JSON_Fetch_Data_For_Command(json_data, action_type_list))
            elif json_data["Protocol"]["Method"].lower() == "eiscp":
                # check to see if eiscp device already open
                if not json_data["Protocol"]["Host IP"] in self.eiscp_devices_dict:
                    pass
                pass
            elif json_data["Protocol"]["Method"].lower() == "kivy":
                if not (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"]) in self.kivy_lan_devices_dict:
                    self.kivy_lan_devices_dict[(json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"])] = (json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"])
                MK_Common_Kodi.common_network_Kodi_Command(json_data["Protocol"]["Host IP"], json_data["Protocol"]["Hardware Port"], self.OctMote_JSON_Fetch_Data_For_Command(json_data, action_type_list))
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
    def main_remote_event_button_calibration_black_level(self):
        self.main_remote_control_event_process(("Calibration", "Black Level"))


    def main_remote_event_button_calibration_brightness(self):
        self.main_remote_control_event_process(("Calibration", "Brightness"))


    def main_remote_event_button_calibration_brightness_up(self):
        self.main_remote_control_event_process(("Calibration", "Brightness Up"))


    def main_remote_event_button_calibration_brightness_down(self):
        self.main_remote_control_event_process(("Calibration", "Brightness Down"))


    def main_remote_event_button_calibration_color(self):
        self.main_remote_control_event_process(("Calibration", "Color"))


    def main_remote_event_button_calibration_color_temp(self):
        self.main_remote_control_event_process(("Calibration", "Color Temperature"))


    def main_remote_event_button_calibration_color_temp_r(self):
        self.main_remote_control_event_process(("Calibration", "Color Temp R"))


    def main_remote_event_button_calibration_color_temp_g(self):
        self.main_remote_control_event_process(("Calibration", "Color Temp G"))


    def main_remote_event_button_calibration_color_temp_b(self):
        self.main_remote_control_event_process(("Calibration", "Color Temp B"))


    def main_remote_event_button_calibration_color_balance_r(self):
        self.main_remote_control_event_process(("Calibration", "Color Balance R"))


    def main_remote_event_button_calibration_color_balance_g(self):
        self.main_remote_control_event_process(("Calibration", "Color Balance G"))


    def main_remote_event_button_calibration_color_balance_b(self):
        self.main_remote_control_event_process(("Calibration", "Color Balance B"))


    def main_remote_event_button_calibration_color_density_up(self):
        self.main_remote_control_event_process(("Calibration", "Color Density Up"))


    def main_remote_event_button_calibration_color_density_down(self):
        self.main_remote_control_event_process(("Calibration", "Color Density Down"))


    def main_remote_event_button_calibration_contrast(self):
        self.main_remote_control_event_process(("Calibration", "Contrast"))


    def main_remote_event_button_calibration_constrast_up(self):
        self.main_remote_control_event_process(("Calibration", "Contrast Up"))


    def main_remote_event_button_calibration_constrast_down(self):
        self.main_remote_control_event_process(("Calibration", "Contrast Down"))


    # calbration convergance
    def main_remote_event_button_calibration_convergance_blanking(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Blanking"))


    def main_remote_event_button_calibration_convergance_blanking_on(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Blanking On"))


    def main_remote_event_button_calibration_convergance_blanking_off(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Blanking Off"))


    def main_remote_event_button_calibration_convergance_bow(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Bow"))


    def main_remote_event_button_calibration_convergance_dynamic(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Dynamic"))


    def main_remote_event_button_calibration_convergance_edge_linearity(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Edge Linearity"))


    def main_remote_event_button_calibration_convergance_keystone(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone"))


    def main_remote_event_button_calibration_convergance_keystone_up(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Up"))


    def main_remote_event_button_calibration_convergance_keystone_down(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Down"))


    def main_remote_event_button_calibration_convergance_keystone_left(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Left"))


    def main_remote_event_button_calibration_convergance_keystone_right(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Keystone Right"))


    def main_remote_event_button_calibration_convergance_linearity(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Linearity"))


    def main_remote_event_button_calibration_convergance_overscan_on(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Overscan On"))


    def main_remote_event_button_calibration_convergance_overscan_off(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Overscan Off"))


    def main_remote_event_button_calibration_convergance_phase(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Phase"))


    def main_remote_event_button_calibration_convergance_pincushion(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Pincushion"))


    def main_remote_event_button_calibration_convergance_shift(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Shift"))


    def main_remote_event_button_calibration_convergance_size(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Size"))


    def main_remote_event_button_calibration_convergance_skew(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Skew"))


    def main_remote_event_button_calibration_convergance_static(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Static"))


    def main_remote_event_button_calibration_convergance_quad_top_left(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Top Left"))


    def main_remote_event_button_calibration_convergance_quad_top(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Top"))


    def main_remote_event_button_calibration_convergance_quad_top_right(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Top Right"))


    def main_remote_event_button_calibration_convergance_quad_right(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Right"))


    def main_remote_event_button_calibration_convergance_quad_left(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Left"))


    def main_remote_event_button_calibration_convergance_quad_bottom_left(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Bottom Left"))


    def main_remote_event_button_calibration_convergance_quad_bottom_right(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Bottom Right"))


    def main_remote_event_button_calibration_convergance_quad_bottom(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Quandrant Bottom"))


    def main_remote_event_button_calibration_convergance_vertical_center(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Veritcal Center"))


    def main_remote_event_button_calibration_convergance_vertical_size(self):
        self.main_remote_control_event_process(("Calibration", "Convergance", "Vertical Size"))


    # calibration continued
    def main_remote_event_button_calibration_detail(self):
        self.main_remote_control_event_process(("Calibration", "Detail"))


    def main_remote_event_button_calibration_detail_up(self):
        self.main_remote_control_event_process(("Calibration", "Detail Up"))


    def main_remote_event_button_calibration_detail_down(self):
        self.main_remote_control_event_process(("Calibration", "Detail Down"))


    def main_remote_event_button_calibration_gamma(self):
        self.main_remote_control_event_process(("Calibration", "Gamma"))


    def main_remote_event_button_calibration_gamma_up(self):
        self.main_remote_control_event_process(("Calibration", "Gamma Up"))


    def main_remote_event_button_calibration_gamma_down(self):
        self.main_remote_control_event_process(("Calibration", "Gamma Down"))


    def main_remote_event_button_calibration_hue(self):
        self.main_remote_control_event_process(("Calibration", "Hue"))


    def main_remote_event_button_calibration_hue_up(self):
        self.main_remote_control_event_process(("Calibration", "Hue Up"))


    def main_remote_event_button_calibration_hue_down(self):
        self.main_remote_control_event_process(("Calibration", "Hue Down"))


    def main_remote_event_button_calibration_tint(self):
        self.main_remote_control_event_process(("Calibration", "Tint"))


    def main_remote_event_button_calibration_tint_up(self):
        self.main_remote_control_event_process(("Calibration", "Tint Up"))


    def main_remote_event_button_calibration_tint_down(self):
        self.main_remote_control_event_process(("Calibration", "Tint Down"))


    def main_remote_event_button_calibration_sharpness(self):
        self.main_remote_control_event_process(("Calibration", "Sharpness"))


    def main_remote_event_button_calibration_sharpness_up(self):
        self.main_remote_control_event_process(("Calibration", "Sharpness Up"))


    def main_remote_event_button_calibration_sharpness_down(self):
        self.main_remote_control_event_process(("Calibration", "Sharpness Down"))


#####################################################
    # main remote control events
    # application
    def main_remote_event_button_commands_application_amazon(self):
        self.main_remote_control_event_process(("Commands", "Application", "Amazon Instant Video"))


    def main_remote_event_button_commands_application_emby(self):
        self.main_remote_control_event_process(("Commands", "Application", "Emby"))


    def main_remote_event_button_commands_application_hbogo(self):
        self.main_remote_control_event_process(("Commands", "Application", "HBO Go"))


    def main_remote_event_button_commands_application_hulu(self):
        self.main_remote_control_event_process(("Commands", "Application", "Hulu Plus"))


    def main_remote_event_button_commands_application_kodi(self):
        self.main_remote_control_event_process(("Commands", "Application", "Kodi"))


    def main_remote_event_button_commands_application_netflix(self):
        self.main_remote_control_event_process(("Commands", "Application", "Netflix"))


    def main_remote_event_button_commands_application_pandora(self):
        self.main_remote_control_event_process(("Commands", "Application", "Pandora"))


    def main_remote_event_button_commands_application_plex(self):
        self.main_remote_control_event_process(("Commands", "Application", "Plex"))


    def main_remote_event_button_commands_application_siriusxm(self):
        self.main_remote_control_event_process(("Commands", "Application", "SiriusXM"))


    def main_remote_event_button_commands_application_slingtv(self):
        self.main_remote_control_event_process(("Commands", "Application", "sling TV"))


    def main_remote_event_button_commands_application_vudu(self):
        self.main_remote_control_event_process(("Commands", "Application", "Vudu"))


    # aspect ratio
    def main_remote_event_button_commands_aspect_next(self):
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Next Ratio"))


    def main_remote_event_button_commands_aspect_auto(self):
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Auto"))


    def main_remote_event_button_commands_aspect_native(self):
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Native"))


    def main_remote_event_button_commands_aspect_letterbox(self):
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Letterbox"))


    def main_remote_event_button_commands_aspect_real(self):
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "Real"))


    def main_remote_event_button_commands_aspect_4x3(self):
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "4:3"))


    def main_remote_event_button_commands_aspect_1x2(self):
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "1:1"))


    def main_remote_event_button_commands_aspect_1x85(self):
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "1.85"))


    def main_remote_event_button_commands_aspect_2x35(self):
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "2.35"))


    def main_remote_event_button_commands_aspect_16x9(self):
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "16:9"))


    def main_remote_event_button_commands_aspect_16x10(self):
        self.main_remote_control_event_process(("Commands", "Aspect Ratio", "16:10"))


    # hardware
    def main_remote_event_button_commands_hardware_channel(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Channel"))


    def main_remote_event_button_commands_hardware_crt_b(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "CRT Blue"))


    def main_remote_event_button_commands_hardware_crt_g(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "CRT Green"))


    def main_remote_event_button_commands_hardware_crt_r(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "CRT Red"))


    def main_remote_event_button_commands_hardware_cut_off(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Cut-Off"))


    def main_remote_event_button_commands_hardware_lamp_hour_reset(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Lamp Hour Reset"))


    def main_remote_event_button_commands_hardware_luminance(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Luminance"))


    def main_remote_event_button_commands_hardware_optical_zoom_shift(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Optical Zoom Shift"))


    def main_remote_event_button_commands_hardware_optical_focus_shift(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Optical Focus Shift"))


    def main_remote_event_button_commands_hardware_projection_mode(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Projection Mode"))


    def main_remote_event_button_commands_hardware_reset(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Reset"))


    def main_remote_event_button_commands_hardware_shutter_on(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Shutter On"))


    def main_remote_event_button_commands_hardware_shutter_off(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Shutter Off"))


    def main_remote_event_button_commands_hardware_unit(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Unit"))


    def main_remote_event_button_commands_hardware_whisper_mode(self):
        self.main_remote_control_event_process(("Commands", "Hardware", "Whisper Mode"))


    # misc
    def main_remote_event_button_commands_misc_background(self):
        self.main_remote_control_event_process(("Commands", "Misc", "Background"))


    def main_remote_event_button_commands_misc_cc_display(self):
        self.main_remote_control_event_process(("Commands", "Misc", "Closed Caption Display"))


    def main_remote_event_button_commands_misc_film_mode(self):
        self.main_remote_control_event_process(("Commands", "Misc", "Film Mode"))


    def main_remote_event_button_commands_misc_freeze(self):
        self.main_remote_control_event_process(("Commands", "Misc", "Freeze"))


    def main_remote_event_button_commands_misc_freeze_on(self):
        self.main_remote_control_event_process(("Commands", "Misc", "Freeze On"))


    def main_remote_event_button_commands_misc_freeze_off(self):
        self.main_remote_control_event_process(("Commands", "Misc", "Freeze Off"))


    def main_remote_event_button_commands_misc_language(self):
        self.main_remote_control_event_process(("Commands", "Misc", "Language"))


    def main_remote_event_button_commands_misc_osd(self):
        self.main_remote_control_event_process(("Commands", "Misc", "OSD"))


    def main_remote_event_button_commands_misc_osd_on(self):
        self.main_remote_control_event_process(("Commands", "Misc", "OSD On"))


    def main_remote_event_button_commands_misc_osd_off(self):
        self.main_remote_control_event_process(("Commands", "Misc", "OSD Off"))


    def main_remote_event_button_commands_misc_startup_image_yes(self):
        self.main_remote_control_event_process(("Commands", "Misc", "Startup Image Yes"))


    def main_remote_event_button_commands_misc_startup_image_no(self):
        self.main_remote_control_event_process(("Commands", "Misc", "Startup Image No"))


    # navigation
    def main_remote_event_button_commands_left(self):
        self.main_remote_control_event_process(("Commands", "Direction", "Left"))


    def main_remote_event_button_commands_right(self):
        self.main_remote_control_event_process(("Commands", "Direction", "Right"))


    def main_remote_event_button_commands_up(self):
        self.main_remote_control_event_process(("Commands", "Direction", "Up"))


    def main_remote_event_button_commands_down(self):
        self.main_remote_control_event_process(("Commands", "Direction", "Down"))


    def main_remote_event_button_commands_one(self):
        self.main_remote_control_event_process(("Commands", "Numeric", "One"))


    def main_remote_event_button_commands_two(self):
        self.main_remote_control_event_process(("Commands", "Numeric", "Two"))


    def main_remote_event_button_commands_three(self):
        self.main_remote_control_event_process(("Commands", "Numeric", "Three"))


    def main_remote_event_button_commands_four(self):
        self.main_remote_control_event_process(("Commands", "Numeric", "Four"))


    def main_remote_event_button_commands_five(self):
        self.main_remote_control_event_process(("Commands", "Numeric", "Five"))


    def main_remote_event_button_commands_six(self):
        self.main_remote_control_event_process(("Commands", "Numeric", "Six"))


    def main_remote_event_button_commands_seven(self):
        self.main_remote_control_event_process(("Commands", "Numeric", "Seven"))


    def main_remote_event_button_commands_eight(self):
        self.main_remote_control_event_process(("Commands", "Numeric", "Eight"))


    def main_remote_event_button_commands_nine(self):
        self.main_remote_control_event_process(("Commands", "Numeric", "Nine"))


    def main_remote_event_button_commands_fast_rewind(self):
        self.main_remote_control_event_process(("Commands", "Navigation", "Fast Rewind"))


    def main_remote_event_button_commands_chapter_rewind(self):
        self.main_remote_control_event_process(("Commands", "Navigation", "Chapter Rewind"))


    def main_remote_event_button_commands_fast_forward(self):
        self.main_remote_control_event_process(("Commands", "Navigation", "Fast Forward"))


    def main_remote_event_button_commands_chapter_forward(self):
        self.main_remote_control_event_process(("Commands", "Navigation", "Chapter Forward"))


    def main_remote_event_button_commands_play(self):
        self.main_remote_control_event_process(("Commands", "Navigation", "Play"))


    def main_remote_event_button_commands_pause(self):
        self.main_remote_control_event_process(("Commands", "Navigation", "Pause"))


    def main_remote_event_button_commands_stop(self):
        self.main_remote_control_event_process(("Commands", "Navigation", "Stop"))


    def main_remote_event_button_commands_info(self):
        self.main_remote_control_event_process(("Commands", "Navigation", "Info"))


    def main_remote_event_button_commands_record(self):
        self.main_remote_control_event_process(("Commands", "Navigation", "Record"))


    # power
    def main_remote_event_button_commands_power_on(self):
        self.main_remote_control_event_process(("Commands", "Power", "On"))


    def main_remote_event_button_commands_power_off(self):
        self.main_remote_control_event_process(("Commands", "Power", "Off"))


    def main_remote_event_button_commands_power_standy(self):
        self.main_remote_control_event_process(("Commands", "Power", "Standby"))


    # sound
    def main_remote_event_button_commands_sound_mute(self):
        self.main_remote_control_event_process(("Commands", "Sound", "Mute"))


    def main_remote_event_button_commands_sound_unmute(self):
        self.main_remote_control_event_process(("Commands", "Sound", "UnMute"))


    def main_remote_event_button_commands_sound_volume_up(self):
        self.main_remote_control_event_process(("Commands", "Sound", "Volume Up"))


    def main_remote_event_button_commands_sound_volume_down(self):
        self.main_remote_control_event_process(("Commands", "Sound", "Volume Down"))


    # zoom
    def main_remote_event_button_commands_zoom_zoom(self):
        self.main_remote_control_event_process(("Commands", "Zoom", "Zoom"))


    def main_remote_event_button_commands_zoom_up(self):
        self.main_remote_control_event_process(("Commands", "Zoom", "Zoom Up"))


    def main_remote_event_button_commands_zoom_down(self):
        self.main_remote_control_event_process(("Commands", "Zoom", "Zoom Down"))


#####################################################
    # querys
    # library media
    def main_remote_event_button_query_library_media_albums(self):
        self.main_remote_control_event_process(("Query", "Library", "Media", "Albums"))


    def main_remote_event_button_query_library_media_artists(self):
        self.main_remote_control_event_process(("Query", "Library", "Media", "Artists"))


    def main_remote_event_button_query_library_media_movies(self):
        self.main_remote_control_event_process(("Query", "Library", "Media", "Movies"))


    def main_remote_event_button_query_library_media_music_videos(self):
        self.main_remote_control_event_process(("Query", "Library", "Media", "Music Videos"))


    def main_remote_event_button_query_library_media_songs(self):
        self.main_remote_control_event_process(("Query", "Library", "Media", "Songs"))


    def main_remote_event_button_query_library_media_tv_shows(self):
        self.main_remote_control_event_process(("Query", "Library", "Media", "TV Shows"))


    # librrary playlist
    def main_remote_event_button_query_library_playlist_audio(self):
        self.main_remote_control_event_process(("Query", "Library", "Playlist", "Audio"))


    def main_remote_event_button_query_library_playlist_video(self):
        self.main_remote_control_event_process(("Query", "Library", "Playlist", "Video"))


    # more queries
    def main_remote_event_button_query_api_commands(self):
        self.main_remote_control_event_process(("Query", "API Commands"))


    def main_remote_event_button_query_aspect_ratio(self):
        self.main_remote_control_event_process(("Query", "Aspect Ratio"))


    def main_remote_event_button_query_blank_status(self):
        self.main_remote_control_event_process(("Query", "Blank Status"))


    def main_remote_event_button_query_brightness(self):
        self.main_remote_control_event_process(("Query", "Brightness"))


    def main_remote_event_button_query_codec(self):
        self.main_remote_control_event_process(("Query", "Codec (Playing Media)"))


    def main_remote_event_button_query_color_video(self):
        self.main_remote_control_event_process(("Query", "Color (Video)"))


    def main_remote_event_button_query_color_mode(self):
        self.main_remote_control_event_process(("Query", "Color Mode"))


    def main_remote_event_button_query_color_temp(self):
        self.main_remote_control_event_process(("Query", "Color Temp"))


    def main_remote_event_button_query_company_name(self):
        self.main_remote_control_event_process(("Query", "Company Name"))


    def main_remote_event_button_query_contrast(self):
        self.main_remote_control_event_process(("Query", "Contrast"))


    def main_remote_event_button_query_density(self):
        self.main_remote_control_event_process(("Query", "Density"))


    def main_remote_event_button_query_error_status(self):
        self.main_remote_control_event_process(("Query", "Error Status"))


    def main_remote_event_button_query_filter_time(self):
        self.main_remote_control_event_process(("Query", "Filter Time"))


    def main_remote_event_button_query_gain_green(self):
        self.main_remote_control_event_process(("Query", "Gain Green"))


    def main_remote_event_button_query_gain_blue(self):
        self.main_remote_control_event_process(("Query", "Gain Blue"))


    def main_remote_event_button_query_gain_red(self):
        self.main_remote_control_event_process(("Query", "Gain Red"))


    def main_remote_event_button_query_input_selected(self):
        self.main_remote_control_event_process(("Query", "Input Selected"))


    def main_remote_event_button_query_lamp_hours(self):
        self.main_remote_control_event_process(("Query", "Lamp Hours"))


    def main_remote_event_button_query_lamp_off(self):
        self.main_remote_control_event_process(("Query", "Lamp Off"))


    def main_remote_event_button_query_lamp_on(self):
        self.main_remote_control_event_process(("Query", "Lamp On"))


    def main_remote_event_button_query_lamp_on_off(self):
        self.main_remote_control_event_process(("Query", "Lamp On/Off"))


    def main_remote_event_button_query_model_name(self):
        self.main_remote_control_event_process(("Query", "Model Name"))


    def main_remote_event_button_query_mute_status(self):
        self.main_remote_control_event_process(("Query", "Mute Status"))


    def main_remote_event_button_query_native_resolution(self):
        self.main_remote_control_event_process(("Query", "Native Resolution"))


    def main_remote_event_button_query_overscan_ratio(self):
        self.main_remote_control_event_process(("Query", "Overscan Ratio"))


    def main_remote_event_button_query_power_state(self):
        self.main_remote_control_event_process(("Query", "Power State"))


    def main_remote_event_button_query_projection_mode(self):
        self.main_remote_control_event_process(("Query", "Projection Mode"))


    def main_remote_event_button_query_serial_number(self):
        self.main_remote_control_event_process(("Query", "Serial Number"))


    def main_remote_event_button_query_sharpness(self):
        self.main_remote_control_event_process(("Query", "Sharpness"))


    def main_remote_event_button_query_status(self):
        self.main_remote_control_event_process(("Query", "Status"))


    def main_remote_event_button_query_tint_video(self):
        self.main_remote_control_event_process(("Query", "Tint (Video)"))


    def main_remote_event_button_query_volume(self):
        self.main_remote_control_event_process(("Query", "Volume"))


#####################################################
    # source
    def main_remote_event_button_source_aux1(self):
        self.main_remote_control_event_process(("Source", "AUX1"))


    def main_remote_event_button_source_aux2(self):
        self.main_remote_control_event_process(("Source", "AUX2"))


    def main_remote_event_button_source_bluray(self):
        self.main_remote_control_event_process(("Source", "BluRay"))


    def main_remote_event_button_source_cable_tv(self):
        self.main_remote_control_event_process(("Source", "Cable/TV"))


    def main_remote_event_button_source_composite(self):
        self.main_remote_control_event_process(("Source", "Composite"))


    def main_remote_event_button_source_component(self):
        self.main_remote_control_event_process(("Source", "Component"))


    def main_remote_event_button_source_dvd(self):
        self.main_remote_control_event_process(("Source", "DVD"))


    def main_remote_event_button_source_game(self):
        self.main_remote_control_event_process(("Source", "Game"))


    def main_remote_event_button_source_hdmi1(self):
        self.main_remote_control_event_process(("Source", "HDMI1"))


    def main_remote_event_button_source_hdmi2(self):
        self.main_remote_control_event_process(("Source", "HDMI2"))


    def main_remote_event_button_source_hdmi3(self):
        self.main_remote_control_event_process(("Source", "HDMI3"))


    def main_remote_event_button_source_hdmi4(self):
        self.main_remote_control_event_process(("Source", "HDMI4"))


    def main_remote_event_button_source_hdmi5(self):
        self.main_remote_control_event_process(("Source", "HDMI5"))


    def main_remote_event_button_source_hdmi6(self):
        self.main_remote_control_event_process(("Source", "HDMI6"))


    def main_remote_event_button_source_hdmi7(self):
        self.main_remote_control_event_process(("Source", "HDMI7"))


    def main_remote_event_button_source_hdmi8(self):
        self.main_remote_control_event_process(("Source", "HDMI8"))


    def main_remote_event_button_source_input(self):
        self.main_remote_control_event_process(("Source", "Input"))


    def main_remote_event_button_source_laserdisc(self):
        self.main_remote_control_event_process(("Source", "LaserDisc"))


    def main_remote_event_button_source_net_usb(self):
        self.main_remote_control_event_process(("Source", "Net/USB"))


    def main_remote_event_button_source_phono(self):
        self.main_remote_control_event_process(("Source", "Phono"))


    def main_remote_event_button_source_rgb1(self):
        self.main_remote_control_event_process(("Source", "RGB1"))


    def main_remote_event_button_source_rgb2(self):
        self.main_remote_control_event_process(("Source", "RGB2"))


    def main_remote_event_button_source_satellite(self):
        self.main_remote_control_event_process(("Source", "Satellite"))


    def main_remote_event_button_source_svideo(self):
        self.main_remote_control_event_process(("Source", "S-Video"))


    def main_remote_event_button_source_usb(self):
        self.main_remote_control_event_process(("Source", "USB"))


if __name__ == '__main__':
    # load the kivy's here so all the classes have been defined
    Builder.load_file('kivy_layouts/main.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Load_Dialog.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Login.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Notification.kv')
    Builder.load_file('kivy_layouts/OctMote_KV_Layout_Slider.kv')
    OctMoteApp().run()
