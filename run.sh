#!/bin/bash

mkdir -p ${SPRC_DVP}/database
mkdir -p ${SPRC_DVP}/grafana-storage

chmod o+w ${SPRC_DVP}/grafana-storage

docker-compose -f stack.yml build
docker stack deploy -c stack.yml sprc3
