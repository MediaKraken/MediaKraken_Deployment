from sanic import Blueprint
from sanic.response import json

bp_about = Blueprint('bp_about')


@bp_about.route('/about')
async def bp_url_about(request):
    return json({'my': 'blueprint'})
