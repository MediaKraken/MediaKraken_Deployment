import xmltodict

from common import common_config_ini

# open the database
option_config_json, db_connection = common_config_ini.com_config_read(force_local=True)

count = 0
update_game = 0
game_xml = ''
first_record = True
insert_game = 0
with open('/mediakraken/emulation/mame0224.xml') as infile:
    for line in infile:
        if line.find('	<machine') == 0:  # first position of line
            # TODO pump out last game_xml to db
            if first_record is False:
                json_data = xmltodict.parse(line + game_xml)
                # print('JSON:', json_data)
                if db_connection.db_meta_game_list_count(json_data['machine']['@name']) > 0:
                    # TODO handle shortname properly
                    db_connection.db_meta_game_update(None, json_data['machine']['@name'],
                                                      json_data['machine']['description'],
                                                      json_data)
                    update_game += 1
                else:
                    # TODO handle shortname properly
                    db_connection.db_meta_game_insert(None, json_data['machine']['@name'],
                                                      json_data['machine']['description'],
                                                      json_data)
                    insert_game += 1

                game_xml = ''
            count += 1
            first_record = False
        else:
            if first_record is False:
                game_xml += line
    game_xml += line  # get last value
print('count =', count)

# commit all changes to db
db_connection.db_commit()

# close the database
db_connection.db_close()
