import os

import asyncpg
from common import common_file
from jinja2 import Environment, FileSystemLoader, select_autoescape
# from common import common_network_pika
from sanic import Sanic
from sanic.response import redirect, html
from web_app_async.blueprint import blueprint_content_mediakraken
from webassets import Environment as AssetsEnvironment
from webassets.ext.jinja2 import AssetsExtension

# setup the Sanic app
app = Sanic(__name__)
# setup the blueprints
app.blueprint(blueprint_content_mediakraken)

db_connection = None

# setup the jinja2 environment
jinja_env = Environment(loader=FileSystemLoader('./web_app_async/templates'),
                        autoescape=select_autoescape(['html', 'xml', 'html_file_name']),
                        extensions=[AssetsExtension])
jinja_env.assets_environment = AssetsEnvironment('.', '.')
# OSError: '/home/spoot/MediaKraken_Deployment/source/static/media/css_all' does not exist

# public templates
jinja_template_url_public_about = jinja_env.get_template('public/about.html')
jinja_template_url_public_homepage = jinja_env.get_template('public/home.html')


# return jinja2_generic_template('index.html', title='Sanic', data='blob', test=test)
def jinja2_render_generic_template(html_file_name, **kwargs):
    template = jinja_env.get_template(html_file_name)
    return html(template.render(kwargs))


# jinja test route
@app.route("/jinja")
async def hello_jinja(request):
    return jinja2_render_generic_template('public/about.html')


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
