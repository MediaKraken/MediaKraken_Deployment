/* @(#)rdummy.c	1.1 00/08/26 Copyright 2000 J. Schilling */
#ifndef lint
static	char _sccsid[] =
	"@(#)rdummy.c	1.1 00/08/26 Copyright 2000 J. Schilling";
#endif
/*
 *	scg Library 
 *	dummy remote ops
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
 * You should have received a copy of the GNU General Public License
 * along with this program; see the file COPYING.  If not, write to
 * the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
 */

#include <mconfig.h>
#include <standard.h>
#include <schily.h>

#include <scg/scsitransp.h>

EXPORT	scg_ops_t *scg_remote	__PR((void));

EXPORT scg_ops_t *
scg_remote()
{
extern	scg_ops_t scg_remote_ops;

	return (&scg_remote_ops);
}
