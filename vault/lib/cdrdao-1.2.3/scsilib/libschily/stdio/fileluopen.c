/* @(#)fileluopen.c	1.17 04/08/08 Copyright 1986, 1995-2003 J. Schilling */
/*
 *	Copyright (c) 1986, 1995-2003 J. Schilling
 */
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * this program; see the file COPYING.  If not, write to the Free Software
 * Foundation, 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */

#include "schilyio.h"

/*
 * Note that because of a definition in schilyio.h we are using fseeko()/ftello()
 * instead of fseek()/ftell() if available.
 */

#ifndef	O_NDELAY		/* This is undefined on BeOS :-( */
#define	O_NDELAY	0
#endif
#ifndef	O_CREAT
#define	O_CREAT		0
#endif
#ifndef	O_TRUNC
#define	O_TRUNC		0
#endif
#ifndef	O_EXCL
#define	O_EXCL		0
#endif

/*
 *	fileluopen - open a stream for lun
 */
EXPORT FILE *
fileluopen(f, mode)
	int		f;
	const char	*mode;
{
	int	omode = 0;
	int	flag = 0;

	if (!_cvmod(mode, &omode, &flag))
		return ((FILE *) NULL);

	if (omode & (O_NDELAY|O_CREAT|O_TRUNC|O_EXCL)) {
		raisecond(_badmode, 0L);
		return ((FILE *) NULL);
	}

#ifdef	F_GETFD
	if (fcntl(f, F_GETFD, 0) < 0) {
		raisecond(_badfile, 0L);
		return ((FILE *) NULL);
	}
#endif

#ifdef	O_APPEND
	if (omode & O_APPEND)
		lseek(f, (off_t)0, SEEK_END);
#endif

	return (_fcons((FILE *)0, f, flag));
}
