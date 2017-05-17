// license:BSD-3-Clause
// copyright-holders:Curt Coder
/**********************************************************************

    Personal Peripheral Products Speakeasy cartridge emulation
    (aka Protecto Enterprizes VIC-20 Voice Synthesizer)

**********************************************************************/

#pragma once

#ifndef __VIC20_SPEAKEASY__
#define __VIC20_SPEAKEASY__

#include "exp.h"
#include "sound/votrax.h"



//**************************************************************************
//  TYPE DEFINITIONS
//**************************************************************************

// ======================> vic20_speakeasy_t

class vic20_speakeasy_t :  public device_t,
						   public device_vic20_expansion_card_interface
{
public:
	// construction/destruction
	vic20_speakeasy_t(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);

	// optional information overrides
	virtual machine_config_constructor device_mconfig_additions() const override;

protected:
	// device-level overrides
	virtual void device_start() override;

	// device_vic20_expansion_card_interface overrides
	virtual uint8_t vic20_cd_r(address_space &space, offs_t offset, uint8_t data, int ram1, int ram2, int ram3, int blk1, int blk2, int blk3, int blk5, int io2, int io3) override;
	virtual void vic20_cd_w(address_space &space, offs_t offset, uint8_t data, int ram1, int ram2, int ram3, int blk1, int blk2, int blk3, int blk5, int io2, int io3) override;

private:
	required_device<votrax_sc01_device> m_votrax;
};


// device type definition
extern const device_type VIC20_SPEAKEASY;



#endif
