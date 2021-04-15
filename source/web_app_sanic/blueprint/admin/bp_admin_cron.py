import json

from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_network_pika
from common import common_pagination_bootstrap
from sanic import Blueprint
from sanic.response import redirect
from web_app_sanic.blueprint.admin.bss_form_cron import BSSCronEditForm

blueprint_admin_cron = Blueprint('name_blueprint_admin_cron', url_prefix='/admin')


@blueprint_admin_cron.route('/admin_cron')
@common_global.jinja_template.template('bss_admin/bss_admin_cron.html')
@common_global.auth.login_required
async def url_bp_admin_cron(request):
    """
    Display cron jobs
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    db_connection = await request.app.db_pool.acquire()
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page=page,
                                                                      url='/admin/admin_cron',
                                                                      item_count=await request.app.db_functions.db_cron_list_count(
                                                                          enabled_only=False,
                                                                          db_connection=db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    cron_data = await request.app.db_functions.db_cron_list(enabled_only=False,
                                                            offset=offset,
                                                            records=int(
                                                                request.ctx.session['per_page']),
                                                            db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return {
        'media_cron': cron_data,
        'pagination_links': pagination,
        'page': page,
        'per_page': int(request.ctx.session['per_page'])
    }


@blueprint_admin_cron.route('/admin_cron_delete', methods=["POST"])
@common_global.auth.login_required
async def url_bp_admin_cron_delete(request):
    """
    Delete action 'page'
    """
    db_connection = await request.app.db_pool.acquire()
    await request.app.db_functions.db_cron_delete(request.form['id'], db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return json.dumps({'status': 'OK'})


@blueprint_admin_cron.route('/admin_cron_edit/<guid>', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_admin/bss_admin_cron_edit.html')
@common_global.auth.login_required
async def url_bp_admin_cron_edit(request, guid):
    """
    Edit cron job page
    """
    form = BSSCronEditForm(request, csrf_enabled=False)
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
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'admin cron run': guid})
    db_connection = await request.app.db_pool.acquire()
    cron_job_data = await request.app.db_functions.db_cron_info(guid, db_connection)
    cron_json_data = cron_job_data['mm_cron_json']
    # submit the message
    common_network_pika.com_net_pika_send({'Type': cron_json_data['Type'],
                                           'User': user.id,
                                           'JSON': cron_json_data},
                                          exchange_name=cron_json_data[
                                              'exchange_key'],
                                          route_key=cron_json_data['route_key'])
    await request.app.db_functions.db_cron_time_update(cron_job_data['mm_cron_name'],
                                                       db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return redirect(request.app.url_for('name_blueprint_admin_cron.url_bp_admin_cron'))
