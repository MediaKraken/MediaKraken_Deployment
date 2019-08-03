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

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .test_webserver_base import *


def test_main_menu_metadata_sports(driver):
    """
    Click metadata sports on nav menu
    """
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(
        driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,
                                                                          "menu_metadata_sports")))
    element.click()
    assert 'MediaKraken' in driver.title
