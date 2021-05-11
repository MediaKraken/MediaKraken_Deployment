from common import common_global
from common import common_logging_elasticsearch_httpx
from sanic import Blueprint
from sanic import response
from sanic.response import redirect

blueprint_user_media_status = Blueprint('name_blueprint_user_media_status', url_prefix='/user')


@blueprint_user_media_status.route('/user_status_movie/<guid>/<event_type>',
                                   methods=['GET', 'POST'])
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_status_movie(request, user, guid, event_type):
    """
    Set media status for specified media, user
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'movie status': guid,
                                                                         'event': event_type})
    if event_type == "sync":
        return redirect(
            request.app.url_for('name_blueprint_user_sync.url_bp_user_sync_edit', guid=guid))
    else:
        db_connection = await request.app.db_pool.acquire()
        if event_type == "mismatch":
            # TODO ummmm, how do I know which specific media to update?
            # TODO as some might be right
            await request.app.db_functions.db_meta_movie_status_update(
                await request.app.db_functions.db_metadata_guid_from_media_guid(
                    guid, db_connection),
                user.id, event_type, db_connection=db_connection)
        else:
            await request.app.db_functions.db_meta_movie_status_update(
                await request.app.db_functions.db_metadata_guid_from_media_guid(
                    guid, db_connection),
                user.id, event_type, db_connection=db_connection)
        await request.app.db_pool.release(db_connection)
        return response.HTTPResponse('', status=200, headers={'Vary': 'Accept-Encoding'})


@blueprint_user_media_status.route('/user_status_movie_metadata/<guid>/<event_type>',
                                   methods=['GET', 'POST'])
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_status_movie_metadata(request, user, guid, event_type):
    """
    Set media status for specified media, user
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'movie metadata status': guid,
                                                                         'event': event_type})
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_meta_movie_status_update(guid, user.id, event_type,
                                                               db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return response.HTTPResponse('', status=200, headers={'Vary': 'Accept-Encoding'})


@blueprint_user_media_status.route('/user_status_tv/<guid>/<event_type>', methods=['GET', 'POST'])
@common_global.auth.login_required
async def url_bp_user_status_tv(request, guid, event_type):
    """
    Set media status for specified media, user
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'tv status': guid,
                                                                         'event': event_type})
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
    return redirect(request.app.url_for('name_blueprint_user_tv.url_bp_user_tv'))


@blueprint_user_media_status.route('/user_meta_tv_status/<guid>/<event_type>',
                                   methods=['GET', 'POST'])
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_status_tv_metadata(request, user, guid, event_type):
    """
    Set media status for specified media, user
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'tv metadata status': guid,
                                                                         'event': event_type})
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_meta_tv_status_update(guid, user.id, event_type,
                                                            db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return response.HTTPResponse('', status=200, headers={'Vary': 'Accept-Encoding'})
