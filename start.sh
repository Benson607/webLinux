#!/bin/bash

time=$(date +"%Y%m%d")

python3 main.py >> "logs/$time.log" 2>&1 &