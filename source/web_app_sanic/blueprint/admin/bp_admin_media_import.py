from common import common_file
from common import common_global
from sanic import Blueprint

blueprint_admin_media_import = Blueprint('name_blueprint_admin_media_import', url_prefix='/admin')


@blueprint_admin_media_import.route("/admin_media_import", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_media_import.html')
@common_global.auth.login_required
async def url_bp_admin_media_import(request):
    """
    Import media
    """
    media_data = []
    media_file_list = common_file.com_file_dir_list('/mediakraken/mnt/incoming',
                                                    filter_text=None,
                                                    walk_dir=True,
                                                    skip_junk=True,
                                                    file_size=True,
                                                    directory_only=False)
    if media_file_list is not None:
        for media_file in media_file_list:
            media_data.append((media_file[0], media_file[1]))
    return {
        'media_dir': media_data,
    }
