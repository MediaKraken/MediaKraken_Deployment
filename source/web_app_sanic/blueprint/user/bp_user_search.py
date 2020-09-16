import json

from common import common_global
from common import common_logging_elasticsearch_httpx
from sanic import Blueprint
from sanic.response import redirect
from web_app_sanic.blueprint.user.bss_form_search import BSSSearchEditForm

blueprint_user_search = Blueprint('name_blueprint_user_search', url_prefix='/user')


@blueprint_user_search.route("/user_search", methods=["GET", "POST"])
@common_global.jinja_template.template('bss_user/media/bss_user_media_search.html')
@common_global.auth.login_required
async def url_bp_user_search_media(request):
    """
    Display search page
    """
    form = BSSSearchEditForm(request)
    movie = []
    tvshow = []
    album = []
    image = []
    publication = []
    game = []
    movie_search = False
    tvshow_search = False
    album_search = False
    image_search = False
    publication_search = False
    game_search = False
    if request.method == 'POST':
        if request.form['action_type'] == 'Search Local':
            if request.form['search_media_type'] == 'any':
                movie_search = True
                tvshow_search = True
                album_search = True
                image_search = True
                publication_search = True
                game_search = True
            elif request.form['search_media_type'] == 'video':
                movie_search = True
                tvshow_search = True
            elif request.form['search_media_type'] == 'audio':
                album_search = True
            elif request.form['search_media_type'] == 'image':
                image_search = True
            elif request.form['search_media_type'] == 'publication':
                publication_search = True
            elif request.form['search_media_type'] == 'game':
                game_search = True
            db_connection = await request.app.db_pool.acquire()
            json_data = json.loads(
                await request.app.db_functions.db_metadata_search(db_connection,
                                                                  request.form['search_string'],
                                                                  search_type='Local',
                                                                  search_movie=movie_search,
                                                                  search_tvshow=tvshow_search,
                                                                  search_album=album_search,
                                                                  search_image=image_search,
                                                                  search_publication=publication_search,
                                                                  search_game=game_search))
            await request.app.db_pool.release(db_connection)
            if 'Movie' in json_data:
                for search_item in json_data['Movie']:
                    movie.append(search_item)
            if 'TVShow' in json_data:
                for search_item in json_data['TVShow']:
                    tvshow.append(search_item)
            if 'Album' in json_data:
                for search_item in json_data['Album']:
                    album.append(search_item)
            if 'Image' in json_data:
                for search_item in json_data['Image']:
                    image.append(search_item)
            if 'Publication' in json_data:
                for search_item in json_data['Publication']:
                    publication.append(search_item)
            if 'Game' in json_data:
                for search_item in json_data['Game']:
                    game.append(search_item)
        elif request.form['action_type'] == 'Search Metadata Providers':
            pass
        # TODO
        # search_primary_language
        # search_secondary_language
        # search_resolution
        # search_audio_channels
        # search_audio_codec
    return {
        'media': movie,
        'media_tvshow': tvshow,
        'media_album': album,
        'media_image': image,
        'media_book': publication,
        'media_game': game,
        'form': form
    }


@blueprint_user_search.route("/user_search_nav", methods=["GET", "POST"])
@common_global.auth.login_required
async def url_bp_user_search_nav_media(request):
    """
    determine what search results screen to show
    """
    # TODO!
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info', message_text={
        "search session": request.ctx.session['search_page']})
    request.ctx.session['search_text'] = request.form.get('nav_search').strip()
    if request.ctx.session['search_page'] == 'media_3d':
        return redirect(request.app.url_for('name_blueprint_user_media_3d.url_bp_user_media_3d'))
    elif request.ctx.session['search_page'] == 'media_album':
        return redirect(request.app.url_for('name_blueprint_user_music.url_bp_user_album_list'))
    elif request.ctx.session['search_page'] == 'media_games':
        return redirect(request.app.url_for('name_blueprint_user_game.url_bp_user_game'))
    elif request.ctx.session['search_page'] == 'media_movie':
        return redirect(
            request.app.url_for('name_blueprint_user_media_genre.url_bp_user_media_genre',
                                genre='All'))
    elif request.ctx.session['search_page'] == 'media_music_video':
        return redirect(
            request.app.url_for('name_blueprint_user_music_video.url_bp_user_music_video_list'))
    elif request.ctx.session['search_page'] == 'media_periodicals':
        return redirect(
            request.app.url_for('name_blueprint_user_periodical.url_bp_user_periodical_list'))
    elif request.ctx.session['search_page'] == 'media_sports':
        return redirect(request.app.url_for('name_blueprint_user_sports.url_bp_user_sports'))
    elif request.ctx.session['search_page'] == 'media_tv':
        return redirect(request.app.url_for('name_blueprint_user_tv.url_bp_user_tv'))
    # begin metadata section
    elif request.ctx.session['search_page'] == 'meta_album':
        return redirect(request.app.url_for(
            'name_blueprint_user_metadata_music.url_bp_user_metadata_music_album_list'))
    elif request.ctx.session['search_page'] == 'meta_game':
        return redirect(
            request.app.url_for('name_blueprint_user_metadata_game.url_bp_user_metadata_game'))
    elif request.ctx.session['search_page'] == 'meta_game_system':
        return redirect(request.app.url_for(
            'name_blueprint_user_metadata_game_system.url_bp_user_metadata_game_system'))
    elif request.ctx.session['search_page'] == 'meta_movie':
        return redirect(request.app.url_for(
            'name_blueprint_user_metadata_movie.url_bp_user_metadata_movie_list'))
    elif request.ctx.session['search_page'] == 'meta_movie_collection':
        return redirect(request.app.url_for(
            'name_blueprint_user_media_collection.url_bp_user_metadata_movie_collection'))
    elif request.ctx.session['search_page'] == 'meta_music_video':
        return redirect(request.app.url_for(
            'name_blueprint_user_metadata_music_video.url_bp_user_metadata_music_video'))
    elif request.ctx.session['search_page'] == 'meta_people':
        return redirect(request.app.url_for(
            'name_blueprint_user_metadata_people.url_bp_user_metadata_person_list'))
    elif request.ctx.session['search_page'] == 'meta_periodical':
        return redirect(request.app.url_for(
            'name_blueprint_user_metadata_periodical.url_bp_user_metadata_periodical'))
    elif request.ctx.session['search_page'] == 'meta_sports':
        return redirect(request.app.url_for(
            'name_blueprint_user_metadata_sports.url_bp_user_metadata_sports_list'))
    elif request.ctx.session['search_page'] == 'meta_tv':
        return redirect(
            request.app.url_for('name_blueprint_user_metadata_tv.url_bp_user_metadata_tvshow_list'))
