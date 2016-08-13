/*++
 *
 * Copyright (c) 2004-2006 Intel Corporation - All Rights Reserved
 *
 * This software program is licensed subject to the BSD License, 
 * available at http://www.opensource.org/licenses/bsd-license.html
 *
 * Abstract: The main routine
 * 
 --*/

#include <stdio.h>
#include "crc.h"
#include "stdlib.h"
#include "string.h"

#pragma warning( disable: 4267 )
//to avod unnecessary warnings when using "touch" variables

/* 
 * the following variables are used for counting cycles and bytes 
 */

extern uint32_t crc_tableil8_o32[256];
extern uint32_t crc_tableil8_o40[256];
extern uint32_t crc_tableil8_o48[256];
extern uint32_t crc_tableil8_o56[256];
extern uint32_t crc_tableil8_o64[256];
extern uint32_t crc_tableil8_o72[256];
extern uint32_t crc_tableil8_o80[256];
extern uint32_t crc_tableil8_o88[256];


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
 *		init_bytes - the number of initial bytes that need to be procesed before
 *					 aligning p_buf to multiples of 4 bytes
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
	uint8_t			mode) 
{
	uint32_t crc;
    const uint8_t* p_end = p_buf + length;
	if(mode == MODE_CONT)
		crc = *p_running_crc;
	else	
		crc = CRC32C_INIT_REFLECTED;
	while(p_buf < p_end )
		crc = crc_tableil8_o32[(crc ^ *p_buf++) & 0x000000FF] ^ (crc >> 8);
	if((mode == MODE_BEGIN) || (mode == MODE_CONT))
		return crc;		
	return crc ^ XOROT;

}



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
	uint8_t			mode)
{
	uint32_t li;
	uint32_t crc, term1, term2;
	uint32_t running_length;
	uint32_t end_bytes;
	if(mode ==  MODE_CONT)
		crc = *p_running_crc;
	else	
		crc = CRC32C_INIT_REFLECTED;
	running_length = ((length - init_bytes)/8)*8;
	end_bytes = length - init_bytes - running_length; 

	for(li=0; li < init_bytes; li++) 
		crc = crc_tableil8_o32[(crc ^ *p_buf++) & 0x000000FF] ^ (crc >> 8);	
	for(li=0; li < running_length/8; li++) 
	{
		crc ^= *(uint32_t *)p_buf;
		p_buf += 4;
		term1 = crc_tableil8_o88[crc & 0x000000FF] ^
				crc_tableil8_o80[(crc >> 8) & 0x000000FF];
		term2 = crc >> 16;
		crc = term1 ^
			  crc_tableil8_o72[term2 & 0x000000FF] ^ 
			  crc_tableil8_o64[(term2 >> 8) & 0x000000FF];
		term1 = crc_tableil8_o56[(*(uint32_t *)p_buf) & 0x000000FF] ^
				crc_tableil8_o48[((*(uint32_t *)p_buf) >> 8) & 0x000000FF];
		
		term2 = (*(uint32_t *)p_buf) >> 16;
		crc =	crc ^ 
				term1 ^		
				crc_tableil8_o40[term2  & 0x000000FF] ^	
				crc_tableil8_o32[(term2 >> 8) & 0x000000FF];	
		p_buf += 4;
	}
	for(li=0; li < end_bytes; li++) 
		crc = crc_tableil8_o32[(crc ^ *p_buf++) & 0x000000FF] ^ (crc >> 8);
	if((mode == MODE_BEGIN) || (mode ==  MODE_CONT))
		return crc;		
    return crc ^ XOROT;	
}


