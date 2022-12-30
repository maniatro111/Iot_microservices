#!/bin/bash

docker stack rm sprc3

docker image rm adapter:latest python:3.8

docker image prune

rm -rf ${SPRC_DVP}/database                                                                            
rm -rf ${SPRC_DVP}/mosquitto/data                                                                      
rm -rf ${SPRC_DVP}/mosquitto/log                                                                       
rm -rf ${SPRC_DVP}/grafana-storage
