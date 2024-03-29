from common import common_file
from common import common_global
from common import common_network_pika
from sanic import Blueprint
from sanic.response import redirect

blueprint_user_hardware_hue = Blueprint('name_blueprint_user_hardware_hue', url_prefix='/user')


@blueprint_user_hardware_hue.route('/user_hardware_hue')
@common_global.jinja_template.template('bss_user/hardware/bss_user_hardware_hue.html')
@common_global.auth.login_required
async def url_bp_user_hardware_hue(request):
    """
    Display hardware page for hue
    """
    # this is checking to see if the hue key exists
    # keep doing this even with not displaying in hardware page
    # as hue might be in the database without the key file
    key_list = common_file.com_file_dir_list('/mediakraken/phue',
                                             filter_text=None,
                                             walk_dir=False,
                                             skip_junk=False,
                                             file_size=False,
                                             directory_only=False)
    if key_list is None:
        data_hue_avail = None
    elif len(key_list) > 0:
        data_hue_avail = True
    else:
        # need to do as could provide an empty list and not None
        data_hue_avail = None
    db_connection = await request.app.db_pool.acquire()
    hue_data = await request.app.db_functions.db_device_list('Phue', db_connection=db_connection)
    await request.app.db_pool.release(db_connection)
    return {
        'data_hue_avail': data_hue_avail,
        'data_hue_list': hue_data
    }


@blueprint_user_hardware_hue.route('/user_hardware_hue_off')
@common_global.auth.login_required
async def url_bp_user_hardware_hue_off(request, target_ip):
    """
    Hue off
    """
    common_network_pika.com_net_pika_send({'Type': 'Hardware', 'Subtype': 'Lights',
                                           'Hardware': 'Hue', 'Action': 'OnOff',
                                           'Setting': False, 'Target': target_ip,
                                           'LightList': (1, 2, 3)},
                                          rabbit_host_name='mkstack_rabbitmq',
                                          exchange_name='mkque_hardware_ex',
                                          route_key='mkhardware')
    return redirect(request.app.url_for('blueprint_user_hardware_hue.url_bp_user_hardware_hue'))


@blueprint_user_hardware_hue.route('/user_hardware_hue_on')
@common_global.auth.login_required
async def url_bp_user_hardware_hue_on(request, target_ip):
    """
    Hue on
    """
    common_network_pika.com_net_pika_send({'Type': 'Hardware', 'Subtype': 'Lights',
                                           'Hardware': 'Hue', 'Action': 'OnOff',
                                           'Setting': True, 'Target': target_ip,
                                           'LightList': (1, 2, 3)},
                                          rabbit_host_name='mkstack_rabbitmq',
                                          exchange_name='mkque_hardware_ex',
                                          route_key='mkhardware')
    return redirect(request.app.url_for('blueprint_user_hardware_hue.url_bp_user_hardware_hue'))
