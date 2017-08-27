/* @(#)rename.c	1.6 04/09/04 Copyright 1998-2003 J. Schilling */
#ifndef lint
static	char sccsid[] =
	"@(#)rename.c	1.6 04/09/04 Copyright 1998-2003 J. Schilling";
#endif
/*
 *	rename() for old systems that don't have it.
 *
 *	Copyright (c) 1998-2003 J. Schilling
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

#define	rename	__nothing__
#include <mconfig.h>

#ifndef	HAVE_RENAME

#include <stdio.h>	/* XXX not OK but needed for js_xx() in schily.h */
#include <unixstd.h>
#include <strdefs.h>
#include <statdefs.h>
#include <maxpath.h>
#include <standard.h>
#include <utypes.h>
#include <schily.h>
#include <errno.h>
#undef	rename
#include <libport.h>

#ifndef	MAXPATHNAME
#define	MAXPATHNAME	1024
#endif

#if	MAXPATHNAME < 1024
#undef	MAXPATHNAME
#define	MAXPATHNAME	1024
#endif

#define	MAXNAME	MAXPATHNAME

#define	FILEDESC struct stat

#ifndef	HAVE_LSTAT
#define	lstat	stat
#endif

EXPORT int
rename(old, new)
	const char	*old;
	const char	*new;
{
	char	nname[MAXNAME];
	char	bakname[MAXNAME];
	char	strpid[32];
	int	strplen;
	BOOL	savpresent = FALSE;
	BOOL	newpresent = FALSE;
	int	serrno;
	FILEDESC ostat;
	FILEDESC xstat;

	serrno = geterrno();

	if (lstat(old, &ostat) < 0)
		return (-1);

	if (lstat(new, &xstat) >= 0) {
		newpresent = TRUE;
		if (ostat.st_dev == xstat.st_dev &&
		    ostat.st_ino == xstat.st_ino)
			return (0);		/* old == new we are done */
	}

	strplen = js_snprintf(strpid, sizeof (strpid), ".%lld",
							(Llong)getpid());

	if (strlen(new) <= (MAXNAME-strplen) ||
	    strchr(&new[MAXNAME-strplen], '/') == NULL) {
		/*
		 * Save old version of file 'new'.
		 */
		strncpy(nname, new, MAXNAME-strplen);
		nname[MAXNAME-strplen] = '\0';
		js_snprintf(bakname, sizeof (bakname), "%s%s", nname, strpid);
		unlink(bakname);
		if (link(new, bakname) >= 0)
			savpresent = TRUE;
	}

	if (newpresent) {
		if (rmdir(new) < 0) {
			if (geterrno() == ENOTDIR) {
				if (unlink(new) < 0)
					return (-1);
			} else {
				return (-1);
			}
		}
	}

	/*
	 * Now add 'new' name to 'old'.
	 */
	if (link(old, new) < 0) {
		serrno = geterrno();
		/*
		 * Make sure not to loose old version of 'new'.
		 */
		if (savpresent) {
			unlink(new);
			link(bakname, new);
			unlink(bakname);
		}
		seterrno(serrno);
		return (-1);
	}
	if (unlink(old) < 0)
		return (-1);
	unlink(bakname);		/* Fails in most cases...	*/
	seterrno(serrno);		/* ...so restore errno		*/
	return (0);
}
#endif	/* HAVE_RENAME */
