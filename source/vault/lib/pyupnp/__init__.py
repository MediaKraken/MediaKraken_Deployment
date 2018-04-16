from twisted.internet import reactor
from pyupnp.ssdp import SSDP_MSearch
from pyupnp.upnp import UPnP, Device

__author__ = 'Dean Gardiner'

PRINT_SERVICES = False

if __name__ == '__main__':
    devices = {}

    def foundDevice(device):
        print "foundDevice", device

    def gotDescription(device):
        print "gotDescription", device

    def finishedSearching(devices):
        print "finishedSearching"
        print

        for dk, dv in devices.items():
            print dv
            UPnP.deviceDescription(dv)  # Get Device Description
            print '\tLocation:', dv.location
            print '\tServer:', dv.server
            print
            print '\tDescribed:', dv.described
            if dv.described:
                print '\t\tFriendly Name:', dv.friendlyName
                print '\t\tManufacturer:', dv.manufacturer
                print '\t\tManufacturer URL:', dv.manufacturerURL
                print '\t\tmodelName:', dv.modelName
                print '\t\tmodelNumber:', dv.modelNumber
                print '\t\tmodelURL:', dv.modelURL
                print '\t\tserialNumber:', dv.serialNumber
            if PRINT_SERVICES:
                print
                for schema, types in dv.services.items():
                    print '\t', schema
                    for type, versions in types.items():
                        print '\t\t', type
                        for version, s in versions.items():
                            print '\t\t\t', version

                            print '\t\t\t\tDescribed:', s.described
                            if s.described:
                                print '\t\t\t\t\tService Type:', s.serviceType
                                print '\t\t\t\t\tService ID:', s.serviceId
                                print '\t\t\t\t\tControlURL:', s.controlURL
                                print '\t\t\t\t\tEventSubURL:', s.eventSubURL
                                print '\t\t\t\t\tSCPDURL:', s.SCPDURL
            print

    SSDP_MSearch.search(foundDevice, finishedSearching)

    reactor.run()