import json
import os
import traceback

import database_async as database_base_async
import pika
from asyncpg import create_pool
from common import common_file
from common import common_global
from common import common_logging_elasticsearch_httpx
from common import common_network
from sanic import Sanic
from sanic import response
from sanic.exceptions import NotFound
from sanic.exceptions import ServerError
from sanic.response import redirect
from sanic_auth import Auth, User
from sanic_jinja2 import SanicJinja2
from sanic_session import Session

# setup the Sanic app
app = Sanic(__name__)

# setup the crypto
# app_crypto = common_hash.CommonHashCrypto()
# set login endpoint
app.config.AUTH_LOGIN_ENDPOINT = 'login'
if 'CSRF_SECRET_KEY' in os.environ:
    csrf_key = os.environ['CSRF_SECRET_KEY']
else:
    csrf_key = common_file.com_file_load_data('/run/secrets/csrf_key')
app.config['WTF_CSRF_SECRET_KEY'] = csrf_key
common_global.auth = Auth(app)
session = Session(app)
# initialize jinja templating
common_global.jinja_template = SanicJinja2(app)
# since I use global jinja....these MUST be after the initialization otherwise template = NONE
from web_app_sanic.blueprint import blueprint_content_mediakraken
from web_app_sanic.blueprint.public.bss_form_login import BSSLoginForm
from web_app_sanic.blueprint.public.bss_form_register import BSSRegisterForm

# keep in this order as sanic-jinja2 seems to grab the last one for it's url_for's
app.static('/favicon.ico', common_global.static_data_directory + '/img/favicon.ico')
app.static('/static', common_global.static_data_directory)
# app.static('/assets', '/mediakraken/web_app_sanic/assets', name='assets')

# copy over modified static files so volumes will pick them up
# as on FIRST run, it will create volume and copy files from container to HOST
# on more runs, will copy files from HOST to container
os.system("cp -rf /mediakraken/web_app_sanic/static_copy/* /mediakraken/web_app_sanic/static/.")

# setup the blueprints
app.blueprint(blueprint_content_mediakraken)

# setup all the db functions and attempt db connection
app.db_functions = database_base_async.MKServerDatabaseAsync()

# setup the pika connection
common_network.mk_network_service_available(host_dns='mkstack_rabbitmq', host_port='5672')
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('mkstack_rabbitmq', socket_timeout=30,
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
app.amqp_channel = connection.channel()


@app.exception(NotFound)
async def page_not_found(request, exception):
    print('This route does not exist {}'.format(request.url), flush=True)
    return redirect(app.url_for('name_blueprint_error.url_bp_public_error_404'))


@app.exception(Exception)
async def no_details_to_user(request, exception):
    print('This route goes BOOM {}'.format(request.url), flush=True)
    print(traceback.print_exc(), flush=True)
    return redirect(app.url_for('name_blueprint_error.url_bp_public_error_500'))


@app.route("/login", methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_public/bss_public_login.html')
async def login(request):
    form = BSSLoginForm(request)
    errors = {}
    print('b4', request.method, flush=True)
    if request.method == 'POST':  # and form.validate():
        print('here i am in post', flush=True)
        username = form.username.data
        db_connection = await request.app.db_pool.acquire()
        user_id, user_admin, user_per_page \
            = await request.app.db_functions.db_user_login(user_name=username,
                                                           user_password=form.password.data,
                                                           db_connection=db_connection)
        await app.db_pool.release(db_connection)
        print(user_id, user_admin, user_per_page, flush=True)
        if user_id is None:  # invalid user name
            errors['username_errors'] = "Username invalid"
        elif user_id == 'inactive_account':
            errors['username_errors'] = "Username inactive"
        elif user_id == 'invalid_password':  # invalid_password
            errors['password_errors'] = "Password invalid"
        else:  # should be valid
            request.ctx.session['search_text'] = None
            request.ctx.session['per_page'] = user_per_page
            common_global.auth.login_user(request,
                                          User(id=user_id,
                                               name=username,
                                               admin=user_admin))
            print('current user', common_global.auth.current_user(request), flush=True)
            return redirect(app.url_for('name_blueprint_user_homepage.url_bp_user_homepage'))
    errors['token_errors'] = '<br>'.join(form.csrf_token.errors)
    errors['username_errors'] = '<br>'.join(form.username.errors)
    errors['password_errors'] = '<br>'.join(form.password.errors)
    return {'form': form,
            'errors': errors}


@app.route("/register", methods=['GET', 'POST'])
@common_global.jinja_template.template('bss_public/bss_public_register.html')
async def register(request):
    errors = {}
    form = BSSRegisterForm(request)
    if request.method == 'POST':  # and form.validate():
        username = form.username.data
        # we need to create a new user
        db_connection = await request.app.db_pool.acquire()
        # verify user doesn't already exist on database
        if await request.app.db_functions.db_user_count(user_name=username,
                                                        db_connection=db_connection) == 0:
            user_id, user_admin, user_per_page = await request.app.db_functions.db_user_insert(
                user_name=username, user_email=form.email.data,
                user_password=form.password.data, db_connection=db_connection)
            await app.db_pool.release(db_connection)
            if user_id.isnumeric():  # valid user
                request.ctx.session['search_text'] = None
                common_global.auth.login_user(request,
                                              User(id=user_id,
                                                   name=username,
                                                   admin=user_admin,
                                                   per_page=user_per_page))
                return redirect(app.url_for('name_blueprint_user_homepage.url_bp_user_homepage'))
            # failed to insert into database
            errors['validate_errors'] = "Failed to create user"
        else:
            errors['validate_errors'] = "Username already exists"
    errors['token_errors'] = '<br>'.join(form.csrf_token.errors)
    errors['username_errors'] = '<br>'.join(form.username.errors)
    errors['password_errors'] = '<br>'.join(form.password.errors)
    return {'form': form,
            'errors': errors}


@app.route('/logout')
@common_global.auth.login_required
async def logout(request):
    common_global.auth.logout_user(request)
    return response.redirect('/login')


async def init_connection(conn):
    await conn.set_type_codec('jsonb',
                              encoder=json.dumps,
                              decoder=json.loads,
                              schema='pg_catalog')


@app.listener('before_server_start')
async def register_db(app, loop):
    # fire up ES logging
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text='START',
                                                                     index_name='webapp_app')
    # need to leave this here so the "loop" is defined
    print('DB connection start', flush=True)
    if 'POSTGRES_PASSWORD' in os.environ:
        database_password = os.environ['POSTGRES_PASSWORD']
    else:
        try:
            database_password = common_file.com_file_load_data('/run/secrets/db_password')
        except FileNotFoundError:
            raise ServerError("Something bad happened", status_code=500)
    app.db_pool = await create_pool(user='postgres',
                                    password='%s' % database_password,
                                    database='postgres',
                                    host='mkstack_database',
                                    loop=loop,
                                    max_size=100,
                                    init=init_connection)
    print('DB pool created', flush=True)


def handle_no_auth(request):
    return redirect('/login')
    # return response.json(dict(message='unauthorized'), status=401)


# route to the default homepage
@app.route("/")
@common_global.auth.login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def hello(request, user):
    return redirect(app.url_for('name_blueprint_user_homepage.url_bp_user_homepage'))


# print out all routes for debugging purposes
for handler, (rule, router) in app.router.routes_names.items():
    print(rule, flush=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
