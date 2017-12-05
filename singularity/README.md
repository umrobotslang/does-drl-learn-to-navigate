Install singularity using

``` bash
make -f ../makefiles/singularity-container.mk
```
To create a singularity image

``` bash
    cd singularity/
    singularity create --size 15000 ubuntu16.img
```


To initialize the image with proper packages and data. If you are creating the
image from scratch uncomment comment the first 3 lines from
`Install-bazel-deepmind-lab-apt.def`


``` bash
    cd singularity/
    sudo singularity bootstrap ubuntu16.img Install-bazel-deepmind-lab-apt.def
```

You can shell as user into the singularity image and compile your current checkout.

``` bash
cd singularity/
singularity shell ubuntu16.img
```
This will give you a new shell

    Singularity ubuntu16.img:~/wrk/implicit-mapping/singularity> cd ..
    Singularity ubuntu16.img:~/wrk/implicit-mapping> make build
    ...

Now your ubuntu image is ready to use at any machine where you don't have root
privilleges. For example on flux you can run:


    scp /z/tmp/dhiman/singularity/ubuntu16.img flux-xfer.arc-ts.umich.edu:/scratch/engin_flux/dhiman/ubuntu16.img
    singularity shell -e -B /scratch/ -B /home/ /scratch/engin_flux/dhiman/ubuntu16.img


The above commands will launch a shell that will given you an environment
exactly same as ubuntu16.04 on your local machine. You can run arbitrary
commands using `singularity run`


    cd openai-a3c-impl/web/
    singularity run -e -B /scratch/ -B /home/ /scratch/engin_flux/dhiman/ubuntu16.img ./run_exps.sh 1