/**
 *
 * Routine Description:
 *
 * warms the tables                      
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
warm_tables( void )
{
	volatile uint32_t i, touch;
	
	//we warm the small tables
	for(i=0; i < 256; i++)
	{
		touch = crc_tableil8_o32[i];
		touch = crc_tableil8_o40[i];
		touch = crc_tableil8_o48[i];
		touch = crc_tableil8_o56[i];
		touch = crc_tableil8_o64[i];
		touch = crc_tableil8_o72[i];
		touch = crc_tableil8_o80[i];
		touch = crc_tableil8_o88[i];
	}

};

/**
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
purge_data_cache( 
				void )
{
	static volatile uint8_t temp;
	// 2* increases the likelihood that all the physical pages
	// in cache were flushed.
	static volatile uint8_t dummy_cache[2 * CPU_DATA_CACHE_SIZE];
	size_t i;

	for( i = 0; i < 2 * CPU_DATA_CACHE_SIZE; i++ )
		temp = dummy_cache[i];
}

/**
 *
 * Routine Description:
 *
 * invalidates a buffer                       
 *
 * Arguments:
 *
 *		the buffer and the buffer size
 *
 * Return value:
 *		
 *		none
 */

void
invalidate_buffer(
	uint8_t* p_buf, 
	uint32_t size)
{
	uint32_t i;
	volatile void const* cache_line;
	for(i=0; i < (size/64); i++)
	{
		cache_line = (void const*)(p_buf+i*64);
		CPU_CACHE_FLUSH(cache_line)
	}
}



/**
 *
 * Routine Description:
 *
 * warms the data buffer                       
 *
 * Arguments:
 *
 *		buf - the buffer
 *		buf_lengh - the length of the buffer
 *
 * Return value:
 *		
 *		none
 */
static void
warm_data(
	const crc_test_t* const p_test,
	uint32_t const num_of_packets )
{
	size_t i;
	size_t j;
	for( i = 0; i < num_of_packets; i++ )
	{
		for( j = 0; j < p_test[i].buf_length; j++)
		{
			volatile uint8_t touch = p_test[i].p_sbuf[j];
		}
	}
}

static void
chill_data(
	const crc_test_t* const p_test,
	uint32_t const num_of_packets )
{
	size_t i;
	for( i = 0; i < num_of_packets; i++ )
	{
		invalidate_buffer( p_test[i].p_sbuf, p_test[i].buf_length );
	}
}

/**
	Warms the specified crc_test object in the cache.
*/
static void
crc_test_warm(
	const crc_test_t* const p_test )
{
	size_t i;
	for( i = 0; i < sizeof(*p_test); i++ )
	{
		volatile uint8_t touch = ((uint8_t*)p_test)[i];
	}
}



static void
set_cache_state(
	crc_test_t* p_test,
	crc_eval_info_t* p_info)
{
	purge_data_cache();

	if( p_info->crc_table_status == WARM )
		warm_tables();

	if( p_info->crc_data_status == WARM )
		warm_data( p_test, p_info->crc_num_of_iterations );	
	else
		chill_data( p_test, p_info->crc_num_of_iterations );	

	// warm the test object itself
	crc_test_warm( p_test );
}

/**
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
					void)
{
	uint8_t	mpa[MPA_FRAME_LENGTH];
	uint32_t result;
	int i;
	for(i = 0; i < MPA_FRAME_LENGTH; i++ )
		mpa[i] = 0;
	mpa[MPA_FRAME_INDEX1] = MPA_FRAME_VALUE1;
	mpa[MPA_FRAME_INDEX2] = MPA_FRAME_VALUE2;
	mpa[MPA_FRAME_INDEX3] = MPA_FRAME_VALUE3;
	mpa[MPA_FRAME_INDEX4] = MPA_FRAME_VALUE4;
	printf("\nVerifying algorithms against MPA sample frame\n\n"); 
	
	printf("testing the Sarwate algorithm..............................");
	result = crc32c(NULL, mpa, MPA_FRAME_LENGTH, MODE_BODY);
	if( result != MPA_FRAME_CRC)
	{
		printf( "error\n" );
		exit(0);
	}
	printf( "passed\n" );
	printf("testing the slicing by 8 over 64 bit algorithm.............");
	result = crc32c_sb8_64_bit(NULL, mpa, MPA_FRAME_LENGTH, 0, MODE_BODY);
	if( result != MPA_FRAME_CRC)
	{
		printf( "error\n" );
		exit(0);
	}
	printf( "passed\n" );
	return;
}

/**
 *
 * Routine Description:
 *
 * The main routine
 *
 * Arguments:
 *
 *		argc, argv
 *
 * Return value:
 *		
 *		none
 */

