import logging
import subprocess


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
    wg_cmd = ['curl', '--interface', 'wg0', 'https://www.cloudflare.com/cdn-cgi/trace/']
    output, errors = get_command_output(wg_cmd)
    if errors:
        log.error(f'Error running wg show: {errors}')
        return None

    return transform_warp_output(output)
