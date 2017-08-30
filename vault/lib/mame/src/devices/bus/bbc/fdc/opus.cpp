// license:BSD-3-Clause
// copyright-holders:Nigel Barnes
/**********************************************************************

    Opus Floppy Disc Controllers

    8272: https://www.youtube.com/watch?v=09alLIz16ck
    EDOS: http://chrisacorns.computinghistory.org.uk/8bit_Upgrades/Opus_DiscController.html
    2791: http://chrisacorns.computinghistory.org.uk/8bit_Upgrades/Opus_DDoss.html
    2793:
    1770: http://chrisacorns.computinghistory.org.uk/8bit_Upgrades/Opus_D-DOS.html

**********************************************************************/


#include "emu.h"
#include "opus.h"


//**************************************************************************
//  DEVICE DEFINITIONS
//**************************************************************************

DEFINE_DEVICE_TYPE(BBC_OPUS8272, bbc_opus8272_device, "bbc_opus8272", "Opus 8272 FDC")
DEFINE_DEVICE_TYPE(BBC_OPUS2791, bbc_opus2791_device, "bbc_opus2791", "Opus 2791 FDC")
DEFINE_DEVICE_TYPE(BBC_OPUS2793, bbc_opus2793_device, "bbc_opus2793", "Opus 2793 FDC")
DEFINE_DEVICE_TYPE(BBC_OPUS1770, bbc_opus1770_device, "bbc_opus1770", "Opus D-DOS(B) 1770 FDC")


//-------------------------------------------------
//  MACHINE_DRIVER( opus2791 )
//-------------------------------------------------

FLOPPY_FORMATS_MEMBER( bbc_opusfdc_device::floppy_formats )
	FLOPPY_ACORN_SSD_FORMAT,
	FLOPPY_ACORN_DSD_FORMAT,
	FLOPPY_FSD_FORMAT,
	FLOPPY_OPUS_DDOS_FORMAT,
	FLOPPY_OPUS_DDCPM_FORMAT
FLOPPY_FORMATS_END0

static SLOT_INTERFACE_START( bbc_floppies_525 )
	SLOT_INTERFACE("525sssd", FLOPPY_525_SSSD)
	SLOT_INTERFACE("525sd",   FLOPPY_525_SD)
	SLOT_INTERFACE("525ssdd", FLOPPY_525_SSDD)
	SLOT_INTERFACE("525dd",   FLOPPY_525_DD)
	SLOT_INTERFACE("525qd",   FLOPPY_525_QD)
SLOT_INTERFACE_END

ROM_START( opus8272 )
	ROM_REGION(0x4000, "dfs_rom", 0)
	ROM_DEFAULT_BIOS("ddos300")
	ROM_SYSTEM_BIOS(0, "ddos300", "Opus DDOS 3.00")
	ROMX_LOAD("opus-ddos300.rom", 0x0000, 0x4000, CRC(1b5fa131) SHA1(6b4e0363a9d39807973a2ef0871a78b287cea27e), ROM_BIOS(1))
ROM_END

ROM_START( opus2791 )
	ROM_REGION(0x4000, "dfs_rom", 0)
	ROM_DEFAULT_BIOS("ddos315")
	ROM_SYSTEM_BIOS(0, "ddos315", "Opus DDOS 3.15")
	ROMX_LOAD("opus-ddos315.rom", 0x0000, 0x4000, CRC(5f06701c) SHA1(9e250dc7ddcde35b19e8f29f2cfe95a79f46d473), ROM_BIOS(1))
	ROM_SYSTEM_BIOS(1, "edos04", "Opus EDOS 0.4")
	ROMX_LOAD("opus-edos04.rom", 0x0000, 0x4000, CRC(1d8a3860) SHA1(05f461464707b4ca24636c9e726af561f227ccdb), ROM_BIOS(2))
ROM_END

