## Contents

* ```gunicorn.service```, ```gunicorn.socket```
instructions on how to set up gunicorn for this project
* ```logrotate_config``` - instructions and example config for rotation of homenet project logs
* ```nginx_homenet``` - nginx configuration for hosting via gunicorn; also has a section that serves my pihole php server on a separate path
* ```speedtest/``` - directory with a python speedtest wrapper that is used both autonomously (via cron scheduling) and by executing via Homenet POST links in the runner django app. It also contains initial setup for influxdb to record measurements fetched by speedtest.py and initial setup for grafana for visualizing data from influxdb.

