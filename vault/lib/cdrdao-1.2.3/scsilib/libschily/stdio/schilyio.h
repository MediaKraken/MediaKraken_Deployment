/* @(#)schilyio.h	2.22 04/09/04 Copyright 1986, 1995-2003 J. Schilling */
/*
 *	Copyright (c) 1986, 1995-2003 J. Schilling
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

#ifndef	_STDIO_SCHILYIO_H
#define	_STDIO_SCHILYIO_H

#include <mconfig.h>
#include <stdio.h>
#include <standard.h>
#include <unixstd.h>
#include <fctldefs.h>
#include <schily.h>

#ifdef	NO_USG_STDIO
#	ifdef	HAVE_USG_STDIO
#		undef	HAVE_USG_STDIO
#	endif
#endif

/*#if	_LFS_LARGEFILE*/
#ifdef	HAVE_LARGEFILES
/*
 * XXX We may need to put this code to a more global place to allow all
 * XXX users of fseek()/ftell() to automaticaly use fseeko()/ftello()
 * XXX if the latter are available.
 *
 * If HAVE_LARGEFILES is defined, it is guaranteed that fseeko()/ftello()
 * both are available.
 */
#	define	fseek	fseeko
#	define	ftell	ftello

#else	/* !HAVE_LARGEFILES */
/*
 * If HAVE_LARGEFILES is not defined, we depend on specific tests for
 * fseeko()/ftello() which must have been done before the tests for
 * Large File support have been done.
 * Note that this only works if the tests used below are really done before
 * the Large File autoconf test is run. This is because autoconf does no
 * clean testing but instead cumulatively modifes the envivonment used for
 * testing.
 */
#ifdef	HAVE_FSEEKO
#	define	fseek	fseeko
#endif
#ifdef	HAVE_FTELLO
#	define	ftell	ftello
#endif

#endif

/*
 * speed things up...
 */
#ifndef	_OPENFD_SRC
#ifdef	_openfd
#undef	_openfd
#endif
#define	_openfd(name, omode)	(open(name, omode, 0666))
#endif

#define	DO_MYFLAG		/* use local flags */

/*
 * Flags used during fileopen(), ... by _fcons()/ _cvmod()
 */
#define	FI_NONE		0x0000	/* no flags defined */

#define	FI_READ		0x0001	/* open for reading */
#define	FI_WRITE	0x0002	/* open for writing */
#define	FI_BINARY	0x0004	/* open in binary mode */
#define	FI_APPEND	0x0008	/* append on each write */

#define	FI_CREATE	0x0010	/* create if nessecary */
#define	FI_TRUNC	0x0020	/* truncate file on open */
#define	FI_UNBUF	0x0080	/* dont't buffer io */
#define	FI_CLOSE	0x1000	/* close file on error */

/*
 * local flags
 */
#define	_IONORAISE	01	/* do no raisecond() on errors */
#define	_IOUNBUF	02	/* do unbuffered i/o */

#ifdef	DO_MYFLAG

struct _io_flags {
	FILE	*fl_io;		/* file pointer */
	struct _io_flags	/* pointer to next struct */
		*fl_next;	/* if more file pointer to same fd */
	int	fl_flags;	/* my flags */
};

typedef	struct _io_flags _io_fl;

extern	int	_io_glflag;	/* global default flag */
extern	_io_fl	*_io_myfl;	/* array of structs to hold my flags */
extern	int	_fl_max;	/* max fd currently in _io_myfl */

/*
 *	if fileno > max
 *		expand
 *	else if map[fileno].pointer == 0
 *		return 0
 *	else if map[fileno].pointer == p
 *		return map[fileno].flags
 *	else
 *		search list
 */
#define	flp(p)		(&_io_myfl[fileno(p)])

#ifdef	MY_FLAG_IS_MACRO
#define	my_flag(p)	((int)fileno(p) >= _fl_max ?			\
				_io_get_my_flag(p) :			\
			((flp(p)->fl_io == 0 || flp(p)->fl_io == p) ?	\
				flp(p)->fl_flags :			\
				_io_get_my_flag(p)))
#else
#define	my_flag(p)	_io_get_my_flag(p)
#endif

#define	set_my_flag(p, v) _io_set_my_flag(p, v)
#define	add_my_flag(p, v) _io_add_my_flag(p, v)

extern	int	_io_get_my_flag __PR((FILE *));
extern	void	_io_set_my_flag __PR((FILE *, int));
extern	void	_io_add_my_flag __PR((FILE *, int));

#else	/* DO_MYFLAG */

#define	my_flag(p)		_IONORAISE	/* Always noraise */
#define	set_my_flag(p, v)			/* Ignore */
#define	add_my_flag(p, v)			/* Ignore */

#endif	/* DO_MYFLAG */

#ifdef	HAVE_USG_STDIO

/*
 * Use the right filbuf()/flsbuf() function.
 */
#ifdef	HAVE___FILBUF
#	define	usg_filbuf(fp)		__filbuf(fp)
#	define	usg_flsbuf(c, fp)	__flsbuf(c, fp)
/*
 * Define prototypes to verify if our interface is right
 */
extern	int	__filbuf		__PR((FILE *));
/*extern	int	__flsbuf		__PR(());*/
#else
#	ifdef	HAVE__FILBUF
#	define	usg_filbuf(fp)		_filbuf(fp)
#	define	usg_flsbuf(c, fp)	_flsbuf(c, fp)
/*
 * Define prototypes to verify if our interface is right
 */
extern	int	_filbuf			__PR((FILE *));
/*extern	int	_flsbuf			__PR(());*/
#	else
/*
 * no filbuf() but this will not happen on USG_STDIO systems.
 */
#	endif
#endif
/*
 * Do not check this because flsbuf()'s 1st parameter may be
 * int			SunOS
 * unsigned int		Apollo
 * unsigned char	HP-UX-11
 *
 * Note that the interface is now checked by autoconf.
 */
/*extern	int	_flsbuf	__PR((int, FILE *));*/
#else
/*
 * If we are on a non USG system we cannot down file pointers
 */
#undef	DO_DOWN
#endif

#ifndef	DO_DOWN
/*
 *	No stream checking
 */
#define	down(f)
#define	down1(f, fl1)
#define	down2(f, fl1, fl2)
#else
/*
 *	Do stream checking (works only on USG stdio)
 *
 *	New version of USG stdio.
 *	_iob[] holds only a small amount of pointers.
 *	Aditional space is allocated.
 *	We may check only if the file pointer is != NULL
 *	and if iop->_flag refers to a stream with appropriate modes.
 *	If _iob[] gets expanded by malloc() we cannot check upper bound.
 */
#define	down(f)		((f) == 0 || (f)->_flag == 0 ? \
				(raisecond(_badfile, 0L), (FILE *)0) : (f))

#define	down1(f, fl1)	((f) == 0 || (f)->_flag == 0 ? \
					(raisecond(_badfile, 0L), (FILE *)0) : \
				(((f)->_flag & fl1) != fl1 ? \
					(raisecond(_badop, 0L), (FILE *)0) : \
					(f)))

#define	down2(f, fl1, fl2)	((f) == 0 || (f)->_flag == 0 ? \
				(raisecond(_badfile, 0L), (FILE *)0) : \
				    (((f)->_flag & fl1) != fl1 && \
				    ((f)->_flag & fl2)  != fl2 ? \
				(raisecond(_badop, 0L), (FILE *)0) : \
				(f)))
#endif	/* DO_DOWN */

extern	char	_badfile[];
extern	char	_badmode[];
extern	char	_badop[];

#endif	/* _STDIO_SCHILYIO_H */
