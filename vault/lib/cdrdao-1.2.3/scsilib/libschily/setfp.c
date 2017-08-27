/* @(#)setfp.c	1.11 03/07/13 Copyright 1988, 1995-2003 J. Schilling */
/*
 *	Set frame pointer
 *
 *	Copyright (c) 1988, 1995-2003 J. Schilling
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
#include <avoffset.h>
#include <schily.h>

#if	!defined(AV_OFFSET) || !defined(FP_INDIR)
#	ifdef	HAVE_SCANSTACK
#	undef	HAVE_SCANSTACK
#	endif
#endif

#	ifdef	HAVE_SCANSTACK
#include <stkframe.h>

#define	MAXWINDOWS	32
#define	NWINDOWS	7

extern	void	**___fpoff	__PR((char *cp));

EXPORT void
setfp(fp)
	void	* const *fp;
{
		long	**dummy[1];

#ifdef	sparc
	flush_reg_windows(MAXWINDOWS-2);
#endif
	*(long ***)(&((struct frame *)___fpoff((char *)&dummy[0]))->fr_savfp) =
								(long **)fp;
#ifdef	sparc
	flush_reg_windows(MAXWINDOWS-2);
#endif
}

#else

EXPORT void
setfp(fp)
	void	* const *fp;
{
	raisecond("setfp_not_implemented", 0L);
}

#endif
