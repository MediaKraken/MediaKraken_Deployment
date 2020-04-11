import json

from common import common_global
from common import common_network_pika
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint
from sanic.response import redirect
from web_app_sanic.blueprint.admin.forms import CronEditForm

blueprint_admin_cron = Blueprint('name_blueprint_admin_cron', url_prefix='/admin')


@blueprint_admin_cron.route('/admin_cron')
@common_global.jinja_template.template('bss_admin/bss_admin_cron.html')
@common_global.auth.login_required
async def url_bp_admin_cron(request):
    """
    Display cron jobs
    """
    db_connection = await request.app.db_pool.acquire()
    cron_count = await request.app.db_functions.db_cron_list_count(db_connection, False)
    page, per_page, offset = Pagination.get_page_args(request)
    pagination = Pagination(request,
                            total=cron_count,
                            record_name='Cron Jobs',
                            format_total=True,
                            format_number=True,
                            )
    cron_data = await request.app.db_functions.db_cron_list(db_connection, False, offset, per_page)
    await request.app.db_pool.release(db_connection)
    return {
        'media_cron': cron_data,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_cron.route('/admin_cron_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_cron_delete(request):
    """
    Delete action 'page'
    """
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_cron_delete(db_connection, request.form['id'])
    await request.app.db_pool.release(db_connection)
    return json.dumps({'status': 'OK'})


@blueprint_admin_cron.route('/admin_cron_edit/<guid>', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_admin/bss_admin_cron_edit.html')
@common_global.auth.login_required
async def url_bp_admin_cron_edit(request, guid):
    """
    Edit cron job page
    """
    form = CronEditForm(request, csrf_enabled=False)
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


@blueprint_admin_cron.route('/admin_cron_run/<guid>', methods=['GET', 'POST'])
@common_global.auth.login_required(user_keyword='user')
async def url_bp_admin_cron_run(request, user, guid):
    """
    Run cron jobs
    """
    common_global.es_inst.com_elastic_index('info', {'admin cron run': guid})
    db_connection = await request.app.db_pool.acquire()
    cron_job_data = await request.app.db_functions.db_cron_info(db_connection, guid)
    cron_json_data = json.loads(cron_job_data['mm_cron_json'])
    # submit the message
    common_network_pika.com_net_pika_send({'Type': cron_json_data['type'],
                                           'User': user.id,
                                           'JSON': cron_json_data},
                                          exchange_name=cron_json_data[
                                              'exchange_key'],
                                          route_key=cron_json_data['route_key'])
    await request.app.db_functions.db_cron_time_update(db_connection,
                                                       cron_job_data['mm_cron_name'])
    await request.app.db_pool.release(db_connection)
    return redirect(request.app.url_for('name_blueprint_admin_cron.url_bp_admin_cron'))
