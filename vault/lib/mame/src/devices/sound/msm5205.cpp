// license:BSD-3-Clause
// copyright-holders:Aaron Giles
/*
 *   streaming ADPCM driver
 *   by Aaron Giles
 *
 *   Library to transcode from an ADPCM source to raw PCM.
 *   Written by Buffoni Mirko in 08/06/97
 *   References: various sources and documents.
 *
 *   HJB 08/31/98
 *   modified to use an automatically selected oversampling factor
 *   for the current sample rate
 *
 *   01/06/99
 *    separate MSM5205 emulator form adpcm.c and some fix
 *
 *   07/29/12
 *    added basic support for the MSM6585
 */

#include "emu.h"
#include "msm5205.h"

/*

    MSM 5205 ADPCM chip:

    Data is streamed from a CPU by means of a clock generated on the chip.

    Holding the rate selector lines (S1 and S2) both high places the MSM5205 in an undocumented
    mode which disables the sampling clock generator and makes VCK an input line.

    A reset signal is set high or low to determine whether playback (and interrupts) are occurring.

  MSM6585: is an upgraded MSM5205 voice synth IC.
   Improvements:
    More precise internal DA converter
    Built in low-pass filter
    Expanded sampling frequency

   Differences between MSM6585 & MSM5205:

                              MSM6585          MSM5205
    Master clock frequency    640kHz           384kHz
    Sampling frequency        4k/8k/16k/32kHz  4k/6k/8kHz
    ADPCM bit length          4-bit            3-bit/4-bit
    DA converter              12-bit           10-bit
    Low-pass filter           -40dB/oct        N/A
    Overflow prevent circuit  Included         N/A

    Data input follows VCK falling edge on MSM5205 (VCK rising edge on MSM6585)

   TODO:
   - lowpass filter for MSM6585

 */

const device_type MSM5205 = device_creator<msm5205_device>;
const device_type MSM6585 = device_creator<msm6585_device>;


msm5205_device::msm5205_device(const machine_config &mconfig, const char *tag, device_t *owner, u32 clock)
	: msm5205_device(mconfig, MSM5205, "MSM5205", tag, owner, clock, "msm5205", __FILE__)
{
}

msm5205_device::msm5205_device(const machine_config &mconfig, device_type type, const char *name, const char *tag, device_t *owner, u32 clock, const char *shortname, const char *source)
	: device_t(mconfig, type, name, tag, owner, clock, shortname, source),
		device_sound_interface(mconfig, *this),
		m_s1(false),
		m_s2(false),
		m_bitwidth(4),
		m_vclk_cb(*this)
{
}


msm6585_device::msm6585_device(const machine_config &mconfig, const char *tag, device_t *owner, u32 clock)
	: msm5205_device(mconfig, MSM6585, "MSM6585", tag, owner, clock, "msm6585", __FILE__)
{
}

//-------------------------------------------------
//  set_prescaler_selector - configuration helper
//-------------------------------------------------

void msm5205_device::set_prescaler_selector(device_t &device, int select)
{
	msm5205_device &msm = downcast<msm5205_device &>(device);
	msm.m_s1 = BIT(select, 1);
	msm.m_s2 = BIT(select, 0);
	msm.m_bitwidth = (select & 4) ? 4 : 3;
}

//-------------------------------------------------
//  device_start - device-specific startup
//-------------------------------------------------

void msm5205_device::device_start()
{
	m_vclk_cb.resolve();

	/* compute the difference tables */
	compute_tables();

	/* stream system initialize */
	m_stream = machine().sound().stream_alloc(*this, 0, 1, clock());
	m_timer = machine().scheduler().timer_alloc(timer_expired_delegate(FUNC(msm5205_device::vclk_callback), this));

	/* register for save states */
	save_item(NAME(m_data));
	save_item(NAME(m_vclk));
	save_item(NAME(m_reset));
	save_item(NAME(m_s1));
	save_item(NAME(m_s2));
	save_item(NAME(m_bitwidth));
	save_item(NAME(m_signal));
	save_item(NAME(m_step));
}

//-------------------------------------------------
//  device_reset - device-specific reset
//-------------------------------------------------

void msm5205_device::device_reset()
{
	/* initialize work */
	m_data    = 0;
	m_vclk     = 0;
	m_reset   = 0;
	m_signal  = 0;
	m_step    = 0;
}


/*
 * ADPCM lookup table
 */

/* step size index shift table */
static const int index_shift[8] = { -1, -1, -1, -1, 2, 4, 6, 8 };

/*
 *   Compute the difference table
 */

void msm5205_device::compute_tables()
{
	/* nibble to bit map */
	static const int nbl2bit[16][4] =
	{
		{ 1, 0, 0, 0}, { 1, 0, 0, 1}, { 1, 0, 1, 0}, { 1, 0, 1, 1},
		{ 1, 1, 0, 0}, { 1, 1, 0, 1}, { 1, 1, 1, 0}, { 1, 1, 1, 1},
		{-1, 0, 0, 0}, {-1, 0, 0, 1}, {-1, 0, 1, 0}, {-1, 0, 1, 1},
		{-1, 1, 0, 0}, {-1, 1, 0, 1}, {-1, 1, 1, 0}, {-1, 1, 1, 1}
	};

	int step, nib;

	/* loop over all possible steps */
	for (step = 0; step <= 48; step++)
	{
		/* compute the step value */
		int stepval = floor (16.0 * pow (11.0 / 10.0, (double)step));

		/* loop over all nibbles and compute the difference */
		for (nib = 0; nib < 16; nib++)
		{
			m_diff_lookup[step*16 + nib] = nbl2bit[nib][0] *
				(stepval   * nbl2bit[nib][1] +
					stepval/2 * nbl2bit[nib][2] +
					stepval/4 * nbl2bit[nib][3] +
					stepval/8);
		}
	}
}

