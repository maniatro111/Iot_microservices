#!/bin/bash

while [ 1 ]; do

	nc -z sprc3_broker 1883 2>/dev/null
	status_broker=$?

	nc -z sprc3_influxdb 8086 2>/dev/null
	status_influx=$?

	if [[ $status_broker -eq 0 && $status_influx -eq 0 ]];
	then
		break
	fi

	sleep 1
done

python3 -u adapter.py
