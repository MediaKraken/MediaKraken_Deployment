#
# A tool for converting Pronto format hex codes to lircd.conf format. Version 1.11
#
# Version History:
#       1.11 - Made more resiliant against whitespace imperfections in input files
#       1.1  - Added support for CCFTools/CCFDecompiler XML files and multiple devices
#       1.0  - Initial release
#
# Copyright by Olavi Akerman <olavi.akerman@gmail.com>
#
# pronto2lirc is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#

import string,xml

class CodeSequence:           # Handles codesequences parsing and conversion
    def ProcessPreamble(self,sPreamble):
        if sPreamble[0]<>"0000":
            raise "Formats other than starting with 0000 are not supported!"
        self.dIRFrequency=1000000/(long(sPreamble[1],16) * 0.241246) # Frequency of the IR carrier in Khz
        self.lOnceSequenceLength=long(sPreamble[2],16)          # No of pulses that is sent once when button is pressed
        self.lRepeatableSequenceLength=long(sPreamble[3],16)    # No of pulses that are repeatable while button pressed

    def CreatePulses(self,sItems):
        self.dPulseWidths=[]             # Table of Pulse widths. Length is repsented in microseconds
        for i in sItems:
            self.dPulseWidths.append(1000000*long(i,16)/self.dIRFrequency) # Convert pulse widths to uS
        if len(self.dPulseWidths)<>2*(self.lOnceSequenceLength+self.lRepeatableSequenceLength):
            raise "Number of actual codes does not match the header information!"

    def AnalyzeCode(self,sCodeName,sHexCodes):
        # sHexTable=sHexCodes.split()
        s=string.join(sHexCodes.split(),'') # Remove whitespace formatting between sequences
        sHexTable=[]
        while s<>'':                        # Re-split into group of 4
            sHexTable.append(s[:4])
            s=s[4:]
        self.sCodeName=sCodeName.rstrip()  # Name of the Code associated with code sequence
        self.ProcessPreamble(sHexTable[:4]) # First four sequences make up Preamble
        self.CreatePulses(sHexTable[4:])    # The rest are OnceSequence + RepeatableSequence
        return self.dPulseWidths[-1]        # Final gap=last off signal length

    def WriteCodeSection(self,fOut):
        fOut.write('\n\t\t\tname '+self.sCodeName.strip().replace(' ','')+'\n')  # Can't contain whitespace
        for i in range(len(self.dPulseWidths)-1):   # Do not write the last signal as lircd.conf
                                                    # does not contain last off signal length
            if (i%6) ==0:
                fOut.write('\t\t\t\t')
            fOut.write('%d ' % round(self.dPulseWidths[i]))
            if (i+1)%6 ==0:      # Group codes as six per line
                fOut.write('\n')
        fOut.write('\n')          # Final EOL

class Device:   # Handles devices
    def AddCodes(self,sCodeName,sHexCodes):  # Add new code sequence
        seq=CodeSequence()
        finalgap=seq.AnalyzeCode(sCodeName,sHexCodes)
        if finalgap>self.lGap:
            self.lGap=finalgap
        self.sCodes.append(seq)

    def ProcessHEX(self,fHexFile,sLine):    # Process HEX files
        while sLine<>'' and sLine.strip()<>'':   # EOF?
            [sCodeName,sHexCodes]=sLine.split(':')
            self.AddCodes(sCodeName,sHexCodes)
            sLine=fHexFile.readline()

    def WriteLIRCCConfDevice(self,f):
        f.write('begin remote\n')
        f.write('\tname\t'+self.sDeviceName.replace(' ','')+'\n')
        f.write('\tflags\tRAW_CODES\n')
        f.write('\teps\t30\n')
        f.write('\taeps\t100\n')
        f.write('\tgap\t%d\n' % self.lGap )
        f.write('\t\tbegin raw_codes\n')
        for i in self.sCodes:
            i.WriteCodeSection(f)
        f.write('\t\tend raw_codes\n')
        f.write('end remote\n')

    def __init__(self,sDeviceName):
        self.sDeviceName=sDeviceName    # Name of the device
        self.sCodes=[]                  # Codes contained in file
        self.lGap=0                     # Final Gap

class RemoteFilesParser:
    def ProcessXML(self,fXMLFile):
        def start_element(name,attrs):
            if name=="RAWCODE":
                self.Devices[-1].AddCodes(attrs['name'],attrs['data'])
            if name=="DEVICE":
                self.Devices.append(Device(attrs['name']))

        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = start_element
        fXMLFile.seek(0)        # Need to start from the beginning
        p.ParseFile(fXMLFile)

    def __init__(self,sFileName):
        self.Devices=[]
        f=open(sFileName,'r')
        sLine=f.readline()
        if sLine.strip()=='<?xml version="1.0"?>':   # Are we dealing with CCF Decompiler XML file?
            self.ProcessXML(f)
        else:
            device=Device(sFileName.split('.')[:1][0])
            self.Devices.append(device)
            device.ProcessHEX(f,sLine)
        f.close()

    def WriteLIRCConf(self,sOutFileName):
        f=open(sOutFileName,'w')
        for d in self.Devices:
            d.WriteLIRCCConfDevice(f)
        f.close()
