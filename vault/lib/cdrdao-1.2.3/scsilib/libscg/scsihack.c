/* @(#)scsihack.c	1.43 03/11/28 Copyright 1997,2000,2001 J. Schilling */
#ifndef lint
static	char _sccsid[] =
	"@(#)scsihack.c	1.43 03/11/28 Copyright 1997,2000,2001 J. Schilling";
#endif
/*
 *	Interface for other generic SCSI implementations.
 *	Emulate the functionality of /dev/scg? with the local
 *	SCSI user land implementation.
 *
 *	To add a new hack, add something like:
 *
 *	#ifdef	__FreeBSD__
 *	#define	SCSI_IMPL
 *	#include some code
 *	#endif
 *
 *	Warning: you may change this source or add new SCSI tranport
 *	implementations, but if you do that you need to change the
 *	_scg_version and _scg_auth* string that are returned by the
 *	SCSI transport code.
 *	Choose your name instead of "schily" and make clear that the version
 *	string is related to a modified source.
 *	If your version has been integrated into the main steam release,
 *	the return value will be set to "schily".
 *
 *	Copyright (c) 1997,2000,2001 J. Schilling
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

#ifdef	HAVE_SYS_PARAM_H
#include <sys/param.h>	/* Include various defs needed with some OS */
#endif
#include <stdio.h>
#include <standard.h>
#include <stdxlib.h>
#include <unixstd.h>
#include <errno.h>
#include <timedefs.h>
#include <sys/ioctl.h>
#include <fctldefs.h>
#include <strdefs.h>
#include <schily.h>

#include <scg/scgcmd.h>
#include <scg/scsitransp.h>
#include "scgtimes.h"

#ifndef	HAVE_ERRNO_DEF
extern	int	errno;
#endif

LOCAL	int	scgo_send	__PR((SCSI *scgp));
LOCAL	char *	scgo_version	__PR((SCSI *scgp, int what));
LOCAL	int	scgo_help	__PR((SCSI *scgp, FILE *f));
LOCAL	int	scgo_open	__PR((SCSI *scgp, char *device));
LOCAL	int	scgo_close	__PR((SCSI *scgp));
LOCAL	long	scgo_maxdma	__PR((SCSI *scgp, long amt));
LOCAL	void *	scgo_getbuf	__PR((SCSI *scgp, long amt));
LOCAL	void	scgo_freebuf	__PR((SCSI *scgp));

LOCAL	BOOL	scgo_havebus	__PR((SCSI *scgp, int busno));
LOCAL	int	scgo_fileno	__PR((SCSI *scgp, int busno, int tgt, int tlun));
LOCAL	int	scgo_initiator_id __PR((SCSI *scgp));
LOCAL	int	scgo_isatapi	__PR((SCSI *scgp));
LOCAL	int	scgo_reset	__PR((SCSI *scgp, int what));

LOCAL	char	_scg_auth_schily[]	= "schily";	/* The author for this module	*/

EXPORT scg_ops_t scg_std_ops = {
	scgo_send,
	scgo_version,
	scgo_help,
	scgo_open,
	scgo_close,
	scgo_maxdma,
	scgo_getbuf,
	scgo_freebuf,
	scgo_havebus,
	scgo_fileno,
	scgo_initiator_id,
	scgo_isatapi,
	scgo_reset,
};

/*#undef sun*/
/*#undef __sun*/
/*#undef __sun__*/

#if defined(sun) || defined(__sun) || defined(__sun__)
#define	SCSI_IMPL		/* We have a SCSI implementation for Sun */

#include "scsi-sun.c"

#endif	/* Sun */


#ifdef	linux
#define	SCSI_IMPL		/* We have a SCSI implementation for Linux */

#ifdef	not_needed		/* We now have a local vrersion of pg.h  */
#ifndef	HAVE_LINUX_PG_H		/* If we are compiling on an old version */
#	undef	USE_PG_ONLY	/* there is no 'pg' driver and we cannot */
#	undef	USE_PG		/* include <linux/pg.h> which is needed  */
#endif				/* by the pg transport code.		 */
#endif

#ifdef	USE_PG_ONLY
#include "scsi-linux-pg.c"
#else
#include "scsi-linux-sg.c"
#endif

#endif	/* linux */

#if	defined(__FreeBSD__) || defined(__NetBSD__) || defined(__OpenBSD__)
#define	SCSI_IMPL		/* We have a SCSI implementation for *BSD */

#include "scsi-bsd.c"

#endif	/* *BSD */

#if	defined(__bsdi__)	/* We have a SCSI implementation for BSD/OS 3.x (and later?) */
# include <sys/param.h>
# if (_BSDI_VERSION >= 199701)
#  define	SCSI_IMPL

#  include "scsi-bsd-os.c"

# endif	/* BSD/OS >= 3.0 */
#endif /* BSD/OS */

#ifdef	__sgi
#define	SCSI_IMPL		/* We have a SCSI implementation for SGI */

