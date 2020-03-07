from sanic import Blueprint

from .bp_user_cctv import blueprint_user_cctv
from .bp_user_game import blueprint_user_game
from .bp_user_game_servers import blueprint_user_game_servers
from .bp_user_hardware import blueprint_user_hardware
from .bp_user_home_media import blueprint_user_home_media
from .bp_user_homepage import blueprint_user_homepage
from .bp_user_image import blueprint_user_image
from .bp_user_internet import blueprint_user_internet
from .bp_user_media_collection import blueprint_user_media_collection
from .bp_user_media_new import blueprint_user_media_new
from .bp_user_metadata_game import blueprint_user_metadata_game
from .bp_user_metadata_game_system import blueprint_user_metadata_game_system
from .bp_user_metadata_movie import blueprint_user_metadata_movie
from .bp_user_metadata_people import blueprint_user_metadata_people
from .bp_user_metadata_periodical import blueprint_user_metadata_periodical
from .bp_user_metadata_sports import blueprint_user_metadata_sports
from .bp_user_metadata_tv import blueprint_user_metadata_tv
from .bp_user_movie import blueprint_user_movie
from .bp_user_music import blueprint_user_music
from .bp_user_music_video import blueprint_user_music_video
from .bp_user_periodical import blueprint_user_periodical
from .bp_user_playback_audio import blueprint_user_playback_audio
from .bp_user_playback_video import blueprint_user_playback_video
from .bp_user_queue import blueprint_user_queue
from .bp_user_search import blueprint_user_search
from .bp_user_sports import blueprint_user_sports
from .bp_user_sync import blueprint_user_sync
from .bp_user_tv import blueprint_user_tv
from .bp_user_tv_live import blueprint_user_tv_live

blueprint_user_content = Blueprint.group(blueprint_user_cctv,
                                         blueprint_user_game,
                                         blueprint_user_game_servers,
                                         blueprint_user_hardware,
                                         blueprint_user_home_media,
                                         blueprint_user_homepage,
                                         blueprint_user_image,
                                         blueprint_user_internet,
                                         blueprint_user_media_collection,
                                         blueprint_user_media_new,
                                         blueprint_user_metadata_game,
                                         blueprint_user_metadata_game_system,
                                         blueprint_user_metadata_sports,
                                         blueprint_user_metadata_movie,
                                         blueprint_user_metadata_people,
                                         blueprint_user_metadata_periodical,
                                         blueprint_user_metadata_tv,
                                         blueprint_user_music,
                                         blueprint_user_music_video,
                                         blueprint_user_movie,
                                         blueprint_user_periodical,
                                         blueprint_user_playback_audio,
                                         blueprint_user_playback_video,
                                         blueprint_user_queue,
                                         blueprint_user_search,
                                         blueprint_user_sports,
                                         blueprint_user_sync,
                                         blueprint_user_tv,
                                         blueprint_user_tv_live,
                                         )
