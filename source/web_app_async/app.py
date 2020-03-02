import os
import crypto
from asyncpg import create_pool
from common import common_file
from sanic import Sanic
from sanic import response
from sanic.exceptions import SanicException
from sanic.handlers import ErrorHandler
from sanic.response import json
from sanic.response import redirect, text
from sanic_auth import Auth
from sanic_jinja2 import SanicJinja2
from sanic_session import Session
from web_app_async.blueprint import blueprint_content_mediakraken
from web_app_async.blueprint.public.loginform import LoginForm, RegistrationForm


class CustomHandler(ErrorHandler):

    def default(self, request, exception):
        # Here, we have access to the exception object
        # and can do anything with it (log, send to external service, etc)

        # Some exceptions are trivial and built into Sanic (404s, etc)
        if not isinstance(exception, SanicException):
            print(exception)

        # Then, we must finish handling the exception by returning
        # our response to the client
        # For this we can just call the super class' default handler
        return super().default(request, exception)


# setup the Sanic app
app = Sanic(__name__)
app.config.AUTH_LOGIN_ENDPOINT = 'login'
auth = Auth(app)
Session(app)
jinja_template = SanicJinja2(app)
handler = CustomHandler()
app.error_handler = handler
app.static('/static', './web_app_async/static')

# setup the blueprints
app.blueprint(blueprint_content_mediakraken)

db_connection = None


@app.route("/login", methods=['GET', 'POST'])
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
    template = env.get_template('login.html')
    content = template.render(links=links, form=form, errors=errors)
    return response.html(content)

@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # fetch user from database
        user = some_datastore.get(name=username)
        if user and user.check_password(password):
            auth.login_user(request, user)
            return response.redirect('/profile')
    return response.html(HTML_LOGIN_FORM)

@app.route("/register", methods=['GET', 'POST'])
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
    template = env.get_template('register.html')
    content = template.render(links=links, form=form, errors=errors)
    return response.html(content)


async def check_password(self, password):
    temp_pass = await crypto.hash_SHA512(password)
    return self.password == temp_pass.decode("utf-8")





@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')


# jinja test route
@app.route("/jinja")
@jinja_template.template('public/about.html')
async def hello_jinja(request):
    return {'greetings': 'Hello, sanic!'}


# @app.listener('after_server_start')
# async def setup_connection(app, loop):
#     print('after server start, connect to db')
#     global db_connection
#     if 'POSTGRES_PASSWORD' in os.environ:
#         database_password = os.environ['POSTGRES_PASSWORD']
#     else:
#         database_password = common_file.com_file_load_data('/run/secrets/db_password')
#     app.db_connection = await asyncpg.connect(user='user',
#                                               password='%s' % database_password,
#                                               database='postgres',
#                                               host='mkstack_pgbouncer')

@app.listener('before_server_start')
async def register_db(app, loop):
    if 'POSTGRES_PASSWORD' in os.environ:
        database_password = os.environ['POSTGRES_PASSWORD']
    else:
        database_password = common_file.com_file_load_data('/run/secrets/db_password')
    app.pool = await create_pool(user='user',
                                 password='%s' % database_password,
                                 database='postgres',
                                 host='mkstack_pgbouncer',
                                 loop=loop, max_size=100)
    async with app.pool.acquire() as connection:
        await connection.execute('DROP TABLE IF EXISTS sanic_post')


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
def index(request):
    request['flash']('error message', 'error')
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
