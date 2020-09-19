import inspect

from common import common_logging_elasticsearch_httpx


async def db_tv_schedule_by_date(self, display_date, db_connection=None):
    """
    # tv shows for schedule display
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
    return await db_conn.fetch('select mm_tv_station_name,'
                               ' mm_tv_station_channel,'
                               ' mm_tv_schedule_json::json'
                               ' from mm_tv_stations, mm_tv_schedule'
                               ' where mm_tv_schedule_station_id = mm_tv_station_id'
                               ' and mm_tv_schedule_date = $1'
                               ' order by LOWER(mm_tv_station_name),'
                               ' mm_tv_schedule_json->\'airDateTime\'',
                               display_date)
