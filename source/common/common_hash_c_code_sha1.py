import zipfile

from np_inline import inline_debug as inline


def com_hash_sha1_c(file_name):
    """
    c call for sha1 hash generation by file name
    """
    num = 0
    while 1:
        zip_handle = zipfile.ZipFile(file_name, 'r')  # issues if u do RB
        for zippedfile in zip_handle.namelist():
            # calculate sha1 hash
            #            SHA1.update(zip_handle.read(zippedfile))
            zip_file_data = zip_handle.read(zippedfile)
            R = inline(COM_C_CODE, [zip_file_data],
                       support_code=COM_SHA1_CODE)
        zip_handle.close()
        num += 1
        if num > 5:
            break


# All C code below is following license
'''
Copyright (C) 1998, 2009
Paul E. Jones <paulej@packetizer.com>

Freeware Public License (FPL)

This software is licensed as "freeware."  Permission to distribute
this software in source and binary forms, including incorporation 
into other products, is hereby granted without a fee.  THIS SOFTWARE 
IS PROVIDED 'AS IS' AND WITHOUT ANY EXPRESSED OR IMPLIED WARRANTIES, 
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
AND FITNESS FOR A PARTICULAR PURPOSE.  THE AUTHOR SHALL NOT BE HELD 
LIABLE FOR ANY DAMAGES RESULTING FROM THE USE OF THIS SOFTWARE, EITHER 
DIRECTLY OR INDIRECTLY, INCLUDING, BUT NOT LIMITED TO, LOSS OF DATA 
OR DATA BEING RENDERED INACCURATE
'''

"""
C code for faster hashing
"""
COM_SHA1_HEADER_CODE = '''
    /*
     *  sha1.h
     *
     *  Copyright (C) 1998, 2009
     *  Paul E. Jones <paulej@packetizer.com>
     *  All Rights Reserved
     *
     *****************************************************************************
     *  $Id: sha1.h 12 2009-06-22 19:34:25Z paulej $
     *****************************************************************************
     *
     *  Description:
     *      This class implements the Secure Hashing Standard as defined
     *      in FIPS PUB 180-1 published April 17, 1995.
     *
     *      Many of the variable names in the SHA1Context, especially the
     *      single character names, were used because those were the names
     *      used in the publication.
     *
     *      Please read the file sha1.c for more information.
     *
     */

    #ifndef _SHA1_H_
    #define _SHA1_H_

    /*
     *  This structure will hold context information for the hashing
     *  operation
     */
    typedef struct SHA1Context
    {
        unsigned Message_Digest[5]; /* Message Digest (output)          */

        unsigned Length_Low;        /* Message length in bits           */
        unsigned Length_High;       /* Message length in bits           */

        unsigned char Message_Block[64]; /* 512-bit message blocks      */
        int Message_Block_Index;    /* Index into message block array   */

        int Computed;               /* Is the digest computed?          */
        int Corrupted;              /* Is the message digest corruped?  */
    } SHA1Context;

    /*
     *  Function Prototypes
     */
    void SHA1Reset(SHA1Context *);
    int SHA1Result(SHA1Context *);
    void SHA1Input( SHA1Context *,
                    const unsigned char *,
                    unsigned);

    #endif
'''

