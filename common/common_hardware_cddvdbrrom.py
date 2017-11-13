import gudev

# https://stackoverflow.com/questions/2861098/how-do-i-use-udev-to-find-info-about-inserted-video-media-e-g-dvds
client = gudev.Client(['block'])
for device in client.query_by_subsystem("block"):
    if device.has_property("ID_CDROM"):
        print "Found CD/DVD drive at %s" % device.get_device_file()
        if device.has_property("ID_FS_LABEL"):
            print "Found disc: %s" % device.get_property("ID_FS_LABEL")
        elif device.has_property("ID_FS_TYPE"):
            print "Found disc"
        else:
            print "No disc"
