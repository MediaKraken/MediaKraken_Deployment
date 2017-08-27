/* @(#)snprintf.c	1.9 04/05/09 Copyright 1985, 1996-2004 J. Schilling */
/*
 *	Copyright (c) 1985, 1996-2004 J. Schilling
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

#define	snprintf __nothing__	/* prototype may be wrong (e.g. IRIX) */
#include <mconfig.h>
#include <unixstd.h>		/* include <sys/types.h> try to get size_t */
#include <stdio.h>		/* Try again for size_t	*/
#include <stdxlib.h>		/* Try again for size_t	*/
#include <vadefs.h>
#include <standard.h>
#include <schily.h>
#undef	snprintf

EXPORT	int snprintf __PR((char *, size_t maxcnt, const char *, ...));

typedef struct {
	char	*ptr;
	int	count;
} *BUF, _BUF;

#ifdef	PROTOTYPES
static void _cput(char c, long l)
#else
static void _cput(c, l)
	char	c;
	long	l;
#endif
{
	register BUF	bp = (BUF)l;

	if (--bp->count > 0) {
		*bp->ptr++ = c;
	} else {
		/*
		 * Make sure that there will never be a negative overflow.
		 */
		bp->count++;
	}
}

/* VARARGS2 */
#ifdef	PROTOTYPES
EXPORT int
snprintf(char *buf, size_t maxcnt, const char *form, ...)
#else
EXPORT int
snprintf(buf, maxcnt, form, va_alist)
	char	*buf;
	unsigned maxcnt;
	char	*form;
	va_dcl
#endif
{
	va_list	args;
	int	cnt;
	_BUF	bb;

	bb.ptr = buf;
	bb.count = maxcnt;

#ifdef	PROTOTYPES
	va_start(args, form);
#else
	va_start(args);
#endif
	cnt = format(_cput, (long)&bb, form,  args);
	va_end(args);
	if (maxcnt > 0)
		*(bb.ptr) = '\0';
	if (bb.count < 0)
		return (-1);

	return (cnt);
}
