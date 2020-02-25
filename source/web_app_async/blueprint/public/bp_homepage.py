from sanic import Blueprint
from sanic import response

blueprint_public_homepage = Blueprint('name_blueprint_public_homepage', url_prefix='/public')


@blueprint_public_homepage.route('/home', methods=["GET"])
async def url_bp_homepage(request):
    return await response.file('./web_app_async/templates/public/home.html')
