from sanic import Blueprint
from sanic import response

blueprint_public_homepage = Blueprint('name_blueprint_public_homepage', url_prefix='/public')


@blueprint_public_homepage.route('/', methods=["GET"])
async def bp_url_homepage(request):
    return await response.file('./web_app_async/templates/public/home.html')
