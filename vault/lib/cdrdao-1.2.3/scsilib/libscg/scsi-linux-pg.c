/* @(#)scsi-linux-pg.c	1.43 04/01/15 Copyright 1997 J. Schilling */
#ifndef lint
static	char ___sccsid[] =
	"@(#)scsi-linux-pg.c	1.43 04/01/15 Copyright 1997 J. Schilling";
#endif
/*
 *	Interface for the Linux PARIDE implementation.
 *
 *	We emulate the functionality of the scg driver, via the pg driver.
 *
 *	Warning: you may change this source, but if you do that
 *	you need to change the _scg_version and _scg_auth* string below.
 *	You may not return "schily" for an SCG_AUTHOR request anymore.
 *	Choose your name instead of "schily" and make clear that the version
 *	string is related to a modified source.
 *
 *	Copyright (c) 1997  J. Schilling
 *	Copyright (c) 1998  Grant R. Guenther	<grant@torque.net>
 *			    Under the terms of the GNU public license.
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

#include <string.h>
#ifdef	HAVE_LINUX_PG_H
#include <linux/pg.h>
#else
#include "pg.h"		/* Use local version as Linux sometimes doesn't have */
#endif			/* installed. Now libscg always supports PP SCSI    */

/*
 *	Warning: you may change this source, but if you do that
 *	you need to change the _scg_version and _scg_auth* string below.
 *	You may not return "schily" for an SCG_AUTHOR request anymore.
 *	Choose your name instead of "schily" and make clear that the version
 *	string is related to a modified source.
 */
LOCAL	char	_scg_trans_version_pg[] = "scsi-linux-pg.c-1.43";	/* The version for this transport*/

#ifdef	USE_PG_ONLY

#define	MAX_SCG		1	/* Max # of SCSI controllers */
#define	MAX_TGT		8
#define	MAX_LUN		8

struct scg_local {
	short	scgfiles[MAX_SCG][MAX_TGT][MAX_LUN];
	short	buscookies[MAX_SCG];
	int	pgbus;
	char	*SCSIbuf;
};
#define	scglocal(p)	((struct scg_local *)((p)->local))

#else

#define	scgo_version	pg_version
#define	scgo_help	pg_help
#define	scgo_open	pg_open
#define	scgo_close	pg_close
#define	scgo_send	pg_send
#define	scgo_maxdma	pg_maxdma
#define	scgo_initiator_id pg_initiator_id
#define	scgo_isatapi	pg_isatapi
#define	scgo_reset	pg_reset

LOCAL	char	*pg_version	__PR((SCSI *scgp, int what));
LOCAL	int	pg_help		__PR((SCSI *scgp, FILE *f));
LOCAL	int	pg_open		__PR((SCSI *scgp, char *device));
LOCAL	int	pg_close	__PR((SCSI *scgp));
LOCAL	long	pg_maxdma	__PR((SCSI *scgp, long amt));
LOCAL	int 	pg_initiator_id	__PR((SCSI *scgp));
LOCAL	int 	pg_isatapi	__PR((SCSI *scgp));
LOCAL	int	pg_reset	__PR((SCSI *scgp, int what));
LOCAL	int	pg_send		__PR((SCSI *scgp));

#endif

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
			return (_scg_trans_version_pg);
		/*
		 * If you changed this source, you are not allowed to
		 * return "schily" for the SCG_AUTHOR request.
		 */
		case SCG_AUTHOR:
			return (_scg_auth_schily);
		case SCG_SCCS_ID:
			return (___sccsid);
		}
	}
	return ((char *)0);
}

LOCAL int
scgo_help(scgp, f)
	SCSI	*scgp;
	FILE	*f;
{
	__scg_help(f, "pg", "SCSI transport for ATAPI over Parallel Port",
		"", "bus,target,lun", "1,2,0", TRUE, FALSE);
	return (0);
}

#include <glob.h>

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
#ifdef	USE_PG_ONLY
	register int	t;
	register int	l;
