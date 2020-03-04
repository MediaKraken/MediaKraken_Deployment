
@blueprint.route('/hardware')
@login_required
def user_hardware():
    """
    Display hardware page
    """
    return render_template("users/user_hardware.html",
                           phue=g.db_connection.db_device_count('Phue'))


