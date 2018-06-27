"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, request, redirect, url_for, session
from flask_login import login_required

blueprint = Blueprint("user_search", __name__,
                      url_prefix='/users', static_folder="../static")
import json
from MediaKraken.user.forms import SearchEditForm
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route("/search", methods=["GET", "POST"])
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
    game = []
    movie_search = False
    tvshow_search = False
    album_search = False
    image_search = False
    publication_search = False
    game_search = False
    if request.method == 'POST':
        if request.form['action_type'] == 'Search Local':
            if request.form['search_media_type'] == 'any':
                movie_search = True
                tvshow_search = True
                album_search = True
                image_search = True
                publication_search = True
                game_search = True
            elif request.form['search_media_type'] == 'video':
                movie_search = True
                tvshow_search = True
            elif request.form['search_media_type'] == 'audio':
                album_search = True
            elif request.form['search_media_type'] == 'image':
                image_search = True
            elif request.form['search_media_type'] == 'publication':
                publication_search = True
            elif request.form['search_media_type'] == 'game':
                game_search = True
            json_data = json.loads(
                db_connection.db_search(request.form['search_string'], search_type='Local',
                                        search_movie=movie_search, search_tvshow=tvshow_search,
                                        search_album=album_search, search_image=image_search,
                                        search_publication=publication_search,
                                        search_game=game_search))
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
            if 'Game' in json_data:
                for search_item in json_data['Game']:
                    game.append(search_item)
        elif request.form['action_type'] == 'Search Metadata Providers':
            pass
        # TODO
        # search_primary_language
        # search_secondary_language
        # search_resolution
        # search_audio_channels
        # search_audio_codec
    return render_template('users/user_search.html', media=movie, media_tvshow=tvshow,
                           media_album=album, media_image=image, media_book=publication,
                           media_game=game, form=form)


@blueprint.route("/search_nav", methods=["GET", "POST"])
@login_required
def search_nav_media():
    """
    determine what search results screen to show
    """
    common_global.es_inst.com_elastic_index('info', {"search session": session['search_page']})
    session['search_text'] = request.form.get('nav_search')
    if session['search_page'] == 'media_3d':
        return redirect(url_for('user_3d.user_3d_list'))
    elif session['search_page'] == 'media_album':
        return redirect(url_for('user_music.user_album_list_page'))
    elif session['search_page'] == 'media_games':
        return redirect(url_for('user_games.user_games_list'))
    elif session['search_page'] == 'media_movie':
        return redirect(url_for('user_movie_genre.user_movie_page', genre='All'))
    elif session['search_page'] == 'media_music_video':
        return redirect(url_for('user_music_video.user_music_video_list'))
    elif session['search_page'] == 'media_periodicals':
        return redirect(url_for('user_periodicals.user_books_list'))
    elif session['search_page'] == 'media_sports':
        return redirect(url_for('user_sports.user_sports_page'))
    elif session['search_page'] == 'media_tv':
        return redirect(url_for('user_tv.user_tv_page'))
    # begin metadata section
    elif session['search_page'] == 'meta_album':
        return redirect(url_for('user_metadata_album.metadata_music_album_list'))
    elif session['search_page'] == 'meta_game':
        return redirect(url_for('user_metadata_game.metadata_game_list'))
    elif session['search_page'] == 'meta_game_system':
        return redirect(url_for('user_metadata_game_system.metadata_game_system_list'))
    elif session['search_page'] == 'meta_movie':
        return redirect(url_for('user_metadata_movie.metadata_movie_list'))
    elif session['search_page'] == 'meta_movie_collection':
        return redirect(url_for('user_movie_collection.metadata_movie_collection_list'))
    elif session['search_page'] == 'meta_music_video':
        return redirect(url_for('user_metadata_music_video.metadata_music_video_list'))
    elif session['search_page'] == 'meta_people':
        return redirect(url_for('user_metadata_people.metadata_person_list'))
    elif session['search_page'] == 'meta_periodical':
        return redirect(url_for('user_metadata_periodical.metadata_periodical_list'))
    elif session['search_page'] == 'meta_sports':
        return redirect(url_for('user_metadata_sports.metadata_sports_list'))
    elif session['search_page'] == 'meta_tv':
        return redirect(url_for('user_metadata_tv.metadata_tvshow_list'))


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
