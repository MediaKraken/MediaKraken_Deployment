/* @(#)scsiopen.c	1.95 04/01/14 Copyright 1995,2000 J. Schilling */
#ifndef lint
static	char sccsid[] =
	"@(#)scsiopen.c	1.95 04/01/14 Copyright 1995,2000 J. Schilling";
#endif
/*
 *	SCSI command functions for cdrecord
 *
 *	Copyright (c) 1995,2000 J. Schilling
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
 * NOTICE:	The Philips CDD 521 has several firmware bugs.
 *		One of them is not to respond to a SCSI selection
 *		within 200ms if the general load on the
 *		SCSI bus is high. To deal with this problem
 *		most of the SCSI commands are send with the
 *		SCG_CMD_RETRY flag enabled.
 *
 *		Note that the only legal place to assign
 *		values to scg_scsibus() scg_target() and scg_lun()
 *		is scg_settarget().
 */
#include <mconfig.h>

#include <stdio.h>
#include <standard.h>
#include <stdxlib.h>
#include <unixstd.h>
#include <fctldefs.h>
#include <errno.h>
#include <strdefs.h>
#include <timedefs.h>

#include <utypes.h>
#include <btorder.h>
#include <schily.h>

#include <scg/scgcmd.h>
#include <scg/scsidefs.h>
#include <scg/scsireg.h>
#include <scg/scsitransp.h>

#define	strbeg(s1, s2)	(strstr((s2), (s1)) == (s2))

extern	int	lverbose;

EXPORT	SCSI	*scg_open	__PR((char *scsidev, char *errs, int slen, int debug,
								int be_verbose));
EXPORT	int	scg_help	__PR((FILE *f));
LOCAL	int	scg_scandev	__PR((char *devp, char *errs, int slen,
							int *busp, int *tgtp, int *lunp));
EXPORT	int	scg_close	__PR((SCSI * scgp));

EXPORT	void	scg_settimeout	__PR((SCSI * scgp, int timeout));

EXPORT	SCSI	*scg_smalloc	__PR((void));
EXPORT	void	scg_sfree	__PR((SCSI *scgp));

/*
 * Open a SCSI device.
 *
 * Possible syntax is:
 *
 * Preferred:
 *	dev=target,lun / dev=scsibus,target,lun
 *
 * Needed on some systems:
 *	dev=devicename:target,lun / dev=devicename:scsibus,target,lun
 *
 * On systems that don't support SCSI Bus scanning this syntax helps:
 *	dev=devicename:@ / dev=devicename:@,lun
 * or	dev=devicename (undocumented)
 *
 * NOTE: As the 'lun' is part of the SCSI command descriptor block, it
 *	 must always be known. If the OS cannot map it, it must be
 *	 specified on command line.
 */
