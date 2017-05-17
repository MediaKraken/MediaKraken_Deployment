// license:BSD-3-Clause
// copyright-holders:Samuele Zannoli

#include "emu.h"
#include "includes/xbox.h"

#include "cpu/i386/i386.h"
#ifdef USE_LEGACY_PCI
#include "machine/lpci.h"
#else
#include "machine/pci.h"
#include "machine/pci-ide.h"
#endif
#include "machine/pit8253.h"
#include "debug/debugcon.h"
#include "debug/debugcmd.h"

#include "debugger.h"

#include "bitmap.h"

#include <functional>

#define LOG_PCI
//#define LOG_AUDIO

const xbox_base_state::debugger_constants xbox_base_state::debugp[] = {
	{ 0x66232714, {0x8003aae0, 0x5c, 0x1c, 0x28, 0x210, 8, 0x28, 0x1c} },
	{ 0x49d8055a, {0x8003aae0, 0x5c, 0x1c, 0x28, 0x210, 8, 0x28, 0x1c} }
};

int xbox_base_state::find_bios_index(running_machine &mach)
{
	u8 sb = mach.driver_data()->system_bios();
	return sb;
}

bool xbox_base_state::find_bios_hash(running_machine &mach, int bios, uint32_t &crc32)
{
	uint32_t crc = 0;
	const std::vector<rom_entry> &rev = mach.root_device().rom_region_vector();

	for (rom_entry re : rev)
	{
		if ((re.flags() & ROMENTRY_TYPEMASK) == ROMENTRYTYPE_ROM)
		{
			if ((re.flags() & ROM_BIOSFLAGSMASK) == ROM_BIOS(bios + 1))
			{
				const std::string &h = re.hashdata();
				util::hash_collection hc(h.c_str());
				if (hc.crc(crc) == true)
				{
					crc32 = crc;
					return true;
				}
			}
		}
	}
	return false;
}

void xbox_base_state::find_debug_params(running_machine &mach)
{
	uint32_t crc;
	int sb;

	sb = (int)find_bios_index(machine());
	debugc_bios = debugp;
	if (find_bios_hash(machine(), sb - 1, crc) == true)
	{
		for (int n = 0; n < 2; n++)
			if (debugp[n].id == crc)
			{
				debugc_bios = &debugp[n];
				break;
			}
	}
}

void xbox_base_state::dump_string_command(int ref, const std::vector<std::string> &params)
{
	debugger_cpu &cpu = machine().debugger().cpu();
	debugger_console &con = machine().debugger().console();
	address_space &space = m_maincpu->space();
	uint64_t addr;
	offs_t address;

	if (params.size() < 2)
		return;

	if (!machine().debugger().commands().validate_number_parameter(params[1], addr))
		return;

	address = (offs_t)addr;
	if (!m_maincpu->translate(AS_PROGRAM, TRANSLATE_READ_DEBUG, address))
	{
		con.printf("Address is unmapped.\n");
		return;
	}
	address = (offs_t)addr;

	uint32_t length = cpu.read_word(space, address, true);
	uint32_t maximumlength = cpu.read_word(space, address + 2, true);
	offs_t buffer = cpu.read_dword(space, address + 4, true);
	con.printf("Length %d word\n", length);
	con.printf("MaximumLength %d word\n", maximumlength);
	con.printf("Buffer %08X byte* ", buffer);

	// limit the number of characters to avoid flooding
	if (length > 256)
		length = 256;

	for (int a = 0; a < length; a++)
	{
		uint8_t c = cpu.read_byte(space, buffer + a, true);
		con.printf("%c", c);
	}
	con.printf("\n");
}

void xbox_base_state::dump_process_command(int ref, const std::vector<std::string> &params)
{
	debugger_cpu &cpu = machine().debugger().cpu();
	debugger_console &con = machine().debugger().console();
	address_space &space = m_maincpu->space();
	uint64_t addr;
	offs_t address;

	if (params.size() < 2)
		return;

	if (!machine().debugger().commands().validate_number_parameter(params[1], addr))
		return;

	address = (offs_t)addr;
	if (!m_maincpu->translate(AS_PROGRAM, TRANSLATE_READ_DEBUG, address))
	{
		con.printf("Address is unmapped.\n");
		return;
	}
	address = (offs_t)addr;

	con.printf("ReadyListHead {%08X,%08X} _LIST_ENTRY\n", cpu.read_dword(space, address, true), cpu.read_dword(space, address + 4, true));
	con.printf("ThreadListHead {%08X,%08X} _LIST_ENTRY\n", cpu.read_dword(space, address + 8, true), cpu.read_dword(space, address + 12, true));
	con.printf("StackCount %d dword\n", cpu.read_dword(space, address + 16, true));
	con.printf("ThreadQuantum %d dword\n", cpu.read_dword(space, address + 20, true));
	con.printf("BasePriority %d byte\n", cpu.read_byte(space, address + 24, true));
	con.printf("DisableBoost %d byte\n", cpu.read_byte(space, address + 25, true));
	con.printf("DisableQuantum %d byte\n", cpu.read_byte(space, address + 26, true));
	con.printf("_padding %d byte\n", cpu.read_byte(space, address + 27, true));
}

void xbox_base_state::dump_list_command(int ref, const std::vector<std::string> &params)
{
	debugger_cpu &cpu = machine().debugger().cpu();
	debugger_console &con = machine().debugger().console();
	address_space &space = m_maincpu->space();
	uint64_t addr;
	offs_t address;

	if (params.size() < 2)
		return;

	if (!machine().debugger().commands().validate_number_parameter(params[1], addr))
		return;

	uint64_t offs = 0;
	offs_t offset = 0;
	if (params.size() >= 3)
	{
		if (!machine().debugger().commands().validate_number_parameter(params[2], offs))
			return;
		offset = (offs_t)offs;
	}

	uint64_t start = addr;
	address = (offs_t)addr;
	if (!m_maincpu->translate(AS_PROGRAM, TRANSLATE_READ_DEBUG, address))
	{
		con.printf("Address is unmapped.\n");
		return;
	}
	address = (offs_t)addr;
	if (params.size() >= 3)
		con.printf("Entry    Object\n");
	else
		con.printf("Entry\n");

	uint64_t old;
	for (int num = 0; num < 32; num++)
	{
		if (params.size() >= 3)
			con.printf("%08X %08X\n", (uint32_t)addr, (offs_t)addr - offset);
		else
			con.printf("%08X\n", (uint32_t)addr);
		old = addr;
		addr = cpu.read_dword(space, address, true);
		if (addr == start)
			break;
		if (addr == old)
			break;
		address = (offs_t)addr;
		if (!m_maincpu->translate(AS_PROGRAM, TRANSLATE_READ_DEBUG, address))
			break;
		address = (offs_t)addr;
	}
}

void xbox_base_state::dump_dpc_command(int ref, const std::vector<std::string> &params)
{
	debugger_cpu &cpu = machine().debugger().cpu();
	debugger_console &con = machine().debugger().console();
	address_space &space = m_maincpu->space();
	uint64_t addr;
	offs_t address;

	if (params.size() < 2)
		return;

	if (!machine().debugger().commands().validate_number_parameter(params[1], addr))
		return;

	address = (offs_t)addr;
	if (!m_maincpu->translate(AS_PROGRAM, TRANSLATE_READ_DEBUG, address))
	{
		con.printf("Address is unmapped.\n");
		return;
	}
	address = (offs_t)addr;
	con.printf("Type %d word\n", cpu.read_word(space, address, true));
	con.printf("Inserted %d byte\n", cpu.read_byte(space, address + 2, true));
	con.printf("Padding %d byte\n", cpu.read_byte(space, address + 3, true));
	con.printf("DpcListEntry {%08X,%08X} _LIST_ENTRY\n", cpu.read_dword(space, address + 4, true), cpu.read_dword(space, address + 8, true));
	con.printf("DeferredRoutine %08X dword\n", cpu.read_dword(space, address + 12, true));
	con.printf("DeferredContext %08X dword\n", cpu.read_dword(space, address + 16, true));
	con.printf("SystemArgument1 %08X dword\n", cpu.read_dword(space, address + 20, true));
	con.printf("SystemArgument2 %08X dword\n", cpu.read_dword(space, address + 24, true));
}

