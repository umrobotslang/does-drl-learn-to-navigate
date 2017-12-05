MAKEFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRDIR:=$(dir $(MAKEFILE_PATH))
include $(CURRDIR)/config.mk
VERSION=2.3.1
IP:=$(INSTALL_PREFIX)
BUILD:=$(SRC_PREFIX)
all: $(IP)/singularity
WGET?=wget
CD?=cd
TAR?=tar
MKDIR?=mkdir
TOUCH?=touch

$(BUILD)/singularity-$(VERSION).tar.gz: $(BUILD)/.mkdir
	$(WGET) https://github.com/singularityware/singularity/releases/download/$(VERSION)/singularity-$(VERSION).tar.gz -O $@

$(BUILD)/singularity-$(VERSION)/configure: $(BUILD)/singularity-$(VERSION).tar.gz
	$(TAR) xvf $< -C $(shell dirname $(@D))

$(BUILD)/singularity-$(VERSION)/Makefile: $(BUILD)/singularity-$(VERSION)/configure
	$(CD) $(<D) \
		&& ./configure --prefix=$(IP)

$(IP)/singularity: $(BUILD)/singularity-$(VERSION)/Makefile
	$(CD) $(<D) \
		&& $(MAKE) \
		&& $(MAKE) install

%/.mkdir:
	$(MKDIR) -p $(@D)
	$(TOUCH) $@
