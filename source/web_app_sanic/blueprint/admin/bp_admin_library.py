import json

from common import common_global
from common import common_network_pika
from common import common_pagination
from sanic import Blueprint

blueprint_admin_library = Blueprint('name_blueprint_admin_library', url_prefix='/admin')


@blueprint.route("/library", methods=["GET", "POST"])
@common_global.jinja_template.template('admin/admin_library.html')
@admin_required
async def url_bp_admin_library(request):
    """
    List all media libraries
    """
    common_global.es_inst.com_elastic_index('info', {'lib': request.method})
    if request.method == 'POST':
        common_global.es_inst.com_elastic_index('info', {'lib': request.form})
        if "scan" in request.form:
            # submit the message
            common_network_pika.com_net_pika_send({'Type': 'Library Scan'},
                                                  rabbit_host_name='mkstack_rabbitmq',
                                                  exchange_name='mkque_ex',
                                                  route_key='mkque')
            flash("Scheduled media scan.")
            common_global.es_inst.com_elastic_index('info', {'stuff': 'scheduled media scan'})
    page, per_page, offset = common_pagination.get_page_items()
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_table_count(
                                                      'mm_media_dir'),
                                                  record_name='library dir(s)',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return_media = []
    for row_data in g.db_connection.db_audit_paths(offset, per_page):
        return_media.append((row_data['mm_media_dir_path'],
                             row_data['mm_media_class_type'],
                             row_data['mm_media_dir_last_scanned'],
                             common_global.DLMediaType.row_data['mm_media_class_guid'].name,
                             row_data['mm_media_dir_guid']))
    return {
        'media_dir': return_media,
        'page': page,
        'per_page': per_page,
        'pagination': pagination,
    }


@blueprint_admin_library.route('/library_delete', methods=["POST"])
@admin_required
async def url_bp_admin_library_delete(request):
    """
    Delete library action 'page'
    """
    g.db_connection.db_audit_path_delete(request.form['id'])
    g.db_connection.db_commit()
    return json.dumps({'status': 'OK'})
