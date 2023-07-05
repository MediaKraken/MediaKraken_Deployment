async def db_brainz_all_artists(self, db_connection=None):
    """
    # read in all artists
    """
    await self.db_cursor.execute('select gid,'
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


async def db_brainz_all_albums_by_artist(self, artist_id, db_connection=None):
    """
    # read in album by artist credit id
    """
    await self.db_cursor.execute('select gid,'
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
    await self.db_cursor.execute(
        'select gid,'
        'name,'
        'recording,'
        'position,'
        'id from track')
    return await self.db_cursor.fetchall()


async def db_brainz_all_songs_by_rec_uuid(self, record_id, db_connection=None):
    """
    # read in all by recording id
    """
    await self.db_cursor.execute('select gid,'
                                 'name,'
                                 'recording,'
                                 'position,'
                                 'id from track'
                                 ' where recording = %s', (record_id,))
    return await self.db_cursor.fetchall()


async def db_brainz_all(self, db_connection=None):
    """
    # read for batch insert
    """
    await self.db_cursor.execute('select count(*) from artist,'
                                 ' release,'
                                 ' track'
                                 ' where release.artist_credit = artist.id'
                                 ' and track.recording = release.id')
    return await self.db_cursor.fetchall()