// timer callback at VCK low edge on MSM5205 (at rising edge on MSM6585)
TIMER_CALLBACK_MEMBER( msm5205_device::vclk_callback )
{
	int val;
	int new_signal;

	// callback user handler and latch next data
	if (!m_vclk_cb.isnull())
		m_vclk_cb(1);

	// reset check at last hiedge of VCK
	if (m_reset)
	{
		new_signal = 0;
		m_step = 0;
	}
	else
	{
		/* update signal */
		/* !! MSM5205 has internal 12bit decoding, signal width is 0 to 8191 !! */
		val = m_data;
		new_signal = m_signal + m_diff_lookup[m_step * 16 + (val & 15)];

		if (new_signal > 2047) new_signal = 2047;
		else if (new_signal < -2048) new_signal = -2048;

		m_step += index_shift[val & 7];

		if (m_step > 48) m_step = 48;
		else if (m_step < 0) m_step = 0;
	}

	/* update when signal changed */
	if( m_signal != new_signal)
	{
		m_stream->update();
		m_signal = new_signal;
	}
}



/*
 *    Handle an update of the VCK status of a chip (1 is reset ON, 0 is reset OFF)
 *    This function can use selector = MSM5205_SEX only
 */
WRITE_LINE_MEMBER(msm5205_device::vclk_w)
{
	if (get_prescaler() != 0)
		logerror("Error: vclk_w() called but VCK selected master mode\n");
	else
	{
		if (m_vclk != state)
		{
			m_vclk = state;
			if (!state)
				vclk_callback(this, 0);
		}
	}
}

/*
 *    Handle an update of the reset status of a chip (1 is reset ON, 0 is reset OFF)
 */

WRITE_LINE_MEMBER(msm5205_device::reset_w)
{
	m_reset = state;
}

/*
 *    Handle an update of the data to the chip
 */

void msm5205_device::data_w(int data)
{
	if (m_bitwidth == 4)
		m_data = data & 0x0f;
	else
		m_data = (data & 0x07) << 1; /* unknown */
}

WRITE8_MEMBER(msm5205_device::data_w)
{
	data_w(data);
}

int msm5205_device::get_prescaler() const
{
	if (m_s1)
		return m_s2 ? 0 : 64;
	else
		return m_s2 ? 48 : 96;
}

int msm6585_device::get_prescaler() const
{
	return (m_s1 ? 20 : 40) * (m_s2 ? 1 : 4);
}

/*
 *    Handle a change of the selector
 */

void msm5205_device::playmode_w(int select)
{
	int bitwidth = (select & 4) ? 4 : 3;

	if ((select & 3) != ((m_s1 << 1) | m_s2))
	{
		m_stream->update();

		m_s1 = BIT(select, 1);
		m_s2 = BIT(select, 0);

		/* timer set */
		notify_clock_changed();
	}

	if (m_bitwidth != bitwidth)
	{
		m_stream->update();
		m_bitwidth = bitwidth;
	}
}

WRITE_LINE_MEMBER(msm5205_device::s1_w)
{
	if (m_s1 != bool(state))
	{
		m_stream->update();
		m_s1 = state;
		notify_clock_changed();
	}
}

WRITE_LINE_MEMBER(msm5205_device::s2_w)
{
	if (m_s2 != bool(state))
	{
		m_stream->update();
		m_s2 = state;
		notify_clock_changed();
	}
}


//-------------------------------------------------
//  device_clock_changed - called when the
//  device clock is altered in any way
//-------------------------------------------------

void msm5205_device::device_clock_changed()
{
	int prescaler = get_prescaler();
	if (prescaler != 0)
	{
		attotime period = attotime::from_hz(clock()) * prescaler;
		m_timer->adjust(period, 0, period);
	}
	else
		m_timer->adjust(attotime::never);
}


//-------------------------------------------------
//  sound_stream_update - handle a stream update
//-------------------------------------------------

void msm5205_device::sound_stream_update(sound_stream &stream, stream_sample_t **inputs, stream_sample_t **outputs, int samples)
{
	stream_sample_t *buffer = outputs[0];

	/* if this voice is active */
	if(m_signal)
	{
		short val = m_signal * 16;
		while (samples)
		{
			*buffer++ = val;
			samples--;
		}
	}
	else
		memset(buffer, 0, samples * sizeof(*buffer));
}


//-------------------------------------------------
//  sound_stream_update - handle a stream update
//-------------------------------------------------

void msm6585_device::sound_stream_update(sound_stream &stream, stream_sample_t **inputs, stream_sample_t **outputs, int samples)
{
	// should this be different?
	msm5205_device::sound_stream_update(stream, inputs, outputs,samples);
}
