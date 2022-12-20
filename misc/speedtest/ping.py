#!/usr/bin/env python3

import json
import logging
import os
import subprocess
import sys
from datetime import datetime

from influxdb import InfluxDBClient

log = logging.getLogger(__file__)

# InfluxDB Settings
DB_ADDRESS = os.environ.get('DB_ADDRESS', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 8086)
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')

# Various settings
LOG_FILE = '/home/pi/speedtest/ping.log'
PROC_TIMEOUT = 10
DEBUG = False


def configure_logging() -> None:
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    file_handler = logging.FileHandler(filename=LOG_FILE)
    handlers = [file_handler, logging.StreamHandler(sys.stdout)]

    logging.basicConfig(
        level=logging.DEBUG if DEBUG else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
        handlers=handlers
    )


def load_config(path: str = None) -> dict:
    if path is None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dir_path, 'ping.json')
        log.debug(f'Using default config at "{path}"')

    try:
        with open(path, 'r') as f:
            cfg = json.loads(f.read())
        log.debug(f'Config loaded.')
    except Exception as e:
        log.error(f'Could not load config: {e}.')
        log.debug('Using default config values')
        cfg = {
            "ping_hosts": []
        }

    log.debug(json.dumps(cfg, indent=2))
    return cfg


def run_ping(host: dict, set_timestamp: str = None) -> dict:
    if set_timestamp is None:
        set_timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    log.debug(f'HOST: {host}')
    log.debug(f'TIMESTAMP: {set_timestamp}')

    cmd = " ".join(['ping', '-c4', '-w5', f'{host["addr"]}'])
    log.info(f'Running ping to {host["name"]} ({host["addr"]})')
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout, stderr = proc.communicate(timeout=PROC_TIMEOUT)
    except subprocess.TimeoutExpired as e:
        log.error(f'PING TIMEOUT: {e}')
        proc.kill()
    except Exception as e:
        log.error(f'Error running speedtest: {e}')

    host_is_up = proc.returncode == 0
    log.info(f'{host["name"]} is {"UP" if host_is_up else "DOWN"}.')
    data = {
        'measurement': 'ping',
        'time': set_timestamp,
        'tags': {
            'name': host['name'],
            'addr': host['addr']
        },
        'fields': {
            'up': host_is_up
        }
    }
    return data


def do_test(hosts: list) -> bool:
    test_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    points = []
    for host in hosts:
        points.append(run_ping(host, set_timestamp=test_time))
    return write_points(points)


def write_points(points: list) -> bool:
    log.debug(f'Received data for write')
    client = InfluxDBClient(DB_ADDRESS, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE)
    log.debug(json.dumps(points, indent=4))

    try:
        if client.write_points(points):
            log.info('Data write to DB succeeded.')
            return True
    except Exception as e:
        log.error(f'Data write to DB failed: {e}')
        return False


def main():
    configure_logging()
    log.info(f'Started {__file__} script.')
    cfg = load_config()
    do_test(cfg['ping_hosts'])
    log.info(f'All done.')


if __name__ == '__main__':
    main()
