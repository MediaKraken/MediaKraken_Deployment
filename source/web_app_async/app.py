import os

import asyncpg
from common import common_file
from common import common_global
from sanic import Blueprint, Sanic
from sanic.response import file, redirect
from sanic_httpauth import HTTPBasicAuth
from sanic_jinja2 import SanicJinja2
from web_app_async.blueprint import content_mediakraken

# setup the Sanic app
app = Sanic(__name__)
auth = HTTPBasicAuth()

blueprint3 = Blueprint('name3', url_prefix='/my_blueprint3')

#common_global.jinja = SanicJinja2(app)
# setup the blueprints
app.blueprint(content_mediakraken)
app.blueprint(blueprint3)

db_connection = None

@blueprint3.route('/foo')
async def index(request):
    return await file('websocket.html')

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
