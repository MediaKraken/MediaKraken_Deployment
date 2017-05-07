// license:BSD-3-Clause
// copyright-holders:Aaron Giles
/***************************************************************************

    Gottlieb hardware

***************************************************************************/

#include "cpu/m6502/m6502.h"
#include "machine/mos6530.h"
#include "machine/6532riot.h"
#include "sound/ay8910.h"
#include "sound/sp0250.h"
#include "sound/votrax.h"


//**************************************************************************
//  GLOBAL VARIABLES
//**************************************************************************

extern const device_type GOTTLIEB_SOUND_REV0;
extern const device_type GOTTLIEB_SOUND_REV1;
extern const device_type GOTTLIEB_SOUND_REV1_WITH_VOTRAX;
extern const device_type GOTTLIEB_SOUND_REV2;



//**************************************************************************
//  DEVICE CONFIGURATION MACROS
//**************************************************************************

#define MCFG_GOTTLIEB_ENABLE_COBRAM3_MODS() \
	gottlieb_sound_r2_device::static_enable_cobram3_mods(*device);


//**************************************************************************
//  TYPE DEFINITIONS
//**************************************************************************

// ======================> gottlieb_sound_r0_device

// rev 0 sound board
class gottlieb_sound_r0_device : public device_t, public device_mixer_interface
{
public:
	// construction/destruction
	gottlieb_sound_r0_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);

	// read/write
	DECLARE_WRITE8_MEMBER( write );

	// internal communications
	DECLARE_READ8_MEMBER( r6530b_r );
	DECLARE_INPUT_CHANGED_MEMBER(audio_nmi);

protected:
	// device-level overrides
	virtual machine_config_constructor device_mconfig_additions() const override;
	virtual ioport_constructor device_input_ports() const override;
	virtual void device_start() override;

private:
	// devices
	required_device<m6502_device>       m_audiocpu;
	required_device<mos6530_device>     m_r6530;

	uint8_t m_sndcmd;
};

// ======================> gottlieb_sound_r1_device

// rev 1 sound board, with unpopulated VOTRAX
class gottlieb_sound_r1_device : public device_t, public device_mixer_interface
{
public:
	// construction/destruction
	gottlieb_sound_r1_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);

	// read/write
	DECLARE_WRITE8_MEMBER( write );

	// internal communications
	DECLARE_WRITE_LINE_MEMBER( snd_interrupt );
	DECLARE_WRITE8_MEMBER( r6532_portb_w );
	DECLARE_WRITE8_MEMBER( votrax_data_w );
	DECLARE_WRITE8_MEMBER( speech_clock_dac_w );
	DECLARE_WRITE_LINE_MEMBER( votrax_request );

protected:
	gottlieb_sound_r1_device(
			const machine_config &mconfig,
			device_type type,
			const char *name,
			const char *tag,
			device_t *owner,
			uint32_t clock,
			const char *shortname,
			const char *source);

	// device-level overrides
	virtual machine_config_constructor device_mconfig_additions() const override;
	virtual ioport_constructor device_input_ports() const override;
	virtual void device_start() override;

private:
	// devices
	required_device<m6502_device>       m_audiocpu;
	required_device<riot6532_device>    m_riot;
	optional_device<votrax_sc01_device> m_votrax;

	// internal state
	//bool            m_populate_votrax;
	uint8_t           m_last_speech_clock;
};

// fully populated rev 1 sound board
class gottlieb_sound_r1_with_votrax_device : public gottlieb_sound_r1_device
{
public:
	// construction/destruction
	gottlieb_sound_r1_with_votrax_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);

protected:
	// device-level overrides
	virtual machine_config_constructor device_mconfig_additions() const override;
	virtual ioport_constructor device_input_ports() const override;
};


// ======================> gottlieb_sound_r2_device

// fully populated rev 2 sound board
class gottlieb_sound_r2_device : public device_t, public device_mixer_interface
{
public:
	// construction/destruction
	gottlieb_sound_r2_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);

	// static configuration helpers
	static void static_enable_cobram3_mods(device_t &device);

	// read/write
	DECLARE_WRITE8_MEMBER( write );

	// internal communications
	DECLARE_READ8_MEMBER( speech_data_r );
	DECLARE_READ8_MEMBER( audio_data_r );
	DECLARE_WRITE8_MEMBER( signal_audio_nmi_w );
	DECLARE_WRITE8_MEMBER( nmi_rate_w );
	CUSTOM_INPUT_MEMBER( speech_drq_custom_r );
	DECLARE_WRITE8_MEMBER( speech_control_w );
	DECLARE_WRITE8_MEMBER( sp0250_latch_w );
	DECLARE_WRITE8_MEMBER( psg_latch_w );

protected:
	// device-level overrides
	virtual machine_config_constructor device_mconfig_additions() const override;
	virtual ioport_constructor device_input_ports() const override;
	virtual void device_start() override;
	virtual void device_timer(emu_timer &timer, device_timer_id id, int param, void *ptr) override;

private:
	// internal helpers
	void nmi_timer_adjust();
	void nmi_state_update();

	// timer IDs
	enum
	{
		TID_NMI_GENERATE,
		TID_NMI_CLEAR,
		TID_SOUND_LATCH_WRITE
	};

	// devices
	required_device<m6502_device>   m_audiocpu;
	required_device<m6502_device>   m_speechcpu;
	required_device<ay8913_device>  m_ay1;
	required_device<ay8913_device>  m_ay2;
	optional_device<sp0250_device>  m_sp0250;

	// internal state
	bool        m_cobram3_mod;
	emu_timer * m_nmi_timer;
	uint8_t       m_nmi_rate;
	uint8_t       m_nmi_state;
	uint8_t       m_audiocpu_latch;
	uint8_t       m_speechcpu_latch;
	uint8_t       m_speech_control;
	uint8_t       m_last_command;
	uint8_t       m_psg_latch;
	uint8_t       m_psg_data_latch;
	uint8_t       m_sp0250_latch;
};

