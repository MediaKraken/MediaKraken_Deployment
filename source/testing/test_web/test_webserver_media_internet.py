'''
  Copyright (C) 2016 Quinn D Granfor <spootdev@gmail.com>

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

from .test_webserver_base import *


def test_main_menu(driver):
    """
    Click home page link
    """
    driver.get(TEST_TARGET)
    driver.find_element_by_id('menu_home').click()
    assert 'MediaKraken' in driver.title


def test_main_internet(driver):
    """
    Click internet
    """
    driver.get(TEST_TARGET)
    driver.find_element_by_id('user_internet_page').click()
    assert 'MediaKraken' in driver.title


def test_main_internet_youtube(driver):
    """
    Click youtube
    """
    driver.get(TEST_TARGET)
    driver.find_element_by_id('user_internet_youtube_page').click()
    assert 'MediaKraken' in driver.title


def test_main_internet_vimeo(driver):
    """
    Click vimeo
    """
    driver.get(TEST_TARGET)
    driver.back()  # go back to main internet page
    driver.find_element_by_id('user_internet_vimeo_page').click()
    assert 'MediaKraken' in driver.title


def test_main_internet_twitch(driver):
    """
    Click vimeo
    """
    driver.get(TEST_TARGET)
    driver.back()  # go back to main internet page
    driver.find_element_by_id('user_internet_twitch_page').click()
    assert 'MediaKraken' in driver.title


def test_main_internet_flickr(driver):
    """
    Click vimeo
    """
    driver.get(TEST_TARGET)
    driver.back()  # go back to main internet page
    driver.find_element_by_id('user_internet_flickr_page').click()
    assert 'MediaKraken' in driver.title
