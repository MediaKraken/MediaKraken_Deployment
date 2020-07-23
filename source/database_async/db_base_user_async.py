async def db_user_count(self, db_connection, user_name=None):
    if user_name is None:
        return await db_connection.fetchval('select count(*) from mm_user')
    else:
        return await db_connection.fetchval('select count(*) from mm_user'
                                            ' where username = $1', user_name)


async def db_user_delete(self, db_connection, user_guid):
    """
    # remove user
    """
    await db_connection.execute('delete from mm_user'
                                ' where id = $1', user_guid)


async def db_user_detail(self, db_connection, guid):
    """
    # return all data for specified user
    """
    return await db_connection.fetchrow('select * from mm_user'
                                        ' where id = $1', guid)


async def db_user_insert(self, db_connection, user_name, user_email, user_password):
    """
    # insert user
    """
    if await self.db_user_count(db_connection) == 0:
        user_admin = True
    else:
        user_admin = False
    return await db_connection.execute(
        'insert into mm_user (username, email, password, active, is_admin)'
        ' values ($1, $2, $3, True, $4) returning id',
        user_name, user_email, user_password, user_admin), user_admin


async def db_user_list_name(self, db_connection, offset=0, records=None):
    """
    # return user list
    """
    return await db_connection.fetch('select id,'
                                     ' username,'
                                     ' email,'
                                     ' created_at,'
                                     ' active,'
                                     ' is_admin,'
                                     ' lang'
                                     ' from mm_user'
                                     ' where id in (select id from mm_user'
                                     ' order by LOWER(username)'
                                     ' offset $1 limit $2) order by LOWER(username)',
                                     offset, records)


async def db_user_login_validation(self, db_connection, user_name, user_password):
    """
    # verify user logon
    """
    result = await db_connection.fetchrow('select id, password, active, is_admin'
                                          ' from mm_user where username = $1', user_name)
    if result is not None:
        print(result, flush=True)
        print(type(result), flush=True)
        if result['active'] is False:
            return 'inactive_account', None
        print(user_password, len(user_password), result['password'], len(result['password']),
              flush=True)
        # the user_password should be app_crypto.com_hash_gen_crypt_encode at this point already
        if user_password == result['password']:
            return result['id'], result['is_admin']
        else:
            return 'invalid_password', None
    return None, None
