from common import common_global
from sanic import Blueprint

blueprint_user_homepage = Blueprint('name_blueprint_user_homepage', url_prefix='/user')


@blueprint_user_homepage.route('/home', methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_user/bss_user_home.html')
@common_global.auth.login_required
async def url_bp_user_homepage(request):
    """
    Display user home page
    """
    db_connection = await request.app.db_pool.acquire()
    media_data = await request.app.db_functions.db_media_new(db_connection, days_old=7)
    await request.app.db_pool.release(db_connection)
    return {
        'data_new_media': media_data
    }