#define WARM_LOCAL_VARS			\
	touch = value1;				\
	touch = value2;				\
	touch = before;				\
	touch = after;				\
	touch = mode;				\
	touch = cycles;				\
	touch = total_bytes;		\
	touch = (uint32_t)mode;


int
main (
	int argc, 
	char* argv[])
{
	uint32_t i, j;
	uint8_t help_requested = FALSE;
	uint8_t alignment = 1;
	uint8_t mode=0;
	volatile uint32_t touch;
	uint32_t packet_size = 0;
	uint32_t cycles = 0;
	volatile uint32_t value1 = 0, value2 = 0;
	uint32_t before = 0;
	uint32_t after = 0;
	size_t total_bytes = 0;
	crc_eval_info_t* p_info;
	crc_test_t* p_test;

	p_info = (crc_eval_info_t *)malloc(sizeof(struct crc_eval_info));
	memset((void *)p_info, 0, sizeof(struct crc_eval_info));
	p_info->crc_table_status = INIT_TABLE_STATUS;		
    p_info->crc_data_status  = INIT_DATA_STATUS;		
    p_info->crc_num_of_iterations = INIT_NUM_OF_ITERATIONS;
	p_info->crc_packet_size = INIT_PACKET_SIZE;
	p_info->crc_iteration_style = INIT_ITERATION_STYLE;
	p_info->crc_alignment = INIT_ALIGNMENT;
	p_info->crc_alignment_style = INIT_ALIGNMENT_STYLE;

	printf("\n");
	printf("Evaluation Suite for CRC Generation Algorithms\n" );
	printf("Intel Research and Development, Intel Corporation.\n\n" ); 
	printf("All results are the confidential property of Intel Corporation.\n\n" );
	printf("Run the program with the -help option for documentation.\n" ); 
	printf("------------------------------------------------------------\n" );

	argv++;
    argc--;
    while(argc >0) 
	{	
		if (**argv != '-') 
		{ 
			printf("invalid option format: option %s must begin with \"-\"\n", *argv);
			exit(0);	
		}
		else if(!strcmp(*argv+1, "t")) 
		{
			argv++;
			argc--;
			if(!strcmp(*argv, "warm"))
				p_info->crc_table_status = WARM;
			else if (!strcmp(*argv, "cold"))
				p_info->crc_table_status = COLD;
			else 
			{
				printf("invalid option %s\n", *argv);
				exit(0);
			}
			if(argc > 0) 
			{
				argv++;
				argc--;
			}
			else
				break;
		}
		else if(!strcmp(*argv+1, "d")) 
		{
			argv++;
			argc--;
			if(!strcmp(*argv, "warm"))
				p_info->crc_data_status = WARM;
			else if (!strcmp(*argv, "cold"))
				p_info->crc_data_status = COLD;
			else 
			{
				printf("invalid option %s\n", *argv);
				exit(0);
			}
			if(argc > 0) 
			{
				argv++;
				argc--;
			}
			else
				break;
		}
		else if(!strcmp(*argv+1, "i")) 
		{
			argv++;
			argc--;
			if(argc && (**argv != '-')) 
			{
				p_info->crc_num_of_iterations = atoi(*argv);
				if(argc) 
				{
					argv++;
					argc--;
				}
			}
			else 
			{
				printf("invalid offset: %s after option -o\n", *argv);
				exit(0);
			}    
		 }
		 else if(!strcmp(*argv+1, "p")) 
		 {
			argv++;
			argc--;
			if(argc && (**argv != '-')) 
			{
				p_info->crc_packet_size = atoi(*argv);
				if(argc) 
				{
					argv++;
					argc--;
				}
			}
			else
			{
				printf("invalid width: %s after option -w\n", *argv);
				exit(0);
			}    
		}
		else if(!strcmp(*argv+1, "a")) 
		 {
			argv++;
			argc--;
			if(argc && (**argv != '-')) 
			{
				p_info->crc_alignment = (uint8_t)atoi(*argv);
				if(argc) 
				{
					argv++;
					argc--;
				}
			}
			else
			{
				printf("invalid width: %s after option -w\n", *argv);
				exit(0);
			}    
		}
		else if(!strcmp(*argv+1, "is")) 
		{
			argv++;
			argc--;
			if(!strcmp(*argv, "random"))
				p_info->crc_iteration_style = RANDOM;
			else if (!strcmp(*argv, "const"))
				p_info->crc_iteration_style = CONSTANT;
			else if (!strcmp(*argv, "incremental"))
				p_info->crc_iteration_style = INCREMENTAL;
			else 
			{
				printf("invalid option %s\n", *argv);
				exit(0);
			}
			if(argc > 0) 
			{
				argv++;
				argc--;
			}
			else
				break;
		}
		else if(!strcmp(*argv+1, "as")) 
		{
			argv++;
			argc--;
			if(!strcmp(*argv, "random"))
				p_info->crc_alignment_style = RANDOM;
			else if (!strcmp(*argv, "const"))
				p_info->crc_alignment_style = CONSTANT;
			else if (!strcmp(*argv, "incremental"))
				p_info->crc_alignment_style = INCREMENTAL;
			else 
			{
				printf("invalid option %s\n", *argv);
				exit(0);
			}
			if(argc > 0) 
			{
				argv++;
				argc--;
			}
			else
				break;
		}
		else if(!strcmp(*argv+1, "help")) 
		{
			help_requested = TRUE;	
			printf("options:\n");
			printf("-t	warm/cold\n");
			printf("	specifies the table status\n");
			printf("-d	warm/cold\n");
			printf("	specifies the data status\n");	
			printf("-i	num_of_iterations\n");
			printf("	sets the number of iterations of the CRC generation tests\n");
			printf("-p	packet_size\n");
			printf("	sets the size of the packets for which CRC is generated\n");
			printf("-a	alignment (between 1 and 64)\n");
			printf("	sets the number of initial bytes that are not aligned\n");
			printf("-is	const/random/incremental n\n");
			printf("	sets iteration style\n");
			printf("-as	const/random\n");
			printf("  	sets the alignment style\n");
			if(argc) 
			{
				 argv++;
				 argc--;
			}
		}
	}

	if(help_requested == TRUE) 
	{
		exit(0);
	}

	if(p_info->crc_table_status == WARM) 
		printf("Table Status, WARM\n");
 	else
		printf("Table Status, COLD\n");
	if(p_info->crc_data_status == WARM) 
		printf("Data Status, WARM\n");
 	else
		printf("Data Status, COLD\n");	
	printf("Number of Iterations, %d\n", p_info->crc_num_of_iterations);
	printf("Packet Size (bytes), %d\n", p_info->crc_packet_size);
	if(p_info->crc_iteration_style == CONSTANT) 
		printf("Iteration Style, CONSTANT\n");
 	else if(p_info->crc_iteration_style == RANDOM) 
		printf("Iteration Style, RANDOM\n");
	else  
		printf("Iteration Style, INCREMENTAL\n");
	printf("Alignment (bytes), %d\n", p_info->crc_alignment);
	if(p_info->crc_alignment_style == CONSTANT) 
		printf("Alignment Style, CONSTANT\n");
 	else if(p_info->crc_alignment_style == RANDOM) 
		printf("Alignment Style, RANDOM\n");
	else  
		printf("Alignment Style, INCREMENTAL\n");
	printf("\n");

	//we begin with setting the packet size and alignment
	packet_size = p_info->crc_packet_size;
	alignment	= p_info->crc_alignment;
	if((alignment == 1) && (p_info->crc_alignment_style == CONSTANT))
		mode = MODE_BODY;
	else
		mode = MODE_ALIGN;

	//second, we perform the mpa sample frame test		
	mpa_sample_frame_test();

	// allocate an array of test objects
	
	p_test = (crc_test_t *)malloc(p_info->crc_num_of_iterations * sizeof(crc_test_t));
	memset((void *)p_test, 0, p_info->crc_num_of_iterations * sizeof(crc_test_t));


	//next, we allocate memory for all packet buffers
	for( i = 0; i < p_info->crc_num_of_iterations; i++)
	{	
		total_bytes += packet_size;
		p_test[i].buf_length = packet_size;
		p_test[i].p_sbuf = (uint8_t *)malloc(packet_size * sizeof(uint8_t));
		p_test[i].p_dbuf = (uint8_t *)malloc(packet_size * sizeof(uint8_t));

		//set the data to be random numbers
		for( j = 0; j < p_test[i].buf_length; j++)
			p_test[i].p_sbuf[j] = (uint8_t)rand();

		// compute the reference CRC used to validate other algos
		p_test[i].crc_value = 
			crc32c( NULL, p_test[i].p_sbuf, p_test[i].buf_length, MODE_BODY);

		// Set the packet size for the next iteration.
		switch( p_info->crc_iteration_style )
		{
		case INCREMENTAL:
			packet_size += PACKET_SIZE_INCREMENT;
			if(packet_size >= MAX_BUF_SIZE)
				packet_size = MIN_BUF_SIZE;
			break;

		case RANDOM:
			packet_size = MIN_BUF_SIZE + (rand() % (MAX_BUF_SIZE - MIN_BUF_SIZE) );
			break;

		default:
			// Nothing to do
			break;
		}

		p_test[i].crc_status = CRC_PASSED; 

		switch( p_info->crc_alignment_style )
		{
		case INCREMENTAL:
			p_test[i].alignment += ALIGNMENT_INCREMENT;
			if(p_test[i].alignment >= MAX_ALIGNMENT)
				p_test[i].alignment = MIN_ALIGNMENT;
			break;

		case RANDOM:
			p_test[i].alignment = (uint8_t)(MIN_ALIGNMENT + (rand() % (MAX_ALIGNMENT - MIN_ALIGNMENT)));
			break;

		default:
			// Nothing to do.
			break;
		}
	}
	

	//we test the slice by 8
	set_cache_state( p_test, p_info );
	WARM_LOCAL_VARS;
	CPU_SYNC;
	CPU_GET_CYCLES( before );

	for( i = 0; i < p_info->crc_num_of_iterations; i++ )
	{	
		value1 = crc32c_sb8_64_bit(NULL, p_test[i].p_sbuf,
			p_test[i].buf_length, p_test[i].alignment, mode);
	}

	CPU_SYNC;
	CPU_GET_CYCLES(after);
	cycles = after - before;

	printf("Slicing by 8 Algorithm (cycles/byte), %f\n", 
		(float)(cycles)/(float)(total_bytes));

	//then we repeat the same loop for the Sarwate algorithm
	set_cache_state( p_test, p_info );
	WARM_LOCAL_VARS;
	CPU_SYNC;
	CPU_GET_CYCLES( before );

	for(i=0; i < p_info->crc_num_of_iterations; i++)
	{	
		value2 = crc32c(NULL, p_test[i].p_sbuf,
			p_test[i].buf_length, mode);
	}


	CPU_SYNC;
	CPU_GET_CYCLES(after);
	cycles = after - before;
	if(value1 != value2)
	{
		printf("CRC calculation error\n");
		exit(0);
	}
	printf("Sarwate Algorithm: (cycles/byte), %f\n", 
		(float)(cycles)/(float)(total_bytes));

}
