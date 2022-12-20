If you want to serve grafana from a path, edit your /etc/grafana/grafana.ini like so:

```
root_url = %(protocol)s://%(domain)s:%(http_port)s/grafana/
serve_from_sub_path = true
```

setup dashboards: https://pimylifeup.com/raspberry-pi-internet-speed-monitor/

You can use ```speedtest-basic-dashboard.json``` as your starting point.