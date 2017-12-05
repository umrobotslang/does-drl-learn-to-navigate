SUDO:=$(if $(filter-out root,$(USER)),sudo,)
APT-GET-INSTALL=dpkg -s $(1) || $(SUDO) apt-get install $(1)
all: deepmind-lab-compile-deps environment-modules-deps
deepmind-lab-compile-deps:
		$(call APT-GET-INSTALL,liblua5.1-0-dev)
		$(call APT-GET-INSTALL,libsdl2-dev)
		$(call APT-GET-INSTALL,python-dev)
		$(call APT-GET-INSTALL,python-numpy)

environment-modules-deps:
		$(call APT-GET-INSTALL,tcl8.4-dev)