ROM_START( opus2793 )
	ROM_REGION(0x4000, "dfs_rom", 0)
	ROM_DEFAULT_BIOS("ddos335")
	ROM_SYSTEM_BIOS(0, "ddos335", "Opus DDOS 3.35")
	ROMX_LOAD("opus-ddos335.rom", 0x0000, 0x4000, CRC(e33167fb) SHA1(42fbc9932db2087708da41cb1ffa94358683cf7a), ROM_BIOS(1))
ROM_END

ROM_START( opus1770 )
	ROM_REGION(0x4000, "dfs_rom", 0)
	ROM_DEFAULT_BIOS("ddos346")
	ROM_SYSTEM_BIOS(0, "ddos345", "Opus DDOS 3.45")
	ROMX_LOAD("opus-ddos345.rom", 0x0000, 0x4000, CRC(c0163b95) SHA1(1c5a68e08abbb7ffe663151c59088f750d2287a9), ROM_BIOS(1))
	ROM_SYSTEM_BIOS(1, "ddos346", "Opus DDOS 3.46")
	ROMX_LOAD("opus-ddos346.rom", 0x0000, 0x4000, CRC(bf9c35cf) SHA1(a1ad3e9acbd15400e7da1e50bc6673835cde1fe7), ROM_BIOS(2))
ROM_END


//-------------------------------------------------
//  device_add_mconfig - add device configuration
//-------------------------------------------------

MACHINE_CONFIG_MEMBER( bbc_opus8272_device::device_add_mconfig )
	MCFG_I8272A_ADD("i8272", true)
	MCFG_UPD765_INTRQ_CALLBACK(WRITELINE(bbc_opus8272_device, fdc_intrq_w))
	MCFG_UPD765_HDL_CALLBACK(WRITELINE(bbc_opus8272_device, motor_w))
	MCFG_FLOPPY_DRIVE_ADD("i8272:0", bbc_floppies_525, "525qd", bbc_opusfdc_device::floppy_formats)
	MCFG_FLOPPY_DRIVE_SOUND(true)
	MCFG_FLOPPY_DRIVE_ADD("i8272:1", bbc_floppies_525, "525qd", bbc_opusfdc_device::floppy_formats)
	MCFG_FLOPPY_DRIVE_SOUND(true)
MACHINE_CONFIG_END

MACHINE_CONFIG_MEMBER( bbc_opus2791_device::device_add_mconfig )
	MCFG_WD2791_ADD("fdc", XTAL_16MHz / 16)
	MCFG_WD_FDC_DRQ_CALLBACK(WRITELINE(bbc_opusfdc_device, fdc_drq_w))
	MCFG_WD_FDC_HLD_CALLBACK(WRITELINE(bbc_opusfdc_device, motor_w))
	MCFG_FLOPPY_DRIVE_ADD("fdc:0", bbc_floppies_525, "525qd", bbc_opusfdc_device::floppy_formats)
	MCFG_FLOPPY_DRIVE_SOUND(true)
	MCFG_FLOPPY_DRIVE_ADD("fdc:1", bbc_floppies_525, "525qd", bbc_opusfdc_device::floppy_formats)
	MCFG_FLOPPY_DRIVE_SOUND(true)
MACHINE_CONFIG_END

MACHINE_CONFIG_MEMBER( bbc_opus2793_device::device_add_mconfig )
	MCFG_WD2793_ADD("fdc", XTAL_16MHz / 16)
	MCFG_WD_FDC_DRQ_CALLBACK(WRITELINE(bbc_opusfdc_device, fdc_drq_w))
	MCFG_WD_FDC_HLD_CALLBACK(WRITELINE(bbc_opusfdc_device, motor_w))
	MCFG_FLOPPY_DRIVE_ADD("fdc:0", bbc_floppies_525, "525qd", bbc_opusfdc_device::floppy_formats)
	MCFG_FLOPPY_DRIVE_SOUND(true)
	MCFG_FLOPPY_DRIVE_ADD("fdc:1", bbc_floppies_525, "525qd", bbc_opusfdc_device::floppy_formats)
	MCFG_FLOPPY_DRIVE_SOUND(true)