void xbox_base_state::dump_timer_command(int ref, const std::vector<std::string> &params)
{
	debugger_cpu &cpu = machine().debugger().cpu();
	debugger_console &con = machine().debugger().console();
	address_space &space = m_maincpu->space();
	uint64_t addr;
	offs_t address;

	if (params.size() < 2)
		return;

	if (!machine().debugger().commands().validate_number_parameter(params[1], addr))
		return;

	address = (offs_t)addr;
	if (!m_maincpu->translate(AS_PROGRAM, TRANSLATE_READ_DEBUG, address))
	{
		con.printf("Address is unmapped.\n");
		return;
	}
	address = (offs_t)addr;
	con.printf("Header.Type %d byte\n", cpu.read_byte(space, address, true));
	con.printf("Header.Absolute %d byte\n", cpu.read_byte(space, address + 1, true));
	con.printf("Header.Size %d byte\n", cpu.read_byte(space, address + 2, true));
	con.printf("Header.Inserted %d byte\n", cpu.read_byte(space, address + 3, true));
	con.printf("Header.SignalState %08X dword\n", cpu.read_dword(space, address + 4, true));
	con.printf("Header.WaitListEntry {%08X,%08X} _LIST_ENTRY\n", cpu.read_dword(space, address + 8, true), cpu.read_dword(space, address + 12, true));
	con.printf("%s", string_format("DueTime %I64x qword\n", (int64_t)cpu.read_qword(space, address + 16, true)).c_str());
	con.printf("TimerListEntry {%08X,%08X} _LIST_ENTRY\n", cpu.read_dword(space, address + 24, true), cpu.read_dword(space, address + 28, true));
	con.printf("Dpc %08X dword\n", cpu.read_dword(space, address + 32, true));
	con.printf("Period %d dword\n", cpu.read_dword(space, address + 36, true));
}

void xbox_base_state::curthread_command(int ref, const std::vector<std::string> &params)
{
	debugger_cpu &cpu = machine().debugger().cpu();
	debugger_console &con = machine().debugger().console();
	address_space &space = m_maincpu->space();
	offs_t address;

	uint64_t fsbase = m_maincpu->state_int(44); // base of FS register
	address = (offs_t)fsbase + (offs_t)debugc_bios->parameter[7-1];
	if (!m_maincpu->translate(AS_PROGRAM, TRANSLATE_READ_DEBUG, address))
	{
		con.printf("Address is unmapped.\n");
		return;
	}
	address = (offs_t)fsbase + (offs_t)debugc_bios->parameter[7-1];

	uint32_t kthrd = cpu.read_dword(space, address, true);
	con.printf("Current thread is %08X\n", kthrd);
	address = (offs_t)(kthrd + debugc_bios->parameter[8-1]);
	uint32_t topstack = cpu.read_dword(space, address, true);
	con.printf("Current thread stack top is %08X\n", topstack);
	address = (offs_t)(kthrd + debugc_bios->parameter[4-1]);
	uint32_t tlsdata = cpu.read_dword(space, address, true);
	if (tlsdata == 0)
		address = (offs_t)(topstack - debugc_bios->parameter[5-1] - debugc_bios->parameter[6-1]);
	else
		address = (offs_t)(tlsdata - debugc_bios->parameter[6-1]);
	con.printf("Current thread function is %08X\n", cpu.read_dword(space, address, true));
}

void xbox_base_state::threadlist_command(int ref, const std::vector<std::string> &params)
{
	address_space &space = m_maincpu->space();
	debugger_cpu &cpu = machine().debugger().cpu();
	debugger_console &con = machine().debugger().console();

	con.printf("Pri. _KTHREAD   Stack  Function\n");
	con.printf("-------------------------------\n");
	for (int pri = 0; pri < 16; pri++)
	{
		uint32_t curr = debugc_bios->parameter[1 - 1] + pri * 8;
		uint32_t next = cpu.read_dword(space, curr, true);

		while ((next != curr) && (next != 0))
		{
			uint32_t kthrd = next - debugc_bios->parameter[2 - 1];
			uint32_t topstack = cpu.read_dword(space, kthrd + debugc_bios->parameter[3 - 1], true);
			uint32_t tlsdata = cpu.read_dword(space, kthrd + debugc_bios->parameter[4 - 1], true);
			uint32_t function;
			if (tlsdata == 0)
				function = cpu.read_dword(space, topstack - debugc_bios->parameter[5 - 1] - debugc_bios->parameter[6 - 1], true);
			else
				function = cpu.read_dword(space, tlsdata - debugc_bios->parameter[6 - 1], true);
			con.printf(" %02d  %08x %08x %08x\n", pri, kthrd, topstack, function);
			next = cpu.read_dword(space, next, true);
		}
	}
}

void xbox_base_state::generate_irq_command(int ref, const std::vector<std::string> &params)
{
	uint64_t irq;

	if (params.size() < 2)
		return;
	if (!machine().debugger().commands().validate_number_parameter(params[1], irq))
		return;
	if (irq > 15)
		return;
	if (irq == 2)
		return;
	debug_generate_irq((int)irq, true);
}

void xbox_base_state::nv2a_combiners_command(int ref, const std::vector<std::string> &params)
{
	debugger_console &con = machine().debugger().console();
	bool en = nvidia_nv2a->toggle_register_combiners_usage();
	if (en == true)
		con.printf("Register combiners enabled\n");
	else
		con.printf("Register combiners disabled\n");
}

void xbox_base_state::nv2a_wclipping_command(int ref, const std::vector<std::string> &params)
{
	debugger_console &con = machine().debugger().console();
	bool en = nvidia_nv2a->toggle_clipping_w_support();
	if (en == true)
		con.printf("W clipping enabled\n");
	else
		con.printf("W clipping disabled\n");
}

void xbox_base_state::waitvblank_command(int ref, const std::vector<std::string> &params)
{
	debugger_console &con = machine().debugger().console();
	bool en = nvidia_nv2a->toggle_wait_vblank_support();
	if (en == true)
		con.printf("Vblank method enabled\n");
	else
		con.printf("Vblank method disabled\n");
}

void xbox_base_state::grab_texture_command(int ref, const std::vector<std::string> &params)
{
	uint64_t type;

	if (params.size() < 3)
		return;
	if (!machine().debugger().commands().validate_number_parameter(params[1], type))
		return;
	if (params[2].empty() || params[2].length() > 127)
		return;
	nvidia_nv2a->debug_grab_texture((int)type, params[2].c_str());
}

void xbox_base_state::grab_vprog_command(int ref, const std::vector<std::string> &params)
{
	uint32_t instruction[4];
	FILE *fil;

	if (params.size() < 2)
		return;
	if (params[1].empty() || params[1].length() > 127)
		return;
	if ((fil = fopen(params[1].c_str(), "wb")) == nullptr)
		return;
	for (int n = 0; n < 136; n++) {
		nvidia_nv2a->debug_grab_vertex_program_slot(n, instruction);
		fwrite(instruction, sizeof(uint32_t), 4, fil);
	}
	fclose(fil);
}

void xbox_base_state::vprogdis_command(int ref, const std::vector<std::string> &params)
{
	address_space &space = m_maincpu->space();

	if (params.size() < 3)
		return;

	uint64_t address;
	if (!machine().debugger().commands().validate_number_parameter(params[1], address))
		return;

	uint64_t length;
	if (!machine().debugger().commands().validate_number_parameter(params[2], length))
		return;

	uint64_t type = 0;
	if (params.size() > 3)
		if (!machine().debugger().commands().validate_number_parameter(params[3], type))
			return;

	vertex_program_disassembler vd;
	while (length > 0)
	{
		uint32_t instruction[4];
		if (type == 1)
		{
			offs_t addr = (offs_t)address;
			if (!m_maincpu->translate(AS_PROGRAM, TRANSLATE_READ_DEBUG, addr))
				return;
			instruction[0] = space.read_dword_unaligned(address);
			instruction[1] = space.read_dword_unaligned(address + 4);
			instruction[2] = space.read_dword_unaligned(address + 8);
			instruction[3] = space.read_dword_unaligned(address + 12);
		}
		else
		{
			nvidia_nv2a->debug_grab_vertex_program_slot((int)address, instruction);
		}

		char line[64];
		while (vd.disassemble(instruction, line) != 0)
			machine().debugger().console().printf("%s\n", line);

		if (type == 1)
			address = address + 4 * 4;
		else
			address++;

		length--;
	}
}

