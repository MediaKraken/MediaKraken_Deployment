/* @(#)scsi-aix.c	1.36 04/01/14 Copyright 1997 J. Schilling */
#ifndef lint
static	char __sccsid[] =
	"@(#)scsi-aix.c	1.36 04/01/14 Copyright 1997 J. Schilling";
#endif
/*
 *	Interface for the AIX generic SCSI implementation.
 *
 *	This is a hack, that tries to emulate the functionality
 *	of the scg driver.
 *
 *	Warning: you may change this source, but if you do that
 *	you need to change the _scg_version and _scg_auth* string below.
 *	You may not return "schily" for an SCG_AUTHOR request anymore.
 *	Choose your name instead of "schily" and make clear that the version
 *	string is related to a modified source.
 *
 *	Copyright (c) 1997 J. Schilling
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

#include <sys/scdisk.h>

/*
 *	Warning: you may change this source, but if you do that
 *	you need to change the _scg_version and _scg_auth* string below.
 *	You may not return "schily" for an SCG_AUTHOR request anymore.
 *	Choose your name instead of "schily" and make clear that the version
 *	string is related to a modified source.
 */
LOCAL	char	_scg_trans_version[] = "scsi-aix.c-1.36";	/* The version for this transport*/


#define	MAX_SCG		16	/* Max # of SCSI controllers */
#define	MAX_TGT		16
#define	MAX_LUN		8

struct scg_local {
	short	scgfiles[MAX_SCG][MAX_TGT][MAX_LUN];
};
#define	scglocal(p)	((struct scg_local *)((p)->local))

#define	MAX_DMA_AIX (64*1024)

LOCAL	int	do_scg_cmd	__PR((SCSI *scgp, struct scg_cmd *sp));
LOCAL	int	do_scg_sense	__PR((SCSI *scgp, struct scg_cmd *sp));

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
	__scg_help(f, "DKIOCMD", "SCSI transport for targets known by AIX drivers",
		"", "bus,target,lun or UNIX device", "1,2,0 or /dev/rcd0@", FALSE, TRUE);
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
	register int	f;
	register int	b;
	register int	t;
	register int	l;
	register int	nopen = 0;
	char		devname[32];

	if (busno >= MAX_SCG || tgt >= MAX_TGT || tlun >= MAX_LUN) {
		errno = EINVAL;
		if (scgp->errstr)
			js_snprintf(scgp->errstr, SCSI_ERRSTR_SIZE,
				"Illegal value for busno, target or lun '%d,%d,%d'",
				busno, tgt, tlun);
		return (-1);
	}

	if (scgp->local == NULL) {
		scgp->local = malloc(sizeof (struct scg_local));
		if (scgp->local == NULL)
			return (0);

		for (b = 0; b < MAX_SCG; b++) {
			for (t = 0; t < MAX_TGT; t++) {
				for (l = 0; l < MAX_LUN; l++)
					scglocal(scgp)->scgfiles[b][t][l] = (short)-1;
			}
		}
	}

	if ((device != NULL && *device != '\0') || (busno == -2 && tgt == -2))
		goto openbydev;

	if (busno >= 0 && tgt >= 0 && tlun >= 0) {

		js_snprintf(devname, sizeof (devname), "/dev/rcd%d", tgt);
		f = openx(devname, 0, 0, SC_DIAGNOSTIC);
		if (f < 0) {
			if (scgp->errstr)
				js_snprintf(scgp->errstr, SCSI_ERRSTR_SIZE,
					"Cannot open '%s'. Specify device number (1 for cd1) as target (1,0)",
					devname);
			return (0);
		}
		scglocal(scgp)->scgfiles[busno][tgt][tlun] = f;
		return (1);
	} else {
		if (scgp->errstr)
			js_snprintf(scgp->errstr, SCSI_ERRSTR_SIZE,
				"Unable to scan on AIX");
		return (0);
	}
openbydev:
	if (device != NULL && *device != '\0' && busno >= 0 && tgt >= 0 && tlun >= 0) {
		f = openx(device, 0, 0, SC_DIAGNOSTIC);
		if (f < 0) {
			if (scgp->errstr)
				js_snprintf(scgp->errstr, SCSI_ERRSTR_SIZE,
					"Cannot open '%s'",
					devname);
			return (0);
		}

		scglocal(scgp)->scgfiles[busno][tgt][tlun] = f;
		scg_settarget(scgp, busno, tgt, tlun);

		return (++nopen);
	}
	return (nopen);
}

