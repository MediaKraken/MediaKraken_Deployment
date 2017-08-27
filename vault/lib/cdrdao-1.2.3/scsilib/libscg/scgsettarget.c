/* @(#)scgsettarget.c	1.2 04/01/14 Copyright 2000 J. Schilling */
#ifndef lint
static	char _sccsid[] =
	"@(#)scgsettarget.c	1.2 04/01/14 Copyright 2000 J. Schilling";
#endif
/*
 *	scg Library
 *	set target SCSI address
 *
 *	This is the only place in libscg that is allowed to assign
 *	values to the scg address structure.
 *
 *	Copyright (c) 2000 J. Schilling
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
#include <standard.h>
#include <schily.h>

#include <scg/scsitransp.h>

EXPORT	int	scg_settarget	__PR((SCSI *scgp, int, int, int));

EXPORT int
scg_settarget(scgp, busno, tgt, tlun)
	SCSI	*scgp;
	int	busno;
	int	tgt;
	int	tlun;
{
	int fd = -1;

	if (scgp->ops != NULL)
		fd = SCGO_FILENO(scgp, busno, tgt, tlun);
	scgp->fd = fd;
	scg_scsibus(scgp) = busno;
	scg_target(scgp)  = tgt;
	scg_lun(scgp)	  = tlun;
	return (fd);
}
