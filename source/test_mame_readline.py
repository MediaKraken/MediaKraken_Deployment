import xmltodict

from common import common_config_ini

# open the database
option_config_json, db_connection = common_config_ini.com_config_read(force_local=True)


def process_mame_record(game_xml):
    global update_game
    global insert_game
    # TODO change this to upsert
    json_data = xmltodict.parse(game_xml)
    # see if exists then need to update
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


count = 0
update_game = 0
game_xml = ''
first_record = True
insert_game = 0
old_line = None
with open('/mediakraken/emulation/mame0224.xml') as infile:
    for line in infile:
        if line.find('</mame>') == 0:  # skip the last line
            pass
        elif line.find('	<machine') == 0:  # first position of line
            old_line = line
            if first_record is False:
                process_mame_record(line + game_xml)
                game_xml = ''
            first_record = False
        else:
            if first_record is False:
                game_xml += line
    # game_xml += line  # get last value - do NOT do this as it'll attach </mame>
# do last machine
process_mame_record(old_line + game_xml)

# commit all changes to db
db_connection.db_commit()

# close the database
db_connection.db_close()
