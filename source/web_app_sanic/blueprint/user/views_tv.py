



# tv show season detail - show guid then season #
@blueprint_user_tv.route("/tv_season_detail/<guid>/<season>", methods=['GET', 'POST'])
@login_required
async def url_bp_user_tv_season_detail_page(request, guid, season):
    """
    Display tv season detail page
    """
    data_metadata = g.db_connection.db_meta_tvshow_detail(guid)
    json_metadata = data_metadata['mm_metadata_tvshow_json']
    if 'tvmaze' in json_metadata['Meta']:
        if 'runtime' in json_metadata['Meta']['tvmaze']:
            data_runtime = json_metadata['Meta']['tvmaze']['runtime']
        else:
            data_runtime = None
        if 'rating' in json_metadata['Meta']['tvmaze']:
            data_rating = json_metadata['Meta']['tvmaze']['rating']['average']
        else:
            data_rating = None
        if 'premiered' in json_metadata['Meta']['tvmaze']:
            data_first_aired = json_metadata['Meta']['tvmaze']['premiered']
        else:
            data_first_aired = None
        if 'summary' in json_metadata['Meta']['tvmaze']:
            data_overview \
                = json_metadata['Meta']['tvmaze']['summary'].replace('<p>', '').replace('</p>', '')
        else:
            data_overview = None
        # build gen list
        data_genres_list = ''
        if 'genres' in json_metadata['Meta']['tvmaze']:
            for ndx in json_metadata['Meta']['tvmaze']['genres']:
                data_genres_list += (ndx + ', ')
    elif 'thetvdb' in json_metadata['Meta']:
        if 'Runtime' in json_metadata['Meta']['thetvdb']['Meta']['Series']:
            data_runtime = json_metadata['Meta']['thetvdb']['Meta']['Series']['Runtime']
        else:
            data_runtime = None
        if 'ContentRating' in json_metadata['Meta']['thetvdb']['Meta']['Series']:
            data_rating = json_metadata['Meta']['thetvdb']['Meta']['Series']['ContentRating']
        else:
            data_rating = None
        if 'FirstAired' in json_metadata['Meta']['thetvdb']['Meta']['Series']:
            data_first_aired = json_metadata['Meta']['thetvdb']['Meta']['Series']['FirstAired']
        else:
            data_first_aired = None
        if 'Overview' in json_metadata['Meta']['thetvdb']['Meta']['Series']:
            data_overview = json_metadata['Meta']['thetvdb']['Meta']['Series']['Overview']
        else:
            data_overview = None
        # build gen list
        data_genres_list = ''
        if 'Genre' in json_metadata['Meta']['thetvdb']['Meta']['Series']:
            for ndx in json_metadata['Meta']['thetvdb']['Meta']['Series']['Genre'].split("|"):
                data_genres_list += (ndx + ', ')
            # since | is at first and end....chop off first and last comma
            data_genres_list = data_genres_list[2:-2]

    data_episode_count = g.db_connection.db_read_tvmeta_season_eps_list(
        guid, int(season))
    common_global.es_inst.com_elastic_index('info', {'dataeps': data_episode_count})
    data_episode_keys = natsort.natsorted(data_episode_count)
    common_global.es_inst.com_elastic_index('info', {'dataepskeys': data_episode_keys})
    # poster image
    try:
        data_poster_image = data_metadata[3]
    except:
        data_poster_image = None
    # background image
    try:
        if json_metadata['LocalImages']['Backdrop'] is not None:
            data_background_image = json_metadata['LocalImages']['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    return render_template("users/user_tv_season_detail.html", data=data_metadata[0],
                           data_guid=guid,
                           data_season=season,
                           data_overview=data_overview,
                           data_rating=data_rating,
                           data_first_aired=data_first_aired,
                           data_runtime=data_runtime,
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image,
                           data_episode_count=data_episode_count,
                           data_episode_keys=data_episode_keys
                           )


# tv show episode detail
@blueprint_user_tv.route("/tv_episode_detail/<guid>/<season>/<episode>", methods=['GET', 'POST'])
@login_required
async def url_bp_user_tv_episode_detail_page(request, guid, season, episode):
    """
    Display tv episode detail page
    """
    data_episode_detail = g.db_connection.db_read_tvmeta_episode(
        guid, season, episode)
    # poster image
    try:
        data_poster_image = data_episode_detail[3]
    except:
        data_poster_image = None
    # background image
    try:
        if data_episode_detail['LocalImages']['Backdrop'] is not None:
            data_background_image = data_episode_detail['LocalImages']['Backdrop']
        else:
            data_background_image = None
    except:
        data_background_image = None
    return render_template("users/user_tv_episode_detail.html", data=data_episode_detail,
                           data_poster_image=data_poster_image,
                           data_background_image=data_background_image
                           )
