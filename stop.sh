#!/bin/bash

pid=$(pgrep -f main.py)

echo $pid

kill $pid
