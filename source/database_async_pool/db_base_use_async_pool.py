async def db_user_login(self, db_connection, user_name, user_password):
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


async def db_user_count(self, db_connection, user_name=None):
    if user_name is None:
        return await db_connection.fetchval('select count(*) from mm_user')
    else:
        return await db_connection.fetchval('select count(*) from mm_user'
                                            ' where username = $1', user_name)


async def db_user_insert(self, db_connection, user_name, user_email, user_password):
    """
    # insert user
    """
    if await db_connection.db_user_count() == 0:
        user_admin = True
    else:
        user_admin = False
    return await db_connection.execute(
        'insert into mm_user (username, email, password, active, is_admin, user_json::json)'
        ' values ($1, $2, crypt($3, gen_salt(\'bf\', 10)), True, $4, {"per_page": 30})'
        ' returning id',
        user_name, user_email, user_password, user_admin), user_admin
