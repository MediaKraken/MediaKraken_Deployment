from common import common_global
from common import common_internationalization
from common import common_string
from sanic import Blueprint

blueprint_admin_database = Blueprint('name_blueprint_admin_database', url_prefix='/admin')


@blueprint_admin_database.route("/admin_database")
@common_global.jinja_template.template('bss_admin/bss_admin_db_statistics.html')
@common_global.auth.login_required
async def url_bp_admin_database_statistics(request):
    """
    Display database statistics page
    """
    db_stats_count = []
    db_stats_total = 0
    db_connection = await request.app.db_pool.acquire()
    for row_data in await request.app.db_functions.db_pgsql_row_count(db_connection=db_connection):
        db_stats_total += row_data[2]
        db_stats_count.append((row_data[1],
                               common_internationalization.com_inter_number_format(row_data[2])))
    db_stats_count.append(
        ('Total records:', common_internationalization.com_inter_number_format(db_stats_total)))
    db_size_data = []
    db_size_total = 0
    for row_data in await request.app.db_functions.db_pgsql_table_sizes(
            db_connection=db_connection):
        db_size_total += row_data['total_size']
        db_size_data.append(
            (row_data['relation'], common_string.com_string_bytes2human(row_data['total_size'])))
    db_size_data.append(('Total Size:', common_string.com_string_bytes2human(db_size_total)))
    data_workers = await request.app.db_functions.db_pgsql_parallel_workers(
        db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return {
        'data_db_size': db_size_data,
        'data_db_count': db_stats_count,
        'data_workers': data_workers,
    }
