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
