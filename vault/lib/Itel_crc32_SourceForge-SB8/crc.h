/*++
 *
 * Copyright (c) 2004-2006 Intel Corporation - All Rights Reserved
 * 
 * This software program is licensed subject to the BSD License, 
 * available at http://www.opensource.org/licenses/bsd-license.html
 *
 --*/

#ifndef CRC_H_INCLUDED
#define CRC_H_INCLUDED

#define TEST_CRC_VERSION			"BUILD 2"
#define CPU_DATA_CACHE_SIZE			0x100000
#define WARM		1
#define	COLD		2
#define RANDOM		3
#define	CONSTANT	4
#define	INCREMENTAL	5
#define	INIT_TABLE_STATUS		WARM	
#define INIT_DATA_STATUS		WARM
#define	INIT_NUM_OF_ITERATIONS	10
#define	INIT_PACKET_SIZE		1024
#define	INIT_ITERATION_STYLE	CONSTANT
#define	INIT_ALIGNMENT			0
#define	INIT_ALIGNMENT_STYLE	CONSTANT
#define MAX_BUF_SIZE			65536
#define MIN_BUF_SIZE			64
#define PACKET_SIZE_INCREMENT	64
#define MAX_ALIGNMENT			8
#define MIN_ALIGNMENT			1
#define ALIGNMENT_INCREMENT		1
#define MPA_FRAME_LENGTH		48
#define MPA_FRAME_INDEX1		5
#define MPA_FRAME_VALUE1		0x2a
#define MPA_FRAME_INDEX2		6
#define MPA_FRAME_VALUE2		0x40
#define MPA_FRAME_INDEX3		7
#define MPA_FRAME_VALUE3		0x03
#define MPA_FRAME_INDEX4		19
#define MPA_FRAME_VALUE4		0x01
#define MPA_FRAME_CRC			0x84B3864C
#define UINT8_MAX				255
#define LONG_WORD_SIZE			4
#define	TRUE					1
#define	FALSE					0
#define CRC_FAILED				1
#define CRC_PASSED				0
#define CRC32C_INIT_REFLECTED 0xFFFFFFFF
#define XOROT 0xFFFFFFFF
#define MODE_BEGIN	0
#define	MODE_CONT	1
#define	MODE_END	2
#define	MODE_BODY	3
#define	MODE_ALIGN	4
#define TWO_CORE_TAIL_LENGTH	16
#define FOUR_CORE_TAIL_LENGTH	32
#define SLICE_LENGTH			8
#define SB8_CHUNK				8
#define POWER_OF_2(X) (1 << (X))
#define MAX_SLICES	8
#define MAX_CHARS	100
#define INIT_WIDTH			32				
#define INIT_POLY			0x1EDC6F41L		
#define INIT_REFLECTED		TRUE	
#define INIT_SLICE_LENGTH   8
#define INIT_NUM_OF_SLICES	8
#define INIT_OFFSET			32
#define INIT_DIR			".\\"	
#define	INIT_FILE			"8x256_tables.c"
#define SB3_1_SLICE_1		10
#define SB3_1_SLICE_2		10
#define SB3_1_SLICE_3		12
#define SB3_NUM_OF_SLICES	3
#define	SB3_1_FILE			"4K_plus_2x1K_tables.c"
#define SB3_2_SLICE_1		10
#define SB3_2_SLICE_2		11
#define SB3_2_SLICE_3		11
#define	SB3_2_FILE			"1K_plus_2x2K_tables.c"
#define SB2_NUM_OF_SLICES	2
#define SB2_SLICE_1			16
#define SB2_SLICE_2			16
#define	SB2_FILE			"2x64K_tables.c"
#define SB1_NUM_OF_SLICES	1
#define	SB1_FILE			"256_table.c"


#define CPU_PREFETCH(cache_line)			\
{ int* address = (int*) (cache_line);		\
	_asm mov edx, address					\
	_asm prefetcht0[edx]					\
}

#define CPU_GET_CYCLES(low)					\
{											\
	_asm	rdtsc							\
	_asm	mov dword ptr [low], eax		\
}

#define CPU_SYNC							\
{											\
	_asm	mov eax, 0						\
	_asm	cpuid							\
}

#define CPU_CACHE_FLUSH(cache_line)			\
{ int* address = (int*) (cache_line);		\
	_asm mov edx, address					\
	_asm clflush[edx]						\
	_asm mfence								\
}


