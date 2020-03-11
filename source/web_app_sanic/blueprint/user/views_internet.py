# iradio
@blueprint.route('/iradio', methods=['GET', 'POST'])
@login_required
async def url_bp_user_iradio_list(request):
    """
    Display main page for internet radio
    """
    page, per_page, offset = Pagination.get_page_args(request)
    media = []
    if request['session']['search_text'] is not None:
        mediadata = g.db_connection.db_iradio_list(db_connection, offset, per_page,
                                                   search_value=request['session']['search_text'])
    else:
        mediadata = g.db_connection.db_iradio_list(db_connection, offset, per_page)
    return render_template("users/user_iradio_list.html")


@blueprint.route('/iradio_detail/<guid>')
@login_required
async def url_bp_user_iradio_detail(request, guid):
    """
    Display main page for internet radio
    """
    pass


@blueprint.before_request
async def before_request():
    """
    Executes before each request
    """
    g.db_connection = database_base.MKServerDatabase()
    g.google_instance = common_google.CommonGoogle(g.db_connection.db_opt_status_read(db_connection)[0])
    g.twitch_api = common_network_twitchv5.CommonNetworkTwitchV5(
        g.db_connection.db_opt_status_read(db_connection)[0])
    g.db_connection.db_open()