#include "scsi-sgi.c"

#endif	/* SGI */

#ifdef	__hpux
#define	SCSI_IMPL		/* We have a SCSI implementation for HP-UX */

#include "scsi-hpux.c"

#endif	/* HP-UX */

#if	defined(_IBMR2) || defined(_AIX)
#define	SCSI_IMPL		/* We have a SCSI implementation for AIX */

#include "scsi-aix.c"

#endif	/* AIX */

#if	defined(__NeXT__) || defined(IS_MACOS_X)
#if	defined(HAVE_BSD_DEV_SCSIREG_H)
/*
 *	This is the
 */
#define	SCSI_IMPL		/* We found a SCSI implementation for NextStep and Mac OS X */

#include "scsi-next.c"
#else

#define	SCSI_IMPL		/* We found a SCSI implementation for Mac OS X (Darwin-1.4) */

#include "scsi-mac-iokit.c"

#endif	/* HAVE_BSD_DEV_SCSIREG_H */

#endif	/* NEXT / Mac OS X */

#if	defined(__osf__)
#define	SCSI_IMPL		/* We have a SCSI implementation for OSF/1 */

#include "scsi-osf.c"

#endif	/* OSF/1 */

#ifdef	VMS
#define	SCSI_IMPL		/* We have a SCSI implementation for VMS */

#include "scsi-vms.c"

#endif	/* VMS */

#ifdef	OPENSERVER
#define	SCSI_IMPL		/* We have a SCSI implementation for SCO OpenServer */

#include "scsi-openserver.c"

#endif  /* SCO */

#ifdef	UNIXWARE
#define	SCSI_IMPL		/* We have a SCSI implementation for SCO UnixWare */

#include "scsi-unixware.c"

#endif  /* UNIXWARE */

#ifdef	__OS2
#define	SCSI_IMPL		/* We have a SCSI implementation for OS/2 */

#include "scsi-os2.c"

#endif  /* OS/2 */

#ifdef	__BEOS__
#define	SCSI_IMPL		/* Yep, BeOS does that funky scsi stuff */
#include "scsi-beos.c"
#endif

#ifdef	__CYGWIN32__
#define	SCSI_IMPL		/* Yep, we support WNT and W9? */
#include "scsi-wnt.c"
#endif

#ifdef	apollo
#define	SCSI_IMPL		/* We have a SCSI implementation for Apollo Domain/OS */
#include "scsi-apollo.c"
#endif

#ifdef	AMIGA			/* We have a SCSI implementation for AmigaOS */
#define	SCSI_IMPL
#include "scsi-amigaos.c"
#endif

#if	defined(__QNXNTO__) || defined(__QNX__)
#define	SCSI_IMPL		/* We have a SCSI implementation for QNX */
#include "scsi-qnx.c"
#endif	/* QNX */

#ifdef	__DJGPP__		/* We have a SCSI implementation for MS-DOS/DJGPP */
#define	SCSI_IMPL
#include "scsi-dos.c"
#endif

#ifdef	__NEW_ARCHITECTURE
#define	SCSI_IMPL		/* We have a SCSI implementation for XXX */
/*
 * Add new hacks here
 */
#include "scsi-new-arch.c"
#endif


#ifndef	SCSI_IMPL
/*
 * To make scsihack.c compile on all architectures.
 * This does not mean that you may use it, but you can see
 * if other problems exist.
 */
#define	scgo_dversion		scgo_version
#define	scgo_dhelp		scgo_help
#define	scgo_dopen		scgo_open
#define	scgo_dclose		scgo_close
#define	scgo_dmaxdma		scgo_maxdma
#define	scgo_dgetbuf		scgo_getbuf
#define	scgo_dfreebuf		scgo_freebuf
#define	scgo_dhavebus		scgo_havebus
#define	scgo_dfileno		scgo_fileno
#define	scgo_dinitiator_id	scgo_initiator_id
#define	scgo_disatapi		scgo_isatapi
#define	scgo_dreset		scgo_reset
#define	scgo_dsend		scgo_send
#endif	/* SCSI_IMPL */

LOCAL	int	scgo_dsend	__PR((SCSI *scgp));
LOCAL	char *	scgo_dversion	__PR((SCSI *scgp, int what));
LOCAL	int	scgo_dhelp	__PR((SCSI *scgp, FILE *f));
LOCAL	int	scgo_nohelp	__PR((SCSI *scgp, FILE *f));
LOCAL	int	scgo_ropen	__PR((SCSI *scgp, char *device));
LOCAL	int	scgo_dopen	__PR((SCSI *scgp, char *device));
LOCAL	int	scgo_dclose	__PR((SCSI *scgp));
LOCAL	long	scgo_dmaxdma	__PR((SCSI *scgp, long amt));
LOCAL	void *	scgo_dgetbuf	__PR((SCSI *scgp, long amt));
LOCAL	void	scgo_dfreebuf	__PR((SCSI *scgp));
LOCAL	BOOL	scgo_dhavebus	__PR((SCSI *scgp, int busno));
LOCAL	int	scgo_dfileno	__PR((SCSI *scgp, int busno, int tgt, int tlun));
LOCAL	int	scgo_dinitiator_id __PR((SCSI *scgp));
LOCAL	int	scgo_disatapi	__PR((SCSI *scgp));
LOCAL	int	scgo_dreset	__PR((SCSI *scgp, int what));

