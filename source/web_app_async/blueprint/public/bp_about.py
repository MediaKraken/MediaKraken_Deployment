from sanic import Blueprint
from sanic import response

bp_about = Blueprint('content_about', url_prefix='/public')


@bp_about.route('/about', methods=["GET"])
async def bp_url_about(request):
    return await response.file('./templates/public/about.html')
