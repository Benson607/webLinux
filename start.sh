#!/bin/bash

time=$(date +"%Y%m%d")
ip=$(hostname -I)

if [[ $ip ]]; then
	echo "start web in $ip"
	python3 main.py >> "logs/$time.log" 2>&1 &
else
	echo "no net"
fi
