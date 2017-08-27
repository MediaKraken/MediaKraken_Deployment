/* @(#)swabbytes.c	1.6 03/06/15 Copyright 1988, 1995-2003 J. Schilling */
/*
 *	swab bytes in memory
 *
 *	Copyright (c) 1988, 1995-2003 J. Schilling
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

#include <standard.h>
#include <schily.h>

#define	DO8(a)	a; a; a; a; a; a; a; a;

EXPORT void
swabbytes(vp, cnt)
		void	*vp;
	register int	cnt;
{
	register char	*bp = (char *)vp;
	register char	c;

	cnt /= 2;	/* even count only */
	while ((cnt -= 8) >= 0) {
		DO8(c = *bp++; bp[-1] = *bp; *bp++ = c;);
	}
	cnt += 8;
	while (--cnt >= 0) {
		c = *bp++; bp[-1] = *bp; *bp++ = c;
	}
}
