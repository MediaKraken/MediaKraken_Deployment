import uuid


async def db_user_count(self, user_name=None):
    if user_name is None:
        return await self.db_connection.fetchval('select count(*) from mm_user')
    else:
        return await self.db_connection.fetchval('select count(*) from mm_user'
                                                 ' where username = $1', user_name)


async def db_user_delete(self, user_guid):
    """
    # remove user
    """
    await self.db_connection.execute('delete from mm_user'
                                     ' where id = $1', user_guid)


async def db_user_detail(self, guid):
    """
    # return all data for specified user
    """
    return await self.db_connection.fetchrow('SELECT row_to_json(json_data)'
                                             ' FROM (select * from mm_user'
                                             ' where id = $1) as json_data', guid)


async def db_user_insert(self, user_name, user_email, user_password):
    """
    # insert user
    """
    if await self.db_user_count() == 0:
        user_admin = True
    else:
        user_admin = False
    return await self.db_connection.execute(
        'insert into mm_user (username, email, password, active, is_admin, user_json)'
        ' values ($1, $2, crypt($3, gen_salt(\'bf\', 10)), True, $4, {"per_page": 30})'
        ' returning id',
        user_name, user_email, user_password, user_admin), user_admin


async def db_user_list_name(self, offset=0, records=None):
    """
    # return user list
    """
    return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                          ' FROM (select id,'
                                          ' username,'
                                          ' email,'
                                          ' created_at,'
                                          ' active,'
                                          ' is_admin,'
                                          ' lang'
                                          ' from mm_user'
                                          ' where id in (select id from mm_user'
                                          ' order by LOWER(username)'
                                          ' offset $1 limit $2) order by LOWER(username))'
                                          ' as json_data',
                                          offset, records)


async def db_user_login(self, user_name, user_password):
    """
    # verify user logon
    """
    result = await self.db_connection.fetchrow('SELECT row_to_json(json_data)'
                                               ' FROM (select id, active, is_admin,'
                                               ' user_json->\'per_page\' as per_page'
                                               ' from mm_user where username = $1'
                                               ' and password = crypt($2, password))'
                                               ' as json_data',
                                               user_name, user_password)
    if result is not None:
        print(result, flush=True)
        if result['active'] is False:
            return 'inactive_account', None, None
        return result['id'], result['is_admin'], result['per_page']
    return 'invalid_password', None, None


async def db_user_group_insert(self, group_name, group_desc, group_rights_json):
    """
    insert user group
    """
    new_user_group_id = str(uuid.uuid4())
    await self.db_connection.execute('insert into mm_user_group (mm_user_group_guid,'
                                     ' mm_user_group_name,'
                                     ' mm_user_group_description,'
                                     ' mm_user_group_rights_json)'
                                     ' values ($1,$2,$3,$4)',
                                     new_user_group_id, group_name,
                                     group_desc, group_rights_json)
    await self.db_connection.execute('commit')
    return new_user_group_id