LOCAL int
scgo_close(scgp)
	SCSI	*scgp;
{
	register int	f;
	register int	b;
	register int	t;
	register int	l;

	if (scgp->local == NULL)
		return (-1);

	for (b = 0; b < MAX_SCG; b++) {
		for (t = 0; t < MAX_TGT; t++) {
			for (l = 0; l < MAX_LUN; l++) {
				f = scglocal(scgp)->scgfiles[b][t][l];
				if (f >= 0)
					close(f);
				scglocal(scgp)->scgfiles[b][t][l] = (short)-1;
			}
		}
	}
	return (0);
}

LOCAL long
scgo_maxdma(scgp, amt)
	SCSI	*scgp;
	long	amt;
{
	return (MAX_DMA_AIX);
}

#define	palign(x, a)	(((char *)(x)) + ((a) - 1 - (((UIntptr_t)((x)-1))%(a))))

LOCAL void *
scgo_getbuf(scgp, amt)
	SCSI	*scgp;
	long	amt;
{
	void	*ret;
	int	pagesize;

#ifdef	_SC_PAGESIZE
	pagesize = sysconf(_SC_PAGESIZE);
#else
	pagesize = getpagesize();
#endif

	if (scgp->debug > 0) {
		js_fprintf((FILE *)scgp->errfile,
				"scgo_getbuf: %ld bytes\n", amt);
	}
	/*
	 * Damn AIX is a paged system but has no valloc()
	 */
	scgp->bufbase = ret = malloc((size_t)(amt+pagesize));
	if (ret == NULL)
		return (ret);
	ret = palign(ret, pagesize);
	return (ret);
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
	register int	t;
	register int	l;

	if (busno < 0 || busno >= MAX_SCG)
		return (FALSE);

	if (scgp->local == NULL)
		return (FALSE);

	for (t = 0; t < MAX_TGT; t++) {
		for (l = 0; l < MAX_LUN; l++)
			if (scglocal(scgp)->scgfiles[busno][t][l] >= 0)
				return (TRUE);
	}
	return (FALSE);
}

LOCAL int
scgo_fileno(scgp, busno, tgt, tlun)
	SCSI	*scgp;
	int	busno;
	int	tgt;
	int	tlun;
{
	if (busno < 0 || busno >= MAX_SCG ||
	    tgt < 0 || tgt >= MAX_TGT ||
	    tlun < 0 || tlun >= MAX_LUN)
		return (-1);

	if (scgp->local == NULL)
		return (-1);

	return ((int)scglocal(scgp)->scgfiles[busno][tgt][tlun]);
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
	return (FALSE);
}

LOCAL int
scgo_reset(scgp, what)
	SCSI	*scgp;
	int	what;
{
	if (what == SCG_RESET_NOP)
		return (0);
	if (what != SCG_RESET_BUS) {
		errno = EINVAL;
		return (-1);
	}
	/*
	 * XXX Does this reset TGT or BUS ???
	 */
	return (ioctl(scgp->fd, SCIORESET, IDLUN(scg_target(scgp), scg_lun(scgp))));
}

LOCAL int
do_scg_cmd(scgp, sp)
	SCSI		*scgp;
	struct scg_cmd	*sp;
{
	struct sc_iocmd req;
	int	ret;

	if (sp->cdb_len > 12)
		comerrno(EX_BAD, "Can't do %d byte command.\n", sp->cdb_len);

	fillbytes(&req, sizeof (req), '\0');

	req.flags = SC_ASYNC;
	if (sp->flags & SCG_RECV_DATA) {
		req.flags |= B_READ;
	} else if (sp->size > 0) {
		req.flags |= B_WRITE;
	}
	req.data_length = sp->size;
	req.buffer = sp->addr;
	req.timeout_value = sp->timeout;
	req.command_length = sp->cdb_len;

	movebytes(&sp->cdb, req.scsi_cdb, 12);
	errno = 0;
	ret = ioctl(scgp->fd, DKIOCMD, &req);

