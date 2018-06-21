"""
User view in webapp
"""
# -*- coding: utf-8 -*-

from quart import Blueprint, render_template, g
from flask_login import current_user
from flask_login import login_required

blueprint = Blueprint("user_playback", __name__,
                      url_prefix='/users', static_folder="../static")
import sys

sys.path.append('..')
sys.path.append('../..')
from common import common_config_ini
from common import common_global
import database as database_base

option_config_json, db_connection = common_config_ini.com_config_read()


@blueprint.route('/playback/<vid_type>/<guid>/')
@blueprint.route('/playback/<vid_type>/<guid>')
@login_required
async def user_playback(vid_type, guid):
    """
    Display playback actions page
    """
    common_global.es_inst.com_elastic_index('info', {'playback action': vid_type})
    common_global.es_inst.com_elastic_index('info', {'playback user': current_user.get_id()})
    return await render_template("users/user_playback_videojs.html",
                           data_mtype=vid_type,
                           data_uuid=guid)


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
