/* @(#)getpagesize.c	1.1 01/11/28 Copyright 2001 J. Schilling */
#ifndef lint
static	char sccsid[] =
	"@(#)getpagesize.c	1.1 01/11/28 Copyright 2001 J. Schilling";
#endif
/*
 *	Copyright (c) 2001 J. Schilling
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
 * You should have received a copy of the GNU General Public License
 * along with this program; see the file COPYING.  If not, write to
 * the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
 */

#include <mconfig.h>

#ifndef	HAVE_GETPAGESIZE
#include <unixstd.h>
#include <standard.h>
#ifdef	HAVE_SYS_PARAM_H
#include <sys/param.h>
#endif
#include <libport.h>

#ifdef	HAVE_OS_H
#include <OS.h>		/* BeOS for B_PAGE_SIZE */
#endif

EXPORT	int	getpagesize	__PR((void));

EXPORT int
getpagesize()
{
	register int	pagesize;

#ifdef	_SC_PAGESIZE
	pagesize = sysconf(_SC_PAGESIZE);
#else	/* ! _SC_PAGESIZE */


#ifdef	PAGESIZE		/* Traditional UNIX page size from param.h */
	pagesize = PAGESIZE;

#else	/* ! PAGESIZE */

#ifdef	B_PAGE_SIZE		/* BeOS page size from OS.h */
	pagesize = B_PAGE_SIZE;

#else	/* ! B_PAGE_SIZE */

	pagesize = 512;
#endif	/* ! B_PAGE_SIZE */
#endif	/* ! PAGESIZE */
#endif	/* ! _SC_PAGESIZE */

	return (pagesize);
}

#endif	/* HAVE_GETPAGESIZE */
