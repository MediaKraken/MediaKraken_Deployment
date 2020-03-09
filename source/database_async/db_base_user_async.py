def db_user_count(db_connection):
    return db_connection.fetchval('select count(*) from mm_user')


def db_user_delete(db_connection, user_guid):
    """
    # remove user
    """
    db_connection.execute('delete from mm_user'
                          ' where id = %s', (user_guid,))


def db_user_detail(db_connection, guid):
    """
    # return all data for specified user
    """
    return db_connection.fetch('select * from mm_user'
                               ' where id = %s', (guid,))


def db_user_insert(db_connection, user_name, user_email, user_password):
    """
    # insert user
    """
    if db_user_count(db_connection) == 0:
        user_admin = True
    else:
        user_admin = False
    return db_connection.execute(
        'insert into mm_user (id, username, email, password, active, is_admin)'
        ' values (NULL, %s, %s, %s, True, %s) returning id',
        (user_name, user_email, user_password, user_admin)), user_admin


def db_user_login_validation(db_connection, user_name, user_password):
    """
    # verify user logon
    """
    result = db_connection.fetch('select id, password, active, is_admin'
                                 ' from mm_user where username = %s',
                                 (user_name,))
    if result is not None:
        if result['active'] is False:
            return 'inactive_account', None
        if user_password == result['password']:
            return result['id'], result['is_admin']
        else:
            return 'invalid_password', None
    return 'user_notfound', None
