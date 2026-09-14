#!/bin/bash

# Start web app 1
python3.10 ./app_1/app.py &
# Start web app 2
python3.10 ./app_2/app.py &

wait

