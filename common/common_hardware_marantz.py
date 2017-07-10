'''
  Copyright (C) 2017 Quinn D Granfor <spootdev@gmail.com>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 2, as published by the Free Software Foundation.

  This program is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License version 2 for more details.

  You should have received a copy of the GNU General Public License
  version 2 along with this program; if not, write to the Free
  Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
'''

from __future__ import absolute_import, division, print_function, unicode_literals
import logging # pylint: disable=W0611
import telnetlib


class CommonHardwareMarantz(object):
    """
    Class for interfacing with Marantz equipment
    """
    def __init__(self, device_ip):
        self.device = telnetlib.Telnet(device_ip)

    def com_hardware_marantz_command(self, command_string, resp_cnt):
        command_string = command_string.encode("ascii")
        print("Sending cmd %s" % command_string)
        self.device.read_very_eager()  # clear any old stuff
        self.device.write(command_string)
        resp = []
        for r in range(resp_cnt):
            # Strip the trailing \r
            resp.append(self.device.read_until('\r', 1)[:-1])
        print("Response: ",resp)
        return resp

    def com_hardware_marantz_close(self):
        self.device.close()

    """
    Power Commands
    """

    def com_hardware_marantz_check_power(self):
        return self.com_hardware_marantz_command('PW?', 1)[0]

    def com_hardware_marantz_power_on(self):
        return self.com_hardware_marantz_command('PWON', 1)[0]

    def com_hardware_marantz_power_standby(self):
        return self.com_hardware_marantz_command('PWSTANDBY', 1)[0]

    """
    Volume Commands
    """

    def com_hardware_marantz_vol_to_db(self, vol):
        """
        Calculate DB from results
        """
        if len(vol) == 2:
            return int(vol) - 80
        # three digits means half dB steps
        return (int(vol) / 10.0) - 80

    def com_hardware_marantz_volume_get(self, in_db=True):
        if in_db:
            return self.com_hardware_marantz_vol_to_db(self.com_hardware_marantz_command('MV?\r', 2)[0][2:])
        else:
            return self.com_hardware_marantz_command('MV?\r', 2)[0][2:]

    def com_hardware_marantz_volume_set(self, volume_value):
        self.com_hardware_marantz_command(('MV%s' % volume_value), 1)

    def com_hardware_marantz_volume_up_down(self, volume_up=True):
        if volume_up:
            cmd = 'MVUP'
        else:
            cmd = 'MVDOWN'
        self.com_hardware_marantz_command(cmd, 1)

