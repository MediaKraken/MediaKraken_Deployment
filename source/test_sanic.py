from sanic import Sanic
from sanic.response import json

app = Sanic("My Hello, world app")


@app.route('/')
async def test(request):
    return json({'hello': 'world'})


for route in app.router.routes_all.items():
    print(route, flush=True)
'''  this is "production" output
(('user', 'user_sports_detail', '<guid>'), <Route: name=web_app_sanic.app.name_blueprint_user_sports.url_bp_user_sports_detail path=user/user_sports_detail/<guid>>)
(('user', 'user_sync_edit', '<guid>'), <Route: name=web_app_sanic.app.name_blueprint_user_sync.url_bp_user_sync_edit path=user/user_sync_edit/<guid>>)
(('user', 'user_tv_show_episode_detail', '<guid>', '<season>', '<episode>'), <Route: name=web_app_sanic.app.name_blueprint_user_tv.url_bp_user_tv_show_episode_detail_page path=user/user_tv_show_episode_detail/<guid>/<season>/<episode>>)
(('user', 'user_tv_show_detail', '<guid>'), <Route: name=web_app_sanic.app.name_blueprint_user_tv.url_bp_user_tv_show_detail path=user/user_tv_show_detail/<guid>>)
(('user', 'user_tv_show_season_detail', '<guid>', '<season>'), <Route: name=web_app_sanic.app.name_blueprint_user_tv.url_bp_user_tv_show_season_detail_page path=user/user_tv_show_season_detail/<guid>/<season>>)
(('user', 'user_tv_live', '<schedule_date>', '<schedule_time>'), <Route: name=web_app_sanic.app.name_blueprint_user_tv_live.url_bp_user_tv_live path=user/user_tv_live/<schedule_date>/<schedule_time>>)
(('user', 'user_tv_live_detail', '<guid>'), <Route: name=web_app_sanic.app.name_blueprint_user_tv_live.url_bp_user_tv_live_detail path=user/user_tv_live_detail/<guid>>)
(('favicon.ico', '<__file_uri__:path>'), <Route: name=web_app_sanic.app.static path=favicon.ico/<__file_uri__:path>>)
(('static', '<__file_uri__:path>'), <Route: name=web_app_sanic.app.static path=static/<__file_uri__:path>>)
'''

if __name__ == '__main__':
    app.run()
