import inspect

from common import common_logging_elasticsearch_httpx


async def db_brainz_open(self, postdbhost, postdbport, postdbname, postdbuser, postdbpass,
                   db_connection=None):
    """
    # open database and pull in config from sqlite and create db if not exist
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    pass
    # setup for unicode
    # psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    # psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
    # # psycopg2.extensions.register_adapter(dict, psycopg2.extras.Json)
    # # psycopg2.extras.register_default_json(loads=lambda x: x)
    # self.sql3_conn = psycopg2.connect("dbname='%s' user='%s' host='%s' port=%s password='%s'",
    #                                   (postdbname, postdbuser, postdbhost, int(postdbport),
    #                                    postdbpass))
    # self.db_cursor = self.sql3_conn.cursor()
    # self.db_cursor.execute('SET TIMEZONE = \'America/Chicago\'')

    #        self.db_cursor.execute('SELECT COUNT (relname) as a FROM pg_class\
    # WHERE relname = \'mm_media\'')
    #        if self.db_cursor.fetchone()[0] == 0:
    #            exit(1)


async def db_brainz_close(self, db_connection=None):
    """
    # close main db file
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    self.sql3_conn.close()


async def db_brainz_all_artists(self, db_connection=None):
    """
    # read in all artists
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    self.db_cursor.execute('select gid,'
                           'name,'
                           'sort_name,'
                           'comment,'
                           'begin_date_year,'
                           'begin_date_month,'
                           'begin_date_day,'
                           'end_date_year,'
                           'end_date_month,'
                           'end_date_day,'
                           ' gender,'
                           'id from artist')
    return self.db_cursor.fetchall()


async def db_brainz_all_albums(self, db_connection=None):
    """
    # read in all albums
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    self.db_cursor.execute('select gid,'
                           'name,'
                           'artist_credit,'
                           'comment,'
                           'language,'
                           'barcode,'
                           'id from release')
    return self.db_cursor.fetchall()


async def db_brainz_all_albums_by_artist(self, artist_id, db_connection=None):
    """
    # read in album by artist credit id
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    self.db_cursor.execute('select gid,'
                           'name,'
                           'artist_credit,'
                           'comment,'
                           'language,'
                           'barcode,'
                           'id'
                           ' from release'
                           ' where artist_credit = %s', (artist_id,))
    return self.db_cursor.fetchall()


async def db_brainz_all_songs(self, db_connection=None):
    """
    # read in all songs
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    self.db_cursor.execute(
        'select gid,'
        'name,'
        'recording,'
        'position,'
        'id from track')
    return self.db_cursor.fetchall()


async def db_brainz_all_songs_by_rec_uuid(self, record_id, db_connection=None):
    """
    # read in all by recording id
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    self.db_cursor.execute('select gid,'
                           'name,'
                           'recording,'
                           'position,'
                           'id from track'
                           ' where recording = %s', (record_id,))
    return self.db_cursor.fetchall()


async def db_brainz_all(self, db_connection=None):
    """
    # read for batch insert
    """
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text={
                                                                         'function':
                                                                             inspect.stack()[0][
                                                                                 3],
                                                                         'locals': locals(),
                                                                         'caller':
                                                                             inspect.stack()[1][
                                                                                 3]})
    if db_connection is None:
        db_conn = self.db_connection
    else:
        db_conn = db_connection
    self.db_cursor.execute('select count(*) from artist,'
                           ' release,'
                           ' track'
                           ' where release.artist_credit = artist.id'
                           ' and track.recording = release.id')
    return self.db_cursor.fetchall()
