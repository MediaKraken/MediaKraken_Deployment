from common import common_global
from sanic import Blueprint

blueprint_user_homepage = Blueprint('name_blueprint_user_homepage', url_prefix='/user')


@blueprint_user_homepage.route('/home', methods=['GET', 'POST'])
@common_global.jinja_template.template('user/user_home.html')
async def url_bp_user_homepage(request):
    """
    Display user home page
    """
    async with request.app.db_pool.acquire() as db_connection:
        return {'data_new_media':
                    await request.app.db_functions.db_media_new(db_connection, days_old=7)}
