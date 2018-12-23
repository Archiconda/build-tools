all: qemu-aarch64-static Archiconda3-0.1.1-Linux-aarch64.sh Dockerfile
	docker build . -t archiconda/archiconda3:ubuntu1604_gcc7

clean:
	rm qemu-aarch64-static
	rm Archiconda3*.sh

upload:
	docker push archiconda/archiconda3

qemu-aarch64-static: /usr/bin/qemu-aarch64-static
	cp /usr/bin/qemu-aarch64-static .

Archiconda3-0.1.1-Linux-aarch64.sh: ../installer/Archiconda3/construct.yaml ../installer/installer_license.txt
	constructor --platform=linux-aarch64 ../installer/Archiconda3


.PHONY: all clean upload
