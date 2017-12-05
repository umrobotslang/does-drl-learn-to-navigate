MAKEFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
# directory in which this Makefile exists
CURRDIR?=$(dir $(MAKEFILE_PATH))
SHELL:=/bin/bash

.PHONY: all
all: .builddeps
	cd $(CURRDIR) && git submodule init && git submodule update
	$(MAKE) -f $(CURRDIR)/makefiles/openai-a3c.mk
	. $(CURRDIR)/setup.sh && $(MAKE) -f $(CURRDIR)/makefiles/deepmind-lab.mk

.builddeps:
	$(MAKE) -f $(CURRDIR)/makefiles/singularity-container.mk
	$(MAKE) -f $(CURRDIR)/makefiles/install-bazel.mk
	$(MAKE) -f $(CURRDIR)/makefiles/install-modules.mk
	touch $@
