#!/usr/bin/env bash

source YOUR_VIRTUAL_ENV
cd YOUR_PROJECT_DIRECTORY || exit

python manage.py run_speedtest --short

finished=$(date '+%d/%m/%Y %H:%M:%S')
echo "Last pingtest run done at ${finished}"
