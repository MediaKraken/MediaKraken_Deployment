import os

from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_pagination_bootstrap
from common import common_string
from sanic import Blueprint

blueprint_admin_report = Blueprint('name_blueprint_admin_report', url_prefix='/admin')


@blueprint_admin_report.route('/admin_report')
@common_global.jinja_template.template('bss_admin/bss_admin_report.html')
@common_global.auth.login_required
async def url_bp_admin_report(request):
    return {}


@blueprint_admin_report.route('/admin_report_all_media')
@common_global.jinja_template.template('bss_admin/bss_admin_report_all_media.html')
@common_global.auth.login_required
async def url_bp_admin_report_all_media(request):
    """
    Display all media list
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    media_data = []
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_media_known(db_connection, offset,
                                                                  int(request.ctx.session[
                                                                          'per_page'])):
        media_data.append((row_data['mm_media_path'],
                           common_string.com_string_bytes2human(
                               os.path.getsize(row_data['mm_media_path']))))
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/admin/admin_report_all_media',
                                                                      item_count=await request.app.db_functions.db_media_known_count(
                                                                          db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    await request.app.db_pool.release(db_connection)
    return {
        'media': media_data,
        'pagination_links': pagination,
    }


@blueprint_admin_report.route('/admin_report_duplicate')
@common_global.jinja_template.template('bss_admin/bss_admin_report_all_duplicate_media.html')
@common_global.auth.login_required
async def url_bp_admin_report_all_duplicate_media(request):
    """
    Display media duplication report page
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    db_connection = await request.app.db_pool.acquire()
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/admin/admin_report_duplicate',
                                                                      item_count=await request.app.db_functions.db_media_duplicate_count(
                                                                          db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    report_media = await request.app.db_functions.db_media_duplicate(db_connection,
                                                                     offset,
                                                                     int(request.ctx.session[
                                                                             'per_page']))
    await request.app.db_pool.release(db_connection)
    return {
        'media': report_media,
        'pagination_links': pagination,
    }


@blueprint_admin_report.route('/admin_report_duplicate_detail/<guid>')
@common_global.jinja_template.template('bss_admin/bss_admin_report_duplicate_media_detail.html')
@common_global.auth.login_required
async def url_bp_admin_report_duplicate_detail(request, guid):
    """
    Display detail of duplicate list
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    media = []
    db_connection = await request.app.db_pool.acquire()
    for media_data in await request.app.db_functions.db_media_duplicate_detail(db_connection, guid,
                                                                               offset, int(
                request.ctx.session[
                    'per_page'])):
        await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                             message_text={"media": media_data[
                                                                 'mm_media_ffprobe_json']})
        if media_data['mm_media_ffprobe_json'] is not None:
            for stream_data in media_data['mm_media_ffprobe_json']['streams']:
                if stream_data['codec_type'] == 'video':
                    media.append((media_data['mm_media_guid'], media_data['mm_media_path'],
                                  str(stream_data['width']) +
                                  'x' + str(stream_data['height']),
                                  media_data['mm_media_ffprobe_json']['format']['duration']))
                    break
        else:
            media.append((media_data['mm_media_guid'], media_data['mm_media_path'],
                          'NA', '999:99:99'))
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/admin/admin_report_duplicate_detail',
                                                                      item_count=await
                                                                      request.app.db_functions.db_media_duplicate_detail_count(
                                                                          db_connection,
                                                                          guid)[0],
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    await request.app.db_pool.release(db_connection)
    return {
        'media': media,
        'pagination_links': pagination,
    }


@blueprint_admin_report.route('/admin_report_top10/<mtype>')
@common_global.jinja_template.template('bss_admin/bss_admin_report_top10_base.html')
@common_global.auth.login_required
async def url_bp_admin_report_top10(request, mtype):
    """
    Display top10 pages
    """
    db_connection = await request.app.db_pool.acquire()
    top10_data = None
    if mtype == '1':  # all time
        top10_data = await request.app.db_functions.db_usage_top10_alltime(db_connection)
    elif mtype == '2':  # movie
        top10_data = await request.app.db_functions.db_usage_top10_movie(db_connection)
    elif mtype == '3':  # tv show
        top10_data = await request.app.db_functions.db_usage_top10_tv_show(db_connection)
    elif mtype == '4':  # tv episode
        top10_data = await request.app.db_functions.db_usage_top10_tv_episode(db_connection)
    await request.app.db_pool.release(db_connection)
    return {'media': top10_data}


@blueprint_admin_report.route('/admin_report_unmatched_media')
@common_global.jinja_template.template('bss_admin/bss_admin_report_unmatched_media.html')
@common_global.auth.login_required
async def url_bp_admin_report_display_all_unmatched_media(request):
    """
    Display list of all unmatched media
    """
    page, offset = common_pagination_bootstrap.com_pagination_page_calc(request)
    db_connection = await request.app.db_pool.acquire()
    pagination = common_pagination_bootstrap.com_pagination_boot_html(page,
                                                                      url='/admin/admin_report_unmatched_media',
                                                                      item_count=await request.app.db_functions.db_media_unmatched_list_count(
                                                                          db_connection),
                                                                      client_items_per_page=
                                                                      int(request.ctx.session[
                                                                              'per_page']),
                                                                      format_number=True)
    unmatched_media = await request.app.db_functions.db_media_unmatched_list(db_connection,
                                                                             offset=offset,
                                                                             list_limit=int(
                                                                                 request.ctx.session[
                                                                                     'per_page']))
    await request.app.db_pool.release(db_connection)
    return {
        'media': unmatched_media,
        'pagination_links': pagination,
    }
