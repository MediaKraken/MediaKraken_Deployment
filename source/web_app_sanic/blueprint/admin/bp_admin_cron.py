import json

import database_async as database_base_async
from common import common_global
from common import common_network_pika
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint
from sanic.response import redirect
from web_app_sanic.blueprint.admin.forms import CronEditForm

blueprint_admin_cron = Blueprint('name_blueprint_admin_cron', url_prefix='/admin')


@blueprint_admin_cron.route('/cron')
@common_global.jinja_template.template('admin/admin_cron.html')
@common_global.auth.login_required
async def url_bp_admin_cron(request):
    """
    Display cron jobs
    """
    async with request.app.db_pool.acquire() as db_connection:
        cron_count = await database_base_async.db_cron_list_count(db_connection, False)
    page, per_page, offset = Pagination.get_page_args(request)
    pagination = Pagination(request,
                            total=cron_count,
                            record_name='Cron Jobs',
                            format_total=True,
                            format_number=True,
                            )
    async with request.app.db_pool.acquire() as db_connection:
        cron_data = await database_base_async.db_cron_list(db_connection, False, offset, per_page)
    return {
        'media_cron': cron_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_cron.route('/cron_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_cron_delete(request):
    """
    Delete action 'page'
    """
    async with request.app.db_pool.acquire() as db_connection:
        await database_base_async.db_cron_delete(db_connection, request.form['id'])
    return json.dumps({'status': 'OK'})


@blueprint_admin_cron.route('/cron_edit/<guid>', methods=['GET', 'POST'])
@common_global.jinja_template.template('admin/admin_cron_edit.html')
@common_global.auth.login_required
async def url_bp_admin_cron_edit(request, guid):
    """
    Edit cron job page
    """
    form = CronEditForm(request.form, csrf_enabled=False)
    if request.method == 'POST':
        if form.validate_on_submit():
            request.form['name']
            request.form['description']
            request.form['enabled']
            request.form['interval']
            request.form['time']
            request.form['json']
    return {
        'guid': guid, 'form': form
    }


@blueprint_admin_cron.route('/cron_run/<guid>', methods=['GET', 'POST'])
@common_global.auth.login_required(user_keyword='user')
async def url_bp_admin_cron_run(request, user, guid):
    """
    Run cron jobs
    """
    common_global.es_inst.com_elastic_index('info', {'admin cron run': guid})
    async with request.app.db_pool.acquire() as db_connection:
        cron_job_data = await database_base_async.db_cron_info(db_connection, guid)
    # submit the message
    common_network_pika.com_net_pika_send({'Type': cron_job_data['mm_cron_json']['type'],
                                           'User': user.id,
                                           'JSON': cron_job_data['mm_cron_json']},
                                          exchange_name=cron_job_data['mm_cron_json'][
                                              'exchange_key'],
                                          route_key=cron_job_data['mm_cron_json']['route_key'])

    async with request.app.db_pool.acquire() as db_connection:
        await database_base_async.db_cron_time_update(db_connection,
                                                      cron_job_data['mm_cron_name'])
    return redirect(request.app.url_for('admins_cron.admin_cron'))
