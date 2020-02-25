# app.py
from sanic import Sanic

from .api import api

app = Sanic(__name__)

app.blueprint(api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
