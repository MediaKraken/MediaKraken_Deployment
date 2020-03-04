
# home media
@blueprint.route('/home_media', methods=['GET', 'POST'])
@login_required
def home_media_list():
    """
    Display mage page for home media
    """
    page, per_page, offset = common_pagination.get_page_items()
    media = []
    # TODO wrong movie query
    return render_template("users/user_home_media_list.html",
                           media=g.db_connection.db_meta_movie_list(offset, per_page,
                                                                    session['search_text']))


@blueprint.route('/home_media_detail/<guid>')
@login_required
def home_media_detail(guid):
    """
    Display mage page for home media
    """
    pass
