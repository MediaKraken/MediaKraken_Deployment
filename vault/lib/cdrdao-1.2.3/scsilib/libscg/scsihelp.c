/* @(#)scsihelp.c	1.4 04/01/14 Copyright 2002 J. Schilling */
#ifndef lint
static	char sccsid[] =
	"@(#)scsihelp.c	1.4 04/01/14 Copyright 2002 J. Schilling";
#endif
/*
 *	scg Library
 *	Help subsystem
 *
 *	Copyright (c) 2002 J. Schilling
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
#include <stdio.h>
#include <standard.h>
#include <schily.h>

#include <scg/scsitransp.h>

EXPORT	void	__scg_help	__PR((FILE *f, char *name, char *tcomment,
					char *tind,
					char *tspec,
					char *texample,
					BOOL mayscan,
					BOOL bydev));

EXPORT void
__scg_help(f, name, tcomment, tind, tspec, texample, mayscan, bydev)
	FILE	*f;
	char	*name;
	char	*tcomment;
	char	*tind;
	char	*tspec;
	char	*texample;
	BOOL	mayscan;
	BOOL	bydev;
{
	fprintf(f, "\nTransport name:		%s\n", name);
	fprintf(f, "Transport descr.:	%s\n", tcomment);
	fprintf(f, "Transp. layer ind.:	%s\n", tind);
	fprintf(f, "Target specifier:	%s\n", tspec);
	fprintf(f, "Target example:		%s\n", texample);
	fprintf(f, "SCSI Bus scanning:	%ssupported\n", mayscan? "":"not ");
	fprintf(f, "Open via UNIX device:	%ssupported\n", bydev? "":"not ");
}