EXPORT SCSI *
scg_open(scsidev, errs, slen, debug, be_verbose)
	char	*scsidev;
	char	*errs;
	int	slen;
	int	debug;
	int	be_verbose;
{
	char	devname[256];
	char	*devp = NULL;
	char	*sdev = NULL;
	int	x1;
	int	bus = 0;
	int	tgt = 0;
	int	lun = 0;
	int	n = 0;
	SCSI	*scgp;

	if (errs)
		errs[0] = '\0';
	scgp = scg_smalloc();
	if (scgp == NULL) {
		if (errs)
			js_snprintf(errs, slen, "No memory for SCSI structure");
		return ((SCSI *)0);
	}
	scgp->debug = debug;
	scgp->overbose = be_verbose;

	devname[0] = '\0';
	if (scsidev != NULL && scsidev[0] != '\0') {
		sdev = scsidev;
		if ((strncmp(scsidev, "HELP", 4) == 0) ||
		    (strncmp(scsidev, "help", 4) == 0)) {

			return ((SCSI *)0);
		}
		if (strncmp(scsidev, "REMOTE", 6) == 0) {
			/*
			 * REMOTE:user@host:scsidev or
			 * REMOTE(transp):user@host:scsidev
			 * e.g.: REMOTE(/usr/bin/ssh):user@host:scsidev
			 *
			 * We must send the complete device spec to the remote
			 * site to allow parsing on both sites.
			 */
			strncpy(devname, scsidev, sizeof (devname)-1);
			devname[sizeof (devname)-1] = '\0';
			if (sdev[6] == '(' || sdev[6] == ':')
				sdev = strchr(sdev, ':');
			else
				sdev = NULL;

			if (sdev == NULL) {
				/*
				 * This seems to be an illegal remote dev spec.
				 * Give it a chance with a standard parsing.
				 */
				sdev = scsidev;
				devname[0] = '\0';
			} else {
				/*
				 * Now try to go past user@host spec.
				 */
				if (sdev)
					sdev = strchr(&sdev[1], ':');
				if (sdev)
					sdev++;	/* Device name follows ... */
				else
					goto nulldevice;
			}
		}
		if ((devp = strchr(sdev, ':')) == NULL) {
			if (strchr(sdev, ',') == NULL) {
				/* Notation form: 'devname' (undocumented)  */
				/* Forward complete name to scg__open()	    */
				/* Fetch bus/tgt/lun values from OS	    */
				/* We may come here too with 'USCSI'	    */
				n = -1;
				lun  = -2;	/* Lun must be known	    */
				if (devname[0] == '\0') {
					strncpy(devname, scsidev,
							sizeof (devname)-1);
					devname[sizeof (devname)-1] = '\0';
				}
			} else {
				/* Basic notation form: 'bus,tgt,lun'	    */
				devp = sdev;
			}
		} else {
			/* Notation form: 'devname:bus,tgt,lun'/'devname:@' */
			/* We may come here too with 'USCSI:'		    */
			if (devname[0] == '\0') {
				/*
				 * Copy over the part before the ':'
				 */
				x1 = devp - scsidev;
				if (x1 >= (int)sizeof (devname))
					x1 = sizeof (devname)-1;
				strncpy(devname, scsidev, x1);
				devname[x1] = '\0';
			}
			devp++;
			/* Check for a notation in the form 'devname:@'	    */
			if (devp[0] == '@') {
				if (devp[1] == '\0') {
					lun = -2;
				} else if (devp[1] == ',') {
					if (*astoi(&devp[2], &lun) != '\0') {
						errno = EINVAL;
						if (errs)
							js_snprintf(errs, slen,
								"Invalid lun specifier '%s'",
										&devp[2]);
						return ((SCSI *)0);
					}
				}
				n = -1;
				/*
				 * Got device:@ or device:@,lun
				 * Make sure not to call scg_scandev()
				 */
				devp = NULL;
			} else if (devp[0] == '\0') {
				/*
				 * Got USCSI: or ATAPI:
				 * Make sure not to call scg_scandev()
				 */
				devp = NULL;
			} else if (strchr(sdev, ',') == NULL) {
				/* We may come here with 'ATAPI:/dev/hdc'   */
				strncpy(devname, scsidev,
						sizeof (devname)-1);
				devname[sizeof (devname)-1] = '\0';
				n = -1;
				lun  = -2;	/* Lun must be known	    */
				/*
				 * Make sure not to call scg_scandev()
				 */
				devp = NULL;
			}
		}
	}
nulldevice:

/*error("10 scsidev '%s' sdev '%s' devp '%s' b: %d t: %d l: %d\n", scsidev, sdev, devp, bus, tgt, lun);*/

	if (devp != NULL) {
		n = scg_scandev(devp, errs, slen, &bus, &tgt, &lun);
		if (n < 0) {
			errno = EINVAL;
			return ((SCSI *)0);
		}
	}
	if (n >= 1 && n <= 3) {	/* Got bus,target,lun or target,lun or tgt*/
		scg_settarget(scgp, bus, tgt, lun);
	} else if (n == -1) {	/* Got device:@, fetch bus/lun from OS	*/
		scg_settarget(scgp, -2, -2, lun);
	} else if (devp != NULL) {
		/*
		 * XXX May this happen after we allow tgt to repesent tgt,0 ?
		 */
		js_fprintf(stderr, "WARNING: device not valid, trying to use default target...\n");
		scg_settarget(scgp, 0, 6, 0);
	}
	if (be_verbose && scsidev != NULL) {
		js_fprintf(stderr, "scsidev: '%s'\n", scsidev);
		if (devname[0] != '\0')
			js_fprintf(stderr, "devname: '%s'\n", devname);
		js_fprintf(stderr, "scsibus: %d target: %d lun: %d\n",
					scg_scsibus(scgp), scg_target(scgp), scg_lun(scgp));
	}
	if (debug > 0) {
		js_fprintf(stderr, "scg__open(%s) %d,%d,%d\n",
			devname,
			scg_scsibus(scgp), scg_target(scgp), scg_lun(scgp));
	}
	if (scg__open(scgp, devname) <= 0) {
		if (errs && scgp->errstr)
			js_snprintf(errs, slen, "%s", scgp->errstr);
		scg_sfree(scgp);
		return ((SCSI *)0);
	}
	return (scgp);
}

EXPORT int
scg_help(f)
	FILE	*f;
{
	SCSI	*scgp;

	scgp = scg_smalloc();
	if (scgp != NULL) {
extern	scg_ops_t scg_std_ops;

		scgp->ops = &scg_std_ops;

		printf("Supported SCSI transports for this platform:\n");
		SCGO_HELP(scgp, f);
		scg_remote()->scgo_help(scgp, f);
		scg_sfree(scgp);
	}
	return (0);
}

