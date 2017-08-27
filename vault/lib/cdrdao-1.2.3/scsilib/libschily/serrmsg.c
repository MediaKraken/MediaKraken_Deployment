/* @(#)serrmsg.c	1.3 03/06/15 Copyright 1985, 2000-2003 J. Schilling */
/*
 *	Routines for printing command errors
 *
 *	Copyright (c) 1985, 2000-2003 J. Schilling
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
#include <unixstd.h>		/* include <sys/types.h> try to get size_t */
#include <stdio.h>		/* Try again for size_t	*/
#include <stdxlib.h>		/* Try again for size_t	*/
#include <standard.h>
#include <stdxlib.h>
#include <vadefs.h>
#include <strdefs.h>
#include <schily.h>
#ifndef	HAVE_STRERROR
extern	char	*sys_errlist[];
extern	int	sys_nerr;
#endif

EXPORT	int	serrmsg		__PR((char *buf, size_t maxcnt, const char *, ...));
EXPORT	int	serrmsgno	__PR((int, char *buf, size_t maxcnt, const char *, ...));
LOCAL	int	_serrmsg	__PR((int, char *buf, size_t maxcnt, const char *, va_list));

/* VARARGS1 */
EXPORT int
#ifdef	PROTOTYPES
serrmsg(char *buf, size_t maxcnt, const char *msg, ...)
#else
serrmsg(buf, maxcnt, msg, va_alist)
	char	*buf;
	size_t	maxcnt;
	char	*msg;
	va_dcl
#endif
{
	va_list	args;
	int	ret;

#ifdef	PROTOTYPES
	va_start(args, msg);
#else
	va_start(args);
#endif
	ret = _serrmsg(geterrno(), buf, maxcnt, msg, args);
	va_end(args);
	return (ret);
}

/* VARARGS2 */
#ifdef	PROTOTYPES
EXPORT int
serrmsgno(int err, char *buf, size_t maxcnt, const char *msg, ...)
#else
serrmsgno(err, buf, maxcnt, msg, va_alist)
	int	err;
	char	*buf;
	size_t	maxcnt;
	char	*msg;
	va_dcl
#endif
{
	va_list	args;
	int	ret;

#ifdef	PROTOTYPES
	va_start(args, msg);
#else
	va_start(args);
#endif
	ret = _serrmsg(err, buf, maxcnt, msg, args);
	va_end(args);
	return (ret);
}

LOCAL int
_serrmsg(err, buf, maxcnt, msg, args)
	int		err;
	char		*buf;
	size_t		maxcnt;
	const char	*msg;
	va_list		args;
{
	int	ret;
	char	errbuf[20];
	char	*errnam;
	char	*prognam = get_progname();

	if (err < 0) {
		ret = js_snprintf(buf, maxcnt, "%s: %r", prognam, msg, args);
	} else {
		errnam = errmsgstr(err);
		if (errnam == NULL) {
			(void) js_snprintf(errbuf, sizeof (errbuf),
						"Error %d", err);
			errnam = errbuf;
		}
		ret = js_snprintf(buf, maxcnt,
				"%s: %s. %r", prognam, errnam, msg, args);
	}
	return (ret);
}
