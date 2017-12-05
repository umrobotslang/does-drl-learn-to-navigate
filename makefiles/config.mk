MAKEFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
CURRDIR:=$(dir $(MAKEFILE_PATH))
INSTALL_PREFIX?=$(abspath $(CURRDIR)/../build/)
SRC_PREFIX?=$(abspath $(INSTALL_PREFIX)/src/)
