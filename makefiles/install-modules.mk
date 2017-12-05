MAKEFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRDIR:=$(dir $(MAKEFILE_PATH))
include $(CURRDIR)/config.mk
VERSION=3.2.10
IP:=$(INSTALL_PREFIX)
BUILD:=$(SRC_PREFIX)
WGET?=wget
CD?=cd
TAR?=tar
MKDIR?=mkdir
TOUCH?=touch
CP?=cp
LN?=ln -sf

$(IP)/bin/modulecmd $(IP)/etc/profile.d/modules.sh $(IP)/Modules/default: \
		$(BUILD)/modules-$(VERSION)/Makefile
	$(CD) $(<D) && $(MAKE) install
	-$(MKDIR) -p $(IP)/etc/profile.d
	$(CP) $(BUILD)/modules-$(VERSION)/etc/global/profile.modules $(IP)/etc/profile.d/modules.sh
	$(CD) $(IP)/Modules && $(LN) $(VERSION) default

$(BUILD)/modules-$(VERSION)/Makefile: $(BUILD)/modules-$(VERSION)/configure
	$(CD) $(@D) && CPPFLAGS="-DUSE_INTERP_ERRORLINE" ./configure --prefix=$(IP) --with-module-path=$(IP)/modules/modulefiles

$(BUILD)/modules-$(VERSION)/configure: $(BUILD)/modules-$(VERSION).tar.gz \
									   environment-modules-deps
	$(TAR) xzf $< -C $(shell dirname $(@D))

$(BUILD)/modules-$(VERSION).tar.gz:
	wget 'http://downloads.sourceforge.net/project/modules/Modules/modules-$(VERSION)/modules-$(VERSION).tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fmodules%2Ffiles%2F&ts=1474517300&use_mirror=heanet' -O $@

include $(CURRDIR)/apt-get-deps.mk
