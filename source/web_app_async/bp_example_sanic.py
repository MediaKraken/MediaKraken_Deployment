# app.py
from sanic import Sanic
from sanic.response import json

from .api import api

app = Sanic(__name__)

app.blueprint(api)

@app.route('/hello/<name>')
async def hello(request, name):
    return json({'hello': name})

for handler, (rule, router) in app.router.routes_names.items():
    print(rule)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
