/* @(#)filemopen.c	1.3 04/08/08 Copyright 1986, 1995-2004 J. Schilling */
/*
 *	Copyright (c) 1986, 1995-2004 J. Schilling
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

EXPORT FILE *
#ifdef	PROTOTYPES
filemopen(const char *name, const char *mode, mode_t cmode)
#else
filemopen(name, mode, cmode)
	const char	*name;
	const char	*mode;
	mode_t		cmode;
#endif
{
	int	ret;
	int	omode = 0;
	int	flag = 0;

	if (!_cvmod(mode, &omode, &flag))
		return ((FILE *) NULL);

/*	if ((ret = _openfd(name, omode)) < 0)*/
	if ((ret = open(name, omode, cmode)) < 0)
		return ((FILE *) NULL);

	return (_fcons((FILE *)0, ret, flag));
}
