

@blueprint.route('/hardware_hue')
@login_required
def user_hardware_hue():
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
    return render_template("users/user_hardware_hue.html",
                           data_hue_avail=data_hue_avail,
                           data_hue_list=g.db_connection.db_device_list('Phue'))


@blueprint.route('/hardware_hue_on')
@login_required
def user_hardware_hue_on():
    """
    Hue on
    """
    common_network_pika.com_net_pika_send({'Type': 'Hardware', 'Subtype': 'Lights',
                                           'Hardware': 'Hue', 'Action': 'OnOff',
                                           'Setting': True, 'Target': '10.0.0.225',
                                           'LightList': (1, 2, 3)},
                                          rabbit_host_name='mkstack_rabbitmq',
                                          exchange_name='mkque_hardware_ex',
                                          route_key='mkhardware')
    return render_template("users/user_hardware_hue.html")


@blueprint.route('/hardware_hue_off')
@login_required
def user_hardware_hue_off():
    """
    Hue off
    """
    common_network_pika.com_net_pika_send({'Type': 'Hardware', 'Subtype': 'Lights',
                                           'Hardware': 'Hue', 'Action': 'OnOff',
                                           'Setting': False, 'Target': '10.0.0.225',
                                           'LightList': (1, 2, 3)},
                                          rabbit_host_name='mkstack_rabbitmq',
                                          exchange_name='mkque_hardware_ex',
                                          route_key='mkhardware')
    return render_template("users/user_hardware_hue.html")