/*
 * Convert target,lun or scsibus,target,lun syntax.
 * Check for bad syntax and invalid values.
 * This is definitely better than using scanf() as it checks for syntax errors.
 */
LOCAL int
scg_scandev(devp, errs, slen, busp, tgtp, lunp)
	char	*devp;
	char	*errs;
	int	slen;
	int	*busp;
	int	*tgtp;
	int	*lunp;
{
	int	x1, x2, x3;
	int	n = 0;
	char	*p = devp;

	x1 = x2 = x3 = 0;
	*busp = *tgtp = *lunp = 0;

	if (*p != '\0') {
		p = astoi(p, &x1);
		if (*p == ',') {
			p++;
			n++;
		} else {
			if (errs)
				js_snprintf(errs, slen, "Invalid bus or target specifier in '%s'", devp);
			return (-1);
		}
	}
	if (*p != '\0') {
		p = astoi(p, &x2);
		if (*p == ',' || *p == '\0') {
			if (*p != '\0')
				p++;
			n++;
		} else {
			if (errs)
				js_snprintf(errs, slen, "Invalid target or lun specifier in '%s'", devp);
			return (-1);
		}
	}
	if (*p != '\0') {
		p = astoi(p, &x3);
		if (*p == '\0') {
			n++;
		} else {
			if (errs)
				js_snprintf(errs, slen, "Invalid lun specifier in '%s'", devp);
			return (-1);
		}
	}
	if (n == 3) {
		*busp = x1;
		*tgtp = x2;
		*lunp = x3;
	}
	if (n == 2) {
		*tgtp = x1;
		*lunp = x2;
	}
	if (n == 1) {
		*tgtp = x1;
	}

	if (x1 < 0 || x2 < 0 || x3 < 0) {
		if (errs)
			js_snprintf(errs, slen, "Invalid value for bus, target or lun (%d,%d,%d)",
				*busp, *tgtp, *lunp);
		return (-1);
	}
	return (n);
}

EXPORT int
scg_close(scgp)
	SCSI	*scgp;
{
	scg__close(scgp);
	scg_sfree(scgp);
	return (0);
}

EXPORT void
scg_settimeout(scgp, timeout)
	SCSI	*scgp;
	int	timeout;
{
#ifdef	nonono
	if (timeout >= 0)
		scgp->deftimeout = timeout;
#else
	scgp->deftimeout = timeout;
#endif
}

EXPORT SCSI *
scg_smalloc()
{
	SCSI	*scgp;
extern	scg_ops_t scg_dummy_ops;

	scgp = (SCSI *)malloc(sizeof (*scgp));
	if (scgp == NULL)
		return ((SCSI *)0);

	fillbytes(scgp, sizeof (*scgp), 0);
	scgp->ops	= &scg_dummy_ops;
	scg_settarget(scgp, -1, -1, -1);
	scgp->fd	= -1;
	scgp->deftimeout = 20;
	scgp->running	= FALSE;

	scgp->cmdstart = (struct timeval *)malloc(sizeof (struct timeval));
	if (scgp->cmdstart == NULL)
		goto err;
	scgp->cmdstop = (struct timeval *)malloc(sizeof (struct timeval));
	if (scgp->cmdstop == NULL)
		goto err;
	scgp->scmd = (struct scg_cmd *)malloc(sizeof (struct scg_cmd));
	if (scgp->scmd == NULL)
		goto err;
	scgp->errstr = malloc(SCSI_ERRSTR_SIZE);
	if (scgp->errstr == NULL)
		goto err;
	scgp->errptr = scgp->errbeg = scgp->errstr;
	scgp->errstr[0] = '\0';
	scgp->errfile = (void *)stderr;
	scgp->inq = (struct scsi_inquiry *)malloc(sizeof (struct scsi_inquiry));
	if (scgp->inq == NULL)
		goto err;
	scgp->cap = (struct scsi_capacity *)malloc(sizeof (struct scsi_capacity));
	if (scgp->cap == NULL)
		goto err;

	return (scgp);
err:
	scg_sfree(scgp);
	return ((SCSI *)0);
}

EXPORT void
scg_sfree(scgp)
	SCSI	*scgp;
{
	if (scgp->cmdstart)
		free(scgp->cmdstart);
	if (scgp->cmdstop)
		free(scgp->cmdstop);
	if (scgp->scmd)
		free(scgp->scmd);
	if (scgp->inq)
		free(scgp->inq);
	if (scgp->cap)
		free(scgp->cap);
	if (scgp->local)
		free(scgp->local);
	scg_freebuf(scgp);
	if (scgp->errstr)
		free(scgp->errstr);
	free(scgp);
}
