/* @(#)scsi-beos.c	1.22 04/01/15 Copyright 1998 J. Schilling */
#ifndef lint
static	char __sccsid[] =
	"@(#)scsi-beos.c	1.22 04/01/15 Copyright 1998 J. Schilling";
#endif
/*
 *	Interface for the BeOS user-land raw SCSI implementation.
 *
 *	This is a hack, that tries to emulate the functionality
 *	of the scg driver.
 *
 *	First version done by swetland@be.com
 *
 *	Warning: you may change this source, but if you do that
 *	you need to change the _scg_version and _scg_auth* string below.
 *	You may not return "schily" for an SCG_AUTHOR request anymore.
 *	Choose your name instead of "schily" and make clear that the version
 *	string is related to a modified source.
 *
 *	Copyright (c) 1998 J. Schilling
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


/*
 *	Warning: you may change this source, but if you do that
 *	you need to change the _scg_version and _scg_auth* string below.
 *	You may not return "schily" for an SCG_AUTHOR request anymore.
 *	Choose your name instead of "schily" and make clear that the version
 *	string is related to a modified source.
 */
LOCAL	char	_scg_trans_version[] = "scsi-beos.c-1.22";	/* The version for this transport*/

/*
 * There are also defines for:
 *	B_BEOS_VERSION_4
 *	B_BEOS_VERSION_4_5
 *
 * in BeOS 5
 */
#ifndef	B_BEOS_VERSION_5
/*
 * New BeOS seems to include <be/kernel/OS.h> from device/scsi.h
 */

/* nasty hack to avoid broken def of bool in SupportDefs.h */
#define	_SUPPORT_DEFS_H

#ifndef _SYS_TYPES_H
typedef unsigned long			ulong;
typedef unsigned int			uint;
typedef unsigned short			ushort;
#endif	/* _SYS_TYPES_H */

#include <BeBuild.h>
#include <sys/types.h>
#include <Errors.h>


/*-------------------------------------------------------------*/
/*----- Shorthand type formats --------------------------------*/

typedef	signed char			int8;
typedef unsigned char			uint8;
typedef volatile signed char		vint8;
typedef volatile unsigned char		vuint8;

typedef	short				int16;
typedef unsigned short			uint16;
typedef volatile short			vint16;
typedef volatile unsigned short		vuint16;

typedef	long				int32;
typedef unsigned long			uint32;
typedef volatile long			vint32;
typedef volatile unsigned long		vuint32;

typedef	long long			int64;
typedef unsigned long long		uint64;
typedef volatile long long		vint64;
typedef volatile unsigned long long	vuint64;

typedef volatile long			vlong;
typedef volatile int			vint;
typedef volatile short			vshort;
typedef volatile char			vchar;

typedef volatile unsigned long		vulong;
typedef volatile unsigned int		vuint;
typedef volatile unsigned short		vushort;
typedef volatile unsigned char		vuchar;

typedef unsigned char			uchar;
typedef unsigned short			unichar;



/*-------------------------------------------------------------*/
/*----- Descriptive formats -----------------------------------*/
typedef int32					status_t;
typedef int64					bigtime_t;
typedef uint32					type_code;
typedef uint32					perform_code;

/* end nasty hack */

#endif	/* ! B_BEOS_VERSION_5 */


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <scg/scgio.h>

/* this is really really dumb (tm) */
/*#undef sense*/
/*#undef scb*/
#include <device/scsi.h>

#undef bool
#include <drivers/CAM.h>

struct _fdmap_ {
	struct _fdmap_ *next;
	int bus;
	int targ;
	int lun;
	int fd;
};

/*
 * Return version information for the low level SCSI transport code.
 * This has been introduced to make it easier to trace down problems
 * in applications.
 */
LOCAL char *
scgo_version(scgp, what)
	SCSI	*scgp;
	int	what;
{
	if (scgp != (SCSI *)0) {
		switch (what) {

		case SCG_VERSION:
			return (_scg_trans_version);
		/*
		 * If you changed this source, you are not allowed to
		 * return "schily" for the SCG_AUTHOR request.
		 */
		case SCG_AUTHOR:
			return (_scg_auth_schily);
		case SCG_SCCS_ID:
			return (__sccsid);
		}
	}
	return ((char *)0);
}

LOCAL int
scgo_help(scgp, f)
	SCSI	*scgp;
	FILE	*f;
{
	__scg_help(f, "CAM", "Generic transport independent SCSI (BeOS CAM variant)",
		"", "bus,target,lun", "1,2,0", TRUE, FALSE);
	return (0);
}

LOCAL int
scgo_open(scgp, device)
	SCSI	*scgp;
	char	*device;
{
	int	busno	= scg_scsibus(scgp);
	int	tgt	= scg_target(scgp);
	int	tlun	= scg_lun(scgp);

#ifdef	nonono
	if (busno >= MAX_SCG || tgt >= MAX_TGT || tlun >= MAX_LUN) {
		errno = EINVAL;
		if (scgp->errstr)
			js_snprintf(scgp->errstr, SCSI_ERRSTR_SIZE,
				"Illegal value for busno, target or lun '%d,%d,%d'",
				busno, tgt, tlun);
		return (-1);
	}
#endif

	if ((device != NULL && *device != '\0') || (busno == -2 && tgt == -2)) {
		errno = EINVAL;
		if (scgp->errstr)
			js_snprintf(scgp->errstr, SCSI_ERRSTR_SIZE,
				"Open by 'devname' not supported on this OS");
		return (-1);
	}
	return (1);
}

