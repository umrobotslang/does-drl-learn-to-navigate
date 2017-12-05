SHELL:=/bin/bash -i
JAVA_HOME:=/usr/lib/jvm/java-8-openjdk-amd64/
export JAVA_HOME
CURRDIR:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PYDIR:=$(CURRDIR)/../build
pymodpath:=$(PYDIR)/lib/python2.7/site-packages/$(1)
RD:=$(CURRDIR)/../deepmind-lab
BUILDDIR:=$(RD)/build/
BAZELCMD:=bazel --output_base=$(BUILDDIR)

.PHONY: deepmind_lab
deepmind_lab_gym_dummy:=$(RD)/build/execroot/deepmind-lab/bazel-out/local-fastbuild/bin/deepmind_lab_gym_dummy.runfiles/org_deepmind_lab
deepmind_lab: $(deepmind_lab_gym_dummy)

$(deepmind_lab_gym_dummy): $(RD)/BUILD $(RD)-sys-dependencies \
						   $(RD)/python/deepmind_lab_gym.py \
						   deepmind-lab-compile-deps
		cd $(RD) && \
					$(BAZELCMD) build :deepmind_lab_gym_dummy --verbose_failures

rand-run: $(RD)/BUILD $(RD)-sys-dependencies
		cd $(RD) && \
					$(BAZELCMD) run :random_agent --define headless=false -- --width=640 --height=480

play: $(RD)/BUILD $(RD)-sys-dependencies
		cd $(RD) && \
					$(BAZELCMD) run :game -- --level_script tests/demo_map

.PHONY:
$(RD)-sys-dependencies: $(JAVA_HOME)/bin/javac /usr/bin/realpath 

$(JAVA_HOME)/bin/javac /usr/bin/realpath:
		#apt-get update
		#apt-get install openjdk-8-jdk realpath


$(call pymodpath,gym)/__init__.py:
		PYTHONUSERBASE=$(PYDIR) pip install --user gym==0.7.4

include $(CURRDIR)/apt-get-deps.mk