void xbox_base_state::help_command(int ref, const std::vector<std::string> &params)
{
	debugger_console &con = machine().debugger().console();

	con.printf("Available Xbox commands:\n");
	con.printf("  xbox dump_string,<address> -- Dump _STRING object at <address>\n");
	con.printf("  xbox dump_process,<address> -- Dump _PROCESS object at <address>\n");
	con.printf("  xbox dump_list,<address>[,<offset>] -- Dump _LIST_ENTRY chain starting at <address>\n");
	con.printf("  xbox dump_dpc,<address> -- Dump _KDPC object at <address>\n");
	con.printf("  xbox dump_timer,<address> -- Dump _KTIMER object at <address>\n");
	con.printf("  xbox curthread -- Print information about current thread\n");
	con.printf("  xbox threadlist -- list of currently active threads\n");
	con.printf("  xbox irq,<number> -- Generate interrupt with irq number 0-15\n");
	con.printf("  xbox nv2a_combiners -- Toggle use of register combiners\n");
	con.printf("  xbox nv2a_wclipping -- Toggle use of negative w vertex clipping\n");
	con.printf("  xbox waitvblank -- Toggle support for wait vblank method\n");
	con.printf("  xbox grab_texture,<type>,<filename> -- Save to <filename> the next used texture of type <type>\n");
	con.printf("  xbox grab_vprog,<filename> -- save current vertex program instruction slots to <filename>\n");
	con.printf("  xbox vprogdis,<address>,<length>[,<type>] -- disassemble <lenght> vertex program instructions at <address> of <type>\n");
	con.printf("  xbox help -- this list\n");
}

void xbox_base_state::xbox_debug_commands(int ref, const std::vector<std::string> &params)
{
	if (params.size() < 1)
		return;
	if (params[0] == "dump_string")
		dump_string_command(ref, params);
	else if (params[0] == "dump_process")
		dump_process_command(ref, params);
	else if (params[0] == "dump_list")
		dump_list_command(ref, params);
	else if (params[0] == "dump_dpc")
		dump_dpc_command(ref, params);
	else if (params[0] == "dump_timer")
		dump_timer_command(ref, params);
	else if (params[0] == "curthread")
		curthread_command(ref, params);
	else if (params[0] == "threadlist")
		threadlist_command(ref, params);
	else if (params[0] == "irq")
		generate_irq_command(ref, params);
	else if (params[0] == "nv2a_combiners")
		nv2a_combiners_command(ref, params);
	else if (params[0] == "nv2a_wclipping")
		nv2a_wclipping_command(ref, params);
	else if (params[0] == "waitvblank")
		waitvblank_command(ref, params);
	else if (params[0] == "grab_texture")
		grab_texture_command(ref, params);
	else if (params[0] == "grab_vprog")
		grab_vprog_command(ref, params);
	else if (params[0] == "vprogdis")
		vprogdis_command(ref, params);
	else
		help_command(ref, params);
}

void xbox_base_state::debug_generate_irq(int irq, bool active)
{
	int state;

	if (active)
	{
		debug_irq_active = true;
		debug_irq_number = irq;
		state = 1;
	}
	else
	{
		debug_irq_active = false;
		state = 0;
	}
	switch (irq)
	{
	case 0:
		xbox_base_devs.pic8259_1->ir0_w(state);
		break;
	case 1:
		xbox_base_devs.pic8259_1->ir1_w(state);
		break;
	case 3:
		xbox_base_devs.pic8259_1->ir3_w(state);
		break;
	case 4:
		xbox_base_devs.pic8259_1->ir4_w(state);
		break;
	case 5:
		xbox_base_devs.pic8259_1->ir5_w(state);
		break;
	case 6:
		xbox_base_devs.pic8259_1->ir6_w(state);
		break;
	case 7:
		xbox_base_devs.pic8259_1->ir7_w(state);
		break;
	case 8:
		xbox_base_devs.pic8259_2->ir0_w(state);
		break;
	case 9:
		xbox_base_devs.pic8259_2->ir1_w(state);
		break;
	case 10:
		xbox_base_devs.pic8259_2->ir2_w(state);
		break;
	case 11:
		xbox_base_devs.pic8259_2->ir3_w(state);
		break;
	case 12:
		xbox_base_devs.pic8259_2->ir4_w(state);
		break;
	case 13:
		xbox_base_devs.pic8259_2->ir5_w(state);
		break;
	case 14:
		xbox_base_devs.pic8259_2->ir6_w(state);
		break;
	case 15:
		xbox_base_devs.pic8259_2->ir7_w(state);
		break;
	}
}

WRITE_LINE_MEMBER(xbox_base_state::vblank_callback)
{
	nvidia_nv2a->vblank_callback(state);
}

uint32_t xbox_base_state::screen_update_callback(screen_device &screen, bitmap_rgb32 &bitmap, const rectangle &cliprect)
{
	return nvidia_nv2a->screen_update_callback(screen, bitmap, cliprect);
}

#ifdef USE_LEGACY_PCI
READ32_MEMBER(xbox_base_state::geforce_r)
{
	return nvidia_nv2a->geforce_r(space, offset, mem_mask);
}

WRITE32_MEMBER(xbox_base_state::geforce_w)
{
	nvidia_nv2a->geforce_w(space, offset, data, mem_mask);
}

static uint32_t geforce_pci_r(device_t *busdevice, device_t *device, int function, int reg, uint32_t mem_mask)
{
#ifdef LOG_PCI
	busdevice->logerror("  bus:1 device:NV_2A function:%d register:%d mask:%08X\n",function,reg,mem_mask);
#endif
	return 0;
}

static void geforce_pci_w(device_t *busdevice, device_t *device, int function, int reg, uint32_t data, uint32_t mem_mask)
{
#ifdef LOG_PCI
	busdevice->logerror("  bus:1 device:NV_2A function:%d register:%d data:%08X mask:%08X\n",function,reg,data,mem_mask);
#endif
}
#endif

/*
 * Audio
 */

READ32_MEMBER(xbox_base_state::audio_apu_r)
{
#ifdef LOG_AUDIO
	logerror("Audio_APU: read from %08X mask %08X\n", 0xfe800000 + offset * 4, mem_mask);
#endif
	if (offset == 0x20010 / 4) // some kind of internal counter or state value
		return 0x20 + 4 + 8 + 0x48 + 0x80;
	return apust.memory[offset];
}

