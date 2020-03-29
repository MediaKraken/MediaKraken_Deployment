from common import common_global
from sanic import Blueprint

blueprint_user_hardware = Blueprint('name_blueprint_user_hardware', url_prefix='/user')


@blueprint_user_hardware.route('/user_hardware', methods=['GET'])
@common_global.jinja_template.template('bss_user/hardware/bss_user_hardware.html')
@common_global.auth.login_required
async def url_bp_user_hardware(request):
    """
    Display hardware page
    """
    db_connection = await request.app.db_pool.acquire()
    phue_hardware = await request.app.db_functions.db_hardware_device_count(db_connection,
                                                                            hardware_manufacturer='Phue')
    await request.app.db_pool.release(db_connection)
    return {
        'phue': phue_hardware
    }
