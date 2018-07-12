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

import telnetlib


class CommonHardwareMarantz(object):
    """
    Class for interfacing with Marantz equipment over network connection
    """

    def __init__(self, device_ip):
        self.device = telnetlib.Telnet(device_ip)

    def com_hardware_command(self, command_string, resp_cnt):
        command_string = command_string.encode("ascii")
        print(("Sending cmd %s" % command_string))
        self.device.read_very_eager()  # clear any old stuff
        self.device.write(command_string)
        resp = []
        for r in range(resp_cnt):
            # Strip the trailing \r
            resp.append(self.device.read_until('\r', 1)[:-1])
        print(("Response: ", resp))
        return resp

    def com_hardware_close(self):
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
            return self.com_hardware_marantz_vol_to_db(
                self.com_hardware_marantz_command('MV?\r', 2)[0][2:])
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
    def com_hardware_marantz_smart_select_smart1(self):
        return self.com_hardware_marantz_command(('MSSMART1'), 1)

    def com_hardware_marantz_smart_select_smart2(self):
        return self.com_hardware_marantz_command(('MSSMART2'), 1)

    def com_hardware_marantz_smart_select_smart3(self):
        return self.com_hardware_marantz_command(('MSSMART3'), 1)

    def com_hardware_marantz_smart_select_smart4(self):
        return self.com_hardware_marantz_command(('MSSMART4'), 1)

    def com_hardware_marantz_smart_select_smart5(self):
        return self.com_hardware_marantz_command(('MSSMART5'), 1)

    def com_hardware_marantz_smart_select_smart1_memory(self):
        return self.com_hardware_marantz_command(('MSSMART1 MEMORY'), 1)

    def com_hardware_marantz_smart_select_smart2_memory(self):
        return self.com_hardware_marantz_command(('MSSMART2 MEMORY'), 1)

    def com_hardware_marantz_smart_select_smart3_memory(self):
        return self.com_hardware_marantz_command(('MSSMART3 MEMORY'), 1)

    def com_hardware_marantz_smart_select_smart4_memory(self):
        return self.com_hardware_marantz_command(('MSSMART4 MEMORY'), 1)

    def com_hardware_marantz_smart_select_smart5_memory(self):
        return self.com_hardware_marantz_command(('MSSMART5 MEMORY'), 1)

    def com_hardware_marantz_smart_select_status(self):
        return self.com_hardware_marantz_command(('MSSMART ?'), 1)

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
    def com_hardware_marantz_video_standby_15m(self):
        return self.com_hardware_marantz_command(('STBY15M'), 1)

    def com_hardware_marantz_video_standby_30m(self):
        return self.com_hardware_marantz_command(('STBY30M'), 1)

    def com_hardware_marantz_video_standby_60m(self):
        return self.com_hardware_marantz_command(('STBY60M'), 1)

    def com_hardware_marantz_video_standby_off(self):
        return self.com_hardware_marantz_command(('STBYOFF'), 1)

    def com_hardware_marantz_video_standy_status(self):
        return self.com_hardware_marantz_command(('STBY?'), 1)

    # ECO
    def com_hardware_marantz_video_eco_on(self):
        return self.com_hardware_marantz_command(('ECOON'), 1)

    def com_hardware_marantz_video_eco_auto(self):
        return self.com_hardware_marantz_command(('ECOAUTO'), 1)

    def com_hardware_marantz_video_eco_off(self):
        return self.com_hardware_marantz_command(('ECOOFF'), 1)

    def com_hardware_marantz_video_eco_status(self):
        return self.com_hardware_marantz_command(('ECO?'), 1)

    # Sleep
    # SLPOFF<CR>
    # SLP***<CR>

    def com_hardware_marantz_video_sleep_status(self):
        return self.com_hardware_marantz_command(('SLP?'), 1)

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
    def com_hardware_marantz_hdmi_out_auto(self):
        return self.com_hardware_marantz_command(('VSMONIAUTO'), 1)

    def com_hardware_marantz_hdmi_out_monitor1(self):
        return self.com_hardware_marantz_command(('VSMONI1'), 1)

    def com_hardware_marantz_hdmi_out_monitor2(self):
        return self.com_hardware_marantz_command(('VSMONI2'), 1)

    def com_hardware_marantz_hdmi_out_status(self):
        return self.com_hardware_marantz_command(('VSMONI ?'), 1)

    # HDMI Output
    def com_hardware_marantz_hdmi_output_480p(self):
        return self.com_hardware_marantz_command(('VSSC48P'), 1)

    def com_hardware_marantz_hdmi_output_720p(self):
        return self.com_hardware_marantz_command(('VSSC72P'), 1)

    def com_hardware_marantz_hdmi_output_1080i(self):
        return self.com_hardware_marantz_command(('VSSC10I'), 1)

    def com_hardware_marantz_hdmi_output_1080p(self):
        return self.com_hardware_marantz_command(('VSSC10P'), 1)

    def com_hardware_marantz_hdmi_output_1080p24(self):
        return self.com_hardware_marantz_command(('VSSC10P24'), 1)

    def com_hardware_marantz_hdmi_output_4k(self):
        return self.com_hardware_marantz_command(('VSSC4K'), 1)

    def com_hardware_marantz_hdmi_output_4kf(self):
        return self.com_hardware_marantz_command(('VSSC4KF'), 1)

    def com_hardware_marantz_hdmi_output_auto(self):
        return self.com_hardware_marantz_command(('VSSCAUTO'), 1)

    def com_hardware_marantz_hdmi_output_status(self):
        return self.com_hardware_marantz_command(('VSSC ?'), 1)

    # HDMI Resolution
    def com_hardware_marantz_hdmi_resolution_480p(self):
        return self.com_hardware_marantz_command(('VSSCH48P'), 1)

    def com_hardware_marantz_hdmi_resolution_720p(self):
        return self.com_hardware_marantz_command(('VSSCH72P'), 1)

    def com_hardware_marantz_hdmi_resolution_1080i(self):
        return self.com_hardware_marantz_command(('VSSCH10I'), 1)

    def com_hardware_marantz_hdmi_resolution_1080p(self):
        return self.com_hardware_marantz_command(('VSSCH10P'), 1)

    def com_hardware_marantz_hdmi_resolution_1080p24(self):
        return self.com_hardware_marantz_command(('VSSCH10P24'), 1)

    def com_hardware_marantz_hdmi_resolution_4k(self):
        return self.com_hardware_marantz_command(('VSSCH4K'), 1)

    def com_hardware_marantz_hdmi_resolution_4kf(self):
        return self.com_hardware_marantz_command(('VSSCH4KF'), 1)

    def com_hardware_marantz_hdmi_resolution_auto(self):
        return self.com_hardware_marantz_command(('VSSCHAUTO'), 1)

    def com_hardware_marantz_hdmi_resolution_status(self):
        return self.com_hardware_marantz_command(('VSSCH ?'), 1)

    # Vertical Stretch
    def com_hardware_marantz_vertical_stretch_on(self):
        return self.com_hardware_marantz_command(('VSVST ON'), 1)

    def com_hardware_marantz_vertical_stretch_off(self):
        return self.com_hardware_marantz_command(('VSVST OFF'), 1)

    def com_hardware_marantz_vertical_stretch_status(self):
        return self.com_hardware_marantz_command(('VSVST ?'), 1)

    # HDMI Audio Decode
    def com_hardware_marantz_hdmi_audio_decode_amp(self):
        return self.com_hardware_marantz_command(('VSAUDIO AMP'), 1)

    def com_hardware_marantz_hdmi_audio_decode_tv(self):
        return self.com_hardware_marantz_command(('VSAUDIO TV'), 1)

    def com_hardware_marantz_hdmi_audio_decode_status(self):
        return self.com_hardware_marantz_command(('VSAUDIO ?'), 1)

    # Video Process
    def com_hardware_marantz_video_process_auto(self):
        return self.com_hardware_marantz_command(('VSVPMAUTO'), 1)

    def com_hardware_marantz_video_process_game(self):
        return self.com_hardware_marantz_command(('VSVPMGAME'), 1)

    def com_hardware_marantz_video_process_movie(self):
        return self.com_hardware_marantz_command(('VSVPMMOVI'), 1)

    def com_hardware_marantz_video_process_status(self):
        return self.com_hardware_marantz_command(('VSVPM ?'), 1)

    # Speaker a/b
    def com_hardware_marantz_spk_a(self):
        return self.com_hardware_marantz_command(('PSFRONT SPA'), 1)

    def com_hardware_marantz_spk_b(self):
        return self.com_hardware_marantz_command(('PSFRONT SPB'), 1)

    def com_hardware_marantz_spk_ab(self):
        return self.com_hardware_marantz_command(('PSFRONT A+B'), 1)

    def com_hardware_marantz_spk_ab_status(self):
        return self.com_hardware_marantz_command(('PSFRONT?'), 1)

        # Effect speaker selection

    # PSSP:FL<CR>
    # PSSP:HF<CR>
    # PSSP:FR<CR>
    # PSSP: ?<CR>
    # PSFH:ON<CR>
    # PSFH:OFF<CR>

    def com_hardware_marantz_spk_effect_fh_status(self):
        return self.com_hardware_marantz_command(('PSFH ?'), 1)

    # Subwoofer
    def com_hardware_marantz_spk_effect_sub_on(self):
        return self.com_hardware_marantz_command(('PSSWR ON'), 1)

    def com_hardware_marantz_spk_effect_sub_off(self):
        return self.com_hardware_marantz_command(('PSSWR OFF'), 1)

    def com_hardware_marantz_spk_effect_sub_status(self):
        return self.com_hardware_marantz_command(('PSSWR ?'), 1)

    # Tone
    def com_hardware_marantz_spk_effect_tone_on(self):
        return self.com_hardware_marantz_command(('PSTONE CTRL ON'), 1)

    def com_hardware_marantz_spk_effect_tone_off(self):
        return self.com_hardware_marantz_command(('PSTONE CTRL OFF'), 1)

    def com_hardware_marantz_spk_effect_tone_status(self):
        return self.com_hardware_marantz_command(('PSTONE CTRL ?'), 1)

    # Bass
    def com_hardware_marantz_spk_effect_bass_up(self):
        return self.com_hardware_marantz_command(('PSBAS UP'), 1)

    def com_hardware_marantz_spk_effect_bass_down(self):
        return self.com_hardware_marantz_command(('PSBAS DOWN'), 1)

    # PSBAS 50<CR>

    def com_hardware_marantz_spk_effect_bass_status(self):
        return self.com_hardware_marantz_command(('PSBAS ?'), 1)

    # Treble
    def com_hardware_marantz_spk_effect_treble_up(self):
        return self.com_hardware_marantz_command(('PSTRE UP'), 1)

    def com_hardware_marantz_spk_effect_treble_down(self):
        return self.com_hardware_marantz_command(('PSTRE DOWN'), 1)

    # PSTRE 50<CR>

    def com_hardware_marantz_spk_effect_treble_status(self):
        return self.com_hardware_marantz_command(('PSTRE ?'), 1)

    # Loudness management
    def com_hardware_marantz_spk_effect_loudness_on(self):
        return self.com_hardware_marantz_command(('PSLOM ON'), 1)

    def com_hardware_marantz_spk_effect_loudness_off(self):
        return self.com_hardware_marantz_command(('PSLOM OFF'), 1)

    def com_hardware_marantz_spk_effect_loudness_status(self):
        return self.com_hardware_marantz_command(('PSLOM ?'), 1)

    # Subwoofer level
    def com_hardware_marantz_spk_effect_sub_level_on(self):
        return self.com_hardware_marantz_command(('PSSWL ON'), 1)

    def com_hardware_marantz_spk_effect_sub_level_off(self):
        return self.com_hardware_marantz_command(('PSSWL OFF'), 1)

    # PSSWL UP<CR>
    # PSSWL DOWN<CR>
    # PSSWL 50<CR>
    # PSSWL2 UP<CR>
    # PSSWL2 DOWN<CR>
    # PSSWL2 50<CR>
    # PSSWL ?<CR>

    # Dialog Level
    def com_hardware_marantz_spk_effect_dialog_level_on(self):
        return self.com_hardware_marantz_command(('PSDIL ON'), 1)

    def com_hardware_marantz_spk_effect_dialog_level_off(self):
        return self.com_hardware_marantz_command(('PSDIL OFF'), 1)

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
    # PSCINEMA EQ.ON < CR >
    # PSCINEMA EQ.OFF < CR >
    # PSCINEMA EQ. ? < CR >
    # MultEQ
    # PSMULTEQ:AUDYSSEY < CR >
    # PSMULTEQ:BYP.LR < CR >
    # PSMULTEQ:FLAT < CR >
    # PSMULTEQ:OFF < CR >
    # PSMULTEQ: ? < CR >
    # Dynamic EQ
    # PSDYNEQ ON < CR >
    # PSDYNEQ OFF < CR >
    # PSDYNEQ ? < CR >
    # PSREFLEV 0 < CR >
    # PSREFLEV 5 < CR >
    # PSREFLEV 10 < CR >
    # PSREFLEV 15 < CR >
    # PSREFLEV ? < CR >
    # Dynamic Vol.
    # PSDYNVOL HEV < CR >
    # PSDYNVOL MED < CR >
    # PSDYNVOL LIT < CR >
    # PSDYNVOL OFF < CR >
    # PSDYNVOL ? < CR >
    # Audyssey LFC
    # PSLFC ON < CR >
    # PSLFC OFF < CR >
    # PSLFC ? < CR >
    # PSCNTAMT UP < CR >
    # PSCNTAMT DOWN < CR >
    # PSCNTAMT 07 < CR >
    # PSCNTAMT ? < CR >
    # Graphic EQ
    # PSGEQ ON < CR >
    # PSGEQ OFF < CR >
    # PSGEQ ? < CR >
    # Headphone EQ
    # PSHEQ ON < CR >
    # PSHEQ OFF < CR >
    # PSHEQ ? < CR >
    # DRC
    # PSDRC AUTO < CR >
    # PSDRC LOW < CR >
    # PSDRC MID < CR >
    # PSDRC HI < CR >
    # PSDRC OFF < CR >
    # PSDRC ? < CR >
    # M-DAX
    # PSMDAX OFF < CR >
    # PSMDAX LOW < CR >
    # PSMDAX MID < CR >
    # PSMDAX HI < CR >
    # PSMDAX ? < CR >
    # Audio Delay
    # PSDELAY UP < CR >
    # PSDELAY DOWN < CR >
    # PSDELAY 200 < CR >
    # PSDELAY ? < CR >
    # Auro-Matic 3D Preset
    # PSAUROPR SMA < CR >
    # PSAUROPR MED < CR >
    # PSAUROPR LAR < CR >
    # PSAUROPR SPE < CR >
    # PSAUROPR ? < CR >
    """
    Video Settings
    """

    # Auro-Matic 3D Strength
    # PSAUROST UP < CR >
    # PSAUROST DOWN < CR >
    # PSAUROST 10 < CR >
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

print((teststuff.com_hardware_marantz_picture_mode_status()))

# connect close
teststuff.com_hardware_marantz_close()
