Default influxdb installation on raspberry pi is not a good version, so first - remove it, and update your packages.

```commandline
sudo apt remove influxdb
sudo apt update
sudo apt upgrade
```

Get keys and set sources for installing a correct version:
```commandline
curl https://repos.influxdata.com/influxdb.key | gpg --dearmor | sudo tee /usr/share/keyrings/influxdb-archive-keyring.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/influxdb-archive-keyring.gpg] https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
```

Update sources and install the correct influxdb:
```commandline
sudo apt update
sudo apt install influxdb
```

if the setup fails at this time due to influxdb being masked, repeat the installation after the next two steps.
After the install works - do these steps anyway:
```commandline
sudo systemctl unmask influxdb
sudo systemctl enable influxdb
```

start influxdb
```commandline
sudo systemctl start influxdb
```