WRITE32_MEMBER(xbox_base_state::audio_apu_w)
{
	//uint32_t old;
	uint32_t v;

#ifdef LOG_AUDIO
	logerror("Audio_APU: write at %08X mask %08X value %08X\n", 0xfe800000 + offset * 4, mem_mask, data);
#endif
	//old = apust.memory[offset];
	apust.memory[offset] = data;
	if (offset == 0x02040 / 4) // address of memory area with scatter-gather info (gpdsp scratch dma)
		apust.gpdsp_sgaddress = data;
	if (offset == 0x020d4 / 4) { // block count (gpdsp)
		apust.gpdsp_sgblocks = data;
		apust.gpdsp_address = apust.space->read_dword(apust.gpdsp_sgaddress); // memory address of first block
		apust.timer->enable();
		apust.timer->adjust(attotime::from_msec(1), 0, attotime::from_msec(1));
	}
	if (offset == 0x02048 / 4) // (epdsp scratch dma)
		apust.epdsp_sgaddress = data;
	if (offset == 0x020dc / 4) // (epdsp)
		apust.epdsp_sgblocks = data;
	if (offset == 0x0204c / 4) // address of memory area with information about blocks
		apust.unknown_sgaddress = data;
	if (offset == 0x020e0 / 4) // block count - 1
		apust.unknown_sgblocks = data;
	if (offset == 0x0202c / 4) { // address of memory area with 0x80 bytes for each voice
		apust.voicedata_address = data;
		return;
	}
	if (offset == 0x04024 / 4) // offset in memory area indicated by 0x204c (analog output ?)
		return;
	if (offset == 0x04034 / 4) // size
		return;
	if (offset == 0x04028 / 4) // offset in memory area indicated by 0x204c (digital output ?)
		return;
	if (offset == 0x04038 / 4) // size
		return;
	if (offset == 0x20804 / 4) { // block number for scatter-gather heap that stores sampled audio to be played
		if (data >= 1024) {
			logerror("Audio_APU: sg block number too high, increase size of voices_heap_blockaddr\n");
			apust.memory[offset] = 1023;
		}
		return;
	}
	if (offset == 0x20808 / 4) { // block address for scatter-gather heap that stores sampled audio to be played
		apust.voices_heap_blockaddr[apust.memory[0x20804 / 4]] = data;
		return;
	}
	if (offset == 0x202f8 / 4) { // voice number for parameters ?
		apust.voice_number = data;
		return;
	}
	if (offset == 0x202fc / 4) // 1 when accessing voice parameters 0 otherwise
		return;
	if (offset == 0x20304 / 4) { // format
		/*
		bits 28-31 sample format:
		0  8-bit pcm
		5  16-bit pcm
		10 adpcm ?
		14 24-bit pcm
		15 32-bit pcm
		bits 16-20 number of channels - 1:
		0  mono
		1  stereo
		*/
		return;
	}
	if (offset == 0x2037c / 4) { // value related to sample rate
		int16_t v0 = (int16_t)(data >> 16); // upper 16 bits as a signed 16 bit value
		float vv = ((float)v0) / 4096.0f; // divide by 4096
		float vvv = powf(2, vv); // two to the vv
		int f = vvv*48000.0f; // sample rate
		apust.voices_frequency[apust.voice_number] = f;
		return;
	}
	if (offset == 0x203a0 / 4) // start offset of data in scatter-gather heap
		return;
	if (offset == 0x203a4 / 4) { // first sample to play
		apust.voices_position_start[apust.voice_number] = data * 1000;
		return;
	}
	if (offset == 0x203dc / 4) { // last sample to play
		apust.voices_position_end[apust.voice_number] = data * 1000;
		return;
	}
	if (offset == 0x2010c / 4) // voice processor 0 idle 1 not idle ?
		return;
	if (offset == 0x20124 / 4) { // voice number to activate ?
		v = apust.voice_number;
		apust.voices_active[v >> 6] |= ((uint64_t)1 << (v & 63));
		apust.voices_position[v] = apust.voices_position_start[apust.voice_number];
		apust.voices_position_increment[apust.voice_number] = apust.voices_frequency[apust.voice_number];
		return;
	}
	if (offset == 0x20128 / 4) { // voice number to deactivate ?
		v = apust.voice_number;
		apust.voices_active[v >> 6] &= ~(1 << (v & 63));
		return;
	}
	if (offset == 0x20140 / 4) // voice number to ?
		return;
	if ((offset >= 0x20200 / 4) && (offset < 0x20280 / 4)) // headroom for each of the 32 mixbins
		return;
	if (offset == 0x20280 / 4) // hrtf headroom ?
		return;
}

READ32_MEMBER(xbox_base_state::audio_ac93_r)
{
	uint32_t ret = 0;

#ifdef LOG_AUDIO
	logerror("Audio_AC3: read from %08X mask %08X\n", 0xfec00000 + offset * 4, mem_mask);
#endif
	if (offset < 0x80 / 4)
	{
		ret = ac97st.mixer_regs[offset];
	}
	if ((offset >= 0x100 / 4) && (offset <= 0x138 / 4))
	{
		offset = offset - 0x100 / 4;
		if (offset == 0x18 / 4)
		{
			ac97st.controller_regs[offset] &= ~0x02000000; // REGRST: register reset
		}
		if (offset == 0x30 / 4)
		{
			ac97st.controller_regs[offset] |= 0x100; // PCRDY: primary codec ready
		}
		if (offset == 0x34 / 4)
		{
			ac97st.controller_regs[offset] &= ~1; // CAS: codec access semaphore
		}
		ret = ac97st.controller_regs[offset];
	}
	return ret;
}

WRITE32_MEMBER(xbox_base_state::audio_ac93_w)
{
#ifdef LOG_AUDIO
	logerror("Audio_AC3: write at %08X mask %08X value %08X\n", 0xfec00000 + offset * 4, mem_mask, data);
#endif
	if (offset < 0x80 / 4)
	{
		COMBINE_DATA(ac97st.mixer_regs + offset);
	}
	if ((offset >= 0x100 / 4) && (offset <= 0x138 / 4))
	{
		offset = offset - 0x100 / 4;
		COMBINE_DATA(ac97st.controller_regs + offset);
	}
}

TIMER_CALLBACK_MEMBER(xbox_base_state::audio_apu_timer)
{
	int cmd;
	int bb, b, v;
	uint64_t bv;
	uint32_t phys;

	cmd = apust.space->read_dword(apust.gpdsp_address + 0x800 + 0x10);
	if (cmd == 3)
		apust.space->write_dword(apust.gpdsp_address + 0x800 + 0x10, 0);
	/*else
	logerror("Audio_APU: unexpected value at address %d\n",apust.gpdsp_address+0x800+0x10);*/
	for (b = 0; b < 4; b++) {
		bv = 1;
		for (bb = 0; bb < 64; bb++) {
			if (apust.voices_active[b] & bv) {
				v = bb + (b << 6);
				apust.voices_position[v] += apust.voices_position_increment[v];
				while (apust.voices_position[v] >= apust.voices_position_end[v])
					apust.voices_position[v] = apust.voices_position_start[v] + apust.voices_position[v] - apust.voices_position_end[v] - 1000;
				phys = apust.voicedata_address + 0x80 * v;
				apust.space->write_dword(phys + 0x58, apust.voices_position[v] / 1000);
			}
			bv = bv << 1;
		}
	}
}

#ifdef USE_LEGACY_PCI
static uint32_t pcibridghostbridg_pci_r(device_t *busdevice, device_t *device, int function, int reg, uint32_t mem_mask)
{
#ifdef LOG_PCI
	busdevice->logerror("  bus:0 function:%d register:%d mask:%08X\n",function,reg,mem_mask);
#endif
	if ((function == 3) && (reg == 0x6c))
		return 0x08800044;
	return 0;
}

static void pcibridghostbridg_pci_w(device_t *busdevice, device_t *device, int function, int reg, uint32_t data, uint32_t mem_mask)
{
#ifdef LOG_PCI
	busdevice->logerror("  bus:0 function:%d register:%d data:%08X mask:%08X\n", function, reg, data, mem_mask);
#endif
}

static uint32_t hubintisabridg_pci_r(device_t *busdevice, device_t *device, int function, int reg, uint32_t mem_mask)
{
#ifdef LOG_PCI
	busdevice->logerror("  bus:0 function:%d register:%d mask:%08X\n",function,reg,mem_mask);
#endif
	if ((function == 0) && (reg == 8))
		return 0xb4; // 0:1:0 revision id must be at least 0xb4, otherwise usb will require a hub
	return 0;
}

static void hubintisabridg_pci_w(device_t *busdevice, device_t *device, int function, int reg, uint32_t data, uint32_t mem_mask)
{
#ifdef LOG_PCI
	busdevice->logerror("  bus:0 function:%d register:%d data:%08X mask:%08X\n", function, reg, data, mem_mask);
#endif
}
#endif

/*
 * dummy for non connected devices
 */

#ifdef USE_LEGACY_PCI
static uint32_t dummy_pci_r(device_t *busdevice, device_t *device, int function, int reg, uint32_t mem_mask)
{
#ifdef LOG_PCI
	busdevice->logerror("  bus:0 function:%d register:%d mask:%08X\n",function,reg,mem_mask);
#endif
	return 0;
}

static void dummy_pci_w(device_t *busdevice, device_t *device, int function, int reg, uint32_t data, uint32_t mem_mask)
{
#ifdef LOG_PCI
	busdevice->logerror("  bus:0 function:%d register:%d data:%08X mask:%08X\n", function, reg, data, mem_mask);
#endif
}
#endif

READ32_MEMBER(xbox_base_state::dummy_r)
{
	return 0;
}

WRITE32_MEMBER(xbox_base_state::dummy_w)
{
}

