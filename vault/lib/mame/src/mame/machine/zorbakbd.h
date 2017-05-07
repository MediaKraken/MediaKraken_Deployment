// license:BSD-3-Clause
// copyright-holders:Vas Crabb
#ifndef MAME_MACHINE_ZORBAKBD_H
#define MAME_MACHINE_ZORBAKBD_H

#include "sound/beep.h"


extern device_type const ZORBA_KEYBOARD;

#define MCFG_ZORBA_KEYBOARD_RXD_CB(cb) \
		zorba_keyboard_device::set_rxd_cb(*device, DEVCB_##cb);

class zorba_keyboard_device : public device_t
{
public:
	template <typename Obj> static devcb_base &set_rxd_cb(device_t &device, Obj &&object)
	{ return downcast<zorba_keyboard_device &>(device).m_rxd_cb.set_callback(std::forward<Obj>(object)); }

	zorba_keyboard_device(machine_config const &mconfig, char const *tag, device_t *owner, uint32_t clock);

	DECLARE_WRITE_LINE_MEMBER(txd_w);

	DECLARE_READ8_MEMBER(mcu_pa_r);
	DECLARE_READ8_MEMBER(mcu_pb_r);
	DECLARE_WRITE8_MEMBER(mcu_pb_w);
	DECLARE_WRITE8_MEMBER(mcu_pc_w);

protected:
	virtual void device_start() override;
	virtual machine_config_constructor device_mconfig_additions() const override;
	virtual ioport_constructor device_input_ports() const override;
	virtual tiny_rom_entry const *device_rom_region() const override;

	required_ioport_array<16>       m_rows;
	required_device<beep_device>    m_beeper;
	devcb_write_line                m_rxd_cb;

	bool    m_txd_high;
	u8      m_row_select;
};

#endif // MAME_MACHINE_ZORBAKBD_H
