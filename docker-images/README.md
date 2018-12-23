# Building docker images

To build the docker images, it is probably easiest to build them on an x86
machine using qemu

```
sudo apt install qemu-user-static
cp /usr/bin/qemu-aarch64-static .
```

You have to copy the file `qemu-aarch64-static` into the local directory
because DockerFiles cannot copy anything outside of the local dir

Then to build the image

```
docker build . -t archiconda:ubuntu1604_gcc7
```

You should also have the `Archiconda3-*.sh` file in there too.

The simple Makefile should help speed up development

Images are available on dockerhub

https://cloud.docker.com/u/archiconda/repository/docker/archiconda/archiconda3
