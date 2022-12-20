# HOMENET

A small dashboard application created for my home network. Additionally, this repo contains a stand-alone python wrapper for speedtest.net cli that periodically runs speedtest and saves results in influxdb. Compatible with raspberry pi devices running debian-based image.

Homenet created using:
* Django
* Bootstrap v5
* jQuery
* Datatables

The app requires at least:
* gunicorn (or alternative) - for running django server 
* sqlite3 - for storing data

Setup instructions for homenet dashboard
* git pull to your server (I use raspberry pi)
* create a virtual env for your django project and install project requirements:
  * ```python3 -m venv .venv```
  * ```source .venv/bin/activate```
  * ```pip install -r requirements.txt```
* Go to the homenet directory: ```cd homenet```
* Create ```app/settings_local.py``` to add any overrides to the config; alternatively, you can just edit the settings.py directly. You can use provided ```app/settings_local.py.sample``` as a base.
* Run db migration: ```python manage.py migrate```
* Create a django superuser: ```python manage.py createsuperuser```
* Collect static files where your nginx can reach them: ```python manage.py collectstatic```
* install ```gunicorn``` and ```nginx``` and set up according to files in the ```misc/``` directory

Setup instructions for speedtest tracking
* install ```speedtest``` cli from speedtest.net (https://www.speedtest.net/apps/cli)
* copy ```misc/speedtest/speedtest.py``` somewhere convenient and install its requirements (influxdb and psutil)
* install and set up influxdb and grafana as per info in ```misc/speedtest/influxdb``` and ```misc/speedtest/grafana```
* setup a cron job (```misc/speedtest/cron```) to schedule speedtest run every X minutes

