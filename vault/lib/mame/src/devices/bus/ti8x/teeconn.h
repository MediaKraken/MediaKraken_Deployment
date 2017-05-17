// license:BSD-3-Clause
// copyright-holders:Vas Crabb
/*
 A T-connector, strangely enough.
 */
#ifndef MAME_DEVICES_BUS_TI8X_TEECONN_H
#define MAME_DEVICES_BUS_TI8X_TEECONN_H

#pragma once

#include "ti8x.h"


extern device_type const TI8X_TEE_CONNECTOR;


namespace bus { namespace ti8x {

class tee_connector_device : public device_t, public device_ti8x_link_port_interface
{
public:
	tee_connector_device(machine_config const &mconfig, char const *tag, device_t *owner, uint32_t clock);

	DECLARE_WRITE_LINE_MEMBER(tip_a_w);
	DECLARE_WRITE_LINE_MEMBER(ring_a_w);
	DECLARE_WRITE_LINE_MEMBER(tip_b_w);
	DECLARE_WRITE_LINE_MEMBER(ring_b_w);

protected:
	virtual machine_config_constructor device_mconfig_additions() const override;
	virtual void device_start() override;

	virtual DECLARE_WRITE_LINE_MEMBER(input_tip) override;
	virtual DECLARE_WRITE_LINE_MEMBER(input_ring) override;

	required_device<ti8x_link_port_device>  m_port_a;
	required_device<ti8x_link_port_device>  m_port_b;

	bool    m_tip_host, m_tip_a, m_tip_b;
	bool    m_ring_host, m_ring_a, m_ring_b;
};

} } // namespace bus::ti8x

#endif // MAME_DEVICES_BUS_TI8X_TEECONN_H
