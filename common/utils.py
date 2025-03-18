import logging
import subprocess
import urllib.request
from functools import lru_cache
import time


log = logging.getLogger()


def timed_lru_cache(seconds: int, maxsize: int = 32):
    """Decorator to add time-based expiration to lru_cache."""
    def decorator(func):
        cache = lru_cache(maxsize=maxsize)(func)
        cache.expiry = time.time() + seconds

        def wrapper(*args, **kwargs):
            if time.time() > cache.expiry:
                cache.cache_clear()  # Clear cache when expired
                cache.expiry = time.time() + seconds
            return cache(*args, **kwargs)

        wrapper.cache_clear = cache.cache_clear
        return wrapper

    return decorator


def get_command_output(command=None):
    if not command:
        return None
    log.debug(f'Running command "{command}" as subprocess.')
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    output, errors = process.communicate()
    return output.decode('utf-8'), errors.decode('utf-8')


def transform_warp_output(output, raw=False):
    warp_data = {}
    for line in output.split('\n'):
        if not line:
            continue
        key, value = line.split('=')
        warp_data[key] = value

    if raw:
        warp_data['raw_warp_data'] = output
    warp_data['up'] = warp_data.get('warp') == 'on'
    return warp_data


@timed_lru_cache(60)
def get_warp_status(raw=False):
    url = 'https://www.cloudflare.com/cdn-cgi/trace'
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                log.error(f'Error getting warp status: {response.status}')
                return None
            return transform_warp_output(response.read().decode(), raw=raw)
    except Exception as e:
        log.error(f'Error getting warp status: {e}')
        return None


@timed_lru_cache(60)
def get_public_ip(interface='eth0'):
    command = f'curl -s --interface {interface} https://ip.me'
    output, _ = get_command_output(command)
    return output.strip()


@timed_lru_cache(60)
def get_private_ip(interface='eth0'):
    command = f'ip addr show {interface} | grep "inet " | awk \'{{print $2}}\''
    output, _ = get_command_output(command)
    return output.strip()
