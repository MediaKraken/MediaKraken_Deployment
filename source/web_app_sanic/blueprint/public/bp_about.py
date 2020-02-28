from sanic import Blueprint
from sanic import response

blueprint_public_about = Blueprint('name_blueprint_public_about', url_prefix='/public')


@blueprint_public_about.route('/about', methods=["GET"])
async def url_bp_public_about(request):
    return await response.file('./web_app_async/templates/public/about.html')
