/* @(#)breakline.c	1.9 03/06/15 Copyright 1985, 1995-2003 J. Schilling */
/*
 *	break a line pointed to by *buf into fields
 *	returns the number of tokens, the line was broken into (>= 1)
 *
 *	delim is the delimiter to break at
 *	array[0 .. found-1] point to strings from broken line
 *	array[found ... len] point to '\0'
 *	len is the size of the array
 *
 *	Copyright (c) 1985, 1995-2003 J. Schilling
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
#include <schily.h>

#ifdef	PROTOTYPES
EXPORT int
breakline(char *buf,
		register char delim,
		register char *array[],
		register int len)
#else
EXPORT int
breakline(buf, delim, array, len)
		char	*buf;
	register char	delim;
	register char	*array[];
	register int	len;
#endif
{
	register char	*bp = buf;
	register char	*dp;
	register int	i;
	register int	found;

	for (i = 0, found = 1; i < len; i++) {
		for (dp = bp; *dp != '\0' && *dp != delim; dp++)
			;

		array[i] = bp;
		if (*dp == delim) {
			*dp++ = '\0';
			found++;
		}
		bp = dp;
	}
	return (found);
}
