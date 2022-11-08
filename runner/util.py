import logging
import psutil

log = logging.getLogger()


def is_running(proc_name):
    """
    Check if there is any running process that contains the given name processName.
    """
    log.debug(f'Checking if process "{proc_name}" is already running.')
    for proc in psutil.process_iter():
        try:
            if proc_name.lower() in proc.name().lower():
                log.info(f'Process "{proc_name}" found!')
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            log.debug(f'Error checking process: {e}')

    log.info(f'Process "{proc_name}" not found in process_iter.')
    return False
