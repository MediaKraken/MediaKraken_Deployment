/* @(#)stdxlib.h	1.6 01/07/15 Copyright 1996 J. Schilling */
/*
 *	Definitions for stdlib
 *
 *	Copyright (c) 1996 J. Schilling
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

#ifndef _STDXLIB_H
#define	_STDXLIB_H

#ifndef	_MCONFIG_H
#include <mconfig.h>
#endif

#ifdef	HAVE_STDLIB_H
#ifndef	_INCL_STDLIB_H
#include <stdlib.h>
#define	_INCL_STDLIB_H
#endif
#else

extern	char	*malloc();
extern	char	*realloc();

extern	double	atof();

#endif	/* HAVE_STDLIB_H */

#ifndef	EXIT_FAILURE
#define	EXIT_FAILURE	1
#endif
#ifndef	EXIT_SUCCESS
#define	EXIT_SUCCESS	0
#endif
#ifndef	RAND_MAX
#define	RAND_MAX	32767
#endif

#endif	/* _STDXLIB_H */
