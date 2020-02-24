from sanic import Blueprint
from sanic import response

bp_about = Blueprint('bp_about', __name__)


@bp_about.route('/about', methods=["GET"])
async def bp_url_about(request):
    return await response.file('./templates/public/about.html')
