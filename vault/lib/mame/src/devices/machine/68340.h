// license:BSD-3-Clause
// copyright-holders:David Haywood
/* 68340 */
#ifndef MAME_MACHINE_68340_H
#define MAME_MACHINE_68340_H

#pragma once

#include "cpu/m68000/m68000.h"

#include "68340sim.h"
#include "68340dma.h"
#include "68340ser.h"
#include "68340tmu.h"

//**************************************************************************
//  INTERFACE CONFIGURATION MACROS
//**************************************************************************
#define MCFG_MC68340_PA_INPUT_CB(_devcb) \
	devcb = &m68340_cpu_device::set_pa_in_callback (*device, DEVCB_##_devcb);

#define MCFG_MC68340_PA_OUTPUT_CB(_devcb) \
	devcb = &m68340_cpu_device::set_pa_out_callback (*device, DEVCB_##_devcb);

#define MCFG_MC68340_PB_INPUT_CB(_devcb) \
	devcb = &m68340_cpu_device::set_pb_in_callback (*device, DEVCB_##_devcb);

#define MCFG_MC68340_PB_OUTPUT_CB(_devcb) \
	devcb = &m68340_cpu_device::set_pb_out_callback (*device, DEVCB_##_devcb);

#define MCFG_MC68340_ADD_CRYSTAL(_crystal) \
	m68340_cpu_device::set_crystal(*device, _crystal);

#define MCFG_MC68340_TOUT1_OUTPUT_CB(_devcb) \
	devcb = &m68340_cpu_device::set_tout1_out_callback (*device, DEVCB_##_devcb);

#define MCFG_MC68340_TIN1_INPUT_CB(_devcb) \
	devcb = &m68340_cpu_device::set_tin1_out_callback (*device, DEVCB_##_devcb);

#define MCFG_MC68340_TGATE1_INPUT_CB(_devcb) \
	devcb = &m68340_cpu_device::set_tgate1_out_callback (*device, DEVCB_##_devcb);

#define MCFG_MC68340_TOUT2_OUTPUT_CB(_devcb) \
	devcb = &m68340_cpu_device::set_tout2_out_callback (*device, DEVCB_##_devcb);

#define MCFG_MC68340_TIN2_INPUT_CB(_devcb) \
	devcb = &m68340_cpu_device::set_tin2_out_callback (*device, DEVCB_##_devcb);

#define MCFG_MC68340_TGATE2_INPUT_CB(_devcb) \
	devcb = &m68340_cpu_device::set_tgate2_out_callback (*device, DEVCB_##_devcb);

class m68340_cpu_device : public fscpu32_device
{
public:
	m68340_cpu_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);

	template <class Object> static devcb_base &set_pa_in_callback (device_t &device, Object &&cb){ return downcast<m68340_cpu_device &>(device).m_pa_in_cb.set_callback (std::forward<Object>(cb)); }
	template <class Object> static devcb_base &set_pa_out_callback (device_t &device, Object &&cb){ return downcast<m68340_cpu_device &>(device).m_pa_out_cb.set_callback (std::forward<Object>(cb)); }
	template <class Object> static devcb_base &set_pb_in_callback (device_t &device, Object &&cb){ return downcast<m68340_cpu_device &>(device).m_pb_in_cb.set_callback (std::forward<Object>(cb)); }
	template <class Object> static devcb_base &set_pb_out_callback (device_t &device, Object &&cb){ return downcast<m68340_cpu_device &>(device).m_pb_out_cb.set_callback (std::forward<Object>(cb)); }

	template <class Object> static devcb_base &set_tout1_out_callback (device_t &device, Object &&cb){ return downcast<m68340_cpu_device &>(device).m_tout1_out_cb.set_callback (std::forward<Object>(cb)); }
	template <class Object> static devcb_base &set_tin1_in_callback (device_t &device, Object &&cb)  { return downcast<m68340_cpu_device &>(device).m_tin1_in_cb.set_callback (std::forward<Object>(cb)); }
	template <class Object> static devcb_base &set_tgate1_in_callback (device_t &device, Object &&cb){ return downcast<m68340_cpu_device &>(device).m_tgate1_in_cb.set_callback (std::forward<Object>(cb)); }
	template <class Object> static devcb_base &set_tout2_out_callback (device_t &device, Object &&cb){ return downcast<m68340_cpu_device &>(device).m_tout2_out_cb.set_callback (std::forward<Object>(cb)); }
	template <class Object> static devcb_base &set_tin2_in_callback (device_t &device, Object &&cb)  { return downcast<m68340_cpu_device &>(device).m_tin2_in_cb.set_callback (std::forward<Object>(cb)); }
	template <class Object> static devcb_base &set_tgate2_in_callback (device_t &device, Object &&cb){ return downcast<m68340_cpu_device &>(device).m_tgate2_in_cb.set_callback (std::forward<Object>(cb)); }

	uint16_t get_cs(offs_t address);

	// TODO: Support Limp mode and external clock with no PLL
	static void set_crystal(device_t &device, int crystal)
	{
		m68340_cpu_device &dev = downcast<m68340_cpu_device &>(device);
		dev.m_crystal = crystal;
		dev.m_clock_mode |= (m68340_sim::CLOCK_MODCK | m68340_sim::CLOCK_PLL);
	}

	READ32_MEMBER( m68340_internal_base_r );
	WRITE32_MEMBER( m68340_internal_base_w );
	READ32_MEMBER( m68340_internal_dma_r );
	WRITE32_MEMBER( m68340_internal_dma_w );
	READ32_MEMBER( m68340_internal_serial_r );
	WRITE32_MEMBER( m68340_internal_serial_w );
	READ16_MEMBER( m68340_internal_sim_r );
	READ8_MEMBER( m68340_internal_sim_ports_r );
	READ32_MEMBER( m68340_internal_sim_cs_r );
	WRITE16_MEMBER( m68340_internal_sim_w );
	WRITE8_MEMBER( m68340_internal_sim_ports_w );
	WRITE32_MEMBER( m68340_internal_sim_cs_w );
	READ16_MEMBER( m68340_internal_timer_r );
	WRITE16_MEMBER( m68340_internal_timer_w );

	// Clock/VCO setting TODO: support external clock with PLL and Limp mode
	DECLARE_WRITE_LINE_MEMBER( set_modck );
	DECLARE_WRITE_LINE_MEMBER( extal_w );

	// Timer input methods, can be used instead of the corresponding polling MCFG callbacks
	DECLARE_WRITE_LINE_MEMBER( tin1_w );
	DECLARE_WRITE_LINE_MEMBER( tgate1_w );
	DECLARE_WRITE_LINE_MEMBER( tin2_w );
	DECLARE_WRITE_LINE_MEMBER( tgate2_w );

protected:
	virtual void device_start() override;
	virtual void device_reset() override;

	TIMER_CALLBACK_MEMBER(periodic_interrupt_timer_callback);
	TIMER_CALLBACK_MEMBER(timer1_callback);
	TIMER_CALLBACK_MEMBER(timer2_callback);

	void start_68340_sim();
	void start_68340_timer();
	void do_pit_irq();
	void do_tick_pit();
	void do_timer_irq(int id);
	void do_timer_tick(int id);

	int calc_cs(offs_t address) const;

	int m_currentcs;
	uint32_t m_clock_mode;
	uint32_t m_modck;
	uint32_t m_crystal;
	uint32_t m_extal;

	/* 68340 peripheral modules */
	m68340_sim*    m68340SIM;
	m68340_dma*    m68340DMA;
	m68340_serial* m68340SERIAL;
	m68340_timer*  m68340TIMER;

	uint32_t m68340_base;

	emu_timer *m_irq_timer;

	devcb_write8        m_pa_out_cb;
	devcb_read8         m_pa_in_cb;
	devcb_write8        m_pb_out_cb;
	devcb_read8         m_pb_in_cb;
	devcb_write_line    m_tout1_out_cb;
	devcb_write_line    m_tin1_in_cb;
	devcb_write_line    m_tgate1_in_cb;
	devcb_write_line    m_tout2_out_cb;
	devcb_write_line    m_tin2_in_cb;
	devcb_write_line    m_tgate2_in_cb;
};

DECLARE_DEVICE_TYPE(M68340, m68340_cpu_device)

#endif // MAME_MACHINE_68340_H
