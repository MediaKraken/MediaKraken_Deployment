import hashlib
import os

import asyncpg
from blueprint import bp_about
from blueprint import bp_homepage
from common import common_file
from sanic import Sanic
from sanic import response
from sanic_httpauth import HTTPBasicAuth

app = Sanic(__name__)
auth = HTTPBasicAuth()
# setup the blueprints
app.blueprint(bp_about)
app.blueprint(bp_homepage)

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


# @auth.login_required
@app.route("/")
async def hello(request):
    return response.html('<p>Hello world!</p>')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