MACHINE_CONFIG_END

MACHINE_CONFIG_MEMBER( bbc_opus1770_device::device_add_mconfig )
	MCFG_WD1770_ADD("fdc", XTAL_16MHz / 2)
	MCFG_WD_FDC_DRQ_CALLBACK(WRITELINE(bbc_opusfdc_device, fdc_drq_w))
	MCFG_FLOPPY_DRIVE_ADD("fdc:0", bbc_floppies_525, "525qd", bbc_opusfdc_device::floppy_formats)
	MCFG_FLOPPY_DRIVE_SOUND(true)
	MCFG_FLOPPY_DRIVE_ADD("fdc:1", bbc_floppies_525, "525qd", bbc_opusfdc_device::floppy_formats)
	MCFG_FLOPPY_DRIVE_SOUND(true)
MACHINE_CONFIG_END

const tiny_rom_entry *bbc_opus8272_device::device_rom_region() const
{
	return ROM_NAME( opus8272 );
}

const tiny_rom_entry *bbc_opus2791_device::device_rom_region() const
{
	return ROM_NAME( opus2791 );
}

const tiny_rom_entry *bbc_opus2793_device::device_rom_region() const
{
	return ROM_NAME( opus2793 );
}

const tiny_rom_entry *bbc_opus1770_device::device_rom_region() const
{
	return ROM_NAME( opus1770 );
}


//**************************************************************************
//  LIVE DEVICE
//**************************************************************************

//-------------------------------------------------
//  bbc_opusfdc_device - constructor
//-------------------------------------------------

bbc_opus8272_device::bbc_opus8272_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock) :
	device_t(mconfig, BBC_OPUS8272, tag, owner, clock),
	device_bbc_fdc_interface(mconfig, *this),
	m_dfs_rom(*this, "dfs_rom"),
	m_fdc(*this, "i8272"),
	m_floppy0(*this, "i8272:0"),
	m_floppy1(*this, "i8272:1")
{
}

bbc_opusfdc_device::bbc_opusfdc_device(const machine_config &mconfig, device_type type, const char *tag, device_t *owner, uint32_t clock) :
	device_t(mconfig, type, tag, owner, clock),
	device_bbc_fdc_interface(mconfig, *this),
	m_dfs_rom(*this, "dfs_rom"),
	m_fdc(*this, "fdc"),
	m_floppy0(*this, "fdc:0"),
	m_floppy1(*this, "fdc:1")
{
}

bbc_opus2791_device::bbc_opus2791_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: bbc_opusfdc_device(mconfig, BBC_OPUS2791, tag, owner, clock)
{
}

bbc_opus2793_device::bbc_opus2793_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: bbc_opusfdc_device(mconfig, BBC_OPUS2793, tag, owner, clock)
{
}

bbc_opus1770_device::bbc_opus1770_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: bbc_opusfdc_device(mconfig, BBC_OPUS1770, tag, owner, clock)
{
}

//-------------------------------------------------
//  device_start - device-specific startup
//-------------------------------------------------

void bbc_opus8272_device::device_start()
{
	device_t* cpu = machine().device("maincpu");
	address_space& space = cpu->memory().space(AS_PROGRAM);
	m_slot = dynamic_cast<bbc_fdc_slot_device *>(owner());

	space.install_readwrite_handler(0xfe80, 0xfe86, READ8_DELEGATE(bbc_opus8272_device, fdc_r), WRITE8_DELEGATE(bbc_opus8272_device, fdc_w));
}

