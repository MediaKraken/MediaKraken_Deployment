"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from quart import Blueprint, render_template, g, session
from flask_login import login_required

blueprint = Blueprint("user_metadata_people", __name__, url_prefix='/users',
                      static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
from common import common_pagination
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/meta_person_detail/<guid>/')
@blueprint.route('/meta_person_detail/<guid>')
@login_required
async def metadata_person_detail(guid):
    """
    Display person detail page
    """
    meta_data = g.db_connection.db_meta_person_by_guid(guid)
    json_metadata = meta_data['mmp_person_meta_json']
    if meta_data['mmp_person_image'] is not None:
        if 'themoviedb' in meta_data['mmp_person_image']['Images']:
            try:
                person_image = meta_data['mmp_person_image']['Images']['themoviedb'].replace(
                    '/mediakraken/web_app/MediaKraken', '') + meta_data['mmp_meta']
            except:
                person_image = "/static/images/person_missing.png"
        else:
            person_image = "/static/images/person_missing.png"
    else:
        person_image = "/static/images/person_missing.png"
    # also appears in
    meta_also_media = g.db_connection.db_meta_person_as_seen_in(meta_data[0])
    return await render_template('users/metadata/meta_people_detail.html',
                           json_metadata=json_metadata,
                           data_person_image=person_image,
                           data_also_media=meta_also_media,
                           )


@blueprint.route('/meta_person_list', methods=['GET', 'POST'])
@blueprint.route('/meta_person_list/', methods=['GET', 'POST'])
@login_required
async def metadata_person_list():
    """
    Display person list page
    """
    page, per_page, offset = common_pagination.get_page_items()
    person_list = []
    if session['search_text'] is not None:
        mediadata = g.db_connection.db_meta_person_list(offset, per_page, session['search_text'])
    else:
        mediadata = g.db_connection.db_meta_person_list(offset, per_page)
    for person_data in mediadata:
        common_global.es_inst.com_elastic_index('info', {'person data': person_data, 'im':
            person_data['mmp_person_image'], 'meta': person_data['mmp_meta']})
        if person_data['mmp_person_image'] is not None:
            if 'themoviedb' in person_data['mmp_person_image']['Images']:
                try:
                    person_image = person_data['mmp_person_image']['Images']['themoviedb'].replace(
                        '/mediakraken/web_app/MediaKraken', '') + person_data['mmp_meta']
                except:
                    person_image = "/static/images/person_missing.png"
            else:
                person_image = "/static/images/person_missing.png"
        else:
            person_image = "/static/images/person_missing.png"
        person_list.append(
            (person_data['mmp_id'], person_data['mmp_person_name'], person_image))
    session['search_page'] = 'meta_people'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_metadata_person'),
                                                  record_name='People',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return await render_template('users/metadata/meta_people_list.html',
                           media_person=person_list,
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
