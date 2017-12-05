# Implicit mapping by learning to navigate

This repository contains the source code corresponding to the paper:
[Do Deep Reinforcement Learning algorithms really learn to navigate](https://openreview.net/forum?id=BkiIkBJ0b)

## Replicating experiments
* Checkout the repository

``` bash
git clone git@github.com:umrobotslang/does-drl-learn-to-navigate.git
```

* Install bazel, module, singularity, python packages and compile
  deepmind lab. To compile inside singularity container read instructions [here](singularity/README.md)

``` bash
cd implicit-mapping
export INSTALL_PREFIX=$(pwd)/build
make build
```

* To run experiments

``` bash
cd ./openai-a3c-impl/web/
./run_exp.sh
```

* To generate plots, edit the `./BaDhGrICLR2018/gennav/exp-results/copy-files.sh` to copy json results from experiment location to the exp-results folder.

``` bash
cd ./BaDhGrICLR2018/gennav/exp-results/
./copy-files.sh
```
* The provided make file takes care of summarizing the results into
  csv files and then generating the plots using the csv files.

``` bash
cd ./BaDhGrICLR2018/gennav/
make exp-results/ntrained.csv ./exp-results/Static_Goal_Random_Spawn_Static_Maze.csv
make images/plot_summary_bar_plots.pdf images/plot_ntrain_summary.pdf
```

## Making deepmind lab

To make deepmind lab
```
make -f makefiles/deepmind-lab.mk
```

To install python depedencies for openai
```
make -f makefiles/openai-a3c.mk
```

## To load the environment paths
```
source setup.sh
```
