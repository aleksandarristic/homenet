import logging
import subprocess
import urllib.request


log = logging.getLogger()


def get_command_output(command=None):
    if not command:
        return None
    log.debug(f'Running command "{command}" as subprocess.')
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    output, errors = process.communicate()
    return output.decode('utf-8'), errors.decode('utf-8')


def transform_warp_output(output):
    warp_data = {}
    for line in output.split('\n'):
        if not line:
            continue
        key, value = line.split('=')
        warp_data[key] = value

    warp_data['raw_warp_data'] = output
    warp_data['up'] = warp_data.get('warp') == 'on'
    return warp_data


def get_warp_status():
    url = 'https://www.cloudflare.com/cdn-cgi/trace'
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                log.error(f'Error getting warp status: {response.status}')
                return None
            return transform_warp_output(response.read().decode())
    except Exception as e:
        log.error(f'Error getting warp status: {e}')
        return None
