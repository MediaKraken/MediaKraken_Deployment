
@blueprint.route('/cast/<action>/<guid>')
@login_required
def user_cast(action, guid):
    """
    Display chromecast actions page
    """
    common_global.es_inst.com_elastic_index('info', {'cast action': action,
                                                     'case user': current_user.get_id()})
    if action == 'base':
        pass
    elif action == 'back':
        pass
    #    elif action == 'rewind':
    #        pass
    elif action == 'stop':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Stop', 'Device': 'Cast',
             'User': current_user.get_id()},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'play':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Play', 'Device': 'Cast',
             'User': current_user.get_id(),
             'Data': g.db_connection.db_read_media(guid)['mm_media_path'],
             'Target': '10.0.0.220'},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'pause':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Pause', 'Device': 'Cast',
             'User': current_user.get_id()},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'forward':
        pass
    elif action == 'mute':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Mute', 'Device': 'Cast',
             'User': current_user.get_id()},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'vol_up':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Volume Up', 'Device': 'Cast',
             'User': current_user.get_id()},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    elif action == 'vol down':
        common_network_pika.com_net_pika_send(
            {'Type': 'Playback', 'Subtype': 'Volume Down', 'Device': 'Cast',
             'User': current_user.get_id()},
            rabbit_host_name='mkstack_rabbitmq',
            exchange_name='mkque_ex',
            route_key='mkque')
    return render_template("users/user_playback_cast.html", data_guid=guid,
                           data_chromecast=g.db_connection.db_device_list('cast'))