LOCAL int
scgo_close(scgp)
	SCSI	*scgp;
{
	struct _fdmap_	*f;
	struct _fdmap_	*fnext;

	for (f = (struct _fdmap_ *)scgp->local; f; f = fnext) {
		scgp->local = 0;
		fnext = f->next;
		close(f->fd);
		free(f);
	}
	return (0);
}

LOCAL long
scgo_maxdma(scgp, amt)
	SCSI	*scgp;
	long	amt;
{
	return (256*1024);
}

LOCAL void *
scgo_getbuf(scgp, amt)
	SCSI	*scgp;
	long	amt;
{
	if (scgp->debug > 0) {
		js_fprintf((FILE *)scgp->errfile,
			"scgo_getbuf: %ld bytes\n", amt);
	}
	scgp->bufbase = malloc((size_t)(amt));
	return (scgp->bufbase);
}

LOCAL void
scgo_freebuf(scgp)
	SCSI	*scgp;
{
	if (scgp->bufbase)
		free(scgp->bufbase);
	scgp->bufbase = NULL;
}

LOCAL BOOL
scgo_havebus(scgp, busno)
	SCSI	*scgp;
	int	busno;
{
	struct stat	sb;
	char		buf[128];

	if (busno < 8)
		js_snprintf(buf, sizeof (buf), "/dev/bus/scsi/%d", busno);
	else
		js_snprintf(buf, sizeof (buf), "/dev/disk/ide/atapi/%d", busno-8);
	if (stat(buf, &sb))
		return (FALSE);
	return (TRUE);
}

LOCAL int
scgo_fileno(scgp, busno, tgt, tlun)
	SCSI	*scgp;
	int	busno;
	int	tgt;
	int	tlun;
{
	struct _fdmap_	*f;
	char		buf[128];
	int		fd;

	for (f = (struct _fdmap_ *)scgp->local; f; f = f->next) {
		if (f->bus == busno && f->targ == tgt && f->lun == tlun)
			return (f->fd);
	}
	if (busno < 8) {
		js_snprintf(buf, sizeof (buf),
					"/dev/bus/scsi/%d/%d/%d/raw",
					busno, tgt, tlun);
	} else {
		char *tgtstr = (tgt == 0) ? "master" : (tgt == 1) ? "slave" : "dummy";
		js_snprintf(buf, sizeof (buf),
					"/dev/disk/ide/atapi/%d/%s/%d/raw",
					busno-8, tgtstr, tlun);
	}
	fd = open(buf, 0);

	if (fd >= 0) {
		f = (struct _fdmap_ *) malloc(sizeof (struct _fdmap_));
		f->bus = busno;
		f->targ = tgt;
		f->lun = tlun;
		f->fd = fd;
		f->next = (struct _fdmap_ *)scgp->local;
		scgp->local = f;
	}
	return (fd);
}

LOCAL int
scgo_initiator_id(scgp)
	SCSI	*scgp;
{
	return (-1);
}

LOCAL int
scgo_isatapi(scgp)
	SCSI	*scgp;
{
	/*
	 * XXX Should check for ATAPI
	 */
	return (-1);
}

LOCAL int
scgo_reset(scgp, what)
	SCSI	*scgp;
	int	what;
{
	errno = EINVAL;
	return (-1);
}

LOCAL int
scgo_send(scgp)
	SCSI	*scgp;
{
	struct scg_cmd		*sp = scgp->scmd;
	int			e;
	int 			scsi_error;
	int			cam_error;
	raw_device_command	rdc;

	if (scgp->fd < 0) {
		sp->error = SCG_FATAL;
		return (0);
	}

	memcpy(rdc.command, &(sp->cdb), 12);
	rdc.command_length = sp->cdb_len;
	rdc.data = sp->addr;
	rdc.data_length = sp->size;
	rdc.sense_data_length = sp->sense_len;
	rdc.sense_data = sp->u_sense.cmd_sense;
	rdc.flags = sp->flags & SCG_RECV_DATA ? B_RAW_DEVICE_DATA_IN : 0;
	rdc.timeout = sp->timeout * 1000000;

	if (scgp->debug > 0) {
		error("SEND(%d): cmd %02x, cdb = %d, data = %d, sense = %d\n",
			scgp->fd, rdc.command[0], rdc.command_length,
			rdc.data_length, rdc.sense_data_length);
	}
	e = ioctl(scgp->fd, B_RAW_DEVICE_COMMAND, &rdc, sizeof (rdc));
	sp->ux_errno = 0;
	if (!e) {
		cam_error = rdc.cam_status;
		scsi_error = rdc.scsi_status;
		if (scgp->debug > 0)
			error("result: cam %02x scsi %02x\n", cam_error, scsi_error);
		sp->u_scb.cmd_scb[0] = scsi_error;

		switch (cam_error) {

		case CAM_REQ_CMP:
			sp->resid = 0;
			sp->error = SCG_NO_ERROR;
			break;
		case CAM_REQ_CMP_ERR:
			sp->sense_count = sp->sense_len; /* XXX */
			sp->error = SCG_RETRYABLE;
			break;
		default:
			sp->error = SCG_FATAL;
		}
	} else {
		sp->error = SCG_FATAL;
	}
	return (0);
}