EXPORT scg_ops_t scg_remote_ops = {
	scgo_dsend,
	scgo_dversion,
	scgo_nohelp,
	scgo_ropen,
	scgo_dclose,
	scgo_dmaxdma,
	scgo_dgetbuf,
	scgo_dfreebuf,
	scgo_dhavebus,
	scgo_dfileno,
	scgo_dinitiator_id,
	scgo_disatapi,
	scgo_dreset,
};

EXPORT scg_ops_t scg_dummy_ops = {
	scgo_dsend,
	scgo_dversion,
	scgo_dhelp,
	scgo_dopen,
	scgo_dclose,
	scgo_dmaxdma,
	scgo_dgetbuf,
	scgo_dfreebuf,
	scgo_dhavebus,
	scgo_dfileno,
	scgo_dinitiator_id,
	scgo_disatapi,
	scgo_dreset,
};

/*
 *	Warning: you may change this source, but if you do that
 *	you need to change the _scg_version and _scg_auth* string below.
 *	You may not return "schily" for an SCG_AUTHOR request anymore.
 *	Choose your name instead of "schily" and make clear that the version
 *	string is related to a modified source.
 */
LOCAL	char	_scg_trans_dversion[] = "scsihack.c-1.43";	/* The version for this transport*/

/*
 * Return version information for the low level SCSI transport code.
 * This has been introduced to make it easier to trace down problems
 * in applications.
 */
LOCAL char *
scgo_dversion(scgp, what)
	SCSI	*scgp;
	int	what;
{
	if (scgp != (SCSI *)0) {
		switch (what) {

		case SCG_VERSION:
			return (_scg_trans_dversion);
		/*
		 * If you changed this source, you are not allowed to
		 * return "schily" for the SCG_AUTHOR request.
		 */
		case SCG_AUTHOR:
			return (_scg_auth_schily);
		case SCG_SCCS_ID:
			return (_sccsid);
		}
	}
	return ((char *)0);
}

LOCAL int
scgo_dhelp(scgp, f)
	SCSI	*scgp;
	FILE	*f;
{
	printf("None.\n");
	return (0);
}

LOCAL int
scgo_nohelp(scgp, f)
	SCSI	*scgp;
	FILE	*f;
{
	return (0);
}

LOCAL int
scgo_ropen(scgp, device)
	SCSI	*scgp;
	char	*device;
{
	comerrno(EX_BAD, "No remote SCSI transport available.\n");
	return (-1);	/* Keep lint happy */
}

#ifndef	SCSI_IMPL
LOCAL int
scgo_dopen(scgp, device)
	SCSI	*scgp;
	char	*device;
{
	comerrno(EX_BAD, "No local SCSI transport implementation for this architecture.\n");
	return (-1);	/* Keep lint happy */
}
#else
LOCAL int
scgo_dopen(scgp, device)
	SCSI	*scgp;
	char	*device;
{
	comerrno(EX_BAD, "SCSI open usage error.\n");
	return (-1);	/* Keep lint happy */
}
#endif	/* SCSI_IMPL */

LOCAL int
scgo_dclose(scgp)
	SCSI	*scgp;
{
	errno = EINVAL;
	return (-1);
}

LOCAL long
scgo_dmaxdma(scgp, amt)
	SCSI	*scgp;
	long	amt;
{
	errno = EINVAL;
	return	(0L);
}

LOCAL void *
scgo_dgetbuf(scgp, amt)
	SCSI	*scgp;
	long	amt;
{
	errno = EINVAL;
	return ((void *)0);
}

LOCAL void
scgo_dfreebuf(scgp)
	SCSI	*scgp;
{
}

LOCAL BOOL
scgo_dhavebus(scgp, busno)
	SCSI	*scgp;
	int	busno;
{
	return (FALSE);
}

LOCAL int
scgo_dfileno(scgp, busno, tgt, tlun)
	SCSI	*scgp;
	int	busno;
	int	tgt;
	int	tlun;
{
	return (-1);
}

LOCAL int
scgo_dinitiator_id(scgp)
	SCSI	*scgp;
{
	return (-1);
}

LOCAL int
scgo_disatapi(scgp)
	SCSI	*scgp;
{
	return (FALSE);
}

LOCAL int
scgo_dreset(scgp, what)
	SCSI	*scgp;
	int	what;
{
	errno = EINVAL;
	return (-1);
}

LOCAL int
scgo_dsend(scgp)
	SCSI	*scgp;
{
	errno = EINVAL;
	return (-1);
}
