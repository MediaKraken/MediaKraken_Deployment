"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from flask import Blueprint, render_template, g, request
from flask_login import login_required

blueprint = Blueprint("user_search", __name__,
                      url_prefix='/users', static_folder="../static")
import logging  # pylint: disable=W0611
import json
from MediaKraken.public.forms import SearchForm
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route("/search", methods=["GET", "POST"])
@blueprint.route("/search/", methods=["GET", "POST"])
@login_required
def search_media():
    """
    Display search page
    """
    form = SearchForm(request.form)
    movie = []
    tvshow = []
    album = []
    if request.method == 'POST':
        if request.form['action_type'] == 'Search Local':
            json_data = json.loads(
                db_connection.db_search(request.form['search_item']))
            for search_item in json_data['Movie']:
                movie.append(search_item)
            for search_item in json_data['TVShow']:
                tvshow.append(search_item)
            for search_item in json_data['Album']:
                album.append(search_item)
    return render_template('users/user_search.html', media=movie, media_tvshow=tvshow,
                           media_album=album, form=form)


@blueprint.before_request
def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.db_connection.db_open()


@blueprint.teardown_request
def teardown_request(exception):  # pylint: disable=W0613
    """
    Executes after each request
    """
    g.db_connection.db_close()
