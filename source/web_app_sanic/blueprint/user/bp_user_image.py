from common import common_global
from sanic import Blueprint

blueprint_user_image = Blueprint('name_blueprint_user_image', url_prefix='/user')


@blueprint_user_image.route('/imagegallery')
@common_global.jinja_template.template('user/user_image_gallery_view.html')
@common_global.auth.login_required
async def url_bp_user_image_gallery(request):
    """
    Display image gallery page
    """
    async with request.app.db_pool.acquire() as db_connection:
        return {'image_data':
                    await request.app.db_functions..db_image_list(db_connection,
                                                                 common_global.DLMediaType.Picture)}
