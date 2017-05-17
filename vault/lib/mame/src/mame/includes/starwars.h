// license:BSD-3-Clause
// copyright-holders:Steve Baines, Frank Palazzolo
/***************************************************************************

    Atari Star Wars hardware

***************************************************************************/

#include "machine/6532riot.h"
#include "includes/slapstic.h"


class starwars_state : public driver_device
{
public:
	starwars_state(const machine_config &mconfig, device_type type, const char *tag)
		: driver_device(mconfig, type, tag),
		m_riot(*this, "riot"),
		m_mathram(*this, "mathram"),
		m_maincpu(*this, "maincpu"),
		m_audiocpu(*this, "audiocpu"),
		m_slapstic_device(*this, "slapstic")
		{ }

	uint8_t m_sound_data;
	uint8_t m_main_data;
	required_device<riot6532_device> m_riot;
	uint8_t *m_slapstic_source;
	uint8_t *m_slapstic_base;
	uint8_t m_slapstic_current_bank;
	uint8_t m_is_esb;
	required_shared_ptr<uint8_t> m_mathram;
	uint8_t m_control_num;
	int m_MPA;
	int m_BIC;
	uint16_t m_dvd_shift;
	uint16_t m_quotient_shift;
	uint16_t m_divisor;
	uint16_t m_dividend;
	std::unique_ptr<uint8_t[]> m_PROM_STR;
	std::unique_ptr<uint8_t[]> m_PROM_MAS;
	std::unique_ptr<uint8_t[]> m_PROM_AM;
	int m_math_run;
	emu_timer *m_math_timer;
	int16_t m_A;
	int16_t m_B;
	int16_t m_C;
	int32_t m_ACC;
	DECLARE_WRITE8_MEMBER(irq_ack_w);
	DECLARE_READ8_MEMBER(esb_slapstic_r);
	DECLARE_WRITE8_MEMBER(esb_slapstic_w);
	DECLARE_WRITE8_MEMBER(starwars_nstore_w);
	DECLARE_WRITE8_MEMBER(starwars_out_w);
	DECLARE_READ8_MEMBER(starwars_adc_r);
	DECLARE_WRITE8_MEMBER(starwars_adc_select_w);
	DECLARE_READ8_MEMBER(starwars_prng_r);
	DECLARE_READ8_MEMBER(starwars_div_reh_r);
	DECLARE_READ8_MEMBER(starwars_div_rel_r);
	DECLARE_WRITE8_MEMBER(starwars_math_w);
	DECLARE_CUSTOM_INPUT_MEMBER(matrix_flag_r);
	DECLARE_READ8_MEMBER(starwars_sin_r);
	DECLARE_WRITE8_MEMBER(starwars_sout_w);
	DECLARE_READ8_MEMBER(starwars_main_read_r);
	DECLARE_READ8_MEMBER(starwars_main_ready_flag_r);
	DECLARE_WRITE8_MEMBER(starwars_main_wr_w);
	DECLARE_WRITE8_MEMBER(starwars_soundrst_w);
	DECLARE_WRITE8_MEMBER(quad_pokeyn_w);
	DECLARE_DRIVER_INIT(esb);
	DECLARE_DRIVER_INIT(starwars);
	virtual void machine_reset() override;
	TIMER_CALLBACK_MEMBER(math_run_clear);
	TIMER_CALLBACK_MEMBER(main_callback);
	TIMER_CALLBACK_MEMBER(sound_callback);
	DECLARE_READ8_MEMBER(r6532_porta_r);
	DECLARE_WRITE8_MEMBER(r6532_porta_w);
	DECLARE_WRITE_LINE_MEMBER(snd_interrupt);
	void starwars_mproc_init();
	void starwars_mproc_reset();
	void run_mproc();
	void esb_slapstic_tweak(address_space &space, offs_t offset);
	required_device<cpu_device> m_maincpu;
	required_device<cpu_device> m_audiocpu;
	optional_device<atari_slapstic_device> m_slapstic_device;
};
