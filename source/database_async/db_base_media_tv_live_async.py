def db_tv_schedule_by_date(self, db_connection, display_date):
    """
    # tv shows for schedule display
    """
    return db_connection.fetch('select mm_tv_station_name,'
                               ' mm_tv_station_channel,'
                               ' mm_tv_schedule_json'
                               ' from mm_tv_stations, mm_tv_schedule'
                               ' where mm_tv_schedule_station_id = mm_tv_station_id'
                               ' and mm_tv_schedule_date = %s'
                               ' order by LOWER(mm_tv_station_name),'
                               ' mm_tv_schedule_json->\'airDateTime\'',
                               (display_date,))
