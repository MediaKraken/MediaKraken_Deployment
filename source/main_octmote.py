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
                            group='setup_base_device_button', )
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
                            group='setup_item_device_button', )
        btn1.bind(on_press=partial(
            self.main_setup_base_item_selected, item_device[0]))
        self.root.ids.setup_base_item_gridlayout.add_widget(btn1)
        self.base_item_guid_dict[item_device[0]] = item_device[1]
