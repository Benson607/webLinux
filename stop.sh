#!/bin/bash

pid=$(pgrep -f webLinux/main.py)

echo $pid

kill $pid
