IMAGE_NAME=build-image-pgbouncer
CONTAINER_NAME=${IMAGE_NAME}_container
BINARY_DEST_DIR=bin

.IGNORE: clean

compile: clean
	docker pull alpine:edge
	docker build -t $(IMAGE_NAME) image
	docker cp `docker run --name ${CONTAINER_NAME} -d ${IMAGE_NAME} /bin/sh`:/usr/bin/pgbouncer ${BINARY_DEST_DIR}/

clean:
	docker rm -f ${CONTAINER_NAME}
