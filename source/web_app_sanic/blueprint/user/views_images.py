

@blueprint.route('/imagegallery')
@login_required
def user_image_gallery():
    """
    Display image gallery page
    """
    return render_template("users/user_image_gallery_view.html",
                           image_data=g.db_connection.db_media_images_list(
                               common_global.DLMediaType.Picture))


