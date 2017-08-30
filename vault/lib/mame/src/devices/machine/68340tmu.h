// license:BSD-3-Clause
// copyright-holders:David Haywood
#ifndef MAME_MACHINE_68340TMU_H
#define MAME_MACHINE_68340TMU_H

#pragma once

class m68340_timer
{
public:
	// Registers for timer 1 and timer 2
	uint16_t m_mcr[2];
	uint16_t m_ir[2];
	uint16_t m_cr[2];
	uint16_t m_sr[2];
	uint16_t m_cntr[2];
	uint16_t m_cntr_reg[2];
	uint16_t m_prel1[2];
	uint16_t m_prel2[2];
	uint16_t m_com[2];
	uint16_t m_timer_counter[2];
	uint32_t m_tin[2];
	uint32_t m_tgate[2];
	uint32_t m_tout[2];
	emu_timer *m_timer[2];

	void reset();

	enum {
			REG_MCR   = 0x00,
			REG_IR    = 0x04,
			REG_CR    = 0x06,
			REG_SR    = 0x08,
			REG_CNTR  = 0x0a,
			REG_PREL1 = 0x0c,
			REG_PREL2 = 0x0e,
			REG_COM   = 0x10,
	};

	enum {
			REG_MCR_STP   = 0x8000,
			REG_MCR_FRZ1  = 0x4000,
			REG_MCR_FRZ2  = 0x2000,
			REG_MCR_SUPV  = 0x0800,
			REG_MCR_ARBLV = 0x000f,
	};

	enum {
			REG_IR_INTLEV = 0x0700,
			REG_IR_INTVEC = 0x00ff,
	};

	enum {
			REG_CR_SWR    = 0x8000,
			REG_CR_INTMSK = 0x7000,
			REG_CR_IE0    = 0x4000,
			REG_CR_IE1    = 0x2000,
			REG_CR_IE2    = 0x1000,
			REG_CR_TGE    = 0x0800,
			REG_CR_PCLK   = 0x0400,
			REG_CR_CPE    = 0x0200,
			REG_CR_CLK    = 0x0100,
			REG_CR_POT_MASK = 0x00e0,
			REG_CR_MODE_MASK   = 0x001c, // Mode mask
			REG_CR_MODE_ICOC   = 0x0000, // Input Capture Output Compare
			REG_CR_MODE_SQWG   = 0x0004, // Square Wave Generator
			REG_CR_MODE_VDCSW  = 0x0008, // Variable Duty Cycle Square Wave generator
			REG_CR_MODE_VWSSPG = 0x000c, // Variable Width Single Shot Pulse Generator
			REG_CR_MODE_PWM    = 0x0010, // Pulse Width Measurement
			REG_CR_MODE_PM     = 0x0014, // Period Measurement
			REG_CR_MODE_EC     = 0x0018, // Event Count
			REG_CR_MODE_TB     = 0x001c, // Timer Bypass
			REG_CR_OC_MASK = 0x0003,
			REG_CR_OC_DISABLED = 0x0000,
			REG_CR_OC_TOGGLE   = 0x0001,
			REG_CR_OC_ZERO     = 0x0002,
			REG_CR_OC_ONE      = 0x0003,
	};

	enum {
			REG_SR_IRQ      = 0x8000,
			REG_SR_TO       = 0x4000,
			REG_SR_TG       = 0x2000,
			REG_SR_TC       = 0x1000,
			REG_SR_TGL      = 0x0800,
			REG_SR_ON       = 0x0400,
			REG_SR_OUT      = 0x0200,
			REG_SR_COM      = 0x0100,
			REG_SR_PSC_OUT  = 0x00ff,
	};

};

#endif // MAME_MACHINE_68340TMU_H
