"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, g, session
from flask_login import login_required

blueprint = Blueprint("user_metadata_album", __name__, url_prefix='/users',
                      static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/meta_music_song_list', methods=['GET', 'POST'])
@login_required
def metadata_music_song_list():
    """
    Display metadata music song list
    """
    page, per_page, offset = common_pagination.get_page_items()
    session['search_page'] = 'meta_music_song'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_metadata_music'),
                                                  record_name='song(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/metadata/meta_music_list.html',
                           media=g.db_connection.db_meta_song_list(offset, per_page,
                                                                   session['search_text']),
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


@blueprint.route('/meta_music_album_list', methods=['GET', 'POST'])
@login_required
def metadata_music_album_list():
    """
    Display metadata of album list
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    for album_data in g.db_connection.db_meta_album_list(offset, per_page, session['search_text']):
        common_global.es_inst.com_elastic_index('info', {'album_data': album_data,
                                                         'id': album_data['mm_metadata_album_guid'],
                                                         'name': album_data[
                                                             'mm_metadata_album_name'],
                                                         'json': album_data[
                                                             'mm_metadata_album_json']})
        if album_data['mmp_person_image'] is not None:
            if 'musicbrainz' in album_data['mm_metadata_album_image']['Images']:
                try:
                    album_image = album_data['mm_metadata_album_image']['Images'][
                        'musicbrainz'].replace(
                        '/mediakraken/web_app/MediaKraken', '')
                except:
                    album_image = "/static/images/music_album_missing.png"
            else:
                album_image = "/static/images/music_album_missing.png"
        else:
            album_image = "/static/images/music_album_missing.png"
            media.append(
                (album_data['mm_metadata_album_guid'], album_data['mm_metadata_album_name'],
                 album_image))
    session['search_page'] = 'meta_album'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_metadata_album'),
                                                  record_name='album(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/metadata/meta_music_album_list.html',
                           media=media,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


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
