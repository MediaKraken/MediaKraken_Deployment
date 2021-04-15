import asyncio

from common import common_config_ini
from common import common_logging_elasticsearch_httpx


# works fine hitting the database and doing the db_connection thing
# passing NONE as it's NOT the pool webapp!!!!

async def main(loop):
    await common_logging_elasticsearch_httpx.com_es_httpx_post_async(message_type='info',
                                                                     message_text='START',
                                                                     index_name='testtest')
    # open the database
    option_config_json, db_connection = \
        await common_config_ini.com_config_read_async(loop=loop,
                                                      as_pool=False,
                                                      force_local=True)
    db_result = await db_connection.db_table_count(table_name='mm_sync',
                                                   db_connection=None)
    print(db_result)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
