// license:BSD-3-Clause
// copyright-holders:hap
// thanks-to:Berger
/******************************************************************************

    Novag generic MCS-48 based chess computer driver

    NOTE: MAME doesn't include a generalized implementation for boardpieces yet,
    greatly affecting user playability of emulated electronic board games.
    As workaround for the chess games, use an external chess GUI on the side,
    such as Arena(in editmode).

    TODO:
    - is presto led handling correct? led data needs to be auto cleared
      similar to novag6502 sforte/sexpert

******************************************************************************

Presto:
- NEC D80C49C MCU(serial 186), OSC from LC circuit measured ~6MHz
- buzzer, 16+4 LEDs, 8*8 chessboard buttons

Octo:
- NEC D80C49HC MCU(serial 111), OSC from LC circuit measured ~12MHz
The buzzer has a little electronic circuit going on, not sure whatfor.
Otherwise, it's identical to Presto. The MCU internal ROM is same too.

******************************************************************************/

#include "emu.h"
#include "includes/novagbase.h"

#include "cpu/mcs48/mcs48.h"
#include "sound/volt_reg.h"
#include "speaker.h"

// internal artwork
#include "novag_presto.lh" // clickable


class novagmcs48_state : public novagbase_state
{
public:
	novagmcs48_state(const machine_config &mconfig, device_type type, const char *tag)
		: novagbase_state(mconfig, type, tag)
	{ }

	// Presto/Octo
	DECLARE_WRITE8_MEMBER(presto_mux_w);
	DECLARE_WRITE8_MEMBER(presto_control_w);
	DECLARE_READ8_MEMBER(presto_input_r);
};



// Devices, I/O

/******************************************************************************
    Presto/Octo
******************************************************************************/

// MCU ports

WRITE8_MEMBER(novagmcs48_state::presto_mux_w)
{
	// D0-D7: input mux low, led data
	m_inp_mux = (m_inp_mux & ~0xff) | (~data & 0xff);
	m_led_data = ~data & 0xff;
}

WRITE8_MEMBER(novagmcs48_state::presto_control_w)
{
	// P21: input mux high
	m_inp_mux = (m_inp_mux & 0xff) | (~data << 7 & 0x100);

	// P22,P23: speaker lead 1,2
	m_dac->write(BIT(data, 2) & BIT(~data, 3));

	// P24-P26: led select
	m_led_select = ~data >> 4 & 7;
	display_matrix(8, 3, m_led_data, m_led_select);
	m_led_data = 0; // ?
}

READ8_MEMBER(novagmcs48_state::presto_input_r)
{
	// P10-P17: multiplexed inputs
	return ~read_inputs(9) & 0xff;
}



/******************************************************************************
    Address Maps
******************************************************************************/

// Presto/Octo

static ADDRESS_MAP_START( presto_map, AS_IO, 8, novagmcs48_state )
	ADDRESS_MAP_UNMAP_HIGH
	AM_RANGE(MCS48_PORT_P1, MCS48_PORT_P1) AM_READ(presto_input_r) AM_WRITENOP
	AM_RANGE(MCS48_PORT_P2, MCS48_PORT_P2) AM_WRITE(presto_control_w)
	AM_RANGE(MCS48_PORT_BUS, MCS48_PORT_BUS) AM_WRITE(presto_mux_w)
ADDRESS_MAP_END



/******************************************************************************
    Input Ports
******************************************************************************/

