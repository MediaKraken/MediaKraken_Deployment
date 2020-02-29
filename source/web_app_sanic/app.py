import hashlib
import os

import asyncpg
from common import common_file
# from common import common_network_pika
from sanic import Sanic
from sanic.response import redirect, text
from sanic_httpauth import HTTPBasicAuth
from sanic_jinja2 import SanicJinja2
from sanic_session import Session
from web_app_async.blueprint import blueprint_content_mediakraken

# setup the Sanic app
app = Sanic(__name__)
Session(app)
auth = HTTPBasicAuth()
jinja_template = SanicJinja2(app)

app.static('/static', './web_app_async/static')

# setup the blueprints
app.blueprint(blueprint_content_mediakraken)

db_connection = None


def hash_password(salt, password):
    salted = password + salt
    return hashlib.sha512(salted.encode("utf8")).hexdigest()


app_salt = "APP_SECRET - don't do this in production"
users = {
    "john": hash_password(app_salt, "hello"),
    "susan": hash_password(app_salt, "bye"),
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return users.get(username) == hash_password(app_salt, password)
    return False


# jinja test route
@app.route("/jinja")
@jinja_template.template('public/about.html')
async def hello_jinja(request):
    request['flash']('error message', 'error')
    return {'greetings': 'Hello, sanic!'}


@app.listener('after_server_start')
async def setup_connection(*args, **kwargs):
    print('after server start, connect to db')
    global db_connection
    if 'POSTGRES_PASSWORD' in os.environ:
        database_password = os.environ['POSTGRES_PASSWORD']
    else:
        database_password = common_file.com_file_load_data('/run/secrets/db_password')
    db_connection = await asyncpg.connect(user='user',
                                          password='%s' % database_password,
                                          database='postgres',
                                          host='mkstack_pgbouncer')


@app.route("/auth")
@auth.login_required
def index(request):
    return text("Hello, %s!" % auth.username(request))


# route to the default homepage
@app.route("/")
async def hello(request):
    return redirect(app.url_for('name_blueprint_public_homepage.url_bp_homepage'))


# print out all routes for debugging purposes
for handler, (rule, router) in app.router.routes_names.items():
    print(rule)

# common_network_pika.com_net_pika_send({'Type': 'Library Scan'},
#                                       rabbit_host_name='mkstack_rabbitmq',
#                                       exchange_name='mkque_ex',
#                                       route_key='mkque')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