#endif
	register int	nopen = 0;
	char		devname[32];
        glob_t globbuf;
        int i;

	if (busno >= MAX_SCG || tgt >= MAX_TGT || tlun >= MAX_LUN) {
		errno = EINVAL;
		if (scgp->errstr)
			js_snprintf(scgp->errstr, SCSI_ERRSTR_SIZE,
				"Illegal value for busno, target or lun '%d,%d,%d'",
				busno, tgt, tlun);
		return (-1);
	}

#ifndef	USE_PG_ONLY
	/*
	 * We need to find a fake bus number for the parallel port interface.
	 * Unfortunatly, the buscookie array may contain holes if
	 * SCSI_IOCTL_GET_BUS_NUMBER works, so we are searching backwards
	 * for some place for us.
	 * XXX Should add extra space in buscookies for a "PP bus".
	 */

	if (scglocal(scgp)->buscookies[MAX_SCG-1] != (short)-1)
		return (0);			/* No space for pgbus */

	for (b = MAX_SCG-1; b >= 0; b--) {
		if (scglocal(scgp)->buscookies[b] != (short)-1) {
			scglocal(scgp)->pgbus = ++b;
			break;
		}
	}
	if (scgp->debug > 0) {
		js_fprintf((FILE *)scgp->errfile,
			"PP Bus: %d\n", scglocal(scgp)->pgbus);
	}
#else
	if (scgp->local == NULL) {
		scgp->local = malloc(sizeof (struct scg_local));
		if (scgp->local == NULL)
			return (0);

		scglocal(scgp)->pgbus = -2;
		scglocal(scgp)->SCSIbuf = (char *)-1;

		for (b = 0; b < MAX_SCG; b++) {
			for (t = 0; t < MAX_TGT; t++) {
				for (l = 0; l < MAX_LUN; l++)
					scglocal(scgp)->scgfiles[b][t][l] = (short)-1;
			}
		}
	}
#endif
	if (scglocal(scgp)->pgbus < 0)
		scglocal(scgp)->pgbus = 0;

	if ((device != NULL && *device != '\0') || (busno == -2 && tgt == -2))
		goto openbydev;

	if (busno >= 0 && tgt >= 0 && tlun >= 0) {
#ifndef	USE_PG_ONLY
		if (scglocal(scgp)->pgbus != busno)
			return (0);
#endif
		js_snprintf(devname, sizeof (devname), "/dev/pg%d", tgt);
		f = open(devname, O_RDWR | O_NONBLOCK);
		if (f < 0) {
			if (scgp->errstr)
				js_snprintf(scgp->errstr, SCSI_ERRSTR_SIZE,
						"Cannot open '%s'", devname);
			return (0);
		}
		scglocal(scgp)->scgfiles[busno][tgt][tlun] = f;
		return (1);
	} else {
		const char *dev;
		tlun = 0;
		glob("/dev/pg[0-9]", GLOB_NOSORT, NULL, &globbuf);
		glob("/dev/pg[0-9][0-9]", GLOB_NOSORT|GLOB_APPEND, NULL, &globbuf);
		for (i = 0; globbuf.gl_pathv && globbuf.gl_pathv[i] != NULL ; i++) {
		        dev = globbuf.gl_pathv[i];
			tgt = atoi(&dev[7]);
			f = open(dev, O_RDWR | O_NONBLOCK);
			if (f < 0) {
				/*
				 * Set up error string but let us clear it later
				 * if at least one open succeeded.
				 */
				if (scgp->errstr)
					js_snprintf(scgp->errstr, SCSI_ERRSTR_SIZE,
							"Cannot open '/dev/pg*'");
				if (errno != ENOENT && errno != ENXIO && errno != ENODEV) {
					if (scgp->errstr)
						js_snprintf(scgp->errstr, SCSI_ERRSTR_SIZE,
							"Cannot open '%s'", dev);
					globfree(&globbuf);
					return (0);
				}
			} else {
				scglocal(scgp)->scgfiles[scglocal(scgp)->pgbus][tgt][tlun] = f;
				nopen++;
			}
		}
		globfree(&globbuf);

	}
	if (nopen > 0 && scgp->errstr)
		scgp->errstr[0] = '\0';

