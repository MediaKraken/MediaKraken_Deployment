import traceback

from sanic import Sanic
from sanic.response import json

app = Sanic("My Hello, world app")


@app.route('/')
async def test(request):
    fake = 0 / 500
    return json({'hello': fake})


@app.exception(Exception)
async def no_details_to_user(request, exception):
    print('This route goes BOOM {}'.format(request.url), flush=True)
    print(traceback.print_exc(), flush=True)


if __name__ == '__main__':
    app.run()
