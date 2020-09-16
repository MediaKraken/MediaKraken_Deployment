async def db_user_login(db_connection, user_name, user_password):
    """
    # verify user logon
    """
    result = await db_connection.fetchrow('select id, active, is_admin,'
                                          ' user_json->\'per_page\' as per_page'
                                          ' from mm_user where username = $1'
                                          ' and password = crypt($2, password)',
                                          user_name, user_password)
    if result is not None:
        print(result, flush=True)
        if result['active'] is False:
            return 'inactive_account', None, None
        return result['id'], result['is_admin'], result['per_page']
    return 'invalid_password', None, None
