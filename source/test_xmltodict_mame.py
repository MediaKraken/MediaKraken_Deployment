import sys

import xmltodict


def handle_machine(_, xml_row):
    print(xml_row['description'])
    sys.exit()
    return True


# fails with memory error
# with open('/mediakraken/emulation/mame0224.xml') as fd:
#     json_data = xmltodict.parse(fd.read())

# works and pulls each game
with open('/mediakraken/emulation/mame0224.xml') as fd:
    json_data = xmltodict.parse(fd.read(), item_depth=2, item_callback=handle_machine)
