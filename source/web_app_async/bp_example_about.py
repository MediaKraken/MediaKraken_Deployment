# Yielding the following routes to the application:
#
# /my_blueprint/foo
# /my_blueprint2/foo

from sanic import Blueprint
from sanic import Sanic
from sanic.response import json
from web_app_async.blueprint.public.bp_about import blueprint_public_about

app = Sanic(__name__)
blueprint2 = Blueprint('name2', url_prefix='/my_blueprint2')


@blueprint2.route('/foo')
async def foo2(request):
    return json({'msg': 'hi from blueprint2'})


app.register_blueprint(blueprint2)
app.register_blueprint(blueprint_public_about)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