/*
 * PIC & PIT
 */

WRITE_LINE_MEMBER(xbox_base_state::xbox_pic8259_1_set_int_line)
{
	m_maincpu->set_input_line(0, state ? HOLD_LINE : CLEAR_LINE);
}

READ8_MEMBER(xbox_base_state::get_slave_ack)
{
	if (offset == 2) { // IRQ = 2
		return xbox_base_devs.pic8259_2->acknowledge();
	}
	return 0x00;
}

IRQ_CALLBACK_MEMBER(xbox_base_state::irq_callback)
{
	int r = 0;
	r = xbox_base_devs.pic8259_1->acknowledge();
	if (debug_irq_active)
		debug_generate_irq(debug_irq_number, false);
	return r;
}

WRITE_LINE_MEMBER(xbox_base_state::xbox_pit8254_out0_changed)
{
	if (xbox_base_devs.pic8259_1)
	{
		xbox_base_devs.pic8259_1->ir0_w(state);
	}
}

WRITE_LINE_MEMBER(xbox_base_state::xbox_pit8254_out2_changed)
{
	//xbox_speaker_set_input( state ? 1 : 0 );
}

/*
 * SMbus devices
 */

int smbus_callback_pic16lc(xbox_base_state &chs, int command, int rw, int data)
{
	return chs.smbus_pic16lc(command, rw, data);
}

int xbox_base_state::smbus_pic16lc(int command, int rw, int data)
{
	if (rw == 1) { // read
		if (command == 0) {
			if (pic16lc_buffer[0] == 'D')
				pic16lc_buffer[0] = 'X';
			else if (pic16lc_buffer[0] == 'X')
				pic16lc_buffer[0] = 'B';
			else if (pic16lc_buffer[0] == 'B')
				pic16lc_buffer[0] = 'D';
		}
		logerror("pic16lc: %d %d %d\n", command, rw, pic16lc_buffer[command]);
		return pic16lc_buffer[command];
	}
	else
		if (command == 0)
			pic16lc_buffer[0] = 'B';
		else
			pic16lc_buffer[command] = (uint8_t)data;
	logerror("pic16lc: %d %d %d\n", command, rw, data);
	return 0;
}

int smbus_callback_cx25871(xbox_base_state &chs, int command, int rw, int data)
{
	return chs.smbus_cx25871(command, rw, data);
}

int xbox_base_state::smbus_cx25871(int command, int rw, int data)
{
	logerror("cx25871: %d %d %d\n", command, rw, data);
	return 0;
}

// let's try to fake the missing eeprom, make sure its ntsc, otherwise chihiro will show an error
static int dummyeeprom[256] = {
	0x39, 0xe3, 0xcc, 0x81, 0xb0, 0xa9, 0x97, 0x09, 0x57, 0xac, 0x57, 0x12, 0xf7, 0xc2, 0xc0, 0x21, 0xce, 0x0d, 0x0a, 0xdb, 0x20, 0x7a, 0xf3, 0xff,
	0xdf, 0x67, 0xed, 0xf4, 0xf8, 0x95, 0x5c, 0xd0, 0x9b, 0xef, 0x7b, 0x81, 0xda, 0xd5, 0x98, 0xc1, 0xb1, 0xb3, 0x74, 0x18, 0x86, 0x05, 0xe2, 0x7c,
	0xd1, 0xad, 0xc9, 0x90, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x41, 0x42, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x00, 0x00,
	0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0xab, 0xcd, 0xef, 0xba, 0xdc, 0xfe, 0xa1, 0xb2, 0xc3, 0xd3, 0x00, 0x01, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00,
	0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
	0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

int smbus_callback_eeprom(xbox_base_state &chs, int command, int rw, int data)
{
	return chs.smbus_eeprom(command, rw, data);
}

int xbox_base_state::smbus_eeprom(int command, int rw, int data)
{
	if (command >= 112)
		return 0;
	if (rw == 1) { // if reading
		// hack to avoid hanging if eeprom contents are not correct
		// this would need dumping the serial eeprom on the xbox board
		if (command == 0) {
			hack_eeprom();
		}
		data = dummyeeprom[command] + dummyeeprom[command + 1] * 256;
		logerror("eeprom: %d %d %d\n", command, rw, data);
		return data;
	}
	logerror("eeprom: %d %d %d\n", command, rw, data);
	dummyeeprom[command] = data;
	return 0;
}

/*
 * SMbus controller
 */

void xbox_base_state::smbus_register_device(int address, int(*handler)(xbox_base_state &chs, int command, int rw, int data))
{
	if (address < 128)
		smbusst.devices[address] = handler;
}

READ32_MEMBER(xbox_base_state::smbus_r)
{
	if ((offset == 0) && (mem_mask == 0xff)) // 0 smbus status
		smbusst.words[offset] = (smbusst.words[offset] & ~mem_mask) | ((smbusst.status << 0) & mem_mask);
	if ((offset == 1) && ((mem_mask == 0x00ff0000) || (mem_mask == 0xffff0000))) // 6 smbus data
		smbusst.words[offset] = (smbusst.words[offset] & ~mem_mask) | ((smbusst.data << 16) & mem_mask);
	return smbusst.words[offset];
}

WRITE32_MEMBER(xbox_base_state::smbus_w)
{
	COMBINE_DATA(smbusst.words);
	if ((offset == 0) && (mem_mask == 0xff)) // 0 smbus status
	{
		if (!((smbusst.status ^ data) & 0x10)) // clearing interrupt
			xbox_base_devs.pic8259_2->ir3_w(0); // IRQ 11
		smbusst.status &= ~data;
	}
	if ((offset == 0) && (mem_mask == 0xff0000)) // 2 smbus control
	{
		data = data >> 16;
		smbusst.control = data;
		int cycletype = smbusst.control & 7;
		if (smbusst.control & 8) { // start
			if ((cycletype & 6) == 2)
			{
				if (smbusst.devices[smbusst.address])
					if (smbusst.rw == 0)
						smbusst.devices[smbusst.address](*this, smbusst.command, smbusst.rw, smbusst.data);
					else
						smbusst.data = smbusst.devices[smbusst.address](*this, smbusst.command, smbusst.rw, smbusst.data);
				else
					logerror("SMBUS: access to missing device at address %d\n", smbusst.address);
				smbusst.status |= 0x10;
				if (smbusst.control & 0x10)
				{
					xbox_base_devs.pic8259_2->ir3_w(1); // IRQ 11
				}
			}
		}
	}
	if ((offset == 1) && (mem_mask == 0xff)) // 4 smbus address
	{
		smbusst.address = data >> 1;
		smbusst.rw = data & 1;
	}
	if ((offset == 1) && ((mem_mask == 0x00ff0000) || (mem_mask == 0xffff0000))) // 6 smbus data
	{
		data = data >> 16;
		smbusst.data = data;
	}
	if ((offset == 2) && (mem_mask == 0xff)) // 8 smbus command
		smbusst.command = data;
	//if ((offset == 2) && (mem_mask == 0x00ff0000)) ;
}

READ32_MEMBER(xbox_base_state::smbus2_r)
{
	return 0;
}

WRITE32_MEMBER(xbox_base_state::smbus2_w)
{
}

/*
* Ethernet controller
*/

READ32_MEMBER(xbox_base_state::network_r)
{
	return 0;
}

WRITE32_MEMBER(xbox_base_state::network_w)
{
}

READ32_MEMBER(xbox_base_state::networkio_r)
{
	return 0;
}

WRITE32_MEMBER(xbox_base_state::networkio_w)
{
}

/*
 * SuperIO
 */

READ8_MEMBER(xbox_base_state::superio_read)
{
	if (superiost.configuration_mode == false)
		return 0;
	if (offset == 0) // index port 0x2e
		return superiost.index;
	if (offset == 1)
	{
		// data port 0x2f
		if (superiost.index < 0x30)
			return superiost.registers[0][superiost.index];
		return superiost.registers[superiost.selected][superiost.index];
	}
	return 0;
}

WRITE8_MEMBER(xbox_base_state::superio_write)
{
	if (superiost.configuration_mode == false)
	{
		// config port 0x2e
		if ((offset == 0) && (data == 0x55))
			superiost.configuration_mode = true;
		return;
	}
	if ((offset == 0) && (data == 0xaa))
	{
		// config port 0x2e
		superiost.configuration_mode = false;
		return;
	}
	if (offset == 0)
	{
		// index port 0x2e
		superiost.index = data;
	}
	if (offset == 1)
	{
		// data port 0x2f
		if (superiost.index < 0x30)
		{
			superiost.registers[0][superiost.index] = data;
			superiost.selected = superiost.registers[0][7];
		} else
		{
			superiost.registers[superiost.selected][superiost.index] = data;
			//if ((superiost.selected == 4) && (superiost.index == 0x30) && (data != 0))
			//  ; // add handlers 0x3f8- +7
		}
	}
}

READ8_MEMBER(xbox_base_state::superiors232_read)
{
	if (offset == 5)
		return 0x20;
	return 0;
}

WRITE8_MEMBER(xbox_base_state::superiors232_write)
{
	if (offset == 0)
	{
		printf("%c", data);
	}
}

READ32_MEMBER(xbox_base_state::ohci_usb_r)
{
	if (offset == 0) /* hacks needed until usb (and jvs) is implemented */
	{
		hack_usb();
	}
	return ohci_usb->read(space, offset, mem_mask);
}

WRITE32_MEMBER(xbox_base_state::ohci_usb_w)
{
	ohci_usb->write(space, offset, data, mem_mask);
}

READ32_MEMBER(xbox_base_state::ohci_usb2_r)
{
	return 0;
}

WRITE32_MEMBER(xbox_base_state::ohci_usb2_w)
{
}

ADDRESS_MAP_START(xbox_base_map, AS_PROGRAM, 32, xbox_base_state)
	AM_RANGE(0x00000000, 0x07ffffff) AM_RAM AM_SHARE("nv2a_share") // 128 megabytes
	AM_RANGE(0xf0000000, 0xf7ffffff) AM_RAM AM_SHARE("nv2a_share") // 3d accelerator wants this
#ifdef USE_LEGACY_PCI
	AM_RANGE(0xfd000000, 0xfdffffff) AM_RAM AM_READWRITE(geforce_r, geforce_w)
#endif
	AM_RANGE(0xfed00000, 0xfed003ff) AM_READWRITE(ohci_usb_r, ohci_usb_w)
	AM_RANGE(0xfed08000, 0xfed08fff) AM_READWRITE(ohci_usb2_r, ohci_usb2_w)
	AM_RANGE(0xfe800000, 0xfe87ffff) AM_READWRITE(audio_apu_r, audio_apu_w)
	AM_RANGE(0xfec00000, 0xfec00fff) AM_READWRITE(audio_ac93_r, audio_ac93_w)
	AM_RANGE(0xfef00000, 0xfef003ff) AM_READWRITE(network_r, network_w)
ADDRESS_MAP_END

ADDRESS_MAP_START(xbox_base_map_io, AS_IO, 32, xbox_base_state)
	AM_RANGE(0x0020, 0x0023) AM_DEVREADWRITE8("pic8259_1", pic8259_device, read, write, 0xffffffff)
	AM_RANGE(0x002c, 0x002f) AM_READWRITE8(superio_read, superio_write, 0xffff0000)
	AM_RANGE(0x0040, 0x0043) AM_DEVREADWRITE8("pit8254", pit8254_device, read, write, 0xffffffff)
	AM_RANGE(0x00a0, 0x00a3) AM_DEVREADWRITE8("pic8259_2", pic8259_device, read, write, 0xffffffff)
	AM_RANGE(0x01f0, 0x01f7) AM_DEVREADWRITE("ide", bus_master_ide_controller_device, read_cs0, write_cs0)
	AM_RANGE(0x03f8, 0x03ff) AM_READWRITE8(superiors232_read, superiors232_write, 0xffffffff)
#ifdef USE_LEGACY_PCI
	AM_RANGE(0x0cf8, 0x0cff) AM_DEVREADWRITE("pcibus", pci_bus_legacy_device, read, write)
#endif
	AM_RANGE(0x8000, 0x80ff) AM_READWRITE(dummy_r, dummy_w) // lpc bridge
	AM_RANGE(0xc000, 0xc00f) AM_READWRITE(smbus_r, smbus_w)
	AM_RANGE(0xc200, 0xc21f) AM_READWRITE(smbus2_r, smbus2_w)
	AM_RANGE(0xd000, 0xd0ff) AM_NOP // ac97
	AM_RANGE(0xd200, 0xd27f) AM_NOP // ac97
	AM_RANGE(0xe000, 0xe007) AM_READWRITE(networkio_r, networkio_w)
	AM_RANGE(0xff60, 0xff6f) AM_DEVREADWRITE("ide", bus_master_ide_controller_device, bmdma_r, bmdma_w)
ADDRESS_MAP_END
#ifndef USE_LEGACY_PCI
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class nv2a_host_device : public pci_host_device {
public:
	nv2a_host_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);
	virtual void map_extra(uint64_t memory_window_start, uint64_t memory_window_end, uint64_t memory_offset, address_space *memory_space,
		uint64_t io_window_start, uint64_t io_window_end, uint64_t io_offset, address_space *io_space) override;
	void set_cpu_tag(const char *_cpu_tag);

protected:
	virtual void device_start() override;
	virtual void device_reset() override;

private:
	const char *cpu_tag;
	cpu_device *cpu;
};

