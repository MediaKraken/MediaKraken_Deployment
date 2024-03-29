import inspect
import json
import uuid

from common import common_logging_elasticsearch_httpx


async def db_user_count(self, user_name=None, db_connection=None):
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
    if user_name is None:
        return await db_conn.fetchval('select count(*) from mm_user')
    else:
        return await db_conn.fetchval('select count(*) from mm_user'
                                      ' where username = $1', user_name)


async def db_user_delete(self, user_guid, db_connection=None):
    """
    # remove user
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
    await db_conn.execute('delete from mm_user'
                          ' where id = $1', user_guid)


async def db_user_detail(self, guid, db_connection=None):
    """
    # return all data for specified user
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
    return await db_conn.fetchrow('select * from mm_user'
                                  ' where id = $1', guid)


async def db_user_exists(self, user_name, db_connection=None):
    """
    # determine if user exists
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
    return await db_conn.fetchval('select exists(select 1 from mm_user'
                                  ' where username = $1 limit 1) limit 1', user_name)


async def db_user_insert(self, user_name, user_email, user_password, db_connection=None):
    """
    # insert user
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
    if await self.db_user_count(user_name=None, db_connection=db_conn) == 0:
        user_admin = True
    else:
        user_admin = False
    return await db_conn.execute(
        'insert into mm_user (username, email, password, active, is_admin, user_json, created_at)'
        ' values ($1, $2, crypt($3, gen_salt(\'bf\', 10)), True, $4, \'{"per_page": 30}\','
        ' current_timestamp)'
        ' returning id',
        user_name, user_email, user_password, user_admin), user_admin, 30


async def db_user_list_name(self, offset=0, records=None, db_connection=None):
    """
    # return user list
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
    return await db_conn.fetch('select id,'
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


async def db_user_login(self, user_name, user_password, db_connection=None):
    """
    # verify user logon
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
    result = await db_conn.fetchrow('select id, active, is_admin,'
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


async def db_user_group_insert(self, group_name, group_desc, group_rights_json,
                               db_connection=None):
    """
    insert user group
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
    new_user_group_id = uuid.uuid4()
    await db_conn.execute('insert into mm_user_group (mm_user_group_guid,'
                          ' mm_user_group_name,'
                          ' mm_user_group_description,'
                          ' mm_user_group_rights_json)'
                          ' values ($1,$2,$3,$4)',
                          new_user_group_id, group_name,
                          group_desc, group_rights_json)
    await db_conn.execute('commit')
    return new_user_group_id