# CVFL UP<CR>
# CVFL DOWN<CR>
# CVFL 50<CR>
# CVFR UP<CR>
# CVFR DOWN<CR>
# CVFR 50<CR>
# CVC UP<CR>
# CVC DOWN<CR>
# CVC 50<CR>
# CVSW UP<CR>
# CVSW DOWN<CR>
# CVSW 50<CR>
# CVSW2 UP<CR>
# CVSW2 DOWN<CR>
# CVSW2 50<CR>
# CVSL UP<CR>
# CVSL DOWN<CR>
# CVSL 50<CR>
# CVSR UP<CR>
# CVSR DOWN<CR>
# CVSR 50<CR>
# CVSBL UP<CR>
# CVSBL DOWN<CR>
# CVSBL 50<CR>
# CVSBR UP<CR>
# CVSBR DOWN<CR>
# CVSBR 50<CR>
# CVSB UP<CR>
# CVSB DOWN<CR>
# CVSB 50<CR>
# CVFHL UP<CR>
# CVFHL DOWN<CR>
# CVFHL 50<CR>
# CVFHR UP<CR>
# CVFHR DOWN<CR>
# CVFHR 50<CR>
# CVFWL UP<CR>
# CVFWL DOWN<CR>
# CVFWL 50<CR>
# CVFWR UP<CR>
# CVFWR DOWN<CR>
# CVFWR 50<CR>
# CVTFL UP<CR>
# CVTFL DOWN<CR>
# CVTFL 50<CR>
# CVTFR UP<CR>
# CVTFR DOWN<CR>
# CVTFR 50<CR>
# CVTML UP<CR>
# CVTML DOWN<CR>
# CVTML 50<CR>
# CVTMR UP<CR>
# CVTMR DOWN<CR>
# CVTMR 50<CR>
# CVTRL UP<CR>
# CVTRL DOWN<CR>
# CVTRL 50<CR>
# CVTRR UP<CR>
# CVTRR DOWN<CR>
# CVTRR 50<CR>
# CVRHL UP<CR>
# CVRHL DOWN<CR>
# CVRHL 50<CR>
# CVRHR UP<CR>
# CVRHR DOWN<CR>
# CVRHR 50<CR>
# CVFDL UP<CR>
# CVFDL DOWN<CR>
# CVFDL 50<CR>
# CVFDR UP<CR>
# CVFDR DOWN<CR>
# CVFDR 50<CR>
# CVSDL UP<CR>
# CVSDL DOWN<CR>
# CVSDL 50<CR>
# CVSDR UP<CR>
# CVSDR DOWN<CR>
# CVSDR 50<CR>
# CVBDL UP<CR>
# CVBDL DOWN<CR>
# CVBDL 50<CR>
# CVBDR UP<CR>
# CVBDR DOWN<CR>
# CVBDR 50<CR>
# CVSHL UP<CR>
# CVSHL DOWN<CR>
# CVSHL 50<CR>
# CVSHR UP<CR>
# CVSHR DOWN<CR>
# CVSHR 50<CR>
# CVTS UP<CR>
# CVTS DOWN<CR>
# CVTS 50<CR>
# CVZRL<CR>
# CV?<CR>


    def com_hardware_marantz_mute_status(self):
        return self.com_hardware_marantz_command(('MU?'), 1)

    def com_hardware_marantz_mute_set(self, mute_status=True):
        if mute_status:
            self.com_hardware_marantz_command(('MUON'), 1)
        else:
            self.com_hardware_marantz_command(('MUOFF'), 1)

    """
    Input Settings Commands
    """
    # Input
        # SIPHONO < CR >
        # SICD < CR >
        # SIDVD < CR >
        # SIBD < CR >
        # SITV < CR >
        # SISAT/CBL < CR >
        # SIMPLAY < CR >
        # SIGAME < CR >
        # SITUNER < CR >  @4: Europe/Japan/China model Only)
        # SIHDRADIO < CR >@3: North America model Only)
        # SISIRIUSXM < CR >@3: North America model Only)
        # SIPANDORA < CR >@3: North America model Only)
        # SIIRADIO < CR >
        # SISERVER < CR >
        # SIFAVORITES < CR >
        # SIAUX1 < CR >
        # SIAUX2 < CR >
        # SIAUX3 < CR >
        # SIAUX4 < CR >
        # SIAUX5 < CR >
        # SIAUX6 < CR >
        # SIAUX7 < CR >
        # SINET < CR >
        # SIBT < CR >
        # SIMXPORT < CR >
        # SIUSB/IPOD < CR >
        # SIUSB < CR >
        # SIIPD < CR >
        # SIIRP < CR >
        # SIFVP < CR >

    def com_hardware_marantz_input_status(self):
        return self.com_hardware_marantz_command(('SI?'), 1)

    # Smart Select
# MSSMART1<CR>
# MSSMART2<CR>
# MSSMART3<CR>
# MSSMART4<CR>
# MSSMART5<CR>
# MSSMART1 MEMORY<CR>
# MSSMART2 MEMORY<CR>
# MSSMART3 MEMORY<CR>
# MSSMART4 MEMORY<CR>
# MSSMART5 MEMORY<CR>
# MSSMART ?<CR>
    # Audio input signal
# SDAUTO<CR>
# SDHDMI<CR>
# SDDIGITAL<CR>
# SDANALOG<CR>
# SD7.1IN<CR>
# SDNO<CR>

    def com_hardware_marantz_audio_input_status(self):
        return self.com_hardware_marantz_command(('SD?'), 1)

    # Video signal
# DCDTS<CR>
# DC?
# SVDVD<CR>
# SVBD<CR>
# SVTV<CR>
# SVSAT/CBL<CR>
# SVMPLAY<CR>
# SVGAME<CR>
# SVAUX1<CR>
# SVAUX2<CR>
# SVCD<CR>
# SVON<CR>
# SVOFF<CR>

    def com_hardware_marantz_video_input_select_status(self):
        return self.com_hardware_marantz_command(('SV?'), 1)

    # Auto standby
# STBY15M<CR>
# STBY30M<CR>
# STBY60M<CR>
# STBYOFF<CR>
# STBY?<CR>
    # ECO
