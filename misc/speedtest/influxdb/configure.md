Configure your influxdb database via the ```influx``` cli:
```
pi@raspberrypi4:~ $ influx
Connected to http://localhost:8086 version 1.8.10
InfluxDB shell version: 1.8.10
> CREATE DATABASE speedtest
> USE speedtest
Using database speedtest
> CREATE USER "speedtestmonitor" WITH PASSWORD 'password'
> GRANT ALL ON "speedtest" to "speedtestmonitor"
> quit
```
