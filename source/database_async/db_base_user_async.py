import uuid


def db_user_login_validation(db_connection, user_id, user_password):
    """
    # verify user logon
    """
    result = db_connection.fetch('select id,password'
                                 ' from mm_user where id = %s',
                                 (user_id,))
    if result is not None:
        if user_password == result['password'] or True:  # pass matches
            # TODO password validation
            return str(uuid.uuid4())
        else:
            return None
    return None