# ECOON<CR>
# ECOAUTO<CR>
# ECOOFF<CR>
# ECO?<CR>
    # Sleep
# SLPOFF<CR>
# SLP***<CR>
# SLP?<CR>
    # Surround mode
# MSMOVIE<CR>
# MSMUSIC<CR>
# MSGAME<CR>
# MSDIRECT<CR>
# MSPURE DIRECT<CR>
# MSSTEREO<CR>
# MSAUTO<CR>
# MSDOLBY DIGITAL<CR>
# MSDTS SURROUND<CR>
# MSAURO3D<CR>  # upgrade only
# MSAURO2DSURR<CR> # upgrade only
# MSMCH STEREO<CR>
# MSVIRTUAL<CR>
# MSLEFT<CR>
# MSRIGHT<CR>
    def com_hardware_marantz_surround_mode_status(self):
        return self.com_hardware_marantz_command(('MS?'), 1)

    # Aspect
# VSASPNRM<CR>
# VSASPFUL<CR>
    def com_hardware_marantz_aspect_ratio_status(self):
        return self.com_hardware_marantz_command(('VSASP ?'), 1)

    # HDMI Out (auto detect)
# VSMONIAUTO<CR>
# VSMONI1<CR>
# VSMONI2<CR>
    def com_hardware_marantz_hdmi_auto_status(self):
        return self.com_hardware_marantz_command(('VSMONI ?'), 1)

        # HDMI Output
# VSSC48P<CR>
# VSSC10I<CR>
# VSSC72P<CR>
# VSSC10P<CR>
# VSSC10P24<CR>
# VSSC4K<CR>
# VSSC4KF<CR>
# VSSCAUTO<CR>
    def com_hardware_marantz_hdmi_output_status(self):
        return self.com_hardware_marantz_command(('VSSC ?'), 1)

        # HDMI Resolution
# VSSCH48P<CR>
# VSSCH10I<CR>
# VSSCH72P<CR>
# VSSCH10P<CR>
# VSSCH10P24<CR>
# VSSCH4K<CR>
# VSSCH4KF<CR>
# VSSCHAUTO<CR>
    def com_hardware_marantz_hdmi_resolution_status(self):
        return self.com_hardware_marantz_command(('VSSCH ?'), 1)

    # Vertical Stretch
# VSVST ON<CR>
# VSVST OFF<CR>
    def com_hardware_marantz_vertical_stretch_status(self):
        return self.com_hardware_marantz_command(('VSVST ?'), 1)

        # HDMI Audio Decode
# VSAUDIO AMP<CR>
# VSAUDIO TV<CR>
# VSAUDIO ?<CR>
    # Video Process
# VSVPMAUTO<CR>
# VSVPMGAME<CR>
# VSVPMMOVI<CR>
# VSVPM ?<CR>

    # Speaker a/b
# PSFRONT SPA<CR>
# PSFRONT SPB<CR>
# PSFRONT A+B<CR>
# PSFRONT?<CR>
    # Effect speaker selection
# PSSP:FL<CR>
# PSSP:HF<CR>
# PSSP:FR<CR>
# PSSP: ?<CR>
# PSFH:ON<CR>
# PSFH:OFF<CR>
# PSFH: ?<CR>
    # Subwoofer
# PSSWR ON<CR>
# PSSWR OFF<CR>
# PSSWR ?<CR>
    # Tone
# PSTONE CTRL ON<CR>
# PSTONE CTRL OFF<CR>
# PSTONE CTRL ?<CR>
    # Bass
# PSBAS UP<CR>
# PSBAS DOWN<CR>
# PSBAS 50<CR>
# PSBAS ?<CR>
    # Treble
# PSTRE UP<CR>
# PSTRE DOWN<CR>
# PSTRE 50<CR>
# PSTRE ?<CR>
    # Loudness management
# PSLOM ON<CR>
# PSLOM OFF<CR>
# PSLOM ?<CR>
    # Subwoofer level
# PSSWL ON<CR
# PSSWL OFF<CR
# PSSWL UP<CR>
# PSSWL DOWN<CR>
# PSSWL 50<CR>
# PSSWL2 UP<CR>
# PSSWL2 DOWN<CR>
# PSSWL2 50<CR>
# PSSWL ?<CR>
    # Dialog Level