extern const device_type NV2A_HOST;
const device_type NV2A_HOST = device_creator<nv2a_host_device>;

nv2a_host_device::nv2a_host_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: pci_host_device(mconfig, NV2A_HOST, "PCI Bridge Device - Host Bridge", tag, owner, clock, "nv2a_host", __FILE__),
	  cpu_tag(nullptr),
	  cpu(nullptr)
{
}

void nv2a_host_device::map_extra(uint64_t memory_window_start, uint64_t memory_window_end, uint64_t memory_offset, address_space *memory_space,
	uint64_t io_window_start, uint64_t io_window_end, uint64_t io_offset, address_space *io_space)
{
	io_space->install_device(0, 0xffff, *static_cast<pci_host_device *>(this), &pci_host_device::io_configuration_access_map);
}

void nv2a_host_device::set_cpu_tag(const char *_cpu_tag)
{
	cpu_tag = _cpu_tag;
}

void nv2a_host_device::device_start()
{
	pci_host_device::device_start();
	cpu = machine().device<cpu_device>(cpu_tag);
	memory_space = &cpu->space(AS_PROGRAM);
	io_space = &cpu->space(AS_IO);

	// do not change the next two
	memory_window_start = 0xfd000000;
	memory_window_end = 0xfdffffff;
	memory_offset = 0;// xfd000000;
	// next two must define an unused area
	io_window_start = 0xf000;
	io_window_end = 0xf00f;
	io_offset = 0xf000;
}

void nv2a_host_device::device_reset()
{
	pci_host_device::device_reset();
}

#define MCFG_PCI_HOST_CPU(_cpu_tag) downcast<nv2a_host_device *>(device)->set_cpu_tag(_cpu_tag);
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class nv2a_ram_device : public pci_device {
public:
	nv2a_ram_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);

	virtual DECLARE_ADDRESS_MAP(config_map, 32) override;

protected:
	DECLARE_READ32_MEMBER(config_register_r);
	DECLARE_WRITE32_MEMBER(config_register_w);
};

DEVICE_ADDRESS_MAP_START(config_map, 32, nv2a_ram_device)
	AM_RANGE(0x6c, 0x6f) AM_READWRITE(config_register_r, config_register_w)
	AM_INHERIT_FROM(pci_device::config_map)
ADDRESS_MAP_END

extern const device_type NV2A_RAM;
const device_type NV2A_RAM = device_creator<nv2a_ram_device>;

nv2a_ram_device::nv2a_ram_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: pci_device(mconfig, NV2A_RAM, "Memory Controller - SDRAM", tag, owner, clock, "nv2a_ram", __FILE__)
{
}

READ32_MEMBER(nv2a_ram_device::config_register_r)
{
	return 0x08800044;
}

WRITE32_MEMBER(nv2a_ram_device::config_register_w)
{
	return;
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class mcpx_lpc_device : public pci_device {
public:
	mcpx_lpc_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);
};

