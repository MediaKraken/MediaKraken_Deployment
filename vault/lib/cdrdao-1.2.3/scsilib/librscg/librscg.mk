#ident @(#)librscg.mk	1.2 02/11/22 
###########################################################################
SRCROOT=	..
RULESDIR=	RULES
include		$(SRCROOT)/$(RULESDIR)/rules.top
###########################################################################

#.SEARCHLIST:	. $(ARCHDIR) stdio $(ARCHDIR)
#VPATH=		.:stdio:$(ARCHDIR)
INSDIR=		lib
TARGETLIB=	rscg
#CPPOPTS +=	-Ispecincl
CPPOPTS +=	-DUSE_PG
CPPOPTS +=	-DUSE_RCMD_RSH
#include		Targets
CFILES=		scsi-remote.c
LIBS=		

###########################################################################
include		$(SRCROOT)/$(RULESDIR)/rules.lib
###########################################################################
#CC=		echo "	==> COMPILING \"$@\""; cc
###########################################################################
