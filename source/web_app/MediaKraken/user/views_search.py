"""
User view in webapp
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from flask import Blueprint, render_template, g, request
from flask_login import login_required

blueprint = Blueprint("user_search", __name__,
                      url_prefix='/users', static_folder="../static")
import json
from MediaKraken.user.forms import SearchEditForm
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
    form = SearchEditForm(request.form)
    movie = []
    tvshow = []
    album = []
    image = []
    publication = []
    movie_search = False
    tvshow_search = False
    album_search = False
    image_search = False
    publication_search = False
    if request.method == 'POST':
        if request.form['action_type'] == 'Search Local':
            if request.form['search_media_type'] == 'any':
                movie_search = True
                tvshow_search = True
                album_search = True
                image_search = True
                publication_search = True
            elif request.form['search_media_type'] == 'video':
                movie_search = True
                tvshow_search = True
            elif request.form['search_media_type'] == 'audio':
                album_search = True
            elif request.form['search_media_type'] == 'image':
                image_search = True
            elif request.form['search_media_type'] == 'publication':
                publication_search = True
            json_data = json.loads(
                db_connection.db_search(request.form['search_string'], search_type='Local',
                                        search_movie=movie_search, search_tvshow=tvshow_search,
                                        search_album=album_search, search_image=image_search,
                                        search_publication=publication_search))
            if 'Movie' in json_data:
                for search_item in json_data['Movie']:
                    movie.append(search_item)
            if 'TVShow' in json_data:
                for search_item in json_data['TVShow']:
                    tvshow.append(search_item)
            if 'Album' in json_data:
                for search_item in json_data['Album']:
                    album.append(search_item)
            if 'Image' in json_data:
                for search_item in json_data['Image']:
                    image.append(search_item)
            if 'Publication' in json_data:
                for search_item in json_data['Publication']:
                    publication.append(search_item)
        elif request.form['action_type'] == 'Search Metadata Providers':
            pass
        # TODO
        #search_resolution
        #search_audio_channels
        #search_audio_codec
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
