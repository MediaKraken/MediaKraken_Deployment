// license:BSD-3-Clause
// copyright-holders:Phil Stroffolino

#include "sound/ay8910.h"

class shangkid_state : public driver_device
{
public:
	shangkid_state(const machine_config &mconfig, device_type type, const char *tag)
		: driver_device(mconfig, type, tag),
		m_maincpu(*this, "maincpu"),
		m_audiocpu(*this, "audiocpu"),
		m_bbx(*this, "bbx"),
		m_aysnd(*this, "aysnd"),
		m_gfxdecode(*this, "gfxdecode"),
		m_palette(*this, "palette"),
		m_videoram(*this, "videoram"),
		m_spriteram(*this, "spriteram"),
		m_videoreg(*this, "videoreg")  { }

	required_device<cpu_device> m_maincpu;
	optional_device<cpu_device> m_audiocpu;
	optional_device<cpu_device> m_bbx;
	required_device<ay8910_device> m_aysnd;
	required_device<gfxdecode_device> m_gfxdecode;
	required_device<palette_device> m_palette;

	required_shared_ptr<uint8_t> m_videoram;
	optional_shared_ptr<uint8_t> m_spriteram;
	optional_shared_ptr<uint8_t> m_videoreg;

	bool m_int_enable[2];
	bool m_nmi_enable[2];
	uint8_t m_sound_latch;
	int m_gfx_type;
	tilemap_t *m_background;

	// shangkid and chinhero
	DECLARE_WRITE_LINE_MEMBER(sound_enable_w);
	DECLARE_WRITE_LINE_MEMBER(int_enable_1_w);
	DECLARE_WRITE_LINE_MEMBER(int_enable_2_w);
	DECLARE_WRITE_LINE_MEMBER(nmi_enable_1_w);
	DECLARE_WRITE_LINE_MEMBER(nmi_enable_2_w);
	DECLARE_WRITE_LINE_MEMBER(irq_1_w);
	DECLARE_WRITE_LINE_MEMBER(irq_2_w);
	DECLARE_WRITE8_MEMBER(nmiq_1_w);
	DECLARE_WRITE8_MEMBER(nmiq_2_w);
	DECLARE_WRITE_LINE_MEMBER(coin_counter_1_w);
	DECLARE_WRITE_LINE_MEMBER(coin_counter_2_w);
	DECLARE_READ8_MEMBER(soundlatch_r);
	DECLARE_WRITE8_MEMBER(videoram_w);
	DECLARE_WRITE8_MEMBER(ay8910_portb_w);

	// game specific
	DECLARE_WRITE8_MEMBER(chinhero_ay8910_porta_w);
	DECLARE_WRITE8_MEMBER(shangkid_ay8910_porta_w);

	TILE_GET_INFO_MEMBER(get_bg_tile_info);

	DECLARE_DRIVER_INIT(dynamski);
	DECLARE_DRIVER_INIT(shangkid);
	DECLARE_DRIVER_INIT(chinhero);
	DECLARE_VIDEO_START(shangkid);
	DECLARE_PALETTE_INIT(dynamski);
	DECLARE_MACHINE_RESET(shangkid);

	uint32_t screen_update_shangkid(screen_device &screen, bitmap_ind16 &bitmap, const rectangle &cliprect);
	uint32_t screen_update_dynamski(screen_device &screen, bitmap_ind16 &bitmap, const rectangle &cliprect);
	void draw_sprite(const uint8_t *source, bitmap_ind16 &bitmap, const rectangle &cliprect);
	void shangkid_draw_sprites(bitmap_ind16 &bitmap, const rectangle &cliprect);
	void dynamski_draw_background(bitmap_ind16 &bitmap, const rectangle &cliprect, int pri );
	void dynamski_draw_sprites(bitmap_ind16 &bitmap, const rectangle &cliprect );
};
