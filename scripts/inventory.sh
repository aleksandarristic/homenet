#!/usr/bin/env bash

source YOUR_VIRTUAL_ENV
cd YOUR_PROJECT_DIRECTORY || exit

python manage.py scan

finished=$(date '+%d/%m/%Y %H:%M:%S')
echo "Last speedtest run done at ${finished}"
