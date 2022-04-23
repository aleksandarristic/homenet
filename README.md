# HOMENET

This application is a small dashboard application. In addition to this, it collects devices connected to your local network by scanning arp cache.

Created using:
* Django
* Bootstrap v5
* jQuery
* Datatables

The app generally requires:
* gunicorn (or alternative) - for running django server 
* sqlite3 - for storing data
* arp-scan - for scanning your arp cache to identify network devices
* cron - for automating periodic scan runs

