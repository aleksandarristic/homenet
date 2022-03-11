#!/usr/bin/env bash

source YOUR_VIRTUAL_ENV
cd YOUR_PROJECT_DIRECTORY || exit

python manage.py run_speedtest
python manage.py calculate_averages

finished=$(date '+%d/%m/%Y %H:%M:%S')
echo "Last speedtest run done at ${finished}"
