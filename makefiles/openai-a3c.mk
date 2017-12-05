SHELL:=/bin/bash
current_dir:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
INSTALL_DIR:=$(current_dir)/../build

.ONESHELL:
all:
	source $(current_dir)/../setup.sh
	PYTHONUSERBASE=$(INSTALL_DIR) pip2 install --user --upgrade --ignore-installed -r "$(current_dir)/py_requirements.txt"
