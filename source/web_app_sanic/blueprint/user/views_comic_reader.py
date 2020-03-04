
@blueprint.route('/comic_view/<guid>')
@login_required
def user_comic_view(guid):
    """
    Display image comic view
    """
    return render_template("users/user_comic_view.html",
                           comic_data=g.db_connection.db_media_path_by_uuid(guid))

