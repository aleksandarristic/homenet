import psutil


def is_running(proc_name):
    """
    Check if there is any running process that contains the given name processName.
    """
    for proc in psutil.process_iter():
        try:
            return proc_name.lower() in proc.name().lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False
