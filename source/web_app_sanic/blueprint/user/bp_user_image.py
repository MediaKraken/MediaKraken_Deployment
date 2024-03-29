from common import common_global
from sanic import Blueprint

blueprint_user_image = Blueprint('name_blueprint_user_image', url_prefix='/user')


@blueprint_user_image.route('/user_imagegallery')
@common_global.jinja_template.template('bss_user/media/bss_user_media_image_gallery.html')
@common_global.auth.login_required
async def url_bp_user_image_gallery(request):
    """
    Display image gallery page
    """
    db_connection = await request.app.db_pool.acquire()
    image_data = await request.app.db_functions.db_image_list(common_global.DLMediaType.Picture,
                                                              db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return {'image_data': image_data
            }
