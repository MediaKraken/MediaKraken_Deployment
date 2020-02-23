import hashlib

from sanic import Sanic
from sanic.response import text
from sanic_httpauth import HTTPBasicAuth
import asyncio
import asyncpg

app = Sanic(__name__)
auth = HTTPBasicAuth()


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


@app.route("/")
@auth.login_required
async def hello(request):
    # request.args is a dict where each value is an array.
    return text("Hello {}".format(request.args["name"][0]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