#ifdef __cplusplus
extern "C"
{
#endif	/* __cplusplus */


typedef __int8				int8_t;
typedef unsigned __int8		uint8_t;
typedef __int16				int16_t;
typedef unsigned __int16	uint16_t;
typedef __int32				int32_t;
typedef unsigned __int32	uint32_t;
typedef __int64				int64_t;
typedef unsigned __int64	uint64_t;

/**
	Defines the boolean type.

	The boolean type must be the same size for both C & C++.
	Otherwise, structures containing a boolean cannot be properly
	shared between C and C++ code.  Thus, make boolean_t a simple
	int and don't use the C++ 'bool' type.
*/
typedef int					boolean_t;

// @}

typedef struct crc_eval_info
{
   uint8_t	 crc_table_status;		//i.e., warm or cold
   uint8_t	 crc_data_status;		//same as above
   uint32_t	 crc_num_of_iterations;
   uint32_t	 crc_packet_size;
   uint8_t	 crc_iteration_style;	//i.e., RANDOM, CONST, INCREMENTAL
   uint8_t	 crc_alignment;		
   uint8_t	 crc_alignment_style;	//i.e., RANDOM, CONST

} crc_eval_info_t;

typedef struct crc_test
{
	uint8_t*	p_sbuf;
	uint8_t*	p_dbuf;
	uint32_t	buf_length;
	uint8_t		alignment;
	uint32_t	crc_value;
	uint8_t		crc_status;

} crc_test_t;


typedef uint8_t	a_uint8_t[MAX_SLICES];

typedef name_t[MAX_CHARS];			

typedef struct table_gen_info
{
   uint32_t	 tb_width;		//the width of the generator polynomial in bits [8,32]
   uint32_t	 tb_polynomial;		//the algorithm's polynomial
   uint8_t	 tb_reflected;  //determines if input bytes are reflected  
   a_uint8_t tb_slice_lengths;	
   uint32_t	 tb_num_of_slices;
   uint32_t	 tb_offset;		//i.e., how far ahead we calculate the current remainder
   name_t	 tb_dir_name;
   name_t	 tb_file_name;
} table_gen_info_t;

typedef table_gen_info_t* p_table_gen_info_t;

/**
 *
 * Routine Description:
 *
 * Computes the CRC32c checksum for the specified buffer.                      
 *
 * Arguments:
 *
 *		p_running_crc - pointer to the initial or final remainder value 
 *						used in CRC computations. It should be set to 
 *						non-NULL if the mode argument is equal to CONT or END
 *		p_buf - the packet buffer where crc computations are being performed
 *		length - the length of p_buf in bytes
 *		mode - can be any of the following: BEGIN, CONT, END, BODY, ALIGN 
 *
 * Return value:
 *		
 *		The computed CRC32c value
 */

uint32_t
crc32c(
	uint32_t*		p_running_crc,
    const uint8_t*	p_buf,
    const uint32_t	length,
	uint8_t			mode);


/**
 *
 * Routine Description:
 *
 * Computes the CRC32c checksum for the specified buffer using the slicing by 8 
 * algorithm over 64 bit quantities.                      
 *
 * Arguments:
 *
 *		p_running_crc - pointer to the initial or final remainder value 
 *						used in CRC computations. It should be set to 
 *						non-NULL if the mode argument is equal to CONT or END
 *		p_buf - the packet buffer where crc computations are being performed
 *		length - the length of p_buf in bytes
 *		init_bytes - the number of initial bytes that need to be procesed before
 *					 aligning p_buf to multiples of 4 bytes
 *		mode - can be any of the following: BEGIN, CONT, END, BODY, ALIGN 
 *
 * Return value:
 *		
 *		The computed CRC32c value
 */

uint32_t
crc32c_sb8_64_bit(
	uint32_t* p_running_crc,
    const uint8_t*	p_buf,
    const uint32_t length,
	const uint32_t init_bytes,
	uint8_t			mode);

/*
 *
 * Routine Description:
 *
 * reads garbage so that data caches are purged                       
 *
 * Arguments:
 *
 *		none
 *
 * Return value:
 *		
 *		none
 */

void
purge_data_cache( void );

/*
 *
 * Routine Description:
 *
 * invalidates a buffer                       
 *
 * Arguments:
 *
 *		the buffer
 *
 * Return value:
 *		
 *		none
 */

void
invalidate_buffer(
				  uint8_t* p_buf,
				  uint32_t size);


/*
 *
 * Routine Description:
 *
 * performs the mpa sample frame test                    
 *
 * Arguments:
 *
 *		non
 *
 * Return value:
 *		
 *		none
 */

void
mpa_sample_frame_test(
					void);


/*
 *
 * Routine Description:
 *
 * Returns the value with the least significant "num" bits reflected.                       
 *
 * Arguments:
 *
 *		value - the value where the bits are reflected
 *		num - the number of bits which are reflected
 *
 * Return value:
 *		
 *		value with the bits reflected
 */

uint32_t 
reflect (uint32_t const val, int num);

/*
 *
 * Routine Description:
 *	
 *	returns a bitmask which is as wide as a given number
 *
 * Arguments:
 *
 *		p_info - the table generation data structure
 *
 * Return value:
 *		
 *		a bitmask which is as wide as the generator polynomial
 *		of a set of tables
 */

uint32_t 
generate_mask( int num);

/*
 *
 * Routine Description:
 *	
 *	returns a bitmask which is as wide as the generator polynomial
 *		of a set of tables
 *
 * Arguments:
 *
 *		p_info - the table generation data structure
 *
 * Return value:
 *		
 *		a bitmask which is as wide as the generator polynomial
 *		of a set of tables
 */

uint32_t 
generate_mask_from_p_info (p_table_gen_info_t p_info);

/*
 *
 * Routine Description:
 *
 * Prints the header of the file where tables are created 
 *
 * Arguments:
 *
 *		p_info - the table generation data structure
 *
 * Return value:
 *		
 *		None
 */

void 
print_header (
	p_table_gen_info_t p_info);

/*
 *
 * Routine Description:
 *
 * Checks the validity of the contents of a table 
 * generation data structure
 *
 * Arguments:
 *
 *		p_info - the table generation data structure
 *
 * Return value:
 *		
 *		None
 */

void 
check_data_str (
	p_table_gen_info_t p_info);

/*
 *
 * Routine Description:
 *
 * prints the contents of a table 
 * generation data structure
 *
 * Arguments:
 *
 *		p_info - the table generation data structure
 *		p_f - the file pointer where the contents are printed
 *
 * Return value:
 *		
 *		None
 */

void 
print_param (
	p_table_gen_info_t p_info,
	FILE *p_f);
	
/*
 *
 * Routine Description:
 *
 * Calculates a single table entry associated with a slice 
 * and a given entry_index
 *
 * Arguments:
 *
 *		p_info - data structure with information about table generation
 *		slice_index - index to the slice associated with the table created;
 *					  slice index 0 contains the least significant bits 
 *					  of the remainder
 *		entry_index - index to the entry of the table which is created 
 *
 * Return value:
 *		
 *		the created entry or 0 if the input arguments are invalid
 */

uint32_t 
gen_table_entry (
	p_table_gen_info_t	p_info,
	uint32_t			slice_index,
	uint32_t			entry_index);

/*
 *
 * Routine Description:
 *
 * Creates a table associated with a given generation data structure
 * and slice index
 *
 * Arguments:
 *
 *		p_info - data structure with information about table generation
 *		slice_index - index to the slice associated with the table created;
 *					  slice index 0 contains the least significant bits 
 *					  of the number which is sliced
 *
 * Return value:
 *		
 *		none
 */


void 
gen_custom_table (
	p_table_gen_info_t	p_info,
	uint32_t			slice_index);

/*
 *
 * Routine Description:
 *
 * The following function generates a set of tables associated with a set of 
 * remainder slices. For example, tables could be indexed by the least significant 
 * 10, 10 and 12 bits of the current remainder. Slice lengths are passed as an 
 * array starting from the slice that contains the least significant bits of the number
 * number which is sliced. Up to MAX_SLICES slices can be passed. 
 *
 * Arguments:
 *
 *		p_info - data structure with information about table generation
 *
 * Return value:
 *		
 *		none
 */

void 
gen_tables_from_slices (
	p_table_gen_info_t	p_info);



#ifdef __cplusplus
}
#endif	/* __cplusplus */

#endif	//CRC_H_INCLUDED

