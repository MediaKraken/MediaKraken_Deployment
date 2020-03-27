from common import common_global
from common import common_network_pika
from sanic import Blueprint

blueprint_user_hardware_chromecast = Blueprint('name_blueprint_user_hardware_chromecast',
                                               url_prefix='/user')


@blueprint_user_hardware_chromecast.route('/user_chromecast/<action>/<guid>')
@common_global.jinja_template.template('bss_user/user_chromecast_playback.html')
@common_global.auth.login_required(user_keyword='user')
async def url_bp_user_chromecast(request, user, action, guid):
    """
    Display chromecast actions page
    """
    common_global.es_inst.com_elastic_index('info', {'cast action': action,
                                                     'case user': user.id})
    db_connection = await request.app.db_pool.acquire()
    if action == 'base':
        pass
    elif action == 'back':
        pass
    #    elif action == 'rewind':
    #        pass
    elif action == 'stop':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Stop', 'Device': 'Cast',
             'User': user.id},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'play':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Play', 'Device': 'Cast',
             'User': user.id,
             'Data': await request.app.db_functions.db_read_media(db_connection, guid)['mm_media_path'],
             'Target': '10.0.0.220'},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'pause':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Pause', 'Device': 'Cast',
             'User': user.id},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'forward':
        pass
    elif action == 'mute':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Mute', 'Device': 'Cast',
             'User': user.id},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'vol_up':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Volume Up', 'Device': 'Cast',
             'User': user.id},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'vol down':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Volume Down', 'Device': 'Cast',
             'User': user.id},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    chromecast_data = await request.app.db_functions.db_device_list(db_connection, 'cast')
    await request.app.db_pool.release(db_connection)
    return {
        'data_guid': guid,
        'data_chromecast': chromecast_data
    }
