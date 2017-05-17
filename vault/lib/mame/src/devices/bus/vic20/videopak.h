// license:BSD-3-Clause
// copyright-holders:Curt Coder
/**********************************************************************

    Data 20 Corporation Video Pak cartridge emulation
    aka Data 20 Display Manager aka Protecto 40/80

**********************************************************************/

#pragma once

#ifndef __VIC20_VIDEO_PAK__
#define __VIC20_VIDEO_PAK__


#include "exp.h"
#include "video/mc6845.h"



//**************************************************************************
//  TYPE DEFINITIONS
//**************************************************************************

// ======================> vic20_video_pak_t

class vic20_video_pak_t : public device_t,
						  public device_vic20_expansion_card_interface
{
public:
	// construction/destruction
	vic20_video_pak_t(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);

	// optional information overrides
	virtual const tiny_rom_entry *device_rom_region() const override;
	virtual machine_config_constructor device_mconfig_additions() const override;

	// not really public
	MC6845_UPDATE_ROW( crtc_update_row );

protected:
	// device-level overrides
	virtual void device_start() override;
	virtual void device_reset() override;

	// device_vic20_expansion_card_interface overrides
	virtual uint8_t vic20_cd_r(address_space &space, offs_t offset, uint8_t data, int ram1, int ram2, int ram3, int blk1, int blk2, int blk3, int blk5, int io2, int io3) override;
	virtual void vic20_cd_w(address_space &space, offs_t offset, uint8_t data, int ram1, int ram2, int ram3, int blk1, int blk2, int blk3, int blk5, int io2, int io3) override;

private:
	required_device<h46505_device> m_crtc;
	required_device<palette_device> m_palette;
	required_memory_region m_char_rom;
	optional_shared_ptr<uint8_t> m_videoram;
	optional_shared_ptr<uint8_t> m_ram;

	bool m_case;
	bool m_bank_size;
	bool m_bank_lsb;
	bool m_bank_msb;
	bool m_ram_enable;
	bool m_columns;
};


// device type definition
extern const device_type VIC20_VIDEO_PAK;


#endif