openbydev:
	if (device != NULL && *device != '\0') {
		char	*p;

		if (tlun < 0)
			return (0);
		f = open(device, O_RDWR | O_NONBLOCK);
/*		if (f < 0 && errno == ENOENT) {*/
		if (f < 0) {
			if (scgp->errstr)
				js_snprintf(scgp->errstr, SCSI_ERRSTR_SIZE,
					"Cannot open '%s'",
					device);
			return (0);
		}

		p = device + strlen(device) -1;
		tgt = *p - '0';
		if (tgt < 0 || tgt > 9)
			return (0);
		scglocal(scgp)->scgfiles[scglocal(scgp)->pgbus][tgt][tlun] = f;
		scg_settarget(scgp, scglocal(scgp)->pgbus, tgt, tlun);

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
	if (scglocal(scgp)->pgbus < 0)
		return (0);
	b = scglocal(scgp)->pgbus;
	scglocal(scgp)->buscookies[b] = (short)-1;

	for (t = 0; t < MAX_TGT; t++) {
		for (l = 0; l < MAX_LUN; l++) {
			f = scglocal(scgp)->scgfiles[b][t][l];
			if (f >= 0)
				close(f);
			scglocal(scgp)->scgfiles[b][t][l] = (short)-1;
		}
	}
	return (0);
}

LOCAL long
scgo_maxdma(scgp, amt)
	SCSI	*scgp;
	long	amt;
{
	return (PG_MAX_DATA);
}

#ifdef	USE_PG_ONLY

LOCAL void *
scgo_getbuf(scgp, amt)
	SCSI	*scgp;
	long	amt;
{
	char    *ret;

	if (scgp->debug > 0) {
		js_fprintf((FILE *)scgp->errfile,
			"scgo_getbuf: %ld bytes\n", amt);
	}
	ret = valloc((size_t)(amt+getpagesize()));
	if (ret == NULL)
		return (ret);
	scgp->bufbase = ret;
	ret += getpagesize();
	scglocal(scgp)->SCSIbuf = ret;
	return ((void *)ret);

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
#endif	/* USE_PG_ONLY */

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
	return (TRUE);
}

LOCAL int
scgo_reset(scgp, what)
	SCSI	*scgp;
	int	what;
{
	struct pg_write_hdr hdr = {PG_MAGIC, PG_RESET, 0};

	if (what == SCG_RESET_NOP)
		return (0);
	if (what != SCG_RESET_BUS) {
		errno = EINVAL;
		return (-1);
	}
	/*
	 * XXX Does this reset TGT or BUS ???
	 */
	return (write(scgp->fd, (char *)&hdr, sizeof (hdr)));

}

#ifndef MAX
#define	MAX(a, b)	((a) > (b) ? (a):(b))
#endif

#define	RHSIZE	sizeof (struct pg_read_hdr)
#define	WHSIZE  sizeof (struct pg_write_hdr)
#define	LEAD	MAX(RHSIZE, WHSIZE)

LOCAL int
do_scg_cmd(scgp, sp)
	SCSI	*scgp;
	struct scg_cmd	*sp;
{

	char	local[LEAD+PG_MAX_DATA];
	int	use_local, i, r;
	int	inward = (sp->flags & SCG_RECV_DATA);

	struct pg_write_hdr *whp;
	struct pg_read_hdr  *rhp;
	char		    *dbp;

	if (sp->cdb_len > 12)
		comerrno(EX_BAD, "Can't do %d byte command.\n", sp->cdb_len);

