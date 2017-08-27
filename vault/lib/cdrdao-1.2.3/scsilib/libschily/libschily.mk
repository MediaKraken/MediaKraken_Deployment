#ident @(#)libschily.mk	1.3 03/07/13 
###########################################################################
SRCROOT=	..
RULESDIR=	RULES
include		$(SRCROOT)/$(RULESDIR)/rules.top
###########################################################################

.SEARCHLIST:	. $(ARCHDIR) stdio $(ARCHDIR)
VPATH=		.:stdio:$(ARCHDIR)
INSDIR=		lib
TARGETLIB=	schily
CPPOPTS +=	-Istdio
CPPOPTS +=	-DUSE_SCANSTACK
include		Targets
LIBS=		

###########################################################################
include		$(SRCROOT)/$(RULESDIR)/rules.lib
###########################################################################
