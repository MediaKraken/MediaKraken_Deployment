import sys
import getopt
import time
import serial

"""
Sharp LC-80LE632U Control Codes

        |               |                   Control Contents
Command |   Parameter   |  
-----------------------------------------------------------------------------------
Power On  Command Setting
R S P W |   0 _ _ _     |   Off             |   The Power On command rejected.
R S P W |   1 _ _ _     |   On(RS-232C)     |   The Power On command accepted.
R S P W |   2 _ _ _     |   On(IP)          |   The Power On command accepted.
                                                When the power is in standby mode,
                                                commands also go to waiting status
                                                and so power consumption is just 
                                                about the same as usual.  With the
                                                commands in waiting status, the 
                                                Center Icon Illumination on the 
                                                front of the TV lights up.

Power Setting
P O W R |   0 _ _ _     |   Power Off       |   It shits to standby.
P O W R |   1 _ _ _     |   Power On        |   Power On

Input Selection

AV Mode Selection

Volume

Position

View Mode

Mute

Surround

Audio Selection

Sleep Timer

Channel

Closed Caption(CC)
C L C P |   x _ _ _     |

Device Name
T V N M |   1 _ _ _     |

Model Name
M N R D |   1 _ _ _     |

Software Verison
S W V N |   1 _ _ _     |

IP Protocol Version
I P P V |   1 _ _ _     |

***NOTE***
-If an underbar (_) appears in the parameter column, enter a space
-If an asterisk (*) appears, enter a value in the range indicated in brackets under Control Contents
-Any numerical value can replace the "x" on the table

Communication Protocol:
	Interface: RS-232C
	Communication: Asynchronous
	Baud Rate: 9600
	Data Length: 8bits
	Parity: None
	Stop Bit: 1bit
    Flow Control: None
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
