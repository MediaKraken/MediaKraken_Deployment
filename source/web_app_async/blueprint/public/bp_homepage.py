from sanic import Blueprint
from sanic import response

bp_homepage = Blueprint('content_homepage', url_prefix='/public')


@bp_homepage.route('/', methods=["GET"])
async def bp_url_homepage(request):
    return await response.file('./templates/public/home.html')
