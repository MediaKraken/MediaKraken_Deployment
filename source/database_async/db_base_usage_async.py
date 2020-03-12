def db_usage_top10_alltime(self, db_connection):
    """
    Top 10 of all time
    """
    return db_connection.fetch('select 1 limit 10')


def db_usage_top10_movie(self, db_connection):
    """
    Top 10 movies
    """
    return db_connection.fetch('select mm_metadata_user_json->\'Watched\'->\'Times\''
                               ' from mm_metadata_movie'
                               ' order by mm_metadata_user_json->\'Watched\'->\'Times\''
                               ' desc limit 10')


def db_usage_top10_tv_episode(self, db_connection):
    """
    Top 10 TV episode
    """
    return db_connection.fetch('select 1 limit 10')


def db_usage_top10_tv_show(self, db_connection):
    """
    Top 10 TV show
    """
    return db_connection.fetch('select mm_metadata_tvshow_user_json->\'Watched\'->\'Times\''
                               ' from mm_metadata_tvshow'
                               ' order by mm_metadata_tvshow_user_json->\'Watched\'->\'Times\''
                               ' desc limit 10')
