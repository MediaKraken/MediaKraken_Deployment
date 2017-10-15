# stuff = 'where mm_media_name %% %s order by mm_media_name offset %s limit %s)' % ('table', 1, 3)
#
# print(stuff)
#
#
# stuff = 'hash/jfslhtr/jhytr'
#
# print stuff[0:5]
#
# print stuff.split('/',1)[1]
#
# print stuff[-1:]
import time
from common import common_lirc

lirc = common_lirc.CommonLIRC(None)

lirc.com_lirc_init()


code = ""
while(code != "quit"):
    print(lirc.com_lirc_nextcode())
    # Delay...
    time.sleep(1)


lirc.com_lirc_close()