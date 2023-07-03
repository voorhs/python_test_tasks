SHELL = /bin/bash

test: 
	docker build -t code_review .
# mount current folder to docker container volume in order to let service read data.tgz
	docker run --rm -v .:/data code_review
.PHONY: test