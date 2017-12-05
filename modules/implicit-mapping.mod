#%Module1.0
proc ModulesHelp { } {
global dotversion
puts stderr "implicit-mapping 0.0.1"
}

set app implicit-mapping
set version 0.0.1
set installDir [file dirname [exec readlink -m $ModulesCurrentModulefile]]

module-whatis "implicit-mapping 0.0.1"

prereq "deepmind-lab.mod"
conflict $app

module load cuda/8.0.61 cudnn/8.0-v5.1
module load numpy/1.12.0 scipy/0.18.1  opencv/2.4.13/16.04
module load gflags tensorflow/1.2.1

prepend-path PYTHONPATH $installDir/../build/lib/python2.7/site-packages/
prepend-path PATH $installDir/../build/bin/
prepend-path LD_LIBRARY_PATH $installDir/../build/lib/
prepend-path CPATH $::env(NUMPY_ROOT)/lib/python2.7/site-packages/numpy/core/include/

