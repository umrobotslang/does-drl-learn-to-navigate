MAKEFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRDIR:=$(dir $(MAKEFILE_PATH))
include $(CURRDIR)/config.mk
BAZELRC?=$(abspath $(INSTALL_PREFIX)/etc/bazel.bazelrc)
WGET?=wget
BAZEL_VERSION=0.4.4

$(INSTALL_PREFIX)/bin/bazel: $(SRC_PREFIX)/bazel-$(BAZEL_VERSION)-installer-linux-x86_64.sh
	chmod +x $<
	-mkdir -p $(dir $(BAZELRC))
	$< --prefix=$(INSTALL_PREFIX) --bazelrc=$(BAZELRC)

$(SRC_PREFIX)/bazel-$(BAZEL_VERSION)-installer-linux-x86_64.sh:
	-mkdir -p $(@D)
	$(WGET) https://github.com/bazelbuild/bazel/releases/download/$(BAZEL_VERSION)/bazel-$(BAZEL_VERSION)-installer-linux-x86_64.sh -O $@
