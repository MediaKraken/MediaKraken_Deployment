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


def test_main_index(driver):
    """
    Display main page
    """
    driver.get(TEST_TARGET)
    assert 'MediaKraken' in driver.title


def test_main_login(driver):
    """
    Login into main page
    """
    driver.get(TEST_TARGET)
    driver.find_element_by_id('main_username').send_keys('metaman')
    driver.find_element_by_id('main_password').send_keys('metaman')
    driver.find_element_by_id('main_button_login').click()


def test_main_menu(driver):
    """
    Click home page link
    """
    driver.get(TEST_TARGET)
    driver.find_element_by_id('menu_home').click()
    assert 'MediaKraken' in driver.title


def test_main_menu_media(driver):
    """
    Click media on nav menu
    """
    driver.get(TEST_TARGET)
    driver.find_element_by_id('menu_media').click()
    assert 'MediaKraken' in driver.title


def test_main_menu_sync(driver):
    """
    Click sync on nav menu
    """
    driver.get(TEST_TARGET)
    driver.find_element_by_id('menu_sync').click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_movies(driver):
    """
    Click metadata movies on nav menu
    """
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(
        driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,
                                                                          "menu_metadata_movies")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_movie_collection(driver):
    """
    Click metadata movies collection on nav menu
    """
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(
        driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,
                                                                          "menu_metadata_movie_collection")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_tv_shows(driver):
    """
    Click metadata tv shows on nav menu
    """
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(
        driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,
                                                                          "menu_metadata_tv_shows")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_music_albums(driver):
    """
    Click metadata music albums on nav menu
    """
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(
        driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,
                                                                          "menu_metadata_music_albums")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_music_videos(driver):
    """
    Click metadata music videos on nav menu
    """
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(
        driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,
                                                                          "menu_metadata_music_videos")))
    element.click()
    assert 'MediaKraken' in driver.title


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


def test_main_menu_metadata_games(driver):
    """
    Click metadata games on nav menu
    """
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(
        driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,
                                                                          "menu_metadata_games")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_game_systems(driver):
    """
    Click metadata game systems on nav menu
    """
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(
        driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,
                                                                          "menu_metadata_game_systems")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_people(driver):
    """
    Click metadata people on nav menu
    """
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(
        driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,
                                                                          "menu_metadata_people")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_periodical(driver):
    """
    Click metadata people on nav menu
    """
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(
        driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,
                                                                          "menu_metadata_periodical")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_metadata_metadata_class_list(driver):
    """
    Click metadata class list on nav menu
    """
    driver.get(TEST_TARGET)
    hov = ActionChains(driver).move_to_element(
        driver.find_element_by_id('menu_metadata'))
    hov.perform()
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,
                                                                          "menu_metadata_class_list")))
    element.click()
    assert 'MediaKraken' in driver.title


def test_main_menu_server(driver):
    """
    Click server on nav menu
    """
    driver.get(TEST_TARGET)
    driver.find_element_by_id('menu_server').click()
    assert 'MediaKraken' in driver.title


def test_main_menu_about(driver):
    """
    Click about on nav menu
    """
    driver.get(TEST_TARGET)
    driver.find_element_by_id('menu_about').click()
    assert 'MediaKraken' in driver.title


def test_main_menu_contact(driver):
    """
    Click contact on footer
    """
    driver.get(TEST_TARGET)
    driver.find_element_by_link_text('Contact').click()