COM_SHA1_CODE = '''
    /*
     *  sha1.c
     *
     *  Copyright (C) 1998, 2009
     *  Paul E. Jones <paulej@packetizer.com>
     *  All Rights Reserved
     *
     *****************************************************************************
     *  $Id: sha1.c 12 2009-06-22 19:34:25Z paulej $
     *****************************************************************************
     *
     *  Description:
     *      This file implements the Secure Hashing Standard as defined
     *      in FIPS PUB 180-1 published April 17, 1995.
     *
     *      The Secure Hashing Standard, which uses the Secure Hashing
     *      Algorithm (SHA), produces a 160-bit message digest for a
     *      given data stream.  In theory, it is highly improbable that
     *      two messages will produce the same message digest.  Therefore,
     *      this algorithm can serve as a means of providing a "fingerprint"
     *      for a message.
     *
     *  Portability Issues:
     *      SHA-1 is defined in terms of 32-bit "words".  This code was
     *      written with the expectation that the processor has at least
     *      a 32-bit machine word size.  If the machine word size is larger,
     *      the code should still function properly.  One caveat to that
     *      is that the input functions taking characters and character
     *      arrays assume that only 8 bits of information are stored in each
     *      character.
     *
     *  Caveats:
     *      SHA-1 is designed to work with messages less than 2^64 bits
     *      long. Although SHA-1 allows a message digest to be generated for
     *      messages of any number of bits less than 2^64, this
     *      implementation only works with messages with a length that is a
     *      multiple of the size of an 8-bit character.
     *
     */

    #include "sha1.h"

    /*
     *  Define the circular shift macro
     */
    #define SHA1CircularShift(bits,word) \
                    ((((word) << (bits)) & 0xFFFFFFFF) | \
                    ((word) >> (32-(bits))))

    /* Function prototypes */
    void SHA1ProcessMessageBlock(SHA1Context *);
    void SHA1PadMessage(SHA1Context *);

    /*
     *  SHA1Reset
     *
     *  Description:
     *      This function will initialize the SHA1Context in preparation
     *      for computing a new message digest.
     *
     *  Parameters:
     *      context: [in/out]
     *          The context to reset.
     *
     *  Returns:
     *      Nothing.
     *
     *  Comments:
     *
     */
    void SHA1Reset(SHA1Context *context)
    {
        context->Length_Low             = 0;
        context->Length_High            = 0;
        context->Message_Block_Index    = 0;

        context->Message_Digest[0]      = 0x67452301;
        context->Message_Digest[1]      = 0xEFCDAB89;
        context->Message_Digest[2]      = 0x98BADCFE;
        context->Message_Digest[3]      = 0x10325476;
        context->Message_Digest[4]      = 0xC3D2E1F0;

        context->Computed   = 0;
        context->Corrupted  = 0;
    }

    /*
     *  SHA1Result
     *
     *  Description:
     *      This function will return the 160-bit message digest into the
     *      Message_Digest array within the SHA1Context provided
     *
     *  Parameters:
     *      context: [in/out]
     *          The context to use to calculate the SHA-1 hash.
     *
     *  Returns:
     *      1 if successful, 0 if it failed.
     *
     *  Comments:
     *
     */
    int SHA1Result(SHA1Context *context)
    {

        if (context->Corrupted)
        {
            return 0;
        }

        if (!context->Computed)
        {
            SHA1PadMessage(context);
            context->Computed = 1;
        }

        return 1;
    }

    /*
     *  SHA1Input
     *
     *  Description:
     *      This function accepts an array of octets as the next portion of
     *      the message.
     *
     *  Parameters:
     *      context: [in/out]
     *          The SHA-1 context to update
     *      message_array: [in]
     *          An array of characters representing the next portion of the
     *          message.
     *      length: [in]
     *          The length of the message in message_array
     *
     *  Returns:
     *      Nothing.
     *
     *  Comments:
     *
     */
    void SHA1Input(     SHA1Context         *context,
                        const unsigned char *message_array,
                        unsigned            length)
    {
        if (!length)
        {
            return;
        }

        if (context->Computed || context->Corrupted)
        {
            context->Corrupted = 1;
            return;
        }

        while(length-- && !context->Corrupted)
        {
            context->Message_Block[context->Message_Block_Index++] =
                                                    (*message_array & 0xFF);

            context->Length_Low += 8;
            /* Force it to 32 bits */
            context->Length_Low &= 0xFFFFFFFF;
            if (context->Length_Low == 0)
            {
                context->Length_High++;
                /* Force it to 32 bits */
                context->Length_High &= 0xFFFFFFFF;
                if (context->Length_High == 0)
                {
                    /* Message is too long */
                    context->Corrupted = 1;
                }
            }

            if (context->Message_Block_Index == 64)
            {
                SHA1ProcessMessageBlock(context);
            }

            message_array++;
        }
    }

    /*
     *  SHA1ProcessMessageBlock
     *
     *  Description:
     *      This function will process the next 512 bits of the message
     *      stored in the Message_Block array.
     *
     *  Parameters:
     *      None.
     *
     *  Returns:
     *      Nothing.
     *
     *  Comments:
     *      Many of the variable names in the SHAContext, especially the
     *      single character names, were used because those were the names
     *      used in the publication.
     *
     *
     */
    void SHA1ProcessMessageBlock(SHA1Context *context)
    {
        const unsigned K[] =            /* Constants defined in SHA-1   */
        {
            0x5A827999,
            0x6ED9EBA1,
            0x8F1BBCDC,
            0xCA62C1D6
        };
        int         t;                  /* Loop counter                 */
        unsigned    temp;               /* Temporary word value         */
        unsigned    W[80];              /* Word sequence                */
        unsigned    A, B, C, D, E;      /* Word buffers                 */

        /*
         *  Initialize the first 16 words in the array W
         */
        for(t = 0; t < 16; t++)
        {
            W[t] = ((unsigned) context->Message_Block[t * 4]) << 24;
            W[t] |= ((unsigned) context->Message_Block[t * 4 + 1]) << 16;
            W[t] |= ((unsigned) context->Message_Block[t * 4 + 2]) << 8;
            W[t] |= ((unsigned) context->Message_Block[t * 4 + 3]);
        }

        for(t = 16; t < 80; t++)
        {
           W[t] = SHA1CircularShift(1,W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16]);
        }

        A = context->Message_Digest[0];
        B = context->Message_Digest[1];
        C = context->Message_Digest[2];
        D = context->Message_Digest[3];
        E = context->Message_Digest[4];

        for(t = 0; t < 20; t++)
        {
            temp =  SHA1CircularShift(5,A) +
                    ((B & C) | ((~B) & D)) + E + W[t] + K[0];
            temp &= 0xFFFFFFFF;
            E = D;
            D = C;
            C = SHA1CircularShift(30,B);
            B = A;
            A = temp;
        }

        for(t = 20; t < 40; t++)
        {
            temp = SHA1CircularShift(5,A) + (B ^ C ^ D) + E + W[t] + K[1];
            temp &= 0xFFFFFFFF;
            E = D;
            D = C;
            C = SHA1CircularShift(30,B);
            B = A;
            A = temp;
        }

        for(t = 40; t < 60; t++)
        {
            temp = SHA1CircularShift(5,A) +
                   ((B & C) | (B & D) | (C & D)) + E + W[t] + K[2];
            temp &= 0xFFFFFFFF;
            E = D;
            D = C;
            C = SHA1CircularShift(30,B);
            B = A;
            A = temp;
        }

        for(t = 60; t < 80; t++)
        {
            temp = SHA1CircularShift(5,A) + (B ^ C ^ D) + E + W[t] + K[3];
            temp &= 0xFFFFFFFF;
            E = D;
            D = C;
            C = SHA1CircularShift(30,B);
            B = A;
            A = temp;
        }

        context->Message_Digest[0] =
                            (context->Message_Digest[0] + A) & 0xFFFFFFFF;
        context->Message_Digest[1] =
                            (context->Message_Digest[1] + B) & 0xFFFFFFFF;
        context->Message_Digest[2] =
                            (context->Message_Digest[2] + C) & 0xFFFFFFFF;
        context->Message_Digest[3] =
                            (context->Message_Digest[3] + D) & 0xFFFFFFFF;
        context->Message_Digest[4] =
                            (context->Message_Digest[4] + E) & 0xFFFFFFFF;

        context->Message_Block_Index = 0;
    }

    /*
     *  SHA1PadMessage
     *
     *  Description:
     *      According to the standard, the message must be padded to an even
     *      512 bits.  The first padding bit must be a '1'.  The last 64
     *      bits represent the length of the original message.  All bits in
     *      between should be 0.  This function will pad the message
     *      according to those rules by filling the Message_Block array
     *      accordingly.  It will also call SHA1ProcessMessageBlock()
     *      appropriately.  When it returns, it can be assumed that the
     *      message digest has been computed.
     *
     *  Parameters:
     *      context: [in/out]
     *          The context to pad
     *
     *  Returns:
     *      Nothing.
     *
     *  Comments:
     *
     */
    void SHA1PadMessage(SHA1Context *context)
    {
        /*
         *  Check to see if the current message block is too small to hold
         *  the initial padding bits and length.  If so, we will pad the
         *  block, process it, and then continue padding into a second
         *  block.
         */
        if (context->Message_Block_Index > 55)
        {
            context->Message_Block[context->Message_Block_Index++] = 0x80;
            while(context->Message_Block_Index < 64)
            {
                context->Message_Block[context->Message_Block_Index++] = 0;
            }

            SHA1ProcessMessageBlock(context);

            while(context->Message_Block_Index < 56)
            {
                context->Message_Block[context->Message_Block_Index++] = 0;
            }
        }
        else
        {
            context->Message_Block[context->Message_Block_Index++] = 0x80;
            while(context->Message_Block_Index < 56)
            {
                context->Message_Block[context->Message_Block_Index++] = 0;
            }
        }

        /*
         *  Store the message length as the last 8 octets
         */
        context->Message_Block[56] = (context->Length_High >> 24) & 0xFF;
        context->Message_Block[57] = (context->Length_High >> 16) & 0xFF;
        context->Message_Block[58] = (context->Length_High >> 8) & 0xFF;
        context->Message_Block[59] = (context->Length_High) & 0xFF;
        context->Message_Block[60] = (context->Length_Low >> 24) & 0xFF;
        context->Message_Block[61] = (context->Length_Low >> 16) & 0xFF;
        context->Message_Block[62] = (context->Length_Low >> 8) & 0xFF;
        context->Message_Block[63] = (context->Length_Low) & 0xFF;

        SHA1ProcessMessageBlock(context);
    }
'''

