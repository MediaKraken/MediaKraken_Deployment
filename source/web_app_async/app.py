from sanic import Sanic
from sanic.response import text

app = Sanic()


@app.route("/")
async def hello(request):
    # request.args is a dict where each value is an array.
    return text("Hello {}".format(request.args["name"][0]))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8800)
