import json
import os

from sanic import Blueprint

blueprint_admin_backup = Blueprint('name_blueprint_admin_backup', url_prefix='/admin')


@blueprint_admin_backup.route('/backup_delete', methods=["POST"])
@login_required
@admin_required
async def url_bp_admin_backup_delete(request):
    """
    Delete backup file action 'page'
    """
    file_path, file_type = request.form['id'].split('|')
    if file_type == "Local":
        os.remove(file_path)
    else:
        pass
        # TODO, do the actual delete
    return json.dumps({'status': 'OK'})
