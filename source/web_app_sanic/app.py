import os

import crypto
from asyncpg import create_pool
from common import common_file
from common import common_global
from sanic import Sanic
from sanic import response
from sanic.exceptions import SanicException
from sanic.exceptions import ServerError
from sanic.log import logger
from sanic.request import Request
from sanic.response import json
from sanic.response import redirect, text
from sanic_auth import Auth
from sanic_jinja2 import SanicJinja2
from sanic_session import Session

# setup the Sanic app
app = Sanic(__name__)
app.config.AUTH_LOGIN_ENDPOINT = 'login'
app.config['WTF_CSRF_SECRET_KEY'] = 'top secret!'  # TODO!  load from secret I guess
auth = Auth(app)
Session(app)
# initialize jinja templating
common_global.jinja_template = SanicJinja2(app)
# since I use global jinja....these MUST be after the initialization otherwise template = NONE
from web_app_async.blueprint import blueprint_content_mediakraken
from web_app_async.blueprint.public.loginform import LoginForm, RegistrationForm

app.static('/static', './web_app_async/static')
# app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))
# setup the blueprints
app.blueprint(blueprint_content_mediakraken)


@app.exception(Exception)
async def no_details_to_user(request: Request, exception: Exception):
    if isinstance(exception, SanicException):
        str_code = str(exception.status_code)
        logger.info(f'[{str_code}]')
        return text(str_code, exception.status_code)
    logger.exception(exception)
    return text('Server error', 500)


@app.route("/login", methods=['GET', 'POST'])
@common_global.jinja_template.template('public/login.html')
async def login(request):
    form = LoginForm(request)
    errors = {}
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        try:
            user = await db_objects.get(Operator, username=username)
            if await user.check_password(password):
                login_user = User(id=user.id, name=user.username)
                auth.login_user(request, login_user)
                return response.redirect("/")
        except:
            errors['validate_errors'] = "Username or password invalid"
    errors['token_errors'] = '<br>'.join(form.csrf_token.errors)
    errors['username_errors'] = '<br>'.join(form.username.errors)
    errors['password_errors'] = '<br>'.join(form.password.errors)
    return {'form': form,
            'errors': errors}


@app.route("/register", methods=['GET', 'POST'])
@common_global.jinja_template.template('public/register.html')
async def register(request):
    errors = {}
    form = RegistrationForm(request)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = await crypto.hash_SHA512(form.password.data)
        # we need to create a new user
        try:
            user = await db_objects.create(Operator, username=username, password=password)
            login_user = User(id=user.id, name=user.username)
            auth.login_user(request, login_user)
            return response.redirect("/")
        except:
            # failed to insert into database
            errors['validate_errors'] = "failed to create user"
    errors['token_errors'] = '<br>'.join(form.csrf_token.errors)
    errors['username_errors'] = '<br>'.join(form.username.errors)
    errors['password_errors'] = '<br>'.join(form.password.errors)
    return {'form': form,
            'errors': errors}


async def check_password(self, password):
    temp_pass = await crypto.hash_SHA512(password)
    return self.password == temp_pass.decode("utf-8")


@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')


@app.listener('before_server_start')
async def register_db(app, loop):
    if 'POSTGRES_PASSWORD' in os.environ:
        database_password = os.environ['POSTGRES_PASSWORD']
    else:
        try:
            database_password = common_file.com_file_load_data('/run/secrets/db_password')
        except FileNotFoundError:
            raise ServerError("Something bad happened", status_code=500)
    app.pool = await create_pool(user='postgres',
                                 password='%s' % database_password,
                                 database='postgres',
                                 host='mkstack_database',
                                 loop=loop,
                                 max_size=100)
    async with app.pool.acquire() as connection:
        # await connection.execute('select * from mm_user')
        values = await connection.fetch('select * from mm_user')
        print(values)


def jsonify(records):
    """
    Parse asyncpg record response into JSON format
    """
    return [dict(r.items()) for r in records]


@app.get('/db')
async def root_get(request):
    async with app.pool.acquire() as connection:
        results = await connection.fetch('SELECT * FROM sanic_post')
        return json({'posts': jsonify(results)})


@app.route("/auth")
@auth.login_required
async def index(request):
    request['flash']('error message', 'error')
    return text("Hello, %s!" % auth.username(request))


# route to the default homepage
@app.route("/")
async def hello(request):
    return redirect(app.url_for('name_blueprint_public_homepage.url_bp_homepage'))


# print out all routes for debugging purposes
for handler, (rule, router) in app.router.routes_names.items():
    print(rule)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
