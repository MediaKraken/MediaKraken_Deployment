// license:BSD-3-Clause
// copyright-holders:Joakim Larsson Edstrom
#ifndef VME_FCSCSI_H
#define VME_FCSCSI_H
#pragma once

#include "machine/68230pit.h"
#include "machine/wd_fdc.h"
#include "machine/hd63450.h" // compatible with MC68450
#include "bus/vme/vme.h"

extern const device_type VME_FCSCSI1;

class vme_fcscsi1_card_device :
	public device_t
	,public device_vme_card_interface
{
public:
	vme_fcscsi1_card_device(const machine_config &mconfig, device_type type, const char *name, const char *tag, device_t *owner, uint32_t clock, const char *shortname, const char *source);
	vme_fcscsi1_card_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);

	// optional information overrides
	virtual machine_config_constructor device_mconfig_additions() const override;
	virtual const tiny_rom_entry *device_rom_region() const override;

	DECLARE_READ16_MEMBER (bootvect_r);
	DECLARE_READ8_MEMBER (tcr_r);
	DECLARE_WRITE8_MEMBER (tcr_w);
	DECLARE_WRITE8_MEMBER (led_w);

	IRQ_CALLBACK_MEMBER(maincpu_irq_acknowledge_callback);

	//dmac
	DECLARE_WRITE8_MEMBER(dma_end);
	DECLARE_WRITE8_MEMBER(dma_error);

	//fdc
	DECLARE_WRITE8_MEMBER(fdc_irq);
	DECLARE_READ8_MEMBER(fdc_read_byte);
	DECLARE_WRITE8_MEMBER(fdc_write_byte);
	DECLARE_FLOPPY_FORMATS(floppy_formats);

	/* Dummy driver routines */
	DECLARE_READ8_MEMBER (not_implemented_r);
	DECLARE_WRITE8_MEMBER (not_implemented_w);

	DECLARE_READ8_MEMBER (scsi_r);
	DECLARE_WRITE8_MEMBER (scsi_w);

	uint8_t fdc_irq_state;
	uint8_t dmac_irq_state;
	int dmac_irq_vector;

	void update_irq_to_maincpu();

protected:
	virtual void device_start() override;
	virtual void device_reset() override;

private:
	required_device<cpu_device> m_maincpu;
	required_device<wd1772_t> m_fdc;
	required_device<pit68230_device> m_pit;
	required_device<hd63450_device> m_dmac;

	uint8_t m_tcr;

	// Pointer to System ROMs needed by bootvect_r
	uint16_t  *m_sysrom;
};

#endif // VME_FCSCSI_H