void bbc_opusfdc_device::device_start()
{
	device_t* cpu = machine().device("maincpu");
	address_space& space = cpu->memory().space(AS_PROGRAM);
	m_slot = dynamic_cast<bbc_fdc_slot_device *>(owner());

	space.install_readwrite_handler(0xfe80, 0xfe83, READ8_DEVICE_DELEGATE(m_fdc, wd_fdc_device_base, read), WRITE8_DEVICE_DELEGATE(m_fdc, wd_fdc_device_base, write));
	space.install_readwrite_handler(0xfe84, 0xfe84, READ8_DELEGATE(bbc_opusfdc_device, ctrl_r), WRITE8_DELEGATE(bbc_opusfdc_device, ctrl_w));
}

//-------------------------------------------------
//  device_reset - device-specific reset
//-------------------------------------------------

void bbc_opus8272_device::device_reset()
{
	machine().root_device().membank("bank4")->configure_entry(12, memregion("dfs_rom")->base());

	m_fdc->soft_reset();
}

void bbc_opusfdc_device::device_reset()
{
	machine().root_device().membank("bank4")->configure_entry(12, memregion("dfs_rom")->base());

	m_fdc->soft_reset();
}


//**************************************************************************
//  IMPLEMENTATION
//**************************************************************************

READ8_MEMBER(bbc_opus8272_device::fdc_r)
{
	uint8_t data = 0xff;

	switch (offset)
	{
	case 0x02:
		data = 0x01;
		break;
	case 0x04:
	case 0x06:
		data = m_fdc->msr_r(space, 0);
		break;
	case 0x05:
	case 0x07:
		data = m_fdc->fifo_r(space, 0);
		break;
	}
	logerror("Read %04x -> %02x\n", offset | 0xfe80, data);
	return data;
}

WRITE8_MEMBER(bbc_opus8272_device::fdc_w)
{
	logerror("Write %04x <- %02x\n", offset | 0xfe80, data);
	floppy_image_device *floppy = nullptr;

	switch (offset)
	{
	case 0x01:
		switch (data & 0x01)
		{
		case 0: floppy = m_floppy1->get_device(); break;
		case 1: floppy = m_floppy0->get_device(); break;
		}
		m_fdc->set_floppy(floppy);

		if (m_floppy0->get_device()) m_floppy0->get_device()->mon_w(0);
		if (m_floppy1->get_device()) m_floppy1->get_device()->mon_w(0);
		break;
	case 0x05:
	case 0x07:
		m_fdc->fifo_w(space, 0, data);
		break;
	}
}

WRITE_LINE_MEMBER(bbc_opus8272_device::motor_w)
{
	if (m_floppy0->get_device()) m_floppy0->get_device()->mon_w(!state);
	if (m_floppy1->get_device()) m_floppy1->get_device()->mon_w(!state);
}

WRITE_LINE_MEMBER(bbc_opus8272_device::fdc_intrq_w)
{
	m_slot->intrq_w(state);
}


READ8_MEMBER(bbc_opusfdc_device::ctrl_r)
{
	return m_drive_control;
}

WRITE8_MEMBER(bbc_opusfdc_device::ctrl_w)
{
	floppy_image_device *floppy = nullptr;

	m_drive_control = data;

	// bit 0: drive select
	switch (BIT(data, 0))
	{
	case 0: floppy = m_floppy0->get_device(); break;
	case 1: floppy = m_floppy1->get_device(); break;
	}
	m_fdc->set_floppy(floppy);

	// bit 1: side select
	if (floppy)
		floppy->ss_w(BIT(data, 1));

	// bit 6: density
	m_fdc->dden_w(!BIT(data, 6));
}

WRITE_LINE_MEMBER(bbc_opusfdc_device::fdc_drq_w)
{
	m_slot->drq_w(state);
}

WRITE_LINE_MEMBER(bbc_opusfdc_device::motor_w)
{
	if (m_floppy0->get_device()) m_floppy0->get_device()->mon_w(!state);
	if (m_floppy1->get_device()) m_floppy1->get_device()->mon_w(!state);
}
