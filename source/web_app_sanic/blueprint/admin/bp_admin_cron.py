import json

from common import common_global
from common import common_network_pika
from python_paginate.web.sanic_paginate import Pagination
from sanic import Blueprint
from sanic.response import redirect

blueprint_admin_cron = Blueprint('name_blueprint_admin_cron', url_prefix='/admin')


@blueprint_admin_cron.route('/cron')
@common_global.jinja_template.template('admin/admin_cron.html')
@common_global.auth.login_required
async def url_bp_admin_cron(request):
    """
    Display cron jobs
    """
    page, per_page, offset = Pagination.get_page_args(request)
    pagination = Pagination(request,
                            total=g.db_connection.db_cron_list_count(False),
                            record_name='Cron Jobs',
                            format_total=True,
                            format_number=True,
                            )
    return {
        'media_cron': g.db_connection.db_cron_list(False, offset, per_page),
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
    g.db_connection.db_cron_delete(request.form['id'])
    g.db_connection.db_commit()
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
@common_global.auth.login_required
async def url_bp_admin_cron_run(request, guid):
    """
    Run cron jobs
    """
    common_global.es_inst.com_elastic_index('info', {'admin cron run': guid})
    cron_job_data = g.db_connection.db_cron_info(guid)
    # submit the message
    common_network_pika.com_net_pika_send({'Type': cron_job_data['mm_cron_json']['type'],
                                           'User': current_user.get_id(),
                                           'JSON': cron_job_data['mm_cron_json']},
                                          exchange_name=cron_job_data['mm_cron_json'][
                                              'exchange_key'],
                                          route_key=cron_job_data['mm_cron_json']['route_key'])
    g.db_connection.db_cron_time_update(cron_job_data['mm_cron_name'])
    return redirect(request.app.url_for('admins_cron.admin_cron'))
