all: qemu-aarch64-static Archiconda3-0.2.2-Linux-aarch64.sh Dockerfile
	docker build . -t archiconda/centos7:builder

clean:
	rm qemu-aarch64-static
	rm Archiconda3*.sh

upload:
	docker push archiconda/centos7:builder

qemu-aarch64-static: /usr/bin/qemu-aarch64-static
	cp /usr/bin/qemu-aarch64-static .

Archiconda3-0.2.2-Linux-aarch64.sh: ../installer/Archiconda3/construct.yaml ../installer/installer_license.txt
	constructor --platform=linux-aarch64 ../installer/Archiconda3


.PHONY: all clean upload
