import json

from common import common_global
from sanic import Blueprint
from sanic.response import redirect

blueprint_user_media_status = Blueprint('name_blueprint_user_media_status', url_prefix='/user')


@blueprint_user_media_status.route('/status_movie/<guid>/<event_type>', methods=['GET', 'POST'])
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_status_movie(request, user, guid, event_type):
    """
    Set media status for specified media, user
    """
    common_global.es_inst.com_elastic_index('info', {'movie status': guid, 'event': event_type})
    if event_type == "sync":
        return redirect(request.app.url_for('user.sync_edit', guid=guid))
    else:
        if event_type == "mismatch":
            # TODO ummmm, how do I know which specific media to update?
            # TODO as some might be right
            await request.app.db_functions.db_media_status_update(db_connection,
                await request.app.db_functions.db_metadata_from_media_guid(db_connection, guid),
                user.id, event_type)
            return json.dumps({'status': 'OK'})
        else:
            # await request.app.db_functions.db_media_rating_update(db_connection,
            #     guid, user.id, event_type)
            await request.app.db_functions.db_meta_movie_status_update(db_connection,
                await request.app.db_functions.db_metadata_from_media_guid(db_connection, guid),
                user.id, event_type)
            return json.dumps({'status': 'OK'})


@blueprint_user_media_status.route('/status_movie_metadata/<guid>/<event_type>',
                                   methods=['GET', 'POST'])
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_status_movie_metadata(request, user, guid, event_type):
    """
    Set media status for specified media, user
    """
    common_global.es_inst.com_elastic_index('info', {'movie metadata status': guid,
                                                     'event': event_type})
    await request.app.db_functions.db_meta_movie_status_update(db_connection,
        guid, user.id, event_type)
    return json.dumps({'status': 'OK'})


@blueprint_user_media_status.route('/status_tv/<guid>/<event_type>', methods=['GET', 'POST'])
@common_global.auth.login_required
async def url_bp_user_status_tv(request, guid, event_type):
    """
    Set media status for specified media, user
    """
    common_global.es_inst.com_elastic_index('info', {'tv status': guid, 'event': event_type})
    if event_type == "watched":
        pass
    elif event_type == "sync":
        pass
    elif event_type == "favorite":
        pass
    elif event_type == "poo":
        pass
    elif event_type == "mismatch":
        pass
    return redirect(request.app.url_for('user_tv.user_tv'))