# PSDIL ON<CR>
# PSDIL OFF<CR>
# PSDIL UP<CR>
# PSDIL DOWN<CR>
# PSDIL 50<CR>
# PSDIL ?<CR>
    # LFE
# PSLEE UP<CR>
# PSLFE DOWN<CR>
# PSLFE 10<CR>
# PSLFE ?<CR>
    # LFE in 7.1 mode
# PSLFL 00<CR>
# PSLFL 05<CR>
# PSLFL 10<CR>
# PSLFL 15<CR>
# PSLFL ?<CR>
    # Center Spread
# PSCES ON<CR>
# PSCES OFF<CR>
# PSCES ?<CR>
    # Dialog control
# PSDIC UP<CR>
# PSDIC DOWN<CR>
# PSDIC 03<CR>
# PSDIC ?<CR>
    # Neural:X
# PSNEURAL ON<CR>
# PSNEURAL OFF<CR>
# PSNEURAL ?<CR>
    # Cinema EQ
# PSCINEMA
# EQ.ON < CR >
# PSCINEMA
# EQ.OFF < CR >
# PSCINEMA
# EQ. ? < CR >
    # MultEQ
# PSMULTEQ:AUDYSSEY < CR >
# PSMULTEQ:BYP.LR < CR >
# PSMULTEQ:FLAT < CR >
# PSMULTEQ:OFF < CR >
# PSMULTEQ: ? < CR >
    # Dynamic EQ
# PSDYNEQ
# ON < CR >
# PSDYNEQ
# OFF < CR >
# PSDYNEQ ? < CR >
# PSREFLEV
# 0 < CR >
# PSREFLEV
# 5 < CR >
# PSREFLEV
# 10 < CR >
# PSREFLEV
# 15 < CR >
# PSREFLEV ? < CR >
    # Dynamic Vol.
# PSDYNVOL
# HEV < CR >
# PSDYNVOL
# MED < CR >
# PSDYNVOL
# LIT < CR >
# PSDYNVOL
# OFF < CR >
# PSDYNVOL ? < CR >
    # Audyssey LFC
# PSLFC
# ON < CR >
# PSLFC
# OFF < CR >
# PSLFC ? < CR >
# PSCNTAMT
# UP < CR >
# PSCNTAMT
# DOWN < CR >
# PSCNTAMT
# 07 < CR >
# PSCNTAMT ? < CR >
    # Graphic EQ
# PSGEQ
# ON < CR >
# PSGEQ
# OFF < CR >
# PSGEQ ? < CR >
    # Headphone EQ
# PSHEQ
# ON < CR >
# PSHEQ
# OFF < CR >
# PSHEQ ? < CR >
    # DRC
# PSDRC
# AUTO < CR >
# PSDRC
# LOW < CR >
# PSDRC
# MID < CR >
# PSDRC
# HI < CR >
# PSDRC
# OFF < CR >
# PSDRC ? < CR >
    # M-DAX
# PSMDAX
# OFF < CR >
# PSMDAX
# LOW < CR >
# PSMDAX
# MID < CR >
# PSMDAX
# HI < CR >
# PSMDAX ? < CR >
    # Audio Delay
# PSDELAY
# UP < CR >
# PSDELAY
# DOWN < CR >
# PSDELAY
# 200 < CR >
# PSDELAY ? < CR >
    # Auro-Matic 3D Preset
# PSAUROPR
# SMA < CR >
# PSAUROPR
# MED < CR >
# PSAUROPR
# LAR < CR >
# PSAUROPR
# SPE < CR >
# PSAUROPR ? < CR >
    """
    Video Settings
    """
    # Auro-Matic 3D Strength
# PSAUROST
# UP < CR >
# PSAUROST
# DOWN < CR >
# PSAUROST
# 10 < CR >
# PSAUROST ? < CR >
    # picture mode
# PVOFF < CR >
# PVSTD < CR >
# PVMOV < CR >
# PVVVD < CR >
# PVSTM < CR >
# PVCTM < CR >
# PVDAY < CR >
# PVNGT < CR >
    def com_hardware_marantz_picture_mode_status(self):
        return self.com_hardware_marantz_command(('PV?'), 1)

# testing against AV7703

# connect test
teststuff = CommonHardwareMarantz('10.0.0.209')

print(teststuff.com_hardware_marantz_picture_mode_status())

# connect close
teststuff.com_hardware_marantz_close()
