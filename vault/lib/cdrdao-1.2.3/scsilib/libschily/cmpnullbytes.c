/* @(#)cmpnullbytes.c	1.2 03/06/15 Copyright 1988,2002-2003 J. Schilling */
#ifndef lint
static	char sccsid[] =
	"@(#)cmpnullbytes.c	1.2 03/06/15 Copyright 1988,2002-2003 J. Schilling";
#endif  /* lint */
/*
 *	compare data against null
 *
 *	Copyright (c) 1988,2002-2003 J. Schilling
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
#include <align.h>
#include <schily.h>

#define	DO8(a)	a; a; a; a; a; a; a; a;

EXPORT int
cmpnullbytes(fromp, cnt)
	const void	*fromp;
	int		cnt;
{
	register const char	*from	= (char *)fromp;
	register int		n;

	/*
	 * If we change cnt to be unsigned, check for == instead of <=
	 */
	if ((n = cnt) <= 0)
		return (cnt);

	/*
	 * Compare byte-wise until properly aligned for a long pointer.
	 */
	while (--n >= 0 && !laligned(from)) {
		if (*from++ != 0)
			goto cdiff;
	}
	n++;

	if (n >= (int)(8 * sizeof (long))) {
		if (laligned(from)) {
			register const long *froml = (const long *)from;
			register int rem = n % (8 * sizeof (long));

			n /= (8 * sizeof (long));
			do {
				DO8(
					if (*froml++ != 0)
						break;
				);
			} while (--n > 0);

			if (n > 0) {
				--froml;
				from = (const char *)froml;
				goto ldiff;
			}
			from = (const char *)froml;
			n = rem;
		}

		if (n >= 8) {
			n -= 8;
			do {
				DO8(
					if (*from++ != 0)
						goto cdiff;
				);
			} while ((n -= 8) >= 0);
			n += 8;
		}
		if (n > 0) do {
			if (*from++ != 0)
				goto cdiff;
		} while (--n > 0);
		return (cnt);
	}
	if (n > 0) do {
		if (*from++ != 0)
			goto cdiff;
	} while (--n > 0);
	return (cnt);
ldiff:
	n = sizeof (long);
	do {
		if (*from++ != 0)
			goto cdiff;
	} while (--n > 0);
cdiff:
	return (--from - (char *)fromp);
}
