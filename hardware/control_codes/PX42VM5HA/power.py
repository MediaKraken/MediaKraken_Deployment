import sys
import getopt
import time
import serial

"""
NEC PX-42VM5HA Control Codes

Power
	ON			9FH 80H 60H 4EH 00H CDH
	OFF			9FH 80H 60H 4FH 00H CEH
Input Switch
	VIDEO1(BNC)		DFH 80H 60H 47H 01H 01H 08H
	VIDEO2(RCA)		DFH 80H 60H 47H 01H 02H 09H
	VIDEO2(S-Video)		DFH 80H 60H 47H 01H 03H 0AH
	DVD1/HD1(RCA/Component)	DFH 80H 60H 47H 01H 05H 0CH
	DVD2/HD2(5BNC/Compnent)	DFH 80H 60H 47H 01H 06H 0DH
	RGB1(15pin HD)		DFH 80H 60H 47H 01H 07H 0EH
	RGB2(5BNC/RGB)		DFH 80H 60H 47H 01H 08H 1FH
	RGB3(DVI)		DFH 80H 60H 47H 01H 0CH 13H
Audio Mute
	ON			9FH 80H 60H 3EH 00H BDH
	OFF			9FH 80H 60H 3FH 00H BEH
Picture Mode
	NORMAL			DFH 80H 60H 0AH 01H 01H CBH
	THEAT.1			DFH 80H 60H 0AH 01H 02H CCH
	THEAT.2			DFH 80H 60H 0AH 01H 03H CDH
	DEFAULT			DFH 80H 60H 0AH 01H 04H CEH
	BRIGHT			DFH 80H 60H 0AH 01H 05H CFH
Screen Mode
	STADIUM			DFH 80H 60H 51H 01H 02H 13H
	ZOOM			DFH 80H 60H 51H 01H 03H 14H
	NORMAL			DFH 80H 60H 51H 01H 04H 15H
	FULL			DFH 80H 60H 51H 01H 05H 16H
	2.35:1			DFH 80H 60H 51H 01H 0AH 1BH
Auto Picture
	ON			DFH 80H 60H 7FH 03H 03H 09H 00H 4DH
	OFF			DFH 80H 60H 7FH 03H 03H 09H 01H 4EH
Cinema Mode
	ON			DFH 80H 60H C1H 01H 01H 82H
	OFF			DFH 80H 60H C1H 01H 02H 83H

Communication Protocol:
	Interface: RS-232C
	Communication: Asynchronous
	Baud Rate: 9600
	Data Length: 8bits
	Parity: Odd
	Stop Bit: 1bit
	Communication Code: Hex
"""

def selectOption():
    #Power Commands
    POWERON=bytearray([0x9F,0x80,0x60,0x4E,0x00,0xCD])
    POWEROFF=bytearray([0x9F,0x80,0x60,0x4F,0x00,0xCE])
    #Input Switch Commands
    VIDEO1=bytearray([0xDF,0x80,0x60,0x47,0x01,0x01,0x08])
    VIDEO2=bytearray([0xDF,0x80,0x60,0x47,0x01,0x02,0x09])
    VIDEO3=bytearray([0xDF,0x80,0x60,0x47,0x01,0x03,0x0A])
    DVD1=bytearray([0xDF,0x80,0x60,0x47,0x01,0x05,0x0C])
    DVD2=bytearray([0xDF,0x80,0x60,0x47,0x01,0x06,0x0D])
    RGB1=bytearray([0xDF,0x80,0x60,0x47,0x01,0x07,0x0E])
    RGB2=bytearray([0xDF,0x80,0x60,0x47,0x01,0x08,0x1F])
    RGB3=bytearray([0xDF,0x80,0x60,0x47,0x01,0x0C,0x13])
    #Audio Mute Commands
    MUTEON=bytearray([0x9F,0x80,0x60,0x3E,0x00,0xBD])
    MUTEOFF=bytearray([0x9F,0x80,0x60,0x3F,0x00,0xBE])
    #Picture Mode Commands
    NORMAL=bytearray([0xDF,0x80,0x60,0x0A,0x01,0x01,0xCB])
    THEAT1=bytearray([0xDF,0x80,0x60,0x0A,0x01,0x02,0xCC])
    THEAT2=bytearray([0xDF,0x80,0x60,0x0A,0x01,0x03,0xCD])
    DEFAULT=bytearray([0xDF,0x80,0x60,0x0A,0x01,0x04,0xCE])
    BRIGHT=bytearray([0xDF,0x80,0x60,0x0A,0x01,0x05,0xCF])
    #Screen Mode Commands
    STADIUM=bytearray([0xDF,0x80,0x60,0x51,0x01,0x02,0x13])
    ZOOM=bytearray([0xDF,0x80,0x60,0x51,0x01,0x03,0x14])
    NORMAL=bytearray([0xDF,0x80,0x60,0x51,0x01,0x04,0x15])
    FULL=bytearray([0xDF,0x80,0x60,0x51,0x01,0x05,0x16])
    S235=bytearray([0xDF,0x80,0x60,0x51,0x01,0x0A,0x1B])
    #Auto Picture Commands
    AUTOON=bytearray([0xDF,0x80,0x60,0x7F,0x03,0x03,0x09,0x00,0x4D])
    AUTOOFF=bytearray([0xDF,0x80,0x60,0x7F,0x03,0x03,0x09,0x01,0x4E])
    #Cinema Mode Commands
    CINEMAON=bytearray([0xDF,0x80,0x60,0xC1,0x01,0x01,0x82])
    CINEMAOFF=bytearray([0xDF,0x80,0x60,0xC1,0x01,02,0x83])

def sendCommand(cmd):
    ser = serial.Serial(
	    port='COM1',
	    baudrate=9600,
	    parity=serial.PARITY_ODD,
	    stopbits=serial.STOPBITS_ONE,
	    bytesize=serial.EIGHTBITS
    )
    
    ser.close()
    ser.open()
    #ser.isOpen()
    ser.write(cmd)
    ser.close()


def main():
    if len(sys.argv) < 2:
        print >> sys.stderr, "Arguments missing... Please select an argument and rerun"
        #showHelp()
        sys.exit(1)
    cmdArray=selectOption()
    sendCommand(cmdArray)

if __name__ == '__main__':
    main()
