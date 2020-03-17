import os

import database_async as database_base_async
import pika
from asyncpg import create_pool
from common import common_file
from common import common_global
from common import common_network
from python_paginate.css.semantic import Semantic
from python_paginate.web.sanic_paginate import Pagination
from sanic import Sanic
from sanic import response
from sanic.exceptions import NotFound
from sanic.exceptions import SanicException
from sanic.exceptions import ServerError
from sanic.log import logger
from sanic.request import Request
from sanic.response import redirect, text
from sanic_auth import Auth, User
from sanic_jinja2 import SanicJinja2
from sanic_session import Session

# setup the Sanic app
app = Sanic(__name__)
# update pagination settings
settings = dict(PREV_LABEL='<i class="left chevron icon"></i>',
                NEXT_LABEL='<i class="right chevron icon"></i>',
                PER_PAGE=30,  # default is 10
                )
app.config.update(settings)
# customize default pagination
if 'PREV_LABEL' in app.config:
    Semantic._prev_label = app.config.PREV_LABEL
if 'NEXT_LABEL' in app.config:
    Semantic._next_label = app.config.NEXT_LABEL
Pagination._css = Semantic()  # for cache
# or
# Pagination._css_framework = 'semantic'
# like above line, but little different
# if you want to get same result, need do below:
# pass css_prev_label, css_next_label to Pagination for initialize
Pagination._per_page = app.config.PER_PAGE
# set login endpoint
app.config.AUTH_LOGIN_ENDPOINT = 'login'
app.config['WTF_CSRF_SECRET_KEY'] = 'top secret!'  # TODO!  load from secret I guess
common_global.auth = Auth(app)
session = Session(app)
# initialize jinja templating
common_global.jinja_template = SanicJinja2(app)
# since I use global jinja....these MUST be after the initialization otherwise template = NONE
from web_app_sanic.blueprint import blueprint_content_mediakraken
from web_app_sanic.blueprint.public.bss_form_login import BSSLoginForm
from web_app_sanic.blueprint.public.bss_form_register import BSSRegisterForm

app.static('/static', './web_app_async/static')
# app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))
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
    print('This route does not exist {}'.format(request.url))
    return {}


@app.exception(Exception)
async def no_details_to_user(request: Request, exception: Exception):
    if isinstance(exception, SanicException):
        str_code = str(exception.status_code)
        logger.info(f'[{str_code}]')
        return text(str_code, exception.status_code)
    logger.exception(exception)
    return text('Server error', 500)


@app.route("/login", methods=['GET', 'POST'])
@common_global.jinja_template.template('public/bss_login.html')
async def login(request):
    form = BSSLoginForm(request)
    errors = {}
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        db_connection = await request.app.db_pool.acquire()
        try:
            user_id, user_admin = await request.app.db_functions.db_user_login_validation(
                db_connection, username, password)
            if user_id.isnumeric():
                common_global.auth.login_user(request,
                                              User(id=user_id, name=username, admin=user_admin))
                await app.db_pool.release(db_connection)
                return response.redirect("/")
        except:
            errors['validate_errors'] = "Username or password invalid"
        await request.app.db_pool.release(db_connection)
    errors['token_errors'] = '<br>'.join(form.csrf_token.errors)
    errors['username_errors'] = '<br>'.join(form.username.errors)
    errors['password_errors'] = '<br>'.join(form.password.errors)
    return {'form': form,
            'errors': errors}


@app.route("/register", methods=['GET', 'POST'])
@common_global.jinja_template.template('public/bss_register.html')
async def register(request):
    errors = {}
    form = BSSRegisterForm(request)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # we need to create a new user
        db_connection = await request.app.db_pool.acquire()
        try:
            user_id, user_admin = await request.app.db_functions.db_user_insert(
                db_connection, user_name=username, user_email=email, user_password=password)
            common_global.auth.login_user(request,
                                          User(id=user_id, name=username, admin=user_admin))
            await request.app.db_pool.release(db_connection)
            return response.redirect("/")
        except:
            # failed to insert into database
            errors['validate_errors'] = "failed to create user"
        await request.app.db_pool.release(db_connection)
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


@app.listener('before_server_start')
async def register_db(app, loop):
    # need to leave this here so the "loop" is defined
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
                                    max_size=100)
    # TODO, test for trigam, etc
    # self.db_cursor.execute('SET TIMEZONE = \'America/Chicago\'')
    # self.db_cursor.execute('SET max_parallel_workers_per_gather TO %s;' %
    #                        multiprocessing.cpu_count())
    # # do here since the db cursor is created now
    # # verify the trigram extension is enabled for the database
    # self.db_cursor.execute("select count(*) from pg_extension where extname = 'pg_trgm'")
    # if self.db_cursor.fetchone()[0] == 0:
    #     common_global.es_inst.com_elastic_index('critical',
    #                                             {'stuff': 'pg_trgm extension needs to '
    #                                                       'be enabled for database!!!!'
    #                                                       '  Exiting!!!'})
    #     sys.exit(1)
    # await db_connection.close() - not needed in pool?


def handle_no_auth(request):
    return redirect('/login')
    # return response.json(dict(message='unauthorized'), status=401)


# route to the default homepage
@app.route("/")
@common_global.auth.login_required(user_keyword='user', handle_no_auth=handle_no_auth)
async def hello(request):
    return redirect(app.url_for('name_blueprint_public_homepage.url_bp_homepage'))


# print out all routes for debugging purposes
for handler, (rule, router) in app.router.routes_names.items():
    print(rule)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
