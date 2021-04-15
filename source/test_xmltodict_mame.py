import sys

import xmltodict


def handle_machine(_, xml_row):
    print(xml_row)
    sys.exit()
    return True


# fails with memory error
# with open('/mediakraken/emulation/mame0224.xml') as fd:
#     json_data = xmltodict.parse(fd.read())


# works and pulls each game
# with open('/mediakraken/emulation/mame0224.xml') as fd:
#     json_data = xmltodict.parse(fd.read(), item_depth=2, item_callback=handle_machine)

# need depth 1.......but memory fails
with open('/mediakraken/emulation/mame0224.xml') as fd:
    json_data = xmltodict.parse(fd.read(), item_depth=1, item_callback=handle_machine)