	if (sp->addr == scglocal(scgp)->SCSIbuf) {
		use_local = 0;
		dbp = sp->addr;
	} else {
		use_local = 1;
		dbp = &local[LEAD];
		if (!inward)
			movebytes(sp->addr, dbp, sp->size);
	}

	whp = (struct pg_write_hdr *)(dbp - WHSIZE);
	rhp = (struct pg_read_hdr *)(dbp - RHSIZE);

	whp->magic   = PG_MAGIC;
	whp->func    = PG_COMMAND;
	whp->dlen    = sp->size;
	whp->timeout = sp->timeout;

	for (i = 0; i < 12; i++) {
		if (i < sp->cdb_len)
			whp->packet[i] = sp->cdb.cmd_cdb[i];
		else
			whp->packet[i] = 0;
	}

	i = WHSIZE;
	if (!inward)
		i += sp->size;

	r = write(scgp->fd, (char *)whp, i);

	if (r < 0) {				/* command was not sent */
		sp->ux_errno = geterrno();
		if (sp->ux_errno == ETIME) {
			/*
			 * If the previous command timed out, we cannot send
			 * any further command until the command in the drive
			 * is ready. So we behave as if the drive did not
			 * respond to the command.
			 */
			sp->error = SCG_FATAL;
			return (0);
		}
		return (-1);
	}

	if (r != i)
		errmsg("scgo_send(%s) wrote %d bytes (expected %d).\n",
			scgp->cmdname, r, i);

	sp->ux_errno = 0;
	sp->sense_count = 0;

	r = read(scgp->fd, (char *)rhp, RHSIZE+sp->size);

	if (r < 0) {
		sp->ux_errno = geterrno();
		if (sp->ux_errno == ETIME) {
			sp->error = SCG_TIMEOUT;
			return (0);
		}
		sp->error = SCG_FATAL;
		return (-1);
	}

	i = rhp->dlen;
	if (i > sp->size) {
		/*
		 * "DMA overrun" should be handled in the kernel.
		 * However this may happen with flaky PP adapters.
		 */
		errmsgno(EX_BAD,
			"DMA (read) overrun by %d bytes (requested %d bytes).\n",
			i - sp->size, sp->size);
		sp->resid = sp->size - i;
		sp->error = SCG_RETRYABLE;
		i = sp->size;
	} else {
		sp->resid = sp->size - i;
	}

	if (use_local && inward)
		movebytes(dbp, sp->addr, i);

	fillbytes(&sp->scb, sizeof (sp->scb), '\0');
	fillbytes(&sp->u_sense.cmd_sense, sizeof (sp->u_sense.cmd_sense), '\0');

	sp->error = SCG_NO_ERROR;
	i = rhp->scsi?2:0;
/*	i = rhp->scsi;*/
	sp->u_scb.cmd_scb[0] = i;
	if (i & 2) {
		if (sp->ux_errno == 0)
			sp->ux_errno = EIO;
		/*
		 * If there is no DMA overrun and there is a
		 * SCSI Status byte != 0 then the SCSI cdb transport was OK
		 * and sp->error must be SCG_NO_ERROR.
		 */
/*		sp->error = SCG_RETRYABLE;*/
	}

	return (0);

}

LOCAL int
do_scg_sense(scgp, sp)
	SCSI	*scgp;
	struct scg_cmd	*sp;
{
	int		ret;
	struct scg_cmd 	s_cmd;

	fillbytes((caddr_t)&s_cmd, sizeof (s_cmd), '\0');
	s_cmd.addr = (caddr_t)sp->u_sense.cmd_sense;
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
	if (sp->u_scb.cmd_scb[0] & 2)
		ret = do_scg_sense(scgp, sp);
	return (ret);
}

/* end of scsi-linux-pg.c */

#ifndef	USE_PG_ONLY

#undef	scgo_version
#undef	scgo_help
#undef	scgo_open
#undef	scgo_close
#undef	scgo_send
#undef	scgo_maxdma
#undef	scgo_initiator_id
#undef	scgo_isatapi
#undef	scgo_reset

#endif
