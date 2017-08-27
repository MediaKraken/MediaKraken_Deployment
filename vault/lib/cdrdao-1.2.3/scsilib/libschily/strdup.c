/* @(#)strdup.c	1.1 03/02/27 Copyright 2003 J. Schilling */
#ifndef lint
static	char sccsid[] =
	"@(#)strdup.c	1.1 03/02/27 Copyright 2003 J. Schilling";
#endif
/*
 *	strdup() to be used if missing on libc
 *
 *	Copyright (c) 2003 J. Schilling
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

#include <mconfig.h>
#include <standard.h>
#include <stdxlib.h>
#include <strdefs.h>
#include <schily.h>
#include <libport.h>

#ifndef	HAVE_STRDUP

EXPORT char *
strdup(s)
	const char	*s;
{
	unsigned i	= strlen(s) + 1;
	char	 *res	= malloc(i);

	if (res == NULL)
		return (NULL);
	if (i > 16) {
		movebytes(s, res, (int) i);
	} else {
		char	*s2 = res;

		while ((*s2++ = *s++) != '\0')
			;
	}
	return (res);
}
#endif	/* HAVE_STRDUP */
