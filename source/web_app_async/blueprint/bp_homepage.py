from sanic import Blueprint
from sanic import response

bp_homepage = Blueprint('bp_homepage', __name__)


@bp_homepage.route('/', methods=["GET"])
async def bp_url_homepage(request):
    return await response.file('./templates/public/home.html')
