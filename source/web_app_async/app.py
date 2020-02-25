import os

import asyncpg
from common import common_file
from sanic import Blueprint, Sanic, response
from sanic.response import json
from sanic.response import redirect
from web_app_async.blueprint import content_mediakraken

# setup the Sanic app
app = Sanic(__name__)
blueprint = Blueprint('name', url_prefix='/public')
blueprint_public = Blueprint('name2', url_prefix='/public')


@blueprint.route('/foo')
async def foo(request):
    return json({'msg': 'hi from blueprint'})


@blueprint_public.route('/about')
async def bp_url_about(request):
    return await response.file('./web_app_async/templates/public/about.html')


# setup the blueprints
app.register_blueprint(content_mediakraken)
app.register_blueprint(blueprint)
app.register_blueprint(blueprint_public)
db_connection = None


@app.listener('before_server_start')
async def setup_connection(*args, **kwargs):
    global db_connection
    if 'POSTGRES_PASSWORD' in os.environ:
        database_password = os.environ['POSTGRES_PASSWORD']
    else:
        database_password = common_file.com_file_load_data('/run/secrets/db_password')
    db_connection = await asyncpg.connect(user='user',
                                          password='%s' % database_password,
                                          database='postgres',
                                          host='mkstack_pgbouncer')


@app.route("/")
async def hello(request):
    return redirect(app.url_for('bp_url_homepage'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
