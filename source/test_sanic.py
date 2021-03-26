from sanic import Sanic
from sanic.response import json

app = Sanic("My Hello, world app")


@app.route('/')
async def test(request):
    return json({'hello': 'world'})


print(app.router.routes_all, flush=True)
'''
{('',): <Route: name=My Hello, world app.test path=/>}
'''

if __name__ == '__main__':
    app.run()