COM_C_CODE = '''
/*
 *  sha.cpp
 *
 *  Copyright (C) 1998, 2009
 *  Paul E. Jones <paulej@packetizer.com>
 *  All Rights Reserved
 *
 *****************************************************************************
 *  $Id: sha.c 12 2009-06-22 19:34:25Z paulej $
 *****************************************************************************
 *
 *  Description:
 *      This utility will display the message digest (fingerprint) for
 *      the specified file(s).
 *
 *  Portability Issues:
 *      None.
 */

#include <stdio.h>
#include <string.h>
#ifdef WIN32
#include <io.h>
#endif
#include <fcntl.h>
#include "sha1.h"

/*
 *  Function prototype
 */
void usage();


/*  
 *  main
 *
 *  Description:
 *      This is the entry point for the program
 *
 *  Parameters:
 *      argc: [in]
 *          This is the count of arguments in the argv array
 *      argv: [in]
 *          This is an array of filenames for which to compute message
 *          digests
 *
 *  Returns:
 *      Nothing.
 *
 *  Comments:
 *
 */
int main(int argc, char *argv[])
{
    SHA1Context sha;                /* SHA-1 context                 */
    FILE        *fp;                /* File pointer for reading files*/
    char        c;                  /* Character read from file      */
    int         i;                  /* Counter                       */
    int         reading_stdin;      /* Are we reading standard in?   */
    int         read_stdin = 0;     /* Have we read stdin?           */

    /*
     *  Check the program arguments and print usage information if -?
     *  or --help is passed as the first argument.
     */
    if (argc > 1 && (!strcmp(argv[1],"-?") ||
        !strcmp(argv[1],"--help")))
    {
        usage();
        return 1;
    }

    /*
     *  For each filename passed in on the command line, calculate the
     *  SHA-1 value and display it.
     */
    for(i = 0; i < argc; i++)
    {
        /*
         *  We start the counter at 0 to guarantee entry into the for
         *  loop. So if 'i' is zero, we will increment it now.  If there
         *  is no argv[1], we will use STDIN below.
         */
        if (i == 0)
        {
            i++;
        }

        if (argc == 1 || !strcmp(argv[i],"-"))
        {
#ifdef WIN32
            setmode(fileno(stdin), _O_BINARY);
#endif
            fp = stdin;
            reading_stdin = 1;
        }
        else
        {
            if (!(fp = fopen(argv[i],"rb")))
            {
                fprintf(stderr,
                        "sha: unable to open file %s\n",
                        argv[i]);
                return 2;
            }
            reading_stdin = 0;
        }

        /*
         *  We do not want to read STDIN multiple times
         */
        if (reading_stdin)
        {
            if (read_stdin)
            {
                continue;
            }

            read_stdin = 1;
        }

        /*
         *  Reset the SHA-1 context and process input
         */
        SHA1Reset(&sha);

        c = fgetc(fp);
        while(!feof(fp))
        {
            SHA1Input(&sha, &c, 1);
            c = fgetc(fp);
        }

        if (!reading_stdin)
        {
            fclose(fp);
        }

        if (!SHA1Result(&sha))
        {
            fprintf(stderr,
                    "sha: could not compute message digest for %s\n",
                    reading_stdin?"STDIN":argv[i]);
        }
        else
        {
            printf( "%08X %08X %08X %08X %08X - %s\n",
                    sha.Message_Digest[0],
                    sha.Message_Digest[1],
                    sha.Message_Digest[2],
                    sha.Message_Digest[3],
                    sha.Message_Digest[4],
                    reading_stdin?"STDIN":argv[i]);
        }
    }

    return 0;
}

/*  
 *  usage
 *
 *  Description:
 *      This function will display program usage information to the
 *      user.
 *
 *  Parameters:
 *      None.
 *
 *  Returns:
 *      Nothing.
 *
 *  Comments:
 *
 */
void usage()
{
    printf("usage: sha <file> [<file> ...]\n");
    printf("\tThis program will display the message digest\n");
    printf("\tfor files using the Secure Hashing Algorithm (SHA-1).\n");
}


    #include <stdio.h>
    #include <string.h>
    #include "sha1.h"

    #define TESTA   "abchhtyjtyj56y5y655h565656655656565656h5"

    SHA1Context sha;
    char st1[40] = "";
    char st2[8];
    int i = 0;
    SHA1Reset(&sha);
    SHA1Input(&sha, (const unsigned char *) TESTA, strlen(TESTA));

    if (!SHA1Result(&sha))
    {
        fprintf(stderr, "ERROR-- could not compute message digest");
    }
    else
    {
        for(i = 0; i < 5 ; i++)
        {
            sprintf(st2, "%X", sha.Message_Digest[i]);
            strcat(st1,st2);
        }
    }
    printf(st1);
    return_val = st1;
'''
