q:=
s:=$q $q
containsspace=$(findstring [:spc:], $(subst $s,[:spc:],$(1)))
assertnospace=$(if $(call containsspace,$(1)),$(error $(2)),) 
assertvarnospace=$(if $(call containsspace,$($1)),\
	$(error Bad file path $1 (contains spaces) $($1)))
MAKEFILE_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
$(call assertvarnospace,MAKEFILE_PATH)

# Where do you want you code to be copied
DEPLOY_PREFIX?=/z/home/$(USER)/install/implicit-mapping
$(call assertvarnospace,DEPLOY_PREFIX)

# User can provide install_version=
install_version?=v1

default_selected_loc:=$(DEPLOY_PREFIX)/$(install_version)
# User can provide selected_install_loc=
selected_install_loc?=$(default_selected_loc)
$(call assertvarnospace,selected_install_loc)

define USAGE:=
Usage:
Install as version v1 and run job my_job.pbs.
`install_version` acts as suffix to the DEPLOY_PREFIX (Default:
$(DEPLOY_PREFIX) ).

	make pbs=my_jobs.pbs

Or equivalently 

	make run pbs=my_jobs.pbs install_version=v1

Just install, do not run 

	make install install_version=v2

Just run my_jobs.pbs , do not install

	make run_no_install pbs=my_jobs.pbs
endef

.PHONY: all install run run_no_install tb_script post_proc_script submit_pbs_job tests
all: run_no_install

Z_CURRDIR:=$(patsubst $(HOME)/%,/z/home/$(USER)/%,$(CURRDIR))

# Do not copy these directories, just make symlinks
linkdirectories:=/.git /build /writeup /deepmind-lab/build/external $(linkdirs)
skipdirectories:=$(linkdirectories) /openai-a3c-impl/logs $(skipdirs)
.ONESHELL:
install:
	rsync -vcra --delete --exclude='/openai-a3c-impl/logs' --safe-links $(CURRDIR)/ $(Z_CURRDIR)/ | grep -v 'ignore unsafe symlink'
	# Not all directories need to be copied. If we are unlikely to
	# modify files in some directories, just create symlinks.
	for d in $(linkdirectories); \
	do \
		mkdir -p $$(dirname $(selected_install_loc)$${d}) ;\
		ln -sfT $(Z_CURRDIR)$${d} $(selected_install_loc)$${d} ;\
	done
	rsync -cra --info=progress2 --delete --safe-links \
	    $(foreach d, $(skipdirectories), --exclude='$(d)') \
	    $(CURRDIR)/ $(selected_install_loc)/ | grep -v 'ignore unsafe symlink'
	git_rev_hash=$$(git rev-parse HEAD) &&\
	cd $(selected_install_loc) &&\
	echo "$(shell date)" >> install_date &&\
	echo "$${git_rev_hash}" >> install_git_hash &&\
	$(MAKE) -f makefiles/deepmind-lab.mk

run: install run_no_install

pbsroot=$(patsubst train-%.pbs,%,$(pbs))
post_proc_script=$(selected_install_loc)/eval-$(pbsroot).pbs

.ONESHELL:
submit_pbs_job:  $(post_proc_script)
ifeq ($(origin pbs), undefined)
	$(error Please provide pbs= \r $(USAGE))
else
	cp $(CURRDIR)/pbs/$(pbs) $(selected_install_loc)/pbs/$(pbs)
	cd $(selected_install_loc)/pbs &&\
	echo "Current directory is : " $$(pwd) &&\
	TRAINJOBID=$$(qsub $(pbs))
	echo $$TRAINJOBID
	qsub -W depend=afterany:$${TRAINJOBID} $(post_proc_script)
	touch $(selected_install_loc) # Set the timestamp so that this
				      # install location is appears
				      # last in ls -rt
endif # ($(origin pbs), undefined)

git_rev_hash=$(shell git rev-parse --short HEAD)
tb_script=$(selected_install_loc)/run_tb_$(pbsroot).sh
logdirroot=$(selected_install_loc)/openai-a3c-impl/logs
logdirtail=$(pbsroot)
post_proc_script: $(post_proc_script)
$(post_proc_script): pbs/template/mkpbs.py pbs/template/eval-conf_name.pbs.jinja
	python pbs/template/mkpbs.py $(pbsroot) -m 'Gen vis' \
		--out_dir $(selected_install_loc) \
		--template pbs/template/eval-conf_name.pbs.jinja \
		--json '{"selected_install_loc" : "$(selected_install_loc)" , "logdirroot" : "$(logdirroot)" , "logdirtail" : "$(logdirtail)" , "CURRDIR"    : "$(CURRDIR)" , "git_rev_hash" : "$(git_rev_hash)" }'

tb_script: $(tb_script)
$(tb_script):
	echo "cd $(logdirroot)" > $(tb_script)
	echo "tensorboard --logdir=$(logdirtail)/train_0/ --host 0.0.0.0" >> $(tb_script)

run_no_install : submit_pbs_job $(tb_script) $(post_proc_script)

tests:
	python -m test_distance_transform
	python -c 'import doctest, deepmind_lab_gym; doctest.testmod(deepmind_lab_gym)'

# Helper functions
print-%:
	@echo $($*)