extern const device_type MCPX_LPC;
const device_type MCPX_LPC = device_creator<mcpx_lpc_device>;

mcpx_lpc_device::mcpx_lpc_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: pci_device(mconfig, MCPX_LPC, "HUB Interface - ISA Bridge", tag, owner, clock, "mcpx_lpc", __FILE__)
{
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class mcpx_smbus_device : public pci_device {
public:
	mcpx_smbus_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);
};

extern const device_type MCPX_SMBUS;
const device_type MCPX_SMBUS = device_creator<mcpx_smbus_device>;

mcpx_smbus_device::mcpx_smbus_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: pci_device(mconfig, MCPX_SMBUS, "SMBus Controller", tag, owner, clock, "mcpx_smbus", __FILE__)
{
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class mcpx_ohci_device : public pci_device {
public:
	mcpx_ohci_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);
};

extern const device_type MCPX_OHCI;
const device_type MCPX_OHCI = device_creator<mcpx_ohci_device>;

mcpx_ohci_device::mcpx_ohci_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: pci_device(mconfig, MCPX_OHCI, "MCPX OHCI USB Controller", tag, owner, clock, "mcpx_ohci", __FILE__)
{
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class mcpx_eth_device : public pci_device {
public:
	mcpx_eth_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);
};

extern const device_type MCPX_ETH;
const device_type MCPX_ETH = device_creator<mcpx_eth_device>;

mcpx_eth_device::mcpx_eth_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: pci_device(mconfig, MCPX_ETH, "MCP Networking Adapter", tag, owner, clock, "mcpx_eth", __FILE__)
{
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class mcpx_apu_device : public pci_device {
public:
	mcpx_apu_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);
};

extern const device_type MCPX_APU;
const device_type MCPX_APU = device_creator<mcpx_apu_device>;

mcpx_apu_device::mcpx_apu_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: pci_device(mconfig, MCPX_APU, "MCP APU", tag, owner, clock, "mcpx_apu", __FILE__)
{
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class mcpx_ac97_audio_device : public pci_device {
public:
	mcpx_ac97_audio_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);
};

extern const device_type MCPX_AC97_AUDIO;
const device_type MCPX_AC97_AUDIO = device_creator<mcpx_ac97_audio_device>;

mcpx_ac97_audio_device::mcpx_ac97_audio_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: pci_device(mconfig, MCPX_AC97_AUDIO, "AC`97 Audio Codec Interface", tag, owner, clock, "mcpx_av97_audio", __FILE__)
{
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class mcpx_ac97_modem_device : public pci_device {
public:
	mcpx_ac97_modem_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);
};

extern const device_type MCPX_AC97_MODEM;
const device_type MCPX_AC97_MODEM = device_creator<mcpx_ac97_modem_device>;

mcpx_ac97_modem_device::mcpx_ac97_modem_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: pci_device(mconfig, MCPX_AC97_MODEM, "AC`97 Modem Controller", tag, owner, clock, "mcpx_ac97_modem", __FILE__)
{
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class mcpx_ide_device : public pci_device {
public:
	mcpx_ide_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);
};

extern const device_type MCPX_IDE;
const device_type MCPX_IDE = device_creator<mcpx_ide_device>;

mcpx_ide_device::mcpx_ide_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: pci_device(mconfig, MCPX_IDE, "MCPX IDE Controller", tag, owner, clock, "mcpx_ide", __FILE__)
{
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class nv2a_agp_device : public agp_bridge_device {
public:
	nv2a_agp_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);

protected:
	virtual void device_start() override;
	virtual void device_reset() override;
};

extern const device_type NV2A_AGP;
const device_type NV2A_AGP = device_creator<nv2a_agp_device>;

nv2a_agp_device::nv2a_agp_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: agp_bridge_device(mconfig, NV2A_AGP, "AGP Host to PCI Bridge", tag, owner, clock, "nv2a_agp", __FILE__)
{
}

void nv2a_agp_device::device_start()
{
	agp_bridge_device::device_start();
}

void nv2a_agp_device::device_reset()
{
	agp_bridge_device::device_reset();
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class nv2a_gpu_device : public pci_device {
public:
	nv2a_gpu_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock);
	DECLARE_READ32_MEMBER(geforce_r);
	DECLARE_WRITE32_MEMBER(geforce_w);
	nv2a_renderer *nvidia_nv2a;

	protected:
	virtual void device_start() override;
	virtual void device_reset() override;

private:
	DECLARE_ADDRESS_MAP(nv2a_mmio, 32);
};

DEVICE_ADDRESS_MAP_START(nv2a_mmio, 32, nv2a_gpu_device)
	AM_RANGE(0x00000000,0x00ffffff) AM_RAM AM_READWRITE(geforce_r, geforce_w)
ADDRESS_MAP_END

extern const device_type NV2A_GPU;
const device_type NV2A_GPU = device_creator<nv2a_gpu_device>;

nv2a_gpu_device::nv2a_gpu_device(const machine_config &mconfig, const char *tag, device_t *owner, uint32_t clock)
	: pci_device(mconfig, NV2A_GPU, "Nvidia NV2A GPU", tag, owner, clock, "nv2a_gpu", __FILE__),
	nvidia_nv2a(nullptr)
{
}

void nv2a_gpu_device::device_start()
{
	pci_device::device_start();
	add_map(0x01000000, M_MEM, FUNC(nv2a_gpu_device::nv2a_mmio));
	//set_map_address(0, 0xfd000000);
	bank_infos[0].adr = 0xfd000000;
}

void nv2a_gpu_device::device_reset()
{
	pci_device::device_reset();
}

READ32_MEMBER(nv2a_gpu_device::geforce_r)
{
	return nvidia_nv2a->geforce_r(space, offset, mem_mask);
}

