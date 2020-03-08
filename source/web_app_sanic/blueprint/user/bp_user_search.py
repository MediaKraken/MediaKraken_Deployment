import json

from common import common_global
from sanic import Blueprint
from sanic.response import redirect

blueprint_user_search = Blueprint('name_blueprint_user_search', url_prefix='/user')


@blueprint_user_search.route("/search", methods=["GET", "POST"])
@common_global.jinja_template.template('user/user_search.html')
@common_global.auth.login_required
async def url_bp_user_search_media(request):
    """
    Display search page
    """
    form = SearchEditForm(request.form)
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
            json_data = json.loads(
                g.db_connection.db_search(request.form['search_string'], search_type='Local',
                                          search_movie=movie_search, search_tvshow=tvshow_search,
                                          search_album=album_search, search_image=image_search,
                                          search_publication=publication_search,
                                          search_game=game_search))
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


@blueprint_user_search.route("/search_nav", methods=["GET", "POST"])
@common_global.auth.login_required
async def url_bp_user_search_nav_media(request):
    """
    determine what search results screen to show
    """
    common_global.es_inst.com_elastic_index('info', {
        "search session": request['session']['search_page']})
    request['session']['search_text'] = request.form.get('nav_search').strip()
    if request['session']['search_page'] == 'media_3d':
        return redirect(request.app.url_for('user_3d.user_3d_list'))
    elif request['session']['search_page'] == 'media_album':
        return redirect(request.app.url_for('user_music.user_album_list_page'))
    elif request['session']['search_page'] == 'media_games':
        return redirect(request.app.url_for('user_games.user_games_list'))
    elif request['session']['search_page'] == 'media_movie':
        return redirect(request.app.url_for('user_movie_genre.user_movie_page', genre='All'))
    elif request['session']['search_page'] == 'media_music_video':
        return redirect(request.app.url_for('user_music_video.user_music_video_list'))
    elif request['session']['search_page'] == 'media_periodicals':
        return redirect(request.app.url_for('user_periodicals.user_books_list'))
    elif request['session']['search_page'] == 'media_sports':
        return redirect(request.app.url_for('user_sports.user_sports_page'))
    elif request['session']['search_page'] == 'media_tv':
        return redirect(request.app.url_for('user_tv.user_tv_page'))
    # begin metadata section
    elif request['session']['search_page'] == 'meta_album':
        return redirect(request.app.url_for('user_metadata_album.metadata_music_album_list'))
    elif request['session']['search_page'] == 'meta_game':
        return redirect(request.app.url_for('user_metadata_game.metadata_game_list'))
    elif request['session']['search_page'] == 'meta_game_system':
        return redirect(request.app.url_for('user_metadata_game_system.metadata_game_system_list'))
    elif request['session']['search_page'] == 'meta_movie':
        return redirect(request.app.url_for('user_metadata_movie.metadata_movie_list'))
    elif request['session']['search_page'] == 'meta_movie_collection':
        return redirect(request.app.url_for('user_movie_collection.metadata_movie_collection_list'))
    elif request['session']['search_page'] == 'meta_music_video':
        return redirect(request.app.url_for('user_metadata_music_video.metadata_music_video_list'))
    elif request['session']['search_page'] == 'meta_people':
        return redirect(request.app.url_for('user_metadata_people.metadata_person_list'))
    elif request['session']['search_page'] == 'meta_periodical':
        return redirect(request.app.url_for('user_metadata_periodical.metadata_periodical_list'))
    elif request['session']['search_page'] == 'meta_sports':
        return redirect(request.app.url_for('user_metadata_sports.metadata_sports_list'))
    elif request['session']['search_page'] == 'meta_tv':
        return redirect(request.app.url_for('user_metadata_tv.metadata_tvshow_list'))
