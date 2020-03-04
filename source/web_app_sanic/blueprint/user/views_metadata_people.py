

@blueprint.route('/meta_person_detail/<guid>')
@login_required
def metadata_person_detail(guid):
    """
    Display person detail page
    """
    person_data = g.db_connection.db_meta_person_by_guid(guid)
    if person_data['mmp_person_image'] is not None:
        if 'themoviedb' in person_data['mmp_person_image']['Images']:
            try:
                person_image = person_data['mmp_person_image']['Images']['themoviedb'].replace(
                    '/mediakraken/web_app/MediaKraken', '') + person_data['mmp_meta']
            except:
                person_image = "/static/images/person_missing.png"
        else:
            person_image = "/static/images/person_missing.png"
    else:
        person_image = "/static/images/person_missing.png"
    return render_template('users/metadata/meta_people_detail.html',
                           json_metadata=person_data['mmp_person_meta_json'],
                           data_person_image=person_image,
                           data_also_media=g.db_connection.db_meta_person_as_seen_in(
                               person_data['mmp_id']),
                           )


@blueprint.route('/meta_person_list', methods=['GET', 'POST'])
@login_required
def metadata_person_list():
    """
    Display person list page
    """
    page, per_page, offset = common_pagination.get_page_items()
    person_list = []
    for person_data in g.db_connection.db_meta_person_list(offset, per_page,
                                                           session['search_text']):
        common_global.es_inst.com_elastic_index('info', {'person data': person_data, 'im':
            person_data['mmp_person_image'], 'meta': person_data['mmp_meta']})
        if person_data['mmp_person_image'] is not None:
            if 'themoviedb' in person_data['mmp_person_image']['Images']:
                try:
                    person_image = person_data['mmp_person_image']['Images']['themoviedb'].replace(
                        '/mediakraken/web_app/MediaKraken', '') + person_data['mmp_meta']
                except:
                    person_image = "/static/images/person_missing.png"
            else:
                person_image = "/static/images/person_missing.png"
        else:
            person_image = "/static/images/person_missing.png"
        person_list.append(
            (person_data['mmp_id'], person_data['mmp_person_name'], person_image))
    session['search_page'] = 'meta_people'
    pagination = common_pagination.get_pagination(page=page,
                                                  per_page=per_page,
                                                  total=g.db_connection.db_meta_person_list_count(
                                                      session['search_text']),
                                                  record_name='person',
                                                  format_total=True,
                                                  format_number=True,
                                                  )
    return render_template('users/metadata/meta_people_list.html',
                           media_person=person_list,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

