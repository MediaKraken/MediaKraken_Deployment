async def db_tv_schedule_by_date(self, display_date):
    """
    # tv shows for schedule display
    """
    return await self.db_connection.fetch('SELECT row_to_json(json_data)'
                                          ' FROM (select mm_tv_station_name,'
                                          ' mm_tv_station_channel,'
                                          ' mm_tv_schedule_json'
                                          ' from mm_tv_stations, mm_tv_schedule'
                                          ' where mm_tv_schedule_station_id = mm_tv_station_id'
                                          ' and mm_tv_schedule_date = $1'
                                          ' order by LOWER(mm_tv_station_name),'
                                          ' mm_tv_schedule_json->\'airDateTime\') as json_data',
                                          display_date)