	if (scgp->debug > 0) {
		js_fprintf((FILE *)scgp->errfile, "ret: %d errno: %d (%s)\n", ret, errno, errmsgstr(errno));
		js_fprintf((FILE *)scgp->errfile, "data_length:     %d\n", req.data_length);
		js_fprintf((FILE *)scgp->errfile, "buffer:          0x%X\n", req.buffer);
		js_fprintf((FILE *)scgp->errfile, "timeout_value:   %d\n", req.timeout_value);
		js_fprintf((FILE *)scgp->errfile, "status_validity: %d\n", req.status_validity);
		js_fprintf((FILE *)scgp->errfile, "scsi_bus_status: 0x%X\n", req.scsi_bus_status);
		js_fprintf((FILE *)scgp->errfile, "adapter_status:  0x%X\n", req.adapter_status);
		js_fprintf((FILE *)scgp->errfile, "adap_q_status:   0x%X\n", req.adap_q_status);
		js_fprintf((FILE *)scgp->errfile, "q_tag_msg:       0x%X\n", req.q_tag_msg);
		js_fprintf((FILE *)scgp->errfile, "flags:           0X%X\n", req.flags);
	}
	if (ret < 0) {
		sp->ux_errno = geterrno();
		/*
		 * Check if SCSI command cound not be send at all.
		 */
		if (sp->ux_errno == ENOTTY || sp->ux_errno == ENXIO ||
		    sp->ux_errno == EINVAL || sp->ux_errno == EACCES) {
			return (-1);
		}
	} else {
		sp->ux_errno = 0;
	}
	ret = 0;
	sp->sense_count = 0;
	sp->resid = 0;		/* AIX is the same rubbish as Linux here */

	fillbytes(&sp->scb, sizeof (sp->scb), '\0');
	fillbytes(&sp->u_sense.cmd_sense, sizeof (sp->u_sense.cmd_sense), '\0');

	if (req.status_validity == 0) {
		sp->error = SCG_NO_ERROR;
		return (0);
	}
	if (req.status_validity & 1) {
		sp->u_scb.cmd_scb[0] = req.scsi_bus_status;
		sp->error = SCG_RETRYABLE;
	}
	if (req.status_validity & 2) {
		if (req.adapter_status & SC_NO_DEVICE_RESPONSE) {
			sp->error = SCG_FATAL;

		} else if (req.adapter_status & SC_CMD_TIMEOUT) {
			sp->error = SCG_TIMEOUT;

		} else if (req.adapter_status != 0) {
			sp->error = SCG_RETRYABLE;
		}
	}

	return (ret);
}

LOCAL int
do_scg_sense(scgp, sp)
	SCSI		*scgp;
	struct scg_cmd	*sp;
{
	int		ret;
	struct scg_cmd	s_cmd;

	fillbytes((caddr_t)&s_cmd, sizeof (s_cmd), '\0');
	s_cmd.addr = sp->u_sense.cmd_sense;
	s_cmd.size = sp->sense_len;
	s_cmd.flags = SCG_RECV_DATA|SCG_DISRE_ENA;
	s_cmd.cdb_len = SC_G0_CDBLEN;
	s_cmd.sense_len = CCS_SENSE_LEN;
	s_cmd.cdb.g0_cdb.cmd = SC_REQUEST_SENSE;
	s_cmd.cdb.g0_cdb.lun = sp->cdb.g0_cdb.lun;
	s_cmd.cdb.g0_cdb.count = sp->sense_len;
	ret = do_scg_cmd(scgp, &s_cmd);

	if (ret < 0)
		return (ret);
	if (s_cmd.u_scb.cmd_scb[0] & 02) {
		/* XXX ??? Check condition on request Sense ??? */
	}
	sp->sense_count = sp->sense_len - s_cmd.resid;
	return (ret);
}

LOCAL int
scgo_send(scgp)
	SCSI		*scgp;
{
	struct scg_cmd	*sp = scgp->scmd;
	int	ret;

	if (scgp->fd < 0) {
		sp->error = SCG_FATAL;
		return (0);
	}
	ret = do_scg_cmd(scgp, sp);
	if (ret < 0)
		return (ret);
	if (sp->u_scb.cmd_scb[0] & 02)
		ret = do_scg_sense(scgp, sp);
	return (ret);
}
