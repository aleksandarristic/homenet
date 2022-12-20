#!/usr/bin/env python3

import json
import logging
import os
import subprocess
import sys
from datetime import datetime

from influxdb import InfluxDBClient

import psutil

log = logging.getLogger(__file__)

# InfluxDB Settings
DB_ADDRESS = os.environ.get('DB_ADDRESS', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 8086)
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')

# Various settings
LOG_FILE = '/home/pi/speedtest/speedtest.log'
TIMEOUT = 60


def configure_logging():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    file_handler = logging.FileHandler(filename=LOG_FILE)
    handlers = [file_handler, logging.StreamHandler(sys.stdout)]

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
        handlers=handlers
    )


def load_config(path: str = None) -> dict:
    if path is None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(dir_path, 'speedtest.json')
        log.debug(f'Using default config at "{path}"')

    try:
        with open(path, 'r') as f:
            cfg = json.loads(f.read())
        log.debug(f'Config loaded.')
    except Exception as e:
        log.error(f'Could not load config: {e}.')
        log.debug('Using default config values')
        cfg = {}

    log.debug(json.dumps(cfg, indent=2))
    return cfg


def is_running(proc_name):
    """
    Check if there is any running process that contains the given name processName.
    """
    log.debug(f'Checking if process "{proc_name}" is already running.')
    for proc in psutil.process_iter():
        try:
            if proc_name.lower() in proc.name().lower():
                log.debug(f'Process "{proc_name}" found!')
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            log.error(f'Error: {e}')

    log.debug(f'Process "{proc_name}" not found in process_iter.')
    return False


def run_speedtest(server_id=None):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    cmd = " ".join(["speedtest", "--accept-license", "--accept-gdpr", "-f", "json"])
    if server_id is not None:
        cmd += f" -s {server_id}"

    stdout = ''

    log.info(f'Running speedtest with server {server_id}, please wait...')
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout, stderr = proc.communicate(timeout=TIMEOUT)
    except subprocess.TimeoutExpired as e:
        log.error(f'SPEEDTEST TIMEOUT: {e}')
        proc.kill()
    except Exception as e:
        log.error(f'Error running speedtest: {e}')
        return None, -1, timestamp

    log.info(f'Speedtest run complete!')

    if proc.returncode == 0:  # Speedtest was successful.
        log.info(f'Speedtest completed with timestamp {timestamp}.')
        try:
            data = json.loads(stdout.decode('utf-8'))
            log.debug('Successfully parsed data to json.')
        except json.JSONDecodeError as e:  # parsing json failed
            log.error(f'Error parsing speedtest data to json: {e}')
            data = {}

    else:  # Speedtest failed.
        log.info(f'Speedtest failed due to return code "{proc.returncode}".')
        if server_id:
            log.info('Attempting to rerun test without server id.')
            return run_speedtest(server_id=None)
        data = None

    return data, proc.returncode, timestamp, server_id


def is_success(raw_test_data, returncode, threshold):
    if returncode != 0:
        log.info(f'Speedtest unsuccessful due to return code {returncode}.')
        return False

    if not raw_test_data:
        log.info(f'Speedtest unsuccessful - no data received.')
        return False

    download_speed = raw_test_data.get('download', {}).get('bandwidth', 0)
    if download_speed < threshold:
        log.info(f'Speedtest unsuccessful - download speed below threshold: {download_speed} (threshold: {threshold}).')
        return False

    log.info(f'Speedtest SUCCESS (download speed {download_speed}).')
    return True


def do_test(server_id):
    log.debug(f'Running speed test.')
    raw_test_data, returncode, timestamp, server = run_speedtest(server_id)
    write_data(raw_test_data, timestamp, server)
    log.debug(f'Test done.')


def format_for_influxdb(raw_test_data, timestamp, server):
    if not raw_test_data:
        raw_test_data = {}
    data = {
        'measurement': 'speedtest',
        'time': timestamp,
        'fields': {
            'download': raw_test_data.get('download', {}).get('bandwidth', 0),
            'upload': raw_test_data.get('upload', {}).get('bandwidth', 0),
            'ping': float(raw_test_data.get('ping', {}).get('latency', 0.0)),
            'jitter': float(raw_test_data.get('ping', {}).get('jitter', 0.0)),
            'loss': float(raw_test_data.get('packetLoss', 1.0)),
            'timestamp': timestamp,
            'url': raw_test_data.get('result', {}).get('url', ''),
            'server_id': raw_test_data.get('server', {}).get('id'),
            'server': raw_test_data.get('server', {}).get('name')
        }
    }

    return [data]


def write_data(test_data, timestamp, server):
    log.info(f'Received data for write with timestamp {timestamp}')
    client = InfluxDBClient(DB_ADDRESS, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE)
    data = format_for_influxdb(test_data, timestamp, server)
    log.debug(json.dumps(data, indent=4))

    try:
        if client.write_points(data):
            log.info('Data write to DB succeeded.')
            return True
    except Exception as e:
        log.error(f'Data write to DB failed: {e}')
        return False


def main():
    configure_logging()
    log.info(f'Started {__file__} script.')
    if is_running('speedtest'):
        log.error('ERROR: PROCESS SPEEDTEST ALREADY RUNNING! Please wait until the previous process finishes before '
                  'starting another instance!')
    else:
        cfg = load_config()
        server_id = cfg.get('server_id')
        do_test(server_id)
    log.info(f'All done.')


if __name__ == '__main__':
    main()
