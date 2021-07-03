from common import common_global
from common import common_network_cloud
from sanic import Blueprint

blueprint_admin_cloud = Blueprint('name_blueprint_admin_cloud', url_prefix='/admin')


@blueprint_admin_cloud.route("/admin_cloud", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_admin/bss_admin_cloud.html')
@common_global.auth.login_required
async def url_bp_admin_cloud(request):
    cloud_providers = []
    cloud_storage_providers = common_network_cloud.com_libcloud_storage_provider_list()
    '''
    Provider
    Active
    API Key
    Secret Key
    Bucket/Path
    '''
    for cloud_provider in sorted(cloud_storage_providers):
        cloud_providers.append((cloud_provider, None, None, None, None))
    return {
        'cloud_providers': cloud_providers
    }
