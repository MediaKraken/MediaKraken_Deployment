import json

from common import common_global
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint
from sanic.response import redirect

blueprint_user_sync = Blueprint('name_blueprint_user_sync', url_prefix='/user')


@blueprint_user_sync.route('/sync')
@common_global.jinja_template.template('user/user_sync.html')
@common_global.auth.login_required
async def url_bp_user_sync_display_all(request):
    """
    Display sync page
    """
    page, per_page, offset = Pagination.get_page_args(request)
    db_connection = await request.app.db_pool.acquire()
    # 0 - mm_sync_guid uuid, 1 - mm_sync_path, 2 - mm_sync_path_to, 3 - mm_sync_options_json
    pagination = Pagination(request,
                            total=await request.app.db_functions.db_table_count(db_connection,
                                                                                'mm_sync'),
                            record_name='sync job(s)',
                            format_total=True,
                            format_number=True,
                            )
    media_data = await request.app.db_functions.db_sync_list(db_connection, offset, per_page)
    await request.app.db_pool.release(db_connection)
    return {
        'media_sync': media_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_user_sync.route('/sync_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_user_admin_sync_delete_page(request):
    """
    Display sync delete action 'page'
    """
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_sync_delete(db_connection, request.form['id'])
    await request.app.db_pool.release(db_connection)
    return json.dumps({'status': 'OK'})


@blueprint_user_sync.route('/sync_edit/<guid>', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_sync_edit.html')
@common_global.auth.login_required
async def url_bp_user_sync_edit(request, guid):
    """
    Allow user to edit sync page
    """
    if request.method == 'POST':
        db_connection = await request.app.db_pool.acquire()
        sync_json = {'Type': request.form['target_type'],
                     'Media GUID': guid,
                     'Options': {'VContainer': request.form['target_container'],
                                 'VCodec': request.form['target_codec'],
                                 'Size': request.form['target_file_size'],
                                 'AudioChannels': request.form['target_audio_channels'],
                                 'ACodec': request.form['target_audio_codec'],
                                 'ASRate': request.form['target_sample_rate']},
                     'Priority': request.form['target_priority'],
                     'Status': 'Scheduled',
                     'Progress': 0}
        await request.app.db_functions.db_sync_insert(db_connection, request.form['name'],
                                                      request.form['target_output_path'],
                                                      json.dumps(sync_json))
        await request.app.db_pool.release(db_connection)
        return redirect(request.app.url_for('user.movie_detail', guid=guid))
    form = SyncEditForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        pass
    else:
        flash_errors(form)
    return {
        'guid': guid,
        'form': form
    }
