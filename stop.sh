#!/bin/bash

docker stack rm sprc3

sleep 20

docker image rm -f  adapter:latest
docker image rm -f python:3.8

docker image prune

rm -rf ${SPRC_DVP}/database
rm -rf ${SPRC_DVP}/mosquitto/data
rm -rf ${SPRC_DVP}/mosquitto/log
sudo rm -rf ${SPRC_DVP}/grafana-storage
