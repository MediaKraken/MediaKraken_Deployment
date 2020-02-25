import os

import asyncpg
from common import common_file
# from common import common_network_pika
from sanic import Blueprint, Sanic, response
from sanic.response import redirect
from web_app_async.blueprint import blueprint_content_mediakraken

# setup the Sanic app
app = Sanic(__name__)
blueprint_public = Blueprint('name_blueprint_public', url_prefix='/public')


@blueprint_public.route('/aboutlocal', methods=["GET"])
async def bp_url_about(request):
    return await response.file('./web_app_async/templates/public/about.html')


# setup the blueprints
app.blueprint(blueprint_public)
# above working
app.blueprint(blueprint_content_mediakraken)
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
    return redirect(app.url_for('url_bp_public_about'))


# print out all routes for debugging purposes
for handler, (rule, router) in app.router.routes_names.items():
    print(rule)

# common_network_pika.com_net_pika_send({'Type': 'Library Scan'},
#                                       rabbit_host_name='mkstack_rabbitmq',
#                                       exchange_name='mkque_ex',
#                                       route_key='mkque')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