static INPUT_PORTS_START( presto )
	PORT_INCLUDE( novag_cb_buttons )

	PORT_START("IN.8")
	PORT_BIT(0x01, IP_ACTIVE_HIGH, IPT_KEYPAD) PORT_CODE(KEYCODE_1) PORT_NAME("Black/White") // Octo calls it "Change Color"
	PORT_BIT(0x02, IP_ACTIVE_HIGH, IPT_KEYPAD) PORT_CODE(KEYCODE_2) PORT_NAME("Verify / Pawn")
	PORT_BIT(0x04, IP_ACTIVE_HIGH, IPT_KEYPAD) PORT_CODE(KEYCODE_3) PORT_NAME("Set Up / Rook")
	PORT_BIT(0x08, IP_ACTIVE_HIGH, IPT_KEYPAD) PORT_CODE(KEYCODE_4) PORT_NAME("Knight")
	PORT_BIT(0x10, IP_ACTIVE_HIGH, IPT_KEYPAD) PORT_CODE(KEYCODE_5) PORT_NAME("Set Level / Bishop")
	PORT_BIT(0x20, IP_ACTIVE_HIGH, IPT_KEYPAD) PORT_CODE(KEYCODE_6) PORT_NAME("Queen")
	PORT_BIT(0x40, IP_ACTIVE_HIGH, IPT_KEYPAD) PORT_CODE(KEYCODE_7) PORT_NAME("Take Back / King")
	PORT_BIT(0x80, IP_ACTIVE_HIGH, IPT_KEYPAD) PORT_CODE(KEYCODE_8) PORT_NAME("Go")
INPUT_PORTS_END



/******************************************************************************
    Machine Drivers
******************************************************************************/

static MACHINE_CONFIG_START( presto, novagmcs48_state )

	/* basic machine hardware */
	MCFG_CPU_ADD("maincpu", I8049, 6000000) // LC circuit, measured
	MCFG_CPU_IO_MAP(presto_map)

	MCFG_TIMER_DRIVER_ADD_PERIODIC("display_decay", novagbase_state, display_decay_tick, attotime::from_msec(1))
	MCFG_DEFAULT_LAYOUT(layout_novag_presto)

	/* sound hardware */
	MCFG_SPEAKER_STANDARD_MONO("speaker")
	MCFG_SOUND_ADD("dac", DAC_1BIT, 0) MCFG_SOUND_ROUTE(ALL_OUTPUTS, "speaker", 0.25)
	MCFG_DEVICE_ADD("vref", VOLTAGE_REGULATOR, 0) MCFG_VOLTAGE_REGULATOR_OUTPUT(5.0)
	MCFG_SOUND_ROUTE_EX(0, "dac", 1.0, DAC_VREF_POS_INPUT)
MACHINE_CONFIG_END

static MACHINE_CONFIG_DERIVED( octo, presto )

	/* basic machine hardware */
	MCFG_CPU_MODIFY("maincpu")
	MCFG_DEVICE_CLOCK(12000000) // LC circuit, measured
MACHINE_CONFIG_END



/******************************************************************************
    ROM Definitions
******************************************************************************/

ROM_START( npresto )
	ROM_REGION( 0x0800, "maincpu", 0 )
	ROM_LOAD("d80c49c_186", 0x0000, 0x0800, CRC(29a0eb4c) SHA1(e058d6018e53ddcaa3b5ec25b33b8bff091b04db) )
ROM_END

ROM_START( nocto )
	ROM_REGION( 0x0800, "maincpu", 0 )
	ROM_LOAD("d80c49hc_111", 0x0000, 0x0800, CRC(29a0eb4c) SHA1(e058d6018e53ddcaa3b5ec25b33b8bff091b04db) ) // same program as npresto
ROM_END



/******************************************************************************
    Drivers
******************************************************************************/

/*    YEAR  NAME      PARENT   COMPAT  MACHINE    INPUT      INIT              COMPANY, FULLNAME, FLAGS */
CONS( 1984, npresto,  0,       0,      presto,    presto,    driver_device, 0, "Novag", "Presto (Novag)", MACHINE_SUPPORTS_SAVE | MACHINE_CLICKABLE_ARTWORK )
CONS( 1987, nocto,    npresto, 0,      octo,      presto,    driver_device, 0, "Novag", "Octo (Novag)", MACHINE_SUPPORTS_SAVE | MACHINE_CLICKABLE_ARTWORK )
