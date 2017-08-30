// license:BSD-3-Clause
// copyright-holders:Angelo Salese
/***************************************************************************

    Taito Yoke + Throttle Flight device

***************************************************************************/
#ifndef MAME_MACHINE_TAITO_YOKE_H
#define MAME_MACHINE_TAITO_YOKE_H

#pragma once




//**************************************************************************
//  INTERFACE CONFIGURATION MACROS
//**************************************************************************

#define MCFG_TAITOIO_YOKE_ADD(_tag) \
	MCFG_DEVICE_ADD(_tag, TAITOIO_YOKE, 0)

//**************************************************************************
//  TYPE DEFINITIONS
//**************************************************************************

// ======================> namcoio_gearbox_device

class taitoio_yoke_device : public device_t
{
public:
	// construction/destruction
	taitoio_yoke_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);

	// I/O operations
	DECLARE_READ16_MEMBER( throttle_r );
	DECLARE_READ16_MEMBER( stickx_r );
	DECLARE_READ16_MEMBER( sticky_r );

	DECLARE_READ_LINE_MEMBER( slot_up_r );
	DECLARE_READ_LINE_MEMBER( slot_down_r );
	DECLARE_READ_LINE_MEMBER( handle_left_r );
	DECLARE_READ_LINE_MEMBER( handle_right_r );
	DECLARE_READ_LINE_MEMBER( handle_up_r );
	DECLARE_READ_LINE_MEMBER( handle_down_r );


	virtual ioport_constructor device_input_ports() const override;

protected:
	// device-level overrides
//  virtual void device_validity_check(validity_checker &valid) const;
	virtual void device_start() override;
	virtual void device_reset() override;
};


// device type definition
DECLARE_DEVICE_TYPE(TAITOIO_YOKE, taitoio_yoke_device)



//**************************************************************************
//  GLOBAL VARIABLES
//**************************************************************************



#endif // MAME_MACHINE_TAITO_YOKE_H