WRITE32_MEMBER(nv2a_gpu_device::geforce_w)
{
	nvidia_nv2a->geforce_w(space, offset, data, mem_mask);
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#endif

void xbox_base_state::machine_start()
{
	find_debug_params(machine());
	nvidia_nv2a = new nv2a_renderer(machine());
#ifndef USE_LEGACY_PCI
	machine().device<nv2a_gpu_device>(":pci:1e.0:00.0")->nvidia_nv2a = nvidia_nv2a;
#endif
	memset(pic16lc_buffer, 0, sizeof(pic16lc_buffer));
	pic16lc_buffer[0] = 'B';
	pic16lc_buffer[4] = 0; // A/V connector, 0=scart 2=vga 4=svideo 7=none
	smbus_register_device(0x10, smbus_callback_pic16lc);
	smbus_register_device(0x45, smbus_callback_cx25871);
	smbus_register_device(0x54, smbus_callback_eeprom);
	xbox_base_devs.pic8259_1 = machine().device<pic8259_device>("pic8259_1");
	xbox_base_devs.pic8259_2 = machine().device<pic8259_device>("pic8259_2");
	xbox_base_devs.ide = machine().device<bus_master_ide_controller_device>("ide");
	memset(apust.memory, 0, sizeof(apust.memory));
	memset(apust.voices_heap_blockaddr, 0, sizeof(apust.voices_heap_blockaddr));
	memset(apust.voices_active, 0, sizeof(apust.voices_active));
	memset(apust.voices_position, 0, sizeof(apust.voices_position));
	memset(apust.voices_position_start, 0, sizeof(apust.voices_position_start));
	memset(apust.voices_position_end, 0, sizeof(apust.voices_position_end));
	memset(apust.voices_position_increment, 0, sizeof(apust.voices_position_increment));
	apust.space = &m_maincpu->space();
	apust.timer = machine().scheduler().timer_alloc(timer_expired_delegate(FUNC(xbox_base_state::audio_apu_timer), this), (void *)"APU Timer");
	apust.timer->enable(false);
	if (machine().debug_flags & DEBUG_FLAG_ENABLED)
	{
		using namespace std::placeholders;
		machine().debugger().console().register_command("xbox", CMDFLAG_NONE, 0, 1, 4, std::bind(&xbox_base_state::xbox_debug_commands, this, _1, _2));
	}
	// PIC challenge handshake data
	pic16lc_buffer[0x1c] = 0x0c;
	pic16lc_buffer[0x1d] = 0x0d;
	pic16lc_buffer[0x1e] = 0x0e;
	pic16lc_buffer[0x1f] = 0x0f;
	// usb
	ohci_usb = machine().device<ohci_usb_controller>("ohci_usb");
	// super-io
	memset(&superiost, 0, sizeof(superiost));
	superiost.configuration_mode = false;
	superiost.registers[0][0x26] = 0x2e; // Configuration port address byte 0
										 // savestates
	save_item(NAME(debug_irq_active));
	save_item(NAME(debug_irq_number));
	save_item(NAME(smbusst.status));
	save_item(NAME(smbusst.control));
	save_item(NAME(smbusst.address));
	save_item(NAME(smbusst.data));
	save_item(NAME(smbusst.command));
	save_item(NAME(smbusst.rw));
	save_item(NAME(smbusst.words));
	save_item(NAME(pic16lc_buffer));
	nvidia_nv2a->set_interrupt_device(xbox_base_devs.pic8259_1);
	nvidia_nv2a->start(&m_maincpu->space());
	nvidia_nv2a->savestate_items();
}

MACHINE_CONFIG_START(xbox_base, xbox_base_state)

	/* basic machine hardware */
	MCFG_CPU_ADD("maincpu", PENTIUM3, 733333333) /* Wrong! family 6 model 8 stepping 10 */
	MCFG_CPU_PROGRAM_MAP(xbox_base_map)
	MCFG_CPU_IO_MAP(xbox_base_map_io)
	MCFG_CPU_IRQ_ACKNOWLEDGE_DRIVER(xbox_base_state, irq_callback)

	MCFG_QUANTUM_TIME(attotime::from_hz(6000))

#ifdef USE_LEGACY_PCI
	MCFG_PCI_BUS_LEGACY_ADD("pcibus", 0)
	MCFG_PCI_BUS_LEGACY_DEVICE(0, "PCI Bridge Device - Host Bridge", pcibridghostbridg_pci_r, pcibridghostbridg_pci_w) // function 0 host function 3 ram
	MCFG_PCI_BUS_LEGACY_DEVICE(1, "HUB Interface - ISA Bridge", hubintisabridg_pci_r, hubintisabridg_pci_w) // function 0 lpc function 1 smbus
	MCFG_PCI_BUS_LEGACY_DEVICE(2, "OHCI USB Controller 1", dummy_pci_r, dummy_pci_w)
	MCFG_PCI_BUS_LEGACY_DEVICE(3, "OHCI USB Controller 2", dummy_pci_r, dummy_pci_w)
	MCFG_PCI_BUS_LEGACY_DEVICE(4, "MCP Networking Adapter", dummy_pci_r, dummy_pci_w)
	MCFG_PCI_BUS_LEGACY_DEVICE(5, "MCP APU", dummy_pci_r, dummy_pci_w)
	MCFG_PCI_BUS_LEGACY_DEVICE(6, "AC`97 Audio Codec Interface", dummy_pci_r, dummy_pci_w) // function 0 ac97 audio function 1 ac97 modem
	MCFG_PCI_BUS_LEGACY_DEVICE(8, "PCI to PCI Bridge", dummy_pci_r, dummy_pci_w)
	MCFG_PCI_BUS_LEGACY_DEVICE(9, "IDE Controller", dummy_pci_r, dummy_pci_w)
	MCFG_PCI_BUS_LEGACY_DEVICE(30, "AGP Host to PCI Bridge", dummy_pci_r, dummy_pci_w)
	MCFG_PCI_BUS_LEGACY_ADD("agpbus", 1)
	MCFG_PCI_BUS_LEGACY_SIBLING("pcibus")
	MCFG_PCI_BUS_LEGACY_DEVICE(0, "NV2A GeForce 3MX Integrated GPU/Northbridge", geforce_pci_r, geforce_pci_w)
#else
	MCFG_PCI_ROOT_ADD(  ":pci")
	MCFG_PCI_HOST_ADD(  ":pci:00.0", NV2A_HOST, 0x10de02a5, 0, 0)
	MCFG_PCI_HOST_CPU("maincpu")
	MCFG_PCI_DEVICE_ADD(":pci:00.3", NV2A_RAM, 0x10de02a6, 0, 0, 0)
	MCFG_PCI_DEVICE_ADD(":pci:01.0", MCPX_LPC, 0x10de01b2, 0xb4, 0, 0) // revision id must be at least 0xb4, otherwise usb will require a hub
	MCFG_PCI_DEVICE_ADD(":pci:01.1", MCPX_SMBUS, 0x10de01b4, 0, 0, 0)
	MCFG_PCI_DEVICE_ADD(":pci:02.0", MCPX_OHCI, 0x10de01c2, 0, 0, 0)
	MCFG_PCI_DEVICE_ADD(":pci:03.0", MCPX_OHCI, 0x10de01c2, 0, 0, 0)
	MCFG_PCI_DEVICE_ADD(":pci:04.0", MCPX_ETH, 0x10de01c3, 0, 0, 0)
	MCFG_PCI_DEVICE_ADD(":pci:05.0", MCPX_APU, 0x10de01b0, 0, 0, 0)
	MCFG_PCI_DEVICE_ADD(":pci:06.0", MCPX_AC97_AUDIO, 0x10de01b1, 0, 0, 0)
	MCFG_PCI_DEVICE_ADD(":pci:06.1", MCPX_AC97_MODEM, 0x10de01c1, 0, 0, 0)
	MCFG_PCI_BRIDGE_ADD(":pci:08.0", 0x10de01b8, 0)
	MCFG_PCI_DEVICE_ADD(":pci:09.0", MCPX_IDE, 0x10de01bc, 0, 0, 0)
	MCFG_AGP_BRIDGE_ADD(":pci:1e.0", NV2A_AGP, 0x10de01b7, 0)
	MCFG_PCI_DEVICE_ADD(":pci:1e.0:00.0", NV2A_GPU, 0x10de02a0, 0, 0, 0)
#endif
	MCFG_PIC8259_ADD("pic8259_1", WRITELINE(xbox_base_state, xbox_pic8259_1_set_int_line), VCC, READ8(xbox_base_state, get_slave_ack))
	MCFG_PIC8259_ADD("pic8259_2", DEVWRITELINE("pic8259_1", pic8259_device, ir2_w), GND, NOOP)

	MCFG_DEVICE_ADD("pit8254", PIT8254, 0)
	MCFG_PIT8253_CLK0(1125000) /* heartbeat IRQ */
	MCFG_PIT8253_OUT0_HANDLER(WRITELINE(xbox_base_state, xbox_pit8254_out0_changed))
	MCFG_PIT8253_CLK1(1125000) /* (unused) dram refresh */
	MCFG_PIT8253_CLK2(1125000) /* (unused) pio port c pin 4, and speaker polling enough */
	MCFG_PIT8253_OUT2_HANDLER(WRITELINE(xbox_base_state, xbox_pit8254_out2_changed))

	MCFG_DEVICE_ADD("ide", BUS_MASTER_IDE_CONTROLLER, 0)
	MCFG_ATA_INTERFACE_IRQ_HANDLER(DEVWRITELINE("pic8259_2", pic8259_device, ir6_w))
	MCFG_BUS_MASTER_IDE_CONTROLLER_SPACE("maincpu", AS_PROGRAM)

	// usb controller
	MCFG_OHCI_USB_CONTROLLER_ADD("ohci_usb")
	MCFG_OHCI_USB_CONTROLLER_INTERRUPT_HANDLER(WRITELINE(xbox_base_state, xbox_ohci_usb_interrupt_changed))

	/* video hardware */
	MCFG_SCREEN_ADD("screen", RASTER)
	MCFG_SCREEN_REFRESH_RATE(60)
	MCFG_SCREEN_VBLANK_TIME(ATTOSECONDS_IN_USEC(2500))  /* not accurate */
	MCFG_SCREEN_SIZE(640, 480)
	MCFG_SCREEN_VISIBLE_AREA(0, 639, 0, 479)
	MCFG_SCREEN_UPDATE_DRIVER(xbox_base_state, screen_update_callback)
	MCFG_SCREEN_VBLANK_CALLBACK(WRITELINE(xbox_base_state, vblank_callback))
MACHINE_CONFIG_END
